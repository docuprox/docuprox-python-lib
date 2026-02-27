import requests
import base64
import json
import os
import dotenv 

dotenv.load_dotenv()

class Docuprox:
    def __init__(self, api_url=None, api_key=None):
        """
        Initialize the Docuprox with the API URL and API key.

        :param api_url: The base URL of the API. If not provided, uses DOCUPROX_API_URL env var or defaults to 'https://api.docuprox.com/v1'
        :param api_key: API key for authentication. If not provided, uses DOCUPROX_API_KEY env var. Required.
        """
        self.api_url = (api_url or os.environ.get("DOCUPROX_API_URL") or "https://api.docuprox.com/v1").rstrip('/')
        self.api_key = api_key or os.environ.get("DOCUPROX_API_KEY")
        if not self.api_key:
            raise ValueError("API key is required. Provide it as parameter or set DOCUPROX_API_KEY environment variable.")
        self.headers = {'X-auth': self.api_key}

    def processfile(self, file_path, template_id, static_values=None):
        """
        Process a file by sending it as multipart/form-data to the API's /process endpoint.

        :param file_path: Path to the file to process
        :param template_id: UUID string of the template to use
        :param static_values: Optional dictionary of static values to include in processing
        :return: JSON response from the API
        :raises: ValueError if file cannot be read or API error
        """
        try:
            with open(file_path, 'rb') as f:
                files = {'actual_image': f}
                data = {'template_id': template_id}
                if static_values is not None:
                    data['static_values'] = json.dumps(static_values)
                response = requests.post(f"{self.api_url}/process", files=files, data=data, headers=self.headers)
                response.raise_for_status()
                return response.json()
        except FileNotFoundError:
            raise ValueError(f"File not found: {file_path}")
        except requests.RequestException as e:
            try:
                error_data = response.json()
                raise ValueError(f"Docuprox_API_Key request failed: {error_data.get('error', str(e))}")
            except (ValueError, json.JSONDecodeError):
                raise ValueError(f"Docuprox_API_Key request failed: {str(e)}")

    def processbase64(self, base64_data, template_id, static_values=None):
        """
        Process a base64 encoded string by sending it as JSON to the API's /process endpoint.

        :param base64_data: Base64 encoded string
        :param template_id: UUID string of the template to use
        :param static_values: Optional dictionary of static values to include in processing
        :return: JSON response from the API
        :raises: ValueError if API error
        """
        try:
            payload = {
                "actual_image": base64_data,
                "template_id": template_id
            }
            if static_values is not None:
                payload["static_values"] = static_values
            response = requests.post(f"{self.api_url}/process", json=payload, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            try:
                error_data = response.json()
                raise ValueError(f"Docuprox_API_Key request failed: {error_data.get('error', str(e))}")
            except (ValueError, json.JSONDecodeError):
                raise ValueError(f"Docuprox_API_Key request failed: {str(e)}")

    def processjobfile(self, file_path, template_id, static_values=None):
        """
        Process a job file by sending it as multipart/form-data to the API's /process-job endpoint.

        :param file_path: Path to the file to process
        :param template_id: UUID string of the template to use
        :param static_values: Optional dictionary of static values to include in processing
        :return: JSON response from the API
        :raises: ValueError if file cannot be read or API error
        """
        try:
            with open(file_path, 'rb') as f:
                files = {'actual_image': f}
                data = {'template_id': template_id}
                if static_values is not None:
                    data['static_values'] = json.dumps(static_values)
                response = requests.post(f"{self.api_url}/process-job", files=files, data=data, headers=self.headers)
                response.raise_for_status()
                return response.json()
        except FileNotFoundError:
            raise ValueError(f"File not found: {file_path}")
        except requests.RequestException as e:
            try:
                error_data = response.json()
                raise ValueError(f"Docuprox_API_Key request failed: {error_data.get('error', str(e))}")
            except (ValueError, json.JSONDecodeError):
                raise ValueError(f"Docuprox_API_Key request failed: {str(e)}")

    def processjobbase64(self, base64_data, template_id, static_values=None):
        """
        Process a job with base64 encoded string by sending it as JSON to the API's /process-job endpoint.

        :param base64_data: Base64 encoded string
        :param template_id: UUID string of the template to use
        :param static_values: Optional dictionary of static values to include in processing
        :return: JSON response from the API
        :raises: ValueError if API error
        """
        try:
            payload = {
                "actual_image": base64_data,
                "template_id": template_id
            }
            if static_values is not None:
                payload["static_values"] = static_values
            response = requests.post(f"{self.api_url}/process-job", json=payload, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            try:
                error_data = response.json()
                raise ValueError(f"Docuprox_API_Key request failed: {error_data.get('error', str(e))}")
            except (ValueError, json.JSONDecodeError):
                raise ValueError(f"Docuprox_API_Key request failed: {str(e)}")

    def getjobstatus(self, job_id):
        """
        Get the status of a processing job by its job ID.

        :param job_id: UUID string of the job to check
        :return: JSON response from the API with job status
        :raises: ValueError if job_id is invalid or API error
        """
        if not job_id:
            raise ValueError("job_id is required")

        try:
            params = {'job_id': job_id}
            response = requests.get(f"{self.api_url}/job-status", params=params, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            try:
                error_data = response.json()
                raise ValueError(f"Docuprox_API_Key request failed: {error_data.get('error', str(e))}")
            except (ValueError, json.JSONDecodeError):
                raise ValueError(f"Docuprox_API_Key request failed: {str(e)}")

    def getjobresults(self, job_id, result_format="json"):
        """
        Get the results of a completed processing job.

        :param job_id: UUID string of the job to retrieve results for
        :param result_format: Format of results - 'json' or 'csv' (default: 'json')
        :return: JSON response from the API with job results
        :raises: ValueError if job_id is invalid, format is invalid, or API error
        """
        if not job_id:
            raise ValueError("job_id is required")

        result_format = result_format.lower()
        if result_format not in ["json", "csv"]:
            raise ValueError("Invalid format. Supported formats are 'json' and 'csv'.")

        try:
            payload = {
                "job_id": job_id,
                "result_format": result_format
            }
            response = requests.post(f"{self.api_url}/job-results", json=payload, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            try:
                error_data = response.json()
                raise ValueError(f"Docuprox_API_Key request failed: {error_data.get('error', str(e))}")
            except (ValueError, json.JSONDecodeError):
                raise ValueError(f"Docuprox_API_Key request failed: {str(e)}")

    def processagentfile(self, file_path, prompt_json, document_type, custom_instructions=None, static_values=None):
        """
        Process a file using AI agent by sending it as multipart/form-data to the API's /process-agent endpoint.

        :param file_path: Path to the file to process
        :param prompt_json: JSON object/dict containing the prompt configuration
        :param document_type: Type of document being processed
        :param custom_instructions: Optional custom instructions for processing
        :param static_values: Optional dictionary of static values to include in processing
        :return: JSON response from the API
        :raises: ValueError if file cannot be read or API error
        """
        try:
            with open(file_path, 'rb') as f:
                files = {'actual_image': f}

                # Build payload
                payload = {
                    "prompt_json": prompt_json,
                    "document_type": document_type
                }
                if custom_instructions is not None:
                    payload["custom_instructions"] = custom_instructions
                if static_values is not None:
                    payload["static_values"] = static_values

                # Send payload as JSON string in form data
                data = {'payload': json.dumps(payload)}

                response = requests.post(f"{self.api_url}/process-agent", files=files, data=data, headers=self.headers)
                response.raise_for_status()
                return response.json()
        except FileNotFoundError:
            raise ValueError(f"File not found: {file_path}")
        except requests.RequestException as e:
            try:
                error_data = response.json()
                raise ValueError(f"Docuprox_API_Key request failed: {error_data.get('error', str(e))}")
            except (ValueError, json.JSONDecodeError):
                raise ValueError(f"Docuprox_API_Key request failed: {str(e)}")

    def processagentbase64(self, base64_data, prompt_json, document_type, custom_instructions=None, static_values=None):
        """
        Process base64 data using AI agent by sending it as JSON to the API's /process-agent endpoint.

        :param base64_data: Base64 encoded string of the image/document
        :param prompt_json: JSON object/dict containing the prompt configuration
        :param document_type: Type of document being processed
        :param custom_instructions: Optional custom instructions for processing
        :param static_values: Optional dictionary of static values to include in processing
        :return: JSON response from the API
        :raises: ValueError if API error
        """
        try:
            # Build payload
            payload_obj = {
                "prompt_json": prompt_json,
                "document_type": document_type
            }
            if custom_instructions is not None:
                payload_obj["custom_instructions"] = custom_instructions
            if static_values is not None:
                payload_obj["static_values"] = static_values

            # Send as JSON
            request_payload = {
                "actual_image": base64_data,
                "payload": payload_obj
            }

            response = requests.post(f"{self.api_url}/process-agent", json=request_payload, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            try:
                error_data = response.json()
                raise ValueError(f"Docuprox_API_Key request failed: {error_data.get('error', str(e))}")
            except (ValueError, json.JSONDecodeError):
                raise ValueError(f"Docuprox_API_Key request failed: {str(e)}")
# ...existing code...

