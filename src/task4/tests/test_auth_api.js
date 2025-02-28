const { MilenageAlgorithm, AuthAPI } = require('../auth_api');
const MockCrypto = require('../mocks/mock_crypto');

// Mock crypto module
jest.mock('crypto', () => require('../mocks/mock_crypto'));

describe('MilenageAlgorithm', () => {
    let milenage;
    
    beforeEach(() => {
        // Use test vectors from 3GPP TS 35.207
        const op = '00000000000000000000000000000000';
        const key = '00000000000000000000000000000000';
        milenage = new MilenageAlgorithm(op, key);
    });
    
    test('should initialize with valid keys', () => {
        expect(milenage).toBeDefined();
    });
    
    test('should throw error with invalid key length', () => {
        expect(() => {
            new MilenageAlgorithm('123', '456');
        }).toThrow();
    });
    
    test('should generate authentication vector', () => {
        const sqn = '000000000000';
        const rand = '00000000000000000000000000000000';
        
        const av = milenage.generateAV(sqn, rand);
        
        // With our mocked crypto, we should get predictable results
        expect(av).toHaveProperty('RAND');
        expect(av).toHaveProperty('XRES');
        expect(av).toHaveProperty('AUTN');
        expect(av).toHaveProperty('CK');
        expect(av).toHaveProperty('IK');
    });
});

describe('AuthAPI', () => {
    let authApi;
    
    beforeEach(() => {
        authApi = new AuthAPI();
    });
    
    test('should handle valid request', async () => {
        const input = {
            op: '00000000000000000000000000000000',
            secretKey: '00000000000000000000000000000000'
        };
        
        const result = await authApi.handleRequest(input);
        
        expect(result).toHaveProperty('RAND');
        expect(result).toHaveProperty('XRES');
        expect(result).toHaveProperty('AUTN');
        expect(result).toHaveProperty('CK');
        expect(result).toHaveProperty('IK');
    });
    
    test('should handle invalid request', async () => {
        const input = {
            // Missing required fields
        };
        
        const result = await authApi.handleRequest(input);
        
        expect(result).toHaveProperty('error', true);
        expect(result).toHaveProperty('message');
    });
    
    test('should handle Lambda event', async () => {
        const event = {
            body: JSON.stringify({
                op: '00000000000000000000000000000000',
                secretKey: '00000000000000000000000000000000'
            })
        };
        
        const { handler } = require('../auth_api');
        const response = await handler(event);
        
        expect(response).toHaveProperty('statusCode', 200);
        expect(response).toHaveProperty('body');
        
        const body = JSON.parse(response.body);
        expect(body).toHaveProperty('RAND');
    });
}); 