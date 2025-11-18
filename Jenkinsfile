pipeline {
    agent any
    
    environment {
        APP_NAME = 'MyAwesomeApp'
        VERSION = '1.0.0'
        BUILD_ENV = 'production'
    }
    
    stages {
        stage('Build') {
            steps {
                echo 'Building..'
                echo "Building ${env.APP_NAME} version ${env.VERSION}"
                echo "Target environment: ${env.BUILD_ENV}"
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
                echo "Testing ${env.APP_NAME}..."
            }
        }
        
        stage('Deploy') {
            steps {
                echo 'Deploying....'
                echo "Deploying ${env.APP_NAME} v${env.VERSION} to ${env.BUILD_ENV}"
            }
        }
    }
    
    post {
        success {
            echo "✅ ${env.APP_NAME} pipeline completed successfully!"
        }
        always {
            echo '🧹 Pipeline completed'
        }
    }
}
