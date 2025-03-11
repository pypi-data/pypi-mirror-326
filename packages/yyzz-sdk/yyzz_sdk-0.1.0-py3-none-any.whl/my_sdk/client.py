from typing import Optional, Dict, Any
import requests
from .exceptions import SDKException

class Client:
    def __init__(
        self,
        api_key: str,
        base_url: str = "https://api.example.com",
        timeout: int = 30
    ):
        self.api_key = api_key
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        })

    def _request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        try:
            response = self.session.request(
                method=method,
                url=f"{self.base_url}/{endpoint.lstrip('/')}",
                params=params,
                json=json,
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise SDKException(f"Request failed: {str(e)}") 