# Task 1: Managing Geo-Distributed Data Across AWS Regions

## Objective
Design an active-active architecture to handle concurrent DynamoDB Global Table transactions with conflict resolution and idempotency.

## Architecture Overview
- **AWS Serverless Components:**  
  - **DynamoDB Global Tables** (Regions 1 and 2) for cross-region replication.  
  - **Lambda Functions** (Python/Node.js) in each region to process events.  
  - **Amazon SQS** (Dead Letter Queue) for failed event handling.  
  - **Step Functions** for idempotent workflow orchestration.  

- **Conflict Resolution Strategy:**  
  - Use **conditional writes** and **last-write-wins** with client-side timestamps.  
  - **AWS AppSync** (optional) for real-time conflict detection.  

## Class Definitions
```python
class EventProcessor:
    def __init__(self, dynamo_table, region):
        self.dynamo = dynamo_table
        self.region = region

    def process_event(self, event):
        # Apply idempotency key check
        if self._is_duplicate(event.idempotency_key):
            return {"status": "duplicate"}
        # Conditional update with versioning
        return self.dynamo.update_item(...)

class ConflictResolver:
    def resolve(self, item_region1, item_region2):
        # Compare timestamps and merge data
        return merged_item
```

## Interfaces
- **DynamoDB Table Schema:**  
  ```json
  {
    "Id": "string",
    "Data": "string",
    "Version": "number",
    "LastUpdatedRegion": "string",
    "Timestamp": "number",
    "IdempotencyKey": "string"
  }
  ```
- **Lambda Handler:**  
  ```python
  def lambda_handler(event, context):
      processor = EventProcessor(dynamo_table, current_region)
      return processor.process_event(event)
  ```

## Unit Tests
- **Test Case 1:** Simulate concurrent updates in two regions and validate conflict resolution.  
- **Test Case 2:** Validate idempotency using repeated idempotency keys.  

## AWS Integration
- **Serverless Framework Template:**  
  ```yaml
  resources:
    DynamoTable:
      Type: AWS::DynamoDB::Table
      Properties:
        TableName: GlobalEventTable
        Replicas:
          - Region: us-east-1
          - Region: eu-west-1
  ```

  **CloudFormation Template Excerpt:**
  ```yaml
  GlobalEventTable:
    Type: AWS::DynamoDB::GlobalTable
    Properties:
      TableName: GlobalEventTable
      BillingMode: PAY_PER_REQUEST
      AttributeDefinitions:
        - AttributeName: Id
          AttributeType: S
        - AttributeName: IdempotencyKey
          AttributeType: S
      KeySchema:
        - AttributeName: Id
          KeyType: HASH
      GlobalSecondaryIndexes:
        - IndexName: IdempotencyIndex
          KeySchema:
            - AttributeName: IdempotencyKey
              KeyType: HASH
          Projection:
            ProjectionType: ALL
      Replicas:
        - Region: us-east-1
          PointInTimeRecoverySpecification:
            PointInTimeRecoveryEnabled: true
        - Region: eu-west-1
          PointInTimeRecoverySpecification:
            PointInTimeRecoveryEnabled: true
            
  EventProcessorLambda:
    Type: AWS::Serverless::Function
    Properties:
      CodeUri: ../src/task1/
      Handler: event_processor.lambda_handler
      Runtime: python3.9
      Timeout: 30
      Policies:
        - DynamoDBCrudPolicy:
            TableName: !Ref GlobalEventTable
  ```

## Telecom Standards & Justifications
- **TM Forum Open API Standards:** Used for event schema design.
- **AWS Well-Architected Framework:** Ensures scalability and cost optimization.

## Active-Active Architecture Overview Diagram

![Active-Active Architecture Overview](geo-distributed_data_architecture.png)
