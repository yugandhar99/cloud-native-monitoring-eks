import os
import boto3
from botocore.exceptions import ClientError

REPOSITORY_NAME = os.environ.get("ECR_REPOSITORY_NAME", "cloud-native-monitoring-eks")
REGION = os.environ.get("AWS_REGION", "us-east-1")

ecr_client = boto3.client("ecr", region_name=REGION)

try:
    response = ecr_client.create_repository(repositoryName=REPOSITORY_NAME)
    repository_uri = response["repository"]["repositoryUri"]
    print(f"Created ECR repository: {repository_uri}")
except ClientError as error:
    if error.response.get("Error", {}).get("Code") == "RepositoryAlreadyExistsException":
        response = ecr_client.describe_repositories(repositoryNames=[REPOSITORY_NAME])
        repository_uri = response["repositories"][0]["repositoryUri"]
        print(f"ECR repository already exists: {repository_uri}")
    else:
        raise
