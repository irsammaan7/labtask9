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
            when {
                expression { 
                    return env.BRANCH_NAME == 'master' || env.BRANCH_NAME == 'main'
                }
            }
            steps {
                echo 'Testing..'
                echo 'Running unit tests...'
                echo 'Tests run only on main/master branch'
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
        }
        always {
            echo '🧹 Pipeline completed'
        }
    }
}
