pipeline {
    agent any
    
    stages {
        stage('Build') {
            steps {
                echo 'Building..'
                echo 'Installing dependencies...'
            }
        }
        
        stage('Test') {
            steps {
                echo 'Testing..'
                echo 'Running unit tests...'
            }
        }
        
        stage('Deploy') {
            steps {
                echo 'Deploying....'
                echo 'Deployment completed successfully!'
            }
        }
    }
}
