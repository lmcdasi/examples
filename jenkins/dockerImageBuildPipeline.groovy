#!groovy

pipeline {
   agent {
      node {
         label('linux')
      }
   }

   environment {
      DEV_DIR = ......
      TAG = ....
      DOCKER_DOMAIN = ....
   }

   options {
     gitLabConnection('YOUR_GIT_LAB_URL') //[$class: 'RebuildSettings', autoRebuild: false, rebuildDisabled: false]
   }

   parameters {
      string(name: 'PARAM_NAME', defaultValue: 'PARAM_VALUE', description: 'PARAM_DESCRIPTION', trim: false)
      string(name: 'VERSION', defaultValue: 'VERSION_VALUE', description:'Docker image version', trim: false)
   }

   stages {
      stage('Build ....') {
         steps {
            script {
               "Build product"   // or copy artifact from another build pipeline
                sh(script: ''' YOUR_BUILD_CMD  ''', returnStdout: true)

                BUILD = sh(script: 'ls -t1 ${FRONTEND_DIR}/build/libs | grep war$ | head -n 1', returnStdout: true).trim()

            }
         }
      }

      stage('Build Environment for Docker img') {
         environment { ... }
         steps {
            echo "Setting environment for docker file image"
            script { "YOUR_SCRIPT_TO_PREPARE docker img" }
         }
      }

      stage('Build Backend Docker Img') {
         environment { ... }

         steps {
            script {
               echo "Build docker image"

               docker.withServer('tcp://localhost:2375') {
                  dockerImage = docker.build('${TAG}:${VERSION}', '--build-arg ${....} ${DEV_DIR}')
               }
            }
         }
      }

      stage('Push Docker Images to Artifactory') {
         steps {
            script {
               echo "Push Docker image to Artifactory"
               docker.withServer('tcp://localhost:2375') {
                  docker.withRegistry('https://${DOCKER_DOMAIN}/${TAG}', 'docker-credentials') {
                     dockerImage.push()
                  }
               }
            }
         }
      }

      stage('Docker Image Cleanup') {
         steps {
            script {
               echo "Remove docker img with tag: ${TAG}:${VERSION}"
               CLEANUP = sh(script: 'docker image rm ${DOCKER_DOMAIN}/${TAG}:${VERSION}', returnStatus: true) != 0
               if ( CLEANUP ) {
                  echo "Unable to cleanup image tag: ${DOCKER_DOMAIN}/${TAG}:${VERSION}"
               }

               CLEANUP = sh(script: 'docker image rm ${TAG}:${VERSION}', returnStatus: true) != 0
               if ( CLEANUP ) {
                  echo "Unable to cleanup image tag: ${TAG}:${VERSION}"
               }
            }

            script {
               echo "Cleanup unused docker images"
               CLEANUP = sh(script: 'docker image prune -f', returnStatus: true) != 0
               if ( CLEANUP ) {
                  echo "Failed to cleanup docker images. Manual cleanup maybe required."
               }
            }
         }
      }
   }
}
