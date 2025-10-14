# DocuProx Package

A Python package to interact with the DocuProx API for processing documents using templates.

## Installation

```bash
pip install docuprox
```

## Configuration

Create a `.env` file in your project root with your API credentials:

```env
DOCUPROX_API_URL=https://api.docuprox.com/v1
DOCUPROX_API_KEY=your-api-key-here
```

Or set environment variables directly:

```bash
export DOCUPROX_API_URL=https://api.docuprox.com/v1
export DOCUPROX_API_KEY=your-api-key-here
```

## Usage

```python
from docuprox import Docuprox

# Initialize the client (API key required, can be set via DOCUPROX_API_KEY env var)
client = Docuprox(api_key="your-api-key-here")  # Uses default URL: https://api.docuprox.com/v1

# Or set custom URL and API key
client = Docuprox(api_url="https://your-custom-api.com/v1", api_key="your-api-key-here")

# Or use environment variables (recommended for production)
# Set DOCUPROX_API_URL and DOCUPROX_API_KEY environment variables
client = Docuprox()  # Will use env vars or defaults

# Process a file with a template (sends as multipart/form-data)
template_id = "your-template-uuid-here"
result = client.processfile("path/to/your/file.pdf", template_id)
print(result)

# Process base64 data with a template (sends as JSON)
base64_string = "your_base64_encoded_data_here"
result = client.processbase64(base64_string, template_id)
print(result)
```

## API

### Docuprox(api_url)

- `api_url`: The base URL of the DocuProx API.

### processfile(file_path, template_id)

Processes a file by reading it, encoding to base64, and sending to the `/process` endpoint with the specified template.

- `file_path`: Path to the file to process.
- `template_id`: UUID string of the template to use for processing.
- Returns: JSON response from the API containing document data.
- Raises: `ValueError` if file not found or API error.

### processbase64(base64_data, template_id)

Processes a base64 encoded string by sending it to the `/process` endpoint with the specified template.

- `base64_data`: Base64 encoded string of the image/document.
- `template_id`: UUID string of the template to use for processing.
- Returns: JSON response from the API containing document data.
- Raises: `ValueError` if API error.
