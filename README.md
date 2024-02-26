# openaiCostsLogger

This library provides a simple way to log OpenAI API usage and costs.

## Usage

Use the library to log responses from OpenAI's completion API, including the model used and the associated costs.

Example:

```python
import openai
import os
from openaiCostsLogger import openaiCostsLogger

# Example OpenAI completion API call
response = openai.ChatCompletion.create(
    model=os.environ["MODEL_NAME"],
    messages=messages,
)

# Logging the response with a usage tag
openaiCostsLogger().log(response, tag='usage_tag')
