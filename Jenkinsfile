pipeline {
    agent any

    environment {
        IMAGE_NAME = "app-pipeline-prc"
        CONTAINER_NAME = "app-pipeline-prc-container"
        APP_PORT = "8000"
        SLACK_WEBHOOK = "https://hooks.slack.com/services/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"
    }

    stages {

        stage('Clone') {
            steps {
                echo 'Cloning repository...'
                checkout scm
            }
        }

        stage('Build') {
            steps {
                echo 'Installing dependencies...'
                sh 'pip install -r requirements.txt --break-system-packages'
            }
        }

        stage('Test') {
            steps {
                echo 'Running unit tests...'
                sh 'python3 -m pytest test_calculator.py -v'
            }
        }

        stage('Docker Build') {
            steps {
                echo 'Building Docker image...'
                sh 'docker build -t ${IMAGE_NAME} .'
            }
        }

        stage('Deploy') {
            steps {
                echo 'Deploying container...'
                sh '''
                    docker stop ${CONTAINER_NAME} || true
                    docker rm ${CONTAINER_NAME} || true
                    docker run -d -p ${APP_PORT}:80 --name ${CONTAINER_NAME} ${IMAGE_NAME}
                '''
            }
        }
    }

    post {
        success {
            sh """
                curl -X POST -H 'Content-type: application/json' \
                --data '{"text":"✅ Pipeline exitoso: ${env.JOB_NAME} #${env.BUILD_NUMBER}"}' \
                ${env.SLACK_WEBHOOK}
            """
        }
        failure {
            sh """
                curl -X POST -H 'Content-type: application/json' \
                --data '{"text":"❌ Pipeline fallido: ${env.JOB_NAME} #${env.BUILD_NUMBER}"}' \
                ${env.SLACK_WEBHOOK}
            """
        }
    }
}
