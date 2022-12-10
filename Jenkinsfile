pipeline {
    agent any

    stages {
        stage('Setup') {
            steps {
                ansiblePlaybook installation: 'Ansible', playbook: 'build.yaml'
            }
                // Run ansible to download dependencies
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
                . /venvs/jenkins/bin/activate
                cat /srv/jenkins/.env > .env
                python run.py
                """
            }
        }
        stage('Test') {
            steps {
                sh """
                . /venvs/jenkins/bin/activate
                cat /srv/jenkins/.env > .env
                pytest functional/
                """
            }
        }
    }
}
