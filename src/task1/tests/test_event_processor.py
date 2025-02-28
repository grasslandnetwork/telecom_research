import unittest
from ..event_processor import EventProcessor, ConflictResolver
from ..mocks.mock_dynamo import MockDynamoDB

class TestEventProcessor(unittest.TestCase):
    def setUp(self):
        self.mock_dynamo = MockDynamoDB()
        self.processor_region1 = EventProcessor(self.mock_dynamo, "us-east-1")
        self.processor_region2 = EventProcessor(self.mock_dynamo, "eu-west-1")
        
    def test_process_new_event(self):
        # Create a new event
        event = {
            'id': 'event-123',
            'data': {'message': 'Hello World'},
            'idempotency_key': 'idem-123'
        }
        
        result = self.processor_region1.process_event(event)
        self.assertEqual(result['status'], 'success')
        
        # Check the data was stored
        stored_item = self.mock_dynamo.get_item(Key={'Id': 'event-123'})
        self.assertIn('Item', stored_item)
        self.assertEqual(stored_item['Item']['Data']['message'], 'Hello World')
        
    def test_idempotency(self):
        # Create an event
        event = {
            'id': 'event-456',
            'data': {'message': 'Test Idempotency'},
            'idempotency_key': 'idem-456'
        }
        
        # Process it once
        first_result = self.processor_region1.process_event(event)
        self.assertEqual(first_result['status'], 'success')
        
        # Process it again
        second_result = self.processor_region1.process_event(event)
        self.assertEqual(second_result['status'], 'duplicate')
        
    def test_conflict_resolution(self):
        # Simulate two regions updating simultaneously
        event1 = {
            'id': 'event-789',
            'data': {'message': 'Region 1 Data'},
            'idempotency_key': 'idem-789-1'
        }
        
        event2 = {
            'id': 'event-789',
            'data': {'message': 'Region 2 Data'},
            'idempotency_key': 'idem-789-2'
        }
        
        # Process in region 1
        self.processor_region1.process_event(event1)
        
        # Mock a conflict situation by updating version manually
        item = self.mock_dynamo.items['event-789']
        item['Version'] = 0  # Force lower version
        
        # Process in region 2
        result = self.processor_region2.process_event(event2)
        
        # Should be resolved with region 2 winning (newer timestamp)
        self.assertEqual(result['status'], 'success')
        self.assertEqual(self.mock_dynamo.items['event-789']['Data']['message'], 
                         'Region 2 Data')

if __name__ == '__main__':
    unittest.main() 