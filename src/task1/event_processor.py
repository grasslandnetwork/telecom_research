import time
import uuid
from datetime import datetime

class EventProcessor:
    def __init__(self, dynamo_table, region):
        self.dynamo = dynamo_table
        self.region = region
        
    def process_event(self, event):
        # Check for duplicate processing using idempotency key
        if self._is_duplicate(event.get('idempotency_key')):
            return {"status": "duplicate", "message": "Event already processed"}
            
        # Generate version and timestamp for conflict resolution
        version = int(time.time() * 1000)  # millisecond timestamp
        
        try:
            # Conditional update with versioning
            response = self.dynamo.update_item(
                Key={'Id': event.get('id')},
                UpdateExpression="SET #data = :data, #version = :version, #region = :region, #timestamp = :timestamp",
                ConditionExpression="attribute_not_exists(#version) OR #version < :version",
                ExpressionAttributeNames={
                    '#data': 'Data',
                    '#version': 'Version',
                    '#region': 'LastUpdatedRegion',
                    '#timestamp': 'Timestamp'
                },
                ExpressionAttributeValues={
                    ':data': event.get('data'),
                    ':version': version,
                    ':region': self.region,
                    ':timestamp': datetime.now().isoformat()
                },
                ReturnValues="ALL_NEW"
            )
            
            # Also store the idempotency key to prevent duplicates
            self.dynamo.put_item(
                Item={
                    'IdempotencyKey': event.get('idempotency_key'),
                    'ProcessedAt': datetime.now().isoformat(),
                    'EventId': event.get('id')
                }
            )
            
            return {
                "status": "success",
                "message": "Event processed successfully",
                "data": response.get('Attributes')
            }
            
        except Exception as e:
            if "ConditionalCheckFailedException" in str(e):
                # Conflict occurred - fetch current item to resolve
                current_item = self.dynamo.get_item(
                    Key={'Id': event.get('id')}
                ).get('Item')
                
                resolver = ConflictResolver()
                result = resolver.resolve_conflict(current_item, event, self.region)
                
                return result
            else:
                # Other error
                return {
                    "status": "error",
                    "message": str(e)
                }
    
    def _is_duplicate(self, idempotency_key):
        if not idempotency_key:
            # Generate one if not provided
            return False
            
        # Check if this key has been processed before
        response = self.dynamo.get_item(
            Key={'IdempotencyKey': idempotency_key}
        )
        
        return 'Item' in response


class ConflictResolver:
    def resolve_conflict(self, existing_item, new_event, current_region):
        # Default to last-write-wins based on version (timestamp)
        existing_version = existing_item.get('Version', 0)
        new_version = int(time.time() * 1000)
        
        if new_version > existing_version:
            # New event wins
            return {
                "status": "resolved",
                "resolution": "new_data_applied",
                "message": "Conflict resolved using last-write-wins"
            }
        else:
            # Existing data wins
            return {
                "status": "resolved",
                "resolution": "existing_data_kept",
                "message": "Conflict resolved using last-write-wins"
            } 