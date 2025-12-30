pipeline {
    agent any
    
    environment {
        PYTHON_VERSION = '3.9'
        VENV_DIR = 'venv'
        DEPLOY_DIR = '/var/www/flask-app'
    }
    
    stages {
        stage('Clone Repository') {
            steps {
                script {
                    echo 'Cloning repository from GitHub...'
                    git branch: 'main',
                        url: 'https://github.com/irsammaan7/labtask9.git'
                }
            }
        }
        
        stage('Install Dependencies') {
            steps {
                script {
                    echo 'Setting up Python virtual environment...'
                    sh '''
                        python3 -m venv ${VENV_DIR}
                        . ${VENV_DIR}/bin/activate
                        pip install --upgrade pip
                        pip install -r requirements.txt
                    '''
                }
            }
        }
        
        stage('Run Unit Tests') {
            steps {
                script {
                    echo 'Running unit tests with pytest...'
                    sh '''
                        . ${VENV_DIR}/bin/activate
                        pytest tests/ --verbose --junit-xml=test-results.xml
                    '''
                }
            }
            post {
                always {
                    junit 'test-results.xml'
                }
            }
        }
        
        stage('Build Application') {
            steps {
                script {
                    echo 'Building Flask application...'
                    sh '''
                        . ${VENV_DIR}/bin/activate
                        # Create distribution package
                        mkdir -p dist
                        tar -czf dist/flask-app-${BUILD_NUMBER}.tar.gz \
                            --exclude=${VENV_DIR} \
                            --exclude=.git \
                            --exclude=dist \
                            --exclude=__pycache__ \
                            --exclude=*.pyc \
                            .
                        echo "Build ${BUILD_NUMBER} completed successfully"
                    '''
                }
            }
        }
        
        stage('Deploy Application') {
            steps {
                script {
                    echo 'Deploying Flask application...'
                    sh '''
                        # Create deployment directory if it doesn't exist
                        mkdir -p ${DEPLOY_DIR}
                        
                        # Copy application files to deployment directory
                        cp -r * ${DEPLOY_DIR}/ || true
                        
                        # Set up virtual environment in deployment directory
                        cd ${DEPLOY_DIR}
                        python3 -m venv venv
                        . venv/bin/activate
                        pip install -r requirements.txt
                        
                        # Simulate service restart (adjust based on your deployment method)
                        # For systemd service: systemctl restart flask-app
                        # For supervisord: supervisorctl restart flask-app
                        # For simple deployment, just log the deployment
                        echo "Application deployed to ${DEPLOY_DIR}"
                        echo "Deployment completed at $(date)"
                        
                        # Optional: Start the Flask app in background (for testing)
                        # pkill -f "flask run" || true
                        # nohup flask run --host=0.0.0.0 --port=5000 > app.log 2>&1 &
                    '''
                }
            }
        }
    }
    
    post {
        success {
            echo 'Pipeline completed successfully!'
            emailext(
                subject: "Jenkins Pipeline Success: ${env.JOB_NAME} - Build #${env.BUILD_NUMBER}",
                body: "The pipeline has completed successfully. Check console output at ${env.BUILD_URL}",
                to: 'irsammaan7@gmail.com'
            )
        }
        failure {
            echo 'Pipeline failed!'
            emailext(
                subject: "Jenkins Pipeline Failed: ${env.JOB_NAME} - Build #${env.BUILD_NUMBER}",
                body: "The pipeline has failed. Check console output at ${env.BUILD_URL}",
                to: 'irsammaan7@gmail.com'
            )
        }
        always {
            cleanWs()
        }
    }
}
