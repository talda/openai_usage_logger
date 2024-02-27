import unittest
from openai_usage_logger import usageLogger
import unittest.mock as mock

class TestUsageLogger(unittest.TestCase):

    def setUp(self):
        # Setup that runs before each test method
        self.logger = usageLogger()

    def test_singleton(self):
        # Test that only one instance of usageLogger is created
        logger1 = usageLogger()
        logger2 = usageLogger()
        self.assertEqual(logger1, logger2)

    def test_log(self):
         # Create a mock response
        usage_mock = mock.Mock()
        usage_mock.prompt_tokens = 500
        usage_mock.completion_tokens = 1000

        response_mock = mock.Mock()
        response_mock.model = 'gpt-4'
        response_mock.usage = usage_mock

        # Use the log method
        log_entry = self.logger.log(response=response_mock, tag='test_tag')

        # Now verify that token counts and costs are updated correctly
        # Assert the prompt tokens are logged
        self.assertEqual(self.logger.prompt_tokens['test_tag']['gpt-4'], 500)
        # Assert the completion tokens are logged
        self.assertEqual(self.logger.completion_tokens['test_tag']['gpt-4'], 1000)

        # Calculate the costs manually
        prompt_cost = 500 * self.logger.prompt_token_cost['gpt-4']
        completion_cost = 1000 * self.logger.completion_token_cost['gpt-4']
        total_cost = prompt_cost + completion_cost

        # Verify the total cost for the tag
        total_cost_for_tag = sum(
            v['Total Cost for Tag']
            for v in log_entry['Costs Per Tag'].values()
        )

        self.assertAlmostEqual(total_cost_for_tag, total_cost)
        pass

    def test_multiple_tags_and_models(self):
        # Initialize the logger
        logger = usageLogger()
        
        # Create mock responses for different models and tags
        models_tags = [('gpt-4', 'test_tag1'), ('gpt-3.5-turbo-0125', 'test_tag2')]
        for model, tag in models_tags:
            response_mock = mock.Mock()
            response_mock.model = model
            response_mock.usage.prompt_tokens = 300
            response_mock.usage.completion_tokens = 600
            
            # Log the mock response under specified tag
            log_entry = logger.log(response_mock, tag=tag)
            
            # Verify that prompt token counts are updated correctly
            self.assertEqual(logger.prompt_tokens[tag][model], 300)
            
            # Verify that completion token counts are updated correctly
            self.assertEqual(logger.completion_tokens[tag][model], 600)
            
        # Now check if the total cost across all tags is computed correctly
        total_cost_across_all_tags = 0
        for model, tag in models_tags:
            expected_prompt_cost = 300 * logger.prompt_token_cost[model]
            expected_completion_cost = 600 * logger.completion_token_cost[model]
            total_cost_across_all_tags += expected_prompt_cost + expected_completion_cost

        pass


if __name__ == '__main__':
    unittest.main()
