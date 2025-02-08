from enum import Enum
from typing import Optional, Dict, Any
import requests
from dataclasses import dataclass
import time

class AspectRatios(str, Enum):
    SQUARE = "square"
    PORTRAIT = "portrait"
    LANDSCAPE = "landscape"

class ImageStatus(str, Enum):
    PROCESSING = "processing"
    COMPLETE = "complete"

@dataclass
class GenerateImageRequest:
    prompt: str
    character: str
    style: Optional[str] = None
    guidance: Optional[float] = None
    seed: Optional[int] = None
    aspect_ratio: Optional[AspectRatios] = None

@dataclass
class GeneratedImage:
    status: ImageStatus
    url: Optional[str] = None
    caption: Optional[str] = None
    created_at: Optional[str] = None

@dataclass
class ApiResponse:
    data: dict
    remaining_balance: Optional[float] = None
    remaining_requests_this_minute: Optional[int] = None

class MemeDeckAPIError(Exception):
    """Base exception for MemeDeck API errors"""
    pass

class MemeDeckClient:
    def __init__(self, api_key: str, deck_id: str, base_url: str = "https://studio.api.memedeck.xyz"):
        """
        Initialize the MemeDeck API client
        
        Args:
            api_key: Your MemeDeck API key
            deck_id: Your deck ID
            base_url: Base URL for the API (optional)
        """
        self.api_key = api_key
        self.deck_id = deck_id.replace("deck:", "") if deck_id.startswith("deck:") else deck_id
        self.base_url = base_url.rstrip('/')
        
    @property
    def _headers(self) -> Dict[str, str]:
        """Get the headers required for API requests"""
        return {
            "X-Memedeck-API-Key": self.api_key,
            "X-Memedeck-Deck-Id": self.deck_id,
        }
    
    def _handle_response(self, response: requests.Response) -> Dict[str, Any]:
        """Handle API response and raise appropriate exceptions"""
        if response.status_code == 401:
            raise MemeDeckAPIError("Invalid API key or deck ID")
        elif response.status_code != 200:
            raise MemeDeckAPIError(f"API request failed with status {response.status_code}: {response.text}")
        
        return ApiResponse(
            data = response.json(),
            remaining_balance = response.headers.get('x-memedeck-remaining-balance'),
            remaining_requests_this_minute = response.headers.get('x-memedeck-remaining-requests-this-minute'),
        )

    def reset_api_key(self, full: bool = False) -> ApiResponse|str:
        """Reset the API key for your deck"""
        response = requests.post(f"{self.base_url}/api/reset_key", headers=self._headers)
        result = self._handle_response(response)
        if full:
            return result
        else:
            return result.data["new_key"]

    def get_balance(self, full: bool = False) -> ApiResponse|float:
        """Get the current rizz balance for your deck"""
        response = requests.get(f"{self.base_url}/api/balance", headers=self._headers)
        result = self._handle_response(response)
        if full:
            return result
        else:
            return float(result.data["rizz_balance"])

    def get_history(self, full: bool = False) -> ApiResponse|list:
        """Get the history of actions for your deck"""
        response = requests.get(f"{self.base_url}/api/history", headers=self._headers)
        result = self._handle_response(response)
        if full:
            return result
        else:
            return result.data

    def get_stats(self, full: bool = False) -> Dict[str, Any]:
        """Get statistics about your deck"""
        response = requests.get(f"{self.base_url}/api/stats", headers=self._headers)
        result = self._handle_response(response)
        if full:
            return result
        else:
            return result.data

    def get_styles(self, full: bool = False) -> list:
        """Get available aesthetic styles"""
        response = requests.get(f"{self.base_url}/api/styles")
        result = self._handle_response(response)
        if full:
            return result
        else:
            return result.data

    def generate_image(
        self,
        request: GenerateImageRequest,
        wait: bool = False,
        timeout: int = 300,
        poll_interval: int = 5
    ) -> ApiResponse|GeneratedImage:
        """
        Generate an image using the provided parameters
        
        Args:
            request: GenerateImageRequest object containing generation parameters
            wait: If True, wait for the image generation to complete
            timeout: Maximum time to wait for completion in seconds (only used if wait=True)
            poll_interval: Time between status checks in seconds (only used if wait=True)
            
        Returns:
            Either an ApiResponse containing the prompt_id to poll, or the final GeneratedImage if wait was True
        """
        payload = {
            "prompt": request.prompt,
            "character": request.character,
            "style": request.style,
            "guidance": request.guidance,
            "seed": request.seed,
            "aspect_ratio": request.aspect_ratio.value if request.aspect_ratio else None
        }
        
        response = requests.post(
            f"{self.base_url}/api/generate/image",
            headers=self._headers,
            json={k: v for k, v in payload.items() if v is not None}
        )
        result = self._handle_response(response)
        
        if not wait:
            return result
            
        prompt_id = result.data["prompt_id"]
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            image = self.get_generated_image(prompt_id)
            if image.status == ImageStatus.COMPLETE:
                return image
            time.sleep(poll_interval)
            
        raise MemeDeckAPIError(f"Image generation timed out after {timeout} seconds")

    def get_generated_image(self, prompt_id: str) -> GeneratedImage:
        """
        Get the status and details of a generated image
        
        Args:
            prompt_id: The ID of the image prompt to check
            
        Returns:
            GeneratedImage object containing the status and image details if complete
        """
        response = requests.get(
            f"{self.base_url}/api/generate/image/{prompt_id}",
            headers=self._headers
        )
        result = self._handle_response(response)
        
        status = ImageStatus(result.data["status"])
        if status == ImageStatus.COMPLETE and "image" in result.data:
            return GeneratedImage(
                status=status,
                url=result.data["image"]["url"],
                caption=result.data["image"]["caption"],
                created_at=result.data["image"]["created_at"]
            )
        return GeneratedImage(status=status)


# Example usage:
if __name__ == "__main__":
    # Initialize client
    client = MemeDeckClient(
        api_key="your_api_key",
        deck_id="your_deck_id"
    )
    
    # Generate an image
    request = GenerateImageRequest(
        prompt="eating ice cream",
        character="pepe",
        aspect_ratio=AspectRatios.SQUARE
    )
    
    # Generate and wait for the result
    result = client.generate_image(request, wait=True)
    print(f"Generated image URL: {result.url}")
