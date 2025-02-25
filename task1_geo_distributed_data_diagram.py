from diagrams import Diagram, Cluster
from diagrams.aws.compute import Lambda
from diagrams.aws.database import Dynamodb
from diagrams.aws.network import Route53
from diagrams.aws.management import Cloudwatch
from diagrams.aws.integration import SQS

with Diagram("Geo-Distributed Data Architecture", show=True, direction="LR"):
    producer = Lambda("Event Producer")
    dlq = SQS("Dead Letter Queue")
    
    with Cluster("AWS Region 1"):
        lambda_1 = Lambda("Process Event A")
        ddb_1 = Dynamodb("Global Table\n(Region 1)")
        cloudwatch_1 = Cloudwatch("Monitoring")
        
    with Cluster("AWS Region 2"):
        lambda_2 = Lambda("Process Event B")
        ddb_2 = Dynamodb("Global Table\n(Region 2)")
        cloudwatch_2 = Cloudwatch("Monitoring")
    
    producer >> lambda_1
    producer >> lambda_2
    lambda_1 >> ddb_1
    lambda_2 >> ddb_2
    ddb_1 - ddb_2  # Replication link
    lambda_1 >> dlq
    lambda_2 >> dlq
    cloudwatch_1 << lambda_1
    cloudwatch_2 << lambda_2

print("Diagram has been generated and should open automatically.")
print("If it doesn't open, look for 'Geo-Distributed Data Architecture.png' in your current directory.")