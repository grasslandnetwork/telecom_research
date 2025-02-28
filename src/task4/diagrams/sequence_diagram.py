from diagrams import Diagram
from diagrams.aws.compute import Lambda
from diagrams.aws.network import APIGateway
from diagrams.aws.security import SecretsManager
from diagrams.aws.management import Cloudwatch
from diagrams.custom import Custom
from diagrams.programming.framework import React

with Diagram("Task 4: Milenage Authentication Sequence", show=False, direction="TB"):
    # Define components
    client = React("Client Application")
    api_gateway = APIGateway("API Gateway")
    lambda_fn = Lambda("Auth Vector Generator")
    secrets = SecretsManager("OP/Key Storage")
    cloudwatch = Cloudwatch("CloudWatch Logs")
    
    # Request flow
    client >> api_gateway
    api_gateway >> lambda_fn
    lambda_fn >> secrets
    
    # Response flow
    secrets >> lambda_fn
    lambda_fn >> api_gateway
    api_gateway >> client
    
    # Monitoring
    lambda_fn >> cloudwatch 