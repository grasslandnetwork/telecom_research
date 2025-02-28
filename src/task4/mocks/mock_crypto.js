class MockCrypto {
    static createCipheriv() {
        return {
            setAutoPadding: () => {},
            update: (buffer) => {
                // Return predictable "encrypted" buffer for testing
                return Buffer.from('0123456789ABCDEF0123456789ABCDEF', 'hex');
            }
        };
    }
    
    static createHmac() {
        return {
            update: () => ({
                digest: () => {
                    // Return predictable hash for testing
                    return Buffer.from(
                        'AABBCCDDEEFF00112233445566778899AABBCCDDEEFF00112233445566778899', 
                        'hex'
                    );
                }
            })
        };
    }
    
    static randomBytes(size) {
        // Return predictable random bytes for testing
        const bytes = Buffer.alloc(size);
        for (let i = 0; i < size; i++) {
            bytes[i] = i % 256;
        }
        return bytes;
    }
}

module.exports = MockCrypto; 