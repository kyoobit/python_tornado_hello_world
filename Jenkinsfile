pipeline {
    agent any
    stages {
        stage('Source') {
            steps {
                // Get the 'main' (default) branch of the repository
                git branch: 'main',
                    url: 'https://github.com/kyoobit/python_tornado_hello_world.git'
            }
        }
        stage('Install Requirements') {
            steps {
                sh 'make install'
            }
        }
        stage('Format Code') {
            steps {
                sh 'make format'
            }
        }
        stage('Lint Code') {
            steps {
                sh 'make lint'
            }
        }
        stage('Test Code') {
            steps {
	            sh 'make test'
            }
        }
        stage('Check Dependencies') {
            steps {
	            sh 'make depcheck'
            }
        }
        stage('Security Scan') {
            steps {
	            sh 'make secscan'
            }
        }
        stage('Build Image') {
            // https://plugins.jenkins.io/docker-workflow/
            def myImage = docker.build("tornado-hello-world:${env.BUILD_ID}")
            myImage.push()
            myImage.push('latest')
        }
    }
}