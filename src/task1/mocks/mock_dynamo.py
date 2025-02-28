class MockDynamoDB:
    def __init__(self):
        self.items = {}
        self.idempotency_keys = {}
        
    def update_item(self, Key, UpdateExpression, ConditionExpression=None, 
                    ExpressionAttributeNames=None, ExpressionAttributeValues=None, 
                    ReturnValues=None):
        item_id = Key['Id']
        
        # Parse update expression
        if "SET" in UpdateExpression:
            updates = UpdateExpression.replace("SET ", "").split(", ")
            
            # Create a new item if it doesn't exist
            if item_id not in self.items:
                self.items[item_id] = {'Id': item_id}
            
            # Process each update
            for update in updates:
                key, value = update.split(" = ")
                actual_key = ExpressionAttributeNames.get(key, key)
                actual_value = ExpressionAttributeValues.get(value)
                self.items[item_id][actual_key] = actual_value
                
            return {"Attributes": self.items[item_id]}
        return {}
    
    def put_item(self, Item):
        if 'IdempotencyKey' in Item:
            self.idempotency_keys[Item['IdempotencyKey']] = Item
        elif 'Id' in Item:
            self.items[Item['Id']] = Item
        return {}
    
    def get_item(self, Key):
        if 'Id' in Key and Key['Id'] in self.items:
            return {"Item": self.items[Key['Id']]}
        elif 'IdempotencyKey' in Key and Key['IdempotencyKey'] in self.idempotency_keys:
            return {"Item": self.idempotency_keys[Key['IdempotencyKey']]}
        return {} 