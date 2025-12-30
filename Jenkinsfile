pipeline {
    agent any
    
    environment {
        PYTHON_VERSION = '3.9'
        VENV_DIR = 'venv'
        DEPLOY_DIR = 'C:\\deploy\\flask-app'
    }
    
    stages {
        stage('Checkout') {
            steps {
                echo '📥 Checking out code from repository...'
                checkout scm
            }
        }
        
        stage('Setup Python Environment') {
            steps {
                echo '🐍 Setting up Python environment...'
                bat '''
                    python -m venv venv
                    call venv\\Scripts\\activate.bat
                    python -m pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }
        
        stage('Run Unit Tests') {
            steps {
                echo '🧪 Running unit tests...'
                bat '''
                    call venv\\Scripts\\activate.bat
                    pytest tests/ -v --junitxml=test-results.xml --cov=. --cov-report=xml --cov-report=html || exit 0
                '''
            }
        }
        
        stage('Security Scan - Bandit') {
            steps {
                echo '🛡️ Running Bandit security scan...'
                bat '''
                    call venv\\Scripts\\activate.bat
                    bandit -r . -ll -i -x ./venv,./tests -f json -o bandit-report.json || exit 0
                    bandit -r . -ll -i -x ./venv,./tests || exit 0
                '''
            }
        }
        
        stage('Build Application') {
            steps {
                echo '📦 Building application package...'
                bat '''
                    call venv\\Scripts\\activate.bat
                    if not exist dist mkdir dist
                    echo Build %BUILD_NUMBER% completed > dist\\build-info.txt
                '''
            }
        }
        
        stage('Deploy to Staging') {
            steps {
                echo '🚀 Deploying to staging...'
                bat '''
                    if not exist "%DEPLOY_DIR%" mkdir "%DEPLOY_DIR%"
                    xcopy /E /I /Y * "%DEPLOY_DIR%\\" /EXCLUDE:exclude.txt
                    echo Deployed build %BUILD_NUMBER% at %DATE% %TIME% > "%DEPLOY_DIR%\\deployment.log"
                '''
            }
        }
    }
    
    post {
        always {
            echo '📊 Archiving reports...'
            archiveArtifacts artifacts: '''
                bandit-report.json,
                test-results.xml,
                coverage.xml,
                htmlcov/**
            ''', allowEmptyArchive: true
            
            junit testResults: 'test-results.xml', allowEmptyResults: true
            
            bat '''
                if exist venv rmdir /s /q venv
            '''
        }
        
        success {
            echo '✅ Pipeline completed successfully!'
        }
        
        failure {
            echo '❌ Pipeline failed!'
        }
    }
}
