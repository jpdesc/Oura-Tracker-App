pipeline {
    agent any

    stages {
        stage('Setup') {
            steps {
                ansiblePlaybook 'build.yaml'

            }
                // Run ansible to download dependencies and activate venv
        }
        stage('Checkout') {
            steps {
                dir('/srv/jenkins') {
                    checkout([$class: 'GitSCM', branches: [[name: 'main']], extensions: [], userRemoteConfigs: [[url: 'https://github.com/jpdesc/Oura-Tracker-App.git']]])
                }
            }
        }
        stage('Build') {
            steps {
                dir('srv/jenkins') {
                    git branch: 'main', url: 'https://github.com/jpdesc/Oura-Tracker-App.git'
                    sh '. /venvs/jenkins_env/bin/activate'
                    sh 'python3 run.py'
                }
            }
        }
        stage('Test') {
            steps {
                sh 'python3 -m pytest'
            }
        }
    }
}
