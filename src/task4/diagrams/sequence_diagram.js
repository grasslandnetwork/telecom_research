// This would be generated with a JS-based diagram tool
// For now, this is pseudocode for sequence diagram generation

/*
sequenceDiagram
    Client->>API Gateway: POST /generate-av
    API Gateway->>Lambda: Forward request
    Lambda->>Secrets Manager: Get OP/Key
    Secrets Manager-->>Lambda: Return secrets
    
    Lambda->>Lambda: Create Milenage instance
    Lambda->>Lambda: Calculate OPc
    Lambda->>Lambda: Generate RAND
    Lambda->>Lambda: Calculate XRES, CK, IK
    Lambda->>Lambda: Calculate AUTN
    
    Lambda-->>API Gateway: Return AV
    API Gateway-->>Client: Return AV response
*/

// This would be implemented with a tool like mermaid.js in a real project 