# openai-costs-logger

This library provides a simple way to log OpenAI API usage and costs. It maintains a record of the number of prompt and completion tokens used for different OpenAI models, as well as the associated costs.

## Features

- Tracks usage and costs for different tags and models.
- Allows logging of token usage and costs in a structured format.
- Provides flexibility to use a custom logger.

## Usage

### Basic Usage

Use the library to log responses from OpenAI's completion API, including the model used and the associated costs.

```python
import openai
from openai_costs_logger import costsLogger

# Example OpenAI completion API call
response = openai.ChatCompletion.create(
    model='gpt-3.5-turbo-0125',
    messages=messages,
)
```
# Logging the response with a usage tag
```python
costsLogger().log(response, tag='usage_tag')
```
# Advanced Usage with Custom Logger
You can also pass a custom logger to the log method if you want to use a specific logging configuration.

```python
import logging
from openai_costs_logger import costsLogger
```
# Set up your custom logger
```python
custom_logger = logging.getLogger('my_custom_logger')
logging.basicConfig(level=logging.INFO)
```
# Using the custom logger
```python
costsLogger().log(response, tag='usage_tag', logger=custom_logger)
```
Model Costs
The package currently supports cost calculation for the following models:

GPT-4 models (including various versions)
GPT-3.5-Turbo models (including various versions)
Costs are based on the number of tokens used for prompts and completions, with different rates for different models.
