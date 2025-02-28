# Solsys Technical Assessment

This repository contains solutions for two selected tasks from the Solsys technical assessment.

## Task Selection

1. **[Task 1: Managing Geo-Distributed Data](task1_geo_distributed_data.md)** - Design of an active-active architecture for handling concurrent DynamoDB Global Table transactions with conflict resolution and idempotency.

2. **[Task 4: 3GPP Milenage Authentication](task4_milenage_authentication.md)** - Implementation of a REST API for generating 3G authentication vectors using AWS serverless technologies.

## Implementation Note

As specified in the requirements, this repository focuses on:
- Setting up project structures
- Defining interfaces and classes
- Creating unit test strategies
- Explaining architecture and design decisions
- Justifying technical choices

The code is not completely functional with all details implemented, but rather demonstrates the architecture and structure of the solution.

## Running Unit Tests using Mocks of AWS Services

This repository includes mock implementations of AWS services to enable testing without actual AWS resources:
- **DynamoDB Mocks**: Simulates DynamoDB Global Tables for testing event processing and conflict resolution
- **Secrets Manager Mocks**: Simulates secure storage for authentication keys
- **Visualizers**: Demonstrates request flows and component interactions
- **Mock Crypto Services**: Simulates cryptographic operations for 3GPP authentication

To run the tests with mocks, see the "Running the Tests" section in each task's documentation.

## Diagrams

Diagrams were generated using the Python `diagrams` library. To regenerate:

```bash
pip install diagrams
python task1_geo_distributed_data_diagram.py
python task4_milenage_authentication_diagram.py
```

## AWS Templates

Infrastructure-as-Code templates are provided in the `templates` directory for AWS CloudFormation/SAM deployment. 