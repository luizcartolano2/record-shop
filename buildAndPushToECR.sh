#!/bin/bash

# IMPORTANT: First of all, retrieve an authentication token and authenticate your
# Docker client to your registry with the following one-line command:
#
#   aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <aws-id>.dkr.ecr.us-east-1.amazonaws.com/
#
# If you don't have AWS cli installed, you can simply do it with the following commands:
#   curl "https://awscli.amazonaws.com/AWSCLIV2.pkg" -o "AWSCLIV2.pkg"
#   sudo installer -pkg AWSCLIV2.pkg -target /
#
# and once installed, configure it with:
#   aws configure

docker build -t record-shop .
docker tag record-shop:latest <aws-id>.dkr.ecr.us-east-1.amazonaws.com/<ecs-project>:latest
docker push <aws-id>.dkr.ecr.us-east-1.amazonaws.com/<ecs-project>:latest
