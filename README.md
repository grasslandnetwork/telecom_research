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

## Diagrams

Diagrams were generated using the Python `diagrams` library. To regenerate:

```bash
pip install diagrams
python task1_geo_distributed_data_diagram.py
python task4_milenage_authentication_diagram.py
```

## AWS Templates

Infrastructure-as-Code templates are provided in the `templates` directory for AWS CloudFormation/SAM deployment. 