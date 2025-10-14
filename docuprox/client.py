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

    def processfile(self, file_path, template_id):
        """
        Process a file by sending it as multipart/form-data to the API's /process endpoint.

        :param file_path: Path to the file to process
        :param template_id: UUID string of the template to use
        :return: JSON response from the API
        :raises: ValueError if file cannot be read or API error
        """
        try:
            with open(file_path, 'rb') as f:
                files = {'actual_image': f}
                data = {'template_id': template_id}
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

    def processbase64(self, base64_data, template_id):
        """
        Process a base64 encoded string by sending it as JSON to the API's /process endpoint.

        :param base64_data: Base64 encoded string
        :param template_id: UUID string of the template to use
        :return: JSON response from the API
        :raises: ValueError if API error
        """
        try:
            payload = {
                "actual_image": base64_data,
                "template_id": template_id
            }
            response = requests.post(f"{self.api_url}/process", json=payload, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            try:
                error_data = response.json()
                raise ValueError(f"Docuprox_API_Key request failed: {error_data.get('error', str(e))}")
            except (ValueError, json.JSONDecodeError):
                raise ValueError(f"Docuprox_API_Key request failed: {str(e)}")
# ...existing code...

