from diagrams import Diagram
from diagrams.aws.compute import Lambda
from diagrams.aws.network import APIGateway
from diagrams.aws.security import SecretsManager
from diagrams.aws.management import Cloudwatch
from diagrams.programming.framework import React  # Using React icon as a generic client

with Diagram("Milenage Authentication API", show=True, filename="milenage_authentication_api", direction="LR"):
    client = React("Mobile Network")
    api = APIGateway("REST API")
    lambda_fn = Lambda("Generate Auth Vector")
    secrets = SecretsManager("OP/Key Storage")
    logs = Cloudwatch("Logs & Metrics")
    
    # Complete flow including client and return path
    client >> api >> lambda_fn
    lambda_fn >> secrets
    lambda_fn >> logs
    lambda_fn >> api >> client  # Return path

print("Diagram has been generated and should open automatically.")
print("If it doesn't open, look for 'milenage_authentication_api.png' in your current directory.")