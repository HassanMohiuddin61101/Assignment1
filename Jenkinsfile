pipeline {
    agent any
    stages {
        stage('Checkout') {
            steps {
                git branch: 'master', url: 'https://github.com/HassanMohiuddin61101/Assignment1.git'
            }
        }
        stage('Test') {
            steps {
                sh 'pip install -r requirements.txt pytest'
                sh 'pytest tests/'
            }
        }
        stage('Deploy to EC2') {
            steps {
                sshagent(['ec2-ssh-key']) {
                    sh '''
                    ssh -o StrictHostKeyChecking=no ubuntu@3.123.456.789 << EOF
                    docker pull hassanmohiuddin61101/assignment1:latest
                    docker stop assignment1 || true
                    docker rm assignment1 || true
                    docker run -d --name assignment1 -p 5000:5000 hassanmohiuddin61101/assignment1:latest
                    EOF
                    '''
                }
            }
        }
    }
}