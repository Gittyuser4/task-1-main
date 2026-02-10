pipeline {
    agent any

    environment {
        COMPOSE_DOCKER_CLI_BUILD = '1'
        DOCKER_BUILDKIT = '1'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build & Run') {
            steps {
                sh '''
                  docker compose down || true
                  docker compose up --build -d
                '''
            }
        }

        stage('Health Check') {
            steps {
                sh '''
                  sleep 10
                  curl -f http://localhost:5000
                '''
            }
        }
    }

    post {
        failure {
            sh 'docker compose logs'
        }
    }
}

