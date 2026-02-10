pipeline {
    agent any

    environment {
        DB_NAME = 'authdb'
        DB_USER = 'authuser'
        DB_PASSWORD = 'authpass'
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

