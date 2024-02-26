import json
import logging
from collections import defaultdict

class openaiCostsLogger:
    _instance = None
    _is_initialized = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not self._is_initialized:
            self.prompt_tokens = defaultdict(lambda: defaultdict(int))
            self.completion_tokens = defaultdict(lambda: defaultdict(int))

            self.prompt_token_cost = {
                'gpt-4-0125-preview': 0.01 / 1000,
                'gpt-4-1106-preview': 0.01 / 1000,
                'gpt-4-1106-vision-preview': 0.01 / 1000,
                'gpt-4': 0.03 / 1000,
                'gpt-4-32k': 0.06 / 1000,
                'gpt-3.5-turbo-0125': 0.0005 / 1000,
                'gpt-3.5-turbo-instruct': 0.0015 / 1000,
                'gpt-3.5-turbo-1106': 0.0010 / 1000,
                'gpt-3.5-turbo-0613': 0.0015 / 1000,
                'gpt-3.5-turbo-16k-0613': 0.0030 / 1000,
                'gpt-3.5-turbo-0301': 0.0015 / 1000
            }
            self.completion_token_cost = {
                'gpt-4-0125-preview': 0.03 / 1000,
                'gpt-4-1106-preview': 0.03 / 1000,
                'gpt-4-1106-vision-preview': 0.03 / 1000,
                'gpt-4': 0.06 / 1000,
                'gpt-4-32k': 0.12 / 1000,
                'gpt-3.5-turbo-0125': 0.0015 / 1000,
                'gpt-3.5-turbo-instruct': 0.0020 / 1000,
                'gpt-3.5-turbo-1106': 0.0020 / 1000,
                'gpt-3.5-turbo-0613': 0.0020 / 1000,
                'gpt-3.5-turbo-16k-0613': 0.0040 / 1000,
                'gpt-3.5-turbo-0301': 0.0020 / 1000
            }

            
            # Set up logging
            self.logger = logging.getLogger(__name__)
            logging.basicConfig(level=logging.INFO)

            self.__class__._is_initialized = True

    def log(self, response, tag=''):
        model = response.model
        prompt_tokens_added = response.usage.prompt_tokens
        completion_tokens_added = response.usage.completion_tokens

        self.prompt_tokens[tag][model] += prompt_tokens_added
        self.completion_tokens[tag][model] += completion_tokens_added

        # Prepare log entry for all tags and calculate total cost
        all_tags_log_entry = {}
        total_cost_across_all_tags = 0

        for each_tag in self.prompt_tokens.keys():
            total_prompt_token_cost = sum(self.prompt_tokens[each_tag][m] * self.prompt_token_cost.get(m, 0) for m in self.prompt_tokens[each_tag])
            total_completion_token_cost = sum(self.completion_tokens[each_tag][m] * self.completion_token_cost.get(m, 0) for m in self.completion_tokens[each_tag])
            total_cost_for_tag = total_prompt_token_cost + total_completion_token_cost

            all_tags_log_entry[each_tag] = {
                'Total Prompt Tokens': dict(self.prompt_tokens[each_tag]),
                'Total Completion Tokens': dict(self.completion_tokens[each_tag]),
                'Total Cost for Prompt Tokens': total_prompt_token_cost,
                'Total Cost for Completion Tokens': total_completion_token_cost,
                'Total Cost for Tag': total_cost_for_tag
            }

            total_cost_across_all_tags += total_cost_for_tag

        # Log the information in a more structured format
        log_entry = {
            'Current Tag': tag,
            'Model': model,
            'Prompt Tokens Added': prompt_tokens_added,
            'Completion Tokens Added': completion_tokens_added,
            'Costs Per Tag': all_tags_log_entry,
            'Total Cost Across All Tags': total_cost_across_all_tags
        }
        
        self.logger.info(json.dumps(log_entry, indent=4))
