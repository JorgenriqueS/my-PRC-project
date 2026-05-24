pipeline {
    agent any

    environment {
        IMAGE_NAME = "app-pipeline-prc"
        CONTAINER_NAME = "app-pipeline-prc-container"
        APP_PORT = "8000"
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
            mail to: 'jorge.najarro@galileo.edu',
                 subject: "✅ Pipeline exitoso: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                 body: "El pipeline ${env.JOB_NAME} #${env.BUILD_NUMBER} se completó exitosamente.\n\nVer detalles en: ${env.BUILD_URL}"
        }
        failure {
            mail to: 'jorge.najarro@galileo.edu',
                 subject: "❌ Pipeline fallido: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                 body: "El pipeline ${env.JOB_NAME} #${env.BUILD_NUMBER} falló.\n\nVer detalles en: ${env.BUILD_URL}"
        }
    }
}
