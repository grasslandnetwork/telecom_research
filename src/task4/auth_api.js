const crypto = require('crypto');

class MilenageAlgorithm {
    constructor(op, secretKey) {
        this.op = Buffer.from(op, 'hex');
        this.secretKey = Buffer.from(secretKey, 'hex');
        
        // Ensure keys are valid
        if (this.op.length !== 16 || this.secretKey.length !== 16) {
            throw new Error('OP and Secret Key must be 16 bytes (32 hex chars)');
        }
    }
    
    // Generate authentication vector according to 3GPP spec
    generateAV(sqn, rand) {
        // Use crypto-secure random if not provided
        if (!rand) {
            rand = crypto.randomBytes(16);
        } else {
            rand = Buffer.from(rand, 'hex');
        }
        
        // Convert sequence number to buffer
        if (!sqn) {
            sqn = Buffer.from('000000000000', 'hex'); // Default SQN
        } else {
            sqn = Buffer.from(sqn, 'hex');
        }
        
        // Step 1: Calculate OPc (Operator Variant Algorithm Configuration Field)
        const OPc = this._calculateOPc();
        
        // Step 2: Calculate f1 (MAC-A for authentication)
        const amf = Buffer.from('0000', 'hex'); // Authentication Management Field
        const macA = this._calculateF1(OPc, rand, sqn, amf);
        
        // Step 3: Calculate f2 (RES for authentication response)
        const res = this._calculateF2(OPc, rand);
        
        // Step 4: Calculate f3 (CK for confidentiality key)
        const ck = this._calculateF3(OPc, rand);
        
        // Step 5: Calculate f4 (IK for integrity key)
        const ik = this._calculateF4(OPc, rand);
        
        // Step 6: Calculate f5 (AK for anonymity key)
        const ak = this._calculateF5(OPc, rand);
        
        // Step 7: Construct AUTN (Authentication Token)
        const sqnXorAk = Buffer.alloc(6);
        for (let i = 0; i < 6; i++) {
            sqnXorAk[i] = sqn[i] ^ ak[i];
        }
        
        const autn = Buffer.concat([sqnXorAk, amf, macA]);
        
        // Return authentication vector
        return {
            RAND: rand.toString('hex').toUpperCase(),
            XRES: res.toString('hex').toUpperCase(),
            AUTN: autn.toString('hex').toUpperCase(),
            CK: ck.toString('hex').toUpperCase(),
            IK: ik.toString('hex').toUpperCase()
        };
    }
    
    // Private methods (simplified implementation)
    _calculateOPc() {
        // This is a simplified version - real implementation uses AES
        const cipher = crypto.createCipheriv('aes-128-ecb', this.secretKey, null);
        cipher.setAutoPadding(false);
        let OPc = cipher.update(this.op);
        for (let i = 0; i < 16; i++) {
            OPc[i] ^= this.op[i];
        }
        return OPc;
    }
    
    _calculateF1(OPc, rand, sqn, amf) {
        // Simplified f1 function (real one is more complex)
        // Normally uses complex temp variables and AES rounds
        return crypto.createHmac('sha256', OPc)
            .update(Buffer.concat([rand, sqn, amf]))
            .digest().slice(0, 8); // 8 bytes for MAC-A
    }
    
    _calculateF2(OPc, rand) {
        // Simplified f2 function
        return crypto.createHmac('sha256', OPc)
            .update(rand)
            .digest().slice(0, 8); // 8 bytes for RES
    }
    
    _calculateF3(OPc, rand) {
        // Simplified f3 function
        return crypto.createHmac('sha256', OPc)
            .update(Buffer.concat([rand, Buffer.from([0x01])]))
            .digest().slice(0, 16); // 16 bytes for CK
    }
    
    _calculateF4(OPc, rand) {
        // Simplified f4 function
        return crypto.createHmac('sha256', OPc)
            .update(Buffer.concat([rand, Buffer.from([0x02])]))
            .digest().slice(0, 16); // 16 bytes for IK
    }
    
    _calculateF5(OPc, rand) {
        // Simplified f5 function
        return crypto.createHmac('sha256', OPc)
            .update(Buffer.concat([rand, Buffer.from([0x03])]))
            .digest().slice(0, 6); // 6 bytes for AK
    }
}

class AuthAPI {
    async handleRequest(input) {
        try {
            // Validate input
            if (!input.op || !input.secretKey) {
                throw new Error('Missing required parameters: op and secretKey');
            }
            
            // Create Milenage algorithm instance
            const milenage = new MilenageAlgorithm(input.op, input.secretKey);
            
            // Generate authentication vector
            return milenage.generateAV(input.sqn, input.rand);
        } catch (error) {
            return {
                error: true,
                message: error.message
            };
        }
    }
}

// Lambda handler
exports.handler = async (event) => {
    try {
        const input = JSON.parse(event.body);
        const auth = new AuthAPI();
        const result = await auth.handleRequest(input);
        
        return {
            statusCode: result.error ? 400 : 200,
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(result)
        };
    } catch (error) {
        return {
            statusCode: 500,
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ error: true, message: 'Internal server error' })
        };
    }
};

// Export for testing
module.exports = { MilenageAlgorithm, AuthAPI }; 