# Gemini Key Rotater

`gemini-key-rotater` is a Python package that rotates Gemini API keys/models based on their rate limits. It loads model configurations from a JSON file and selects the best available model based on remaining quota. It also includes methods to increment usage after a request and swap models when rate limits are exceeded.

## Installation

You can install the package via pip (after uploading to PyPI):


```bash
pip install gemini-key-rotater
```

## Usage

```python
from gemini_key_rotater import ModelManager

# Initialize with the JSON file containing your model configurations.
manager = ModelManager("models.json")

# Get the best available model.
model = manager.get_available_model()
if model:
    print("Using model:", model.name)
    # Perform your API call here.
    manager.increment_request(model.name)
else:
    print("No models available. Please wait for limits to reset.")

# If a 429 error occurs, swap to an alternative model.
alternative_model = manager.swap_model(model.name)
if alternative_model:
    print("Swapped to model:", alternative_model.name)
else:
    print("No alternative models available.")
```

## Json File Format

```json
[
  {
    "name": "model_A",
    "requests_per_minute": 10,
    "requests_per_day": 100,
    "ranking": 1
  },
  {
    "name": "model_B",
    "requests_per_minute": 5,
    "requests_per_day": 50,
    "ranking": 2
  }
]

```


### 3. LICENSE

Below is an example of the MIT License. Update the copyright year and your name.

```text
MIT License

Copyright (c) 2025 Your Name

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
```
