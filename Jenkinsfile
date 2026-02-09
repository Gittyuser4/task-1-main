pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    sh 'docker build -t login-app:latest .'
                }
            }
        }

        stage('Stop Existing Container') {
            steps {
                script {
                    sh '''
                    if [ "$(docker ps -q -f name=login-container)" ]; then
                        docker stop login-container
                        docker rm login-container
                    fi
                    '''
                }
            }
        }

        stage('Run Container') {
            steps {
                script {
                    sh '''
                    docker run -d \
                      -p 5000:5000 \
                      --name login-container \
                      --env-file .env \
                      login-app:latest
                    '''
                }
            }
        }
    }
}

