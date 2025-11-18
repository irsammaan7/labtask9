pipeline {
    agent any
    
    environment {
        APP_NAME = 'MyAwesomeApp'
        VERSION = '1.0.0'
    }
    
    parameters {
        booleanParam(name: 'EXECUTE_TESTS', defaultValue: true, description: 'Run tests?')
        choice(name: 'DEPLOY_ENV', choices: ['dev', 'staging', 'production'], description: 'Deployment environment')
    }
    
    stages {
        stage('Build') {
            steps {
                echo 'Building..'
                echo "Building ${env.APP_NAME} version ${env.VERSION}"
            }
        }
        
        stage('Test') {
            when {
                expression { 
                    return params.EXECUTE_TESTS == true
                }
            }
            steps {
                echo 'Testing..'
                echo "Running tests for ${env.APP_NAME}..."
                echo 'All tests passed!'
            }
        }
        
        stage('Deploy') {
            steps {
                echo 'Deploying....'
                echo "Deploying to ${params.DEPLOY_ENV} environment"
                echo "✅ Deployed ${env.APP_NAME} to ${params.DEPLOY_ENV}!"
            }
        }
    }
    
    post {
        success {
            echo "✅ Pipeline completed successfully!"
            echo "Application deployed to ${params.DEPLOY_ENV}"
        }
        failure {
            echo "❌ Pipeline failed!"
        }
        always {
            echo '🧹 Cleaning up...'
            echo 'Pipeline finished'
        }
    }
}
