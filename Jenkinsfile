pipeline {
  agent any

  

  environment {
    DB_NAME     = 'authdb'
    DB_USER     = 'authuser'
    DB_PASSWORD = 'authpass'
    IMAGE_NAME  = 'task-1-flask'
   // COMPOSE_PROJECT_NAME = "task1-${BUILD_NUMBER}"
    SCANNER_HOME = tool 'SonarScanner'

  }

  stages {

    stage('Checkout') {
      steps {
        checkout scm
      }
    }

    stage('SonarQube Analysis') {
      steps {
        withSonarQubeEnv('SonarQube') {
          sh '''
            sonar-scanner \
              -Dsonar.projectKey=task-1 \
              -Dsonar.sources=. \
              -Dsonar.python.version=3
          '''
        }
      }
    }

    stage('Quality Gate') {
      steps {
        timeout(time: 2, unit: 'MINUTES') {
          waitForQualityGate abortPipeline: true
        }
      }
    }

    stage('Docker Build') {
      steps {
        sh '''
          docker build -t $IMAGE_NAME:${BUILD_NUMBER} .
        '''
      }
    }

    stage('Trivy Image Scan') {
      steps {
        sh '''
          docker run --rm \
            -v /var/run/docker.sock:/var/run/docker.sock \
            aquasec/trivy:latest image \
            --exit-code 1 \
            --severity HIGH,CRITICAL \
            $IMAGE_NAME:${BUILD_NUMBER}
        '''
      }
    }

    stage('Deploy (Docker Compose)') {
      steps {
        sh '''
          docker compose up -d
        '''
      }
    }

    stage('Health Check') {
      steps {
        sh '''
          sleep 15
          curl -f http://localhost:5000
        '''
      }
    }
  }

  post {
    always {
      sh '''
        docker compose down -v || true
        docker system prune -f || true
      '''
    }
  }
}
