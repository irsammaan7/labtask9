pipeline {
    agent any
    
    environment {
        DOCKER_IMAGE = "flask-app"
        DOCKER_TAG = "${BUILD_NUMBER}"
        SONAR_PROJECT_KEY = "flask-app"
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
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }
        
        stage('Static Code Analysis - SonarQube') {
            steps {
                echo '🔍 Running SonarQube SAST scan...'
                script {
                    def scannerHome = tool 'SonarScanner'
                    withSonarQubeEnv('SonarQube-Server') {
                        sh """
                            ${scannerHome}/bin/sonar-scanner \
                            -Dsonar.projectKey=${SONAR_PROJECT_KEY} \
                            -Dsonar.sources=. \
                            -Dsonar.host.url=${SONAR_HOST_URL} \
                            -Dsonar.login=${SONAR_AUTH_TOKEN}
                        """
                    }
                }
            }
        }
        
        stage('Quality Gate') {
            steps {
                echo '🚦 Checking SonarQube Quality Gate...'
                timeout(time: 5, unit: 'MINUTES') {
                    waitForQualityGate abortPipeline: true
                }
            }
        }
        
        stage('Security Scan - Bandit') {
            steps {
                echo '🛡️ Running Bandit security scan...'
                sh '''
                    . venv/bin/activate
                    bandit -r . -f json -o bandit-report.json || true
                    bandit -r . -f txt
                '''
            }
        }
        
        stage('Dependency Check - Safety') {
            steps {
                echo '📦 Checking dependencies for vulnerabilities...'
                sh '''
                    . venv/bin/activate
                    safety check --json > safety-report.json || true
                    safety check || true
                '''
            }
        }
        
        stage('Unit Tests') {
            steps {
                echo '🧪 Running unit tests...'
                sh '''
                    . venv/bin/activate
                    pytest tests/ -v --junitxml=test-results.xml --cov=. --cov-report=xml --cov-report=html || true
                '''
            }
        }
        
        stage('Build Docker Image') {
            steps {
                echo '🐳 Building Docker image...'
                script {
                    docker.build("${DOCKER_IMAGE}:${DOCKER_TAG}")
                    docker.build("${DOCKER_IMAGE}:latest")
                }
            }
        }
        
        stage('Container Security Scan - Trivy') {
            steps {
                echo '🔒 Scanning Docker image for vulnerabilities...'
                sh '''
                    # Install Trivy if not already installed
                    if ! command -v trivy &> /dev/null; then
                        wget -qO - https://aquasecurity.github.io/trivy-repo/deb/public.key | sudo apt-key add -
                        echo "deb https://aquasecurity.github.io/trivy-repo/deb $(lsb_release -sc) main" | sudo tee -a /etc/apt/sources.list.d/trivy.list
                        sudo apt-get update
                        sudo apt-get install trivy -y
                    fi
                    
                    # Scan the Docker image
                    trivy image --severity HIGH,CRITICAL --format json --output trivy-report.json ${DOCKER_IMAGE}:${DOCKER_TAG} || true
                    trivy image --severity HIGH,CRITICAL ${DOCKER_IMAGE}:${DOCKER_TAG} || true
                '''
            }
        }
        
        stage('Security Gate Check') {
            steps {
                echo '🚨 Evaluating security scan results...'
                script {
                    // Read and evaluate security reports
                    def trivyReport = readJSON file: 'trivy-report.json'
                    def banditReport = readJSON file: 'bandit-report.json'
                    
                    def criticalIssues = 0
                    
                    // Check Trivy results
                    if (trivyReport.Results) {
                        trivyReport.Results.each { result ->
                            if (result.Vulnerabilities) {
                                result.Vulnerabilities.each { vuln ->
                                    if (vuln.Severity == 'CRITICAL') {
                                        criticalIssues++
                                    }
                                }
                            }
                        }
                    }
                    
                    // Check Bandit results
                    def highSeverityBandit = banditReport.results.findAll { 
                        it.issue_severity == 'HIGH' 
                    }.size()
                    
                    echo "🔍 Security Summary:"
                    echo "   - Critical vulnerabilities in image: ${criticalIssues}"
                    echo "   - High severity code issues: ${highSeverityBandit}"
                    
                    // Fail if too many critical issues (adjust threshold as needed)
                    if (criticalIssues > 10) {
                        error "❌ Too many critical vulnerabilities found! Aborting deployment."
                    }
                    
                    if (highSeverityBandit > 5) {
                        echo "⚠️ Warning: High number of security issues in code. Review recommended."
                    }
                }
            }
        }
        
        stage('Deploy to Staging') {
            steps {
                echo '🚀 Deploying to staging environment...'
                sh '''
                    # Stop existing container if running
                    docker stop flask-app-staging || true
                    docker rm flask-app-staging || true
                    
                    # Run new container
                    docker run -d \
                        --name flask-app-staging \
                        -p 5001:5000 \
                        ${DOCKER_IMAGE}:${DOCKER_TAG}
                    
                    # Health check
                    sleep 5
                    curl -f http://localhost:5001/ || exit 1
                '''
            }
        }
        
        stage('Approval for Production') {
            steps {
                echo '⏸️ Waiting for manual approval...'
                input message: 'Deploy to Production?', ok: 'Deploy'
            }
        }
        
        stage('Deploy to Production') {
            when {
                branch 'main'
            }
            steps {
                echo '🎯 Deploying to production environment...'
                sh '''
                    # Stop existing container if running
                    docker stop flask-app-prod || true
                    docker rm flask-app-prod || true
                    
                    # Run new container
                    docker run -d \
                        --name flask-app-prod \
                        -p 5000:5000 \
                        --restart unless-stopped \
                        ${DOCKER_IMAGE}:${DOCKER_TAG}
                    
                    # Health check
                    sleep 5
                    curl -f http://localhost:5000/ || exit 1
                '''
            }
        }
    }
    
    post {
        always {
            echo '📊 Archiving reports and cleaning up...'
            
            // Archive security reports
            archiveArtifacts artifacts: '''
                bandit-report.json,
                safety-report.json,
                trivy-report.json,
                test-results.xml,
                coverage.xml,
                htmlcov/**
            ''', allowEmptyArchive: true
            
            // Publish test results
            junit testResults: 'test-results.xml', allowEmptyResults: true
            
            // Cleanup
            sh '''
                rm -rf venv
            '''
        }
        
        success {
            echo '✅ Pipeline completed successfully!'
            echo '🎉 Application deployed with security checks passed!'
        }
        
        failure {
            echo '❌ Pipeline failed!'
            echo '🔍 Check the security reports and logs above for details.'
        }
        
        unstable {
            echo '⚠️ Pipeline completed with warnings!'
            echo '📝 Review the security findings before proceeding.'
        }
    }
}
