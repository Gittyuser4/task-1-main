pipeline {
    agent any

    environment {
        DB_NAME = 'authdb'
        DB_USER = 'authuser'
        DB_PASSWORD = 'authpass'
        IMAGE_NAME = 'task-1-flask'
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
      			-Dsonar.sources=.
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
                  docker build -t $IMAGE_NAME .
                '''
            }
        }

        stage('Trivy Image Scan') {
            steps {
                sh '''
                  trivy image --exit-code 1 --severity HIGH,CRITICAL $IMAGE_NAME
                '''
            }
        }

        stage('Deploy (Docker Compose)') {
            steps {
                sh '''
                  docker compose down || true
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

