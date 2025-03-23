pipeline {
    agent any

    environment {
        BACKEND_IMAGE = 'stefan5andonov/kiii2025-backend-image'
        FRONTEND_IMAGE = 'stefan5andonov/kiii2025-frontend-image'
    }

    stages {
        stage('Clone repository') {
            checkout scm
        }
        stage('Build Backend Image') {
            steps {
                script {
                    backend_app = docker.build("${env.BACKEND_IMAGE}", './backend')
                }
            }
        }
        stage('Build Frontend Image') {
            steps {
                script {
                    frontend_app = docker.build("${env.FRONTEND_IMAGE}", './frontend')
                }
            }
        }
        stage('Push Backend Image') {
            steps {
                script {
                    docker.withRegistry('https://registry.hub.docker.com', "dockerhub") {
                        backend_app.push("${env.BRANCH_NAME}-${env.BUILD_NUMBER}")
                        backend_app.push("${env.BRANCH_NAME}-latest")
                    }
                }
            }
        }
        stage('Push Frontend Image') {
            steps {
                script {
                    docker.withRegistry('https://registry.hub.docker.com', "dockerhub") {
                        frontend_app.push("${env.BRANCH_NAME}-${env.BUILD_NUMBER}")
                        frontend_app.push("${env.BRANCH_NAME}-latest")
                    }
                }
            }
        }
    }
}
