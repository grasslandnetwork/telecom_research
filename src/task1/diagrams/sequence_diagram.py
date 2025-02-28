from diagrams import Diagram
from diagrams.aws.compute import Lambda
from diagrams.aws.database import Dynamodb
from diagrams.aws.integration import SimpleQueueServiceSqs
from diagrams.aws.management import Cloudwatch
from diagrams.custom import Custom
from diagrams.programming.framework import React

with Diagram("Task 1: Event Processing Sequence", show=False, direction="TB"):
    # Define components
    client = React("Client Application")
    lambda_region1 = Lambda("Lambda Region 1")
    lambda_region2 = Lambda("Lambda Region 2")
    dynamo_region1 = Dynamodb("DynamoDB Region 1")
    dynamo_region2 = Dynamodb("DynamoDB Region 2")
    sqs = SimpleQueueServiceSqs("Dead Letter Queue")
    cloudwatch = Cloudwatch("CloudWatch Logs")
    
    # Normal flow
    client >> lambda_region1
    lambda_region1 >> dynamo_region1
    dynamo_region1 >> dynamo_region2
    
    # Error handling
    lambda_region1 >> sqs
    
    # Conflict resolution flow
    client >> lambda_region2
    lambda_region2 >> dynamo_region2
    dynamo_region2 >> dynamo_region1
    
    # Monitoring
    lambda_region1 >> cloudwatch
    lambda_region2 >> cloudwatch 