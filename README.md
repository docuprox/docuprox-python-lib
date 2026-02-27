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

# Process with static values (optional key-value pairs)
# Note: Static values will be returned in the response. By default, the value will be
# the value set in the UI. If you provide static_values, it will override the UI defaults.
static_values = {
    "company_name": "Acme Corp",
    "invoice_number": "INV-2024-001"
}
result = client.processfile("path/to/your/file.pdf", template_id, static_values=static_values)
print(result)
```

### Batch Processing with Zip Files

You can process multiple documents at once by uploading a zip file. All images and PDFs must be placed in the root of the zip file (not in subdirectories).

**Zip File Structure:**
```
documents.zip
├── invoice1.pdf
├── invoice2.pdf
├── receipt1.jpg
├── receipt2.png
└── document.pdf

✓ Correct - All files in root

documents.zip
└── folder/
    ├── invoice1.pdf
    └── invoice2.pdf

✗ Incorrect - Files in subdirectory
```

**Usage:**
```python
# Process a zip file containing multiple documents
result = client.processfile("documents.zip", template_id)

# Or with static values
result = client.processfile(
    "documents.zip",
    template_id,
    static_values={"batch_id": "BATCH-001"}
)
```

**Important:**
- All image files (JPG, PNG, etc.) and PDF files must be in the root directory of the zip
- Files in subdirectories will be ignored
- Supported formats: PDF, JPG, JPEG, PNG, TIFF, etc.

### Static Values

Static values allow you to pass predefined key-value pairs to the processing API. These values will be included in the returned response.

**Priority:**
- **Default**: If no `static_values` are provided, the response will include values set in the template UI
- **Override**: If you provide `static_values` parameter, these values will override the UI defaults

**Example:**

Let's say in the UI, `company_name` is set to "Docuprox" as the default value.

```python
# Without static_values - uses UI default
result = client.processfile("file.pdf", template_id)
# Response will include: company_name = "Docuprox" (from UI)

# With static_values - overrides UI default
static_values = {
    "company_name": "Acme Corp",  # Overrides "Docuprox" from UI
    "invoice_number": "INV-2024-001",
    "date": "2024-01-15"
}
result = client.processfile("file.pdf", template_id, static_values=static_values)
# Response will include: company_name = "Acme Corp" (from static_values)

# Works with all processing methods
result = client.processbase64(base64_string, template_id, static_values=static_values)
result = client.processjobfile("file.pdf", template_id, static_values=static_values)
result = client.processjobbase64(base64_string, template_id, static_values=static_values)
```

### Async Job Processing

For long-running or batch processing tasks, use the async job workflow:

```python
from docuprox import Docuprox

client = Docuprox(api_key="your-api-key-here")
template_id = "your-template-uuid-here"

# Step 1: Submit a job (returns immediately with job_id)
job_response = client.processjobfile("path/to/your/file.pdf", template_id)
job_id = job_response['job_id']
print(f"Job submitted: {job_id}")

# Or submit with base64 data
job_response = client.processjobbase64(base64_string, template_id)
job_id = job_response['job_id']

# Step 2: Check job status
status = client.getjobstatus(job_id)
print(f"Job status: {status}")

# Step 3: Retrieve results when job is complete (default: JSON format)
results = client.getjobresults(job_id)
print(results)

# Or get results in CSV format
results_csv = client.getjobresults(job_id, result_format="csv")
print(results_csv)
```

### AI Agent Processing

Use the AI agent endpoint for intelligent document processing with custom prompts:

```python
from docuprox import Docuprox

client = Docuprox(api_key="your-api-key-here")

# Define your prompt configuration (field: instruction mapping)
prompt_json = {
    "invoice_number": "Extract the invoice number",
    "date": "Extract the invoice date",
    "total_amount": "Extract the total amount",
    "vendor_name": "Extract the vendor name"
}

# Process a file with AI agent
result = client.processagentfile(
    file_path="path/to/invoice.pdf",
    prompt_json=prompt_json,
    document_type="invoice",
    custom_instructions="Focus on itemized line items",  # Optional
    static_values={"company_name": "Acme Corp"}  # Optional
)
print(result)

