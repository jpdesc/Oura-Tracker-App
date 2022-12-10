pipeline {
    agent any

    stages {
        stage('Setup') {
            steps {
                ansiblePlaybook installation: 'Ansible', playbook: 'build.yaml'
            }
                // Run ansible to download dependencies and activate venv
        }
        stage('Checkout') {
            steps {
                checkout([$class: 'GitSCM', branches: [[name: 'main']], extensions: [], userRemoteConfigs: [[url: 'https://github.com/jpdesc/Oura-Tracker-App.git']]])
            }
        }
        stage('Build') {
            steps {
                git branch: 'main', url: 'https://github.com/jpdesc/Oura-Tracker-App.git'
                sh """
                ./srv/jenkins/setup.sh
                python3 run.py
                """
            }
        }
        stage('Test') {
            steps {
                sh """
                ./srv/jenkins/setup.sh
                python3 -m pytest
                """
            }
        }
    }
}
