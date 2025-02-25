# Task 4: Implementing 3GPP Milenage Authentication

## Objective
Build a Node.js REST API to generate 3G authentication vectors using AWS serverless architecture.

## Architecture Overview
- **AWS Components:**  
  - **API Gateway** (REST) for endpoint exposure.  
  - **Lambda** (Node.js) for cryptographic processing.  
  - **Secrets Manager** for secure storage of OP/Secret Keys.

## Class Definitions
```javascript
class MilenageAlgorithm {
    constructor(op, secretKey) {
        this.op = op;
        this.secretKey = secretKey;
    }

    generateAV() {
        // Implement 3GPP 35.206 logic
        return { RAND, XRES, CK, IK, AUTN };
    }
}

class AuthAPI {
    async handleRequest(input) {
        const milenage = new MilenageAlgorithm(input.op, input.secretKey);
        return milenage.generateAV();
    }
}
```

## Interfaces
- **API Endpoint:**  
  ```bash
  POST /generate-av
  Body: { "op": "hex-string", "secretKey": "hex-string" }
  Response: { "RAND": "...", "XRES": "...", ... }
  ```

## Unit Tests
- **Test Case 1:** Validate output against 3GPP test vectors from TS 35.206.  
- **Test Case 2:** Ensure error handling for invalid key lengths.
- **Test Case 3:** Verify proper operation with keys retrieved from Secrets Manager.

## AWS Integration
- **Lambda Function Code:**  
  ```javascript
  exports.handler = async (event) => {
    const { op, secretKey } = JSON.parse(event.body);
    const auth = new AuthAPI();
    return auth.handleRequest({ op, secretKey });
  };
  ```


## Standards & Open Source
- **3GPP TS 35.206:** Direct implementation of Milenage.
- **Node.js Crypto Module:** For AES and SHA-256 operations.
- **License Compliance:** MIT-licensed `crypto-js` for encoding.

## Diagram

### Milenage Authentication Architecture
![Milenage Authentication Architecture](milenage_authentication_api.png)

### Milenage Algorithm Flow
Milenage algorithm:
1. Start with K (secret key) and OP
2. Generate random RAND
3. Apply AES-based operations (f1-f5)
4. Generate MAC (for AUTN)
5. Generate XRES, CK, IK
6. Assemble final authentication vector
7. Return to caller

### 3G Authentication Sequence
1. Mobile Device requesting access
2. Network sending authentication request to API
3. API generating authentication vector
4. Network challenging mobile device with RAND and AUTN
5. Mobile device computing response
6. Network verifying response against XRES
7. Successful authentication and key agreement

Include timing markers and security boundaries in this diagram. 