# Or process base64 data with AI agent
result = client.processagentbase64(
    base64_data=base64_string,
    prompt_json=prompt_json,
    document_type="invoice",
    custom_instructions="Extract vendor details",  # Optional
    static_values={"invoice_prefix": "INV-2024"}  # Optional
)
print(result)
```

## API

### Docuprox(api_url)

- `api_url`: The base URL of the DocuProx API.

### processfile(file_path, template_id, static_values=None)

Processes a file by reading it, encoding to base64, and sending to the `/process` endpoint with the specified template.

- `file_path`: Path to the file to process.
- `template_id`: UUID string of the template to use for processing.
- `static_values`: Optional dictionary of static key-value pairs to include in processing.
- Returns: JSON response from the API containing document data.
- Raises: `ValueError` if file not found or API error.

### processbase64(base64_data, template_id, static_values=None)

Processes a base64 encoded string by sending it to the `/process` endpoint with the specified template.

- `base64_data`: Base64 encoded string of the image/document.
- `template_id`: UUID string of the template to use for processing.
- `static_values`: Optional dictionary of static key-value pairs to include in processing.
- Returns: JSON response from the API containing document data.
- Raises: `ValueError` if API error.

### processjobfile(file_path, template_id, static_values=None)

Submits an async processing job by sending a file to the `/process-job` endpoint. Returns immediately with a job_id.

- `file_path`: Path to the file to process.
- `template_id`: UUID string of the template to use for processing.
- `static_values`: Optional dictionary of static key-value pairs to include in processing.
- Returns: JSON response from the API containing job_id and status.
- Raises: `ValueError` if file not found or API error.

### processjobbase64(base64_data, template_id, static_values=None)

Submits an async processing job with base64 encoded data to the `/process-job` endpoint. Returns immediately with a job_id.

- `base64_data`: Base64 encoded string of the image/document.
- `template_id`: UUID string of the template to use for processing.
- `static_values`: Optional dictionary of static key-value pairs to include in processing.
- Returns: JSON response from the API containing job_id and status.
- Raises: `ValueError` if API error.

### getjobstatus(job_id)

Checks the status of a processing job.

- `job_id`: UUID string of the job to check.
- Returns: JSON response from the API with job status information (e.g., pending, processing, completed, failed).
- Raises: `ValueError` if job_id is invalid or API error.

### getjobresults(job_id, result_format="json")

Retrieves the results of a completed processing job.

- `job_id`: UUID string of the job to retrieve results for.
- `result_format`: Format of results - 'json' or 'csv' (default: 'json').
- Returns: JSON response from the API with job results in the specified format.
- Raises: `ValueError` if job_id is invalid, format is invalid, or API error.

### processagentfile(file_path, prompt_json, document_type, custom_instructions=None, static_values=None)

Processes a file using AI agent for intelligent document extraction.

- `file_path`: Path to the file to process.
- `prompt_json`: JSON object/dict containing the prompt configuration with fields and instructions.
- `document_type`: Type of document being processed (e.g., "invoice", "receipt", "contract").
- `custom_instructions`: Optional custom instructions for processing.
- `static_values`: Optional dictionary of static key-value pairs to include in processing.
- Returns: JSON response from the API with AI-extracted data.
- Raises: `ValueError` if file not found or API error.

### processagentbase64(base64_data, prompt_json, document_type, custom_instructions=None, static_values=None)

Processes base64 encoded data using AI agent for intelligent document extraction.

- `base64_data`: Base64 encoded string of the image/document.
- `prompt_json`: JSON object/dict containing the prompt configuration with fields and instructions.
- `document_type`: Type of document being processed (e.g., "invoice", "receipt", "contract").
- `custom_instructions`: Optional custom instructions for processing.
- `static_values`: Optional dictionary of static key-value pairs to include in processing.
- Returns: JSON response from the API with AI-extracted data.
- Raises: `ValueError` if API error.
