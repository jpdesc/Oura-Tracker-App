pipeline {
    agent any

    stages {
        stage('Setup') {
            steps {
                ansiblePlaybook installation: 'Ansible', playbook: 'build.yaml'
                properties([[$class: 'EnvInjectJobProperty', info: [loadFilesFromMaster: false, propertiesFilePath: '/srv/jenkins/.env', secureGroovyScript: [classpath: [], oldScript: '', sandbox: false, script: '']], keepBuildVariables: true, keepJenkinsSystemVariables: true, on: true], pipelineTriggers([pollSCM('* * * * *')])])
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
                . /venvs/jenkins_env/bin/activate
                python3 run.py
                """
            }
        }
        stage('Test') {
            steps {
                sh """
                . /venvs/jenkins_env/bin/activate
                python3 -m pytest
                """
            }
        }
    }
}
