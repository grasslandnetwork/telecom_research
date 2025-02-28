import time
from mocks.mock_dynamo import MockDynamoDB
from event_processor import EventProcessor

def simulate_event_flow():
    print("Starting simulation of event flow across regions...")
    
    # Create mock database and processors
    db = MockDynamoDB()
    processor_us = EventProcessor(db, "us-east-1")
    processor_eu = EventProcessor(db, "eu-west-1")
    
    print("\n1. Client sends event to US region")
    event_us = {
        'id': 'customer-update-123',
        'data': {'name': 'John Doe', 'status': 'Active'},
        'idempotency_key': 'idem-abc-123'
    }
    
    print("2. US Lambda processes event and writes to DynamoDB")
    result_us = processor_us.process_event(event_us)
    print(f"   Result: {result_us['status']}")
    
    print("3. DynamoDB Global Tables replicates to EU region")
    print("   [Replication occurs automatically in production]")
    
    print("\n4. Client sends conflicting update to EU region")
    event_eu = {
        'id': 'customer-update-123',  # Same ID - potential conflict
        'data': {'name': 'John Doe', 'status': 'Inactive'},  # Different data
        'idempotency_key': 'idem-xyz-456'  # Different idempotency key
    }
    
    print("5. EU Lambda processes event")
    time.sleep(1)  # Ensure timestamp is newer
    result_eu = processor_eu.process_event(event_eu)
    print(f"   Result: {result_eu['status']}")
    
    print("\n6. Final state after conflict resolution:")
    final_data = db.get_item(Key={'Id': 'customer-update-123'})['Item']
    print(f"   Data: {final_data['Data']}")
    print(f"   Last Updated Region: {final_data['LastUpdatedRegion']}")
    
    print("\n7. Client sends duplicate request to US region")
    duplicate_event = {
        'id': 'customer-update-123',
        'data': {'name': 'John Doe', 'status': 'Changed Again'},
        'idempotency_key': 'idem-abc-123'  # Same as first request
    }
    
    print("8. US Lambda detects duplicate and ignores")
    result_dup = processor_us.process_event(duplicate_event)
    print(f"   Result: {result_dup['status']}")
    
    print("\nSimulation completed successfully")

if __name__ == "__main__":
    simulate_event_flow() 