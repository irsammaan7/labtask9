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
    
    post {
        success {
            echo '✅ Pipeline executed successfully!'
            echo 'All stages completed without errors'
        }
        failure {
            echo '❌ Pipeline execution failed!'
            echo 'Please check the logs for errors'
        }
        always {
            echo '🧹 Cleaning up...'
            echo 'Pipeline completed'
        }
    }
}
