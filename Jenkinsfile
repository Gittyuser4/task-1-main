pipeline {
    agent any

    environment {
        IMAGE_NAME = "task-1-main-flask"
        SONAR_SCANNER = "/var/lib/jenkins/tools/hudson.plugins.sonar.SonarRunnerInstallation/SonarScanner/bin/sonar-scanner"
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Start SonarQube') {
            steps {
                sh '''
                  docker compose up -d sonarqube
                  sleep 30
                '''
            }
        }

        stage('SonarQube Analysis') {
            steps {
                withSonarQubeEnv('SonarQube') {
                    withCredentials([string(credentialsId: 'sonar-token', variable: 'SONAR_TOKEN')]) {
                        sh """
                          ${SONAR_SCANNER} \
                            -Dsonar.projectKey=task-1 \
                            -Dsonar.sources=. \
                            -Dsonar.python.version=3 \
                            -Dsonar.login=$SONAR_TOKEN \
                            -Dsonar.host.url=http://localhost:9000
                        """
                    }
                }
            }
        }

        stage('Quality Gate') {
            steps {
                timeout(time: 3, unit: 'MINUTES') {
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

        stage('Deploy App (Flask + Postgres)') {
            steps {
                sh '''
                  docker compose up -d flask postgres
                '''
            }
        }

        stage('Health Check') {
            steps {
                sh '''
                  sleep 15
                  curl -f http://localhost:5000 || exit 1
                '''
            }
        }
    }

    post {
        always {
            sh '''
              docker compose stop flask postgres || true
              docker system prune -f || true
            '''
        }
    }
}
