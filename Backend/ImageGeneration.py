import asyncio
import logging
import re
from random import randint
from PIL import Image
import requests
from dotenv import get_key
import os
from time import sleep
from typing import List, Optional
import sys

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ImageGenerationError(Exception):
    """Custom exception for image generation errors"""
    pass

class ImageGenerator:
    def __init__(self):
        self.api_url = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
        self.api_key = self._get_api_key()
        self.headers = {"Authorization": f"Bearer {self.api_key}"}
        self.data_folder = "Data"
        self.frontend_data_file = "Frontend/Files/ImageGeneration.data"
        
        # Ensure directories exist
        os.makedirs(self.data_folder, exist_ok=True)
        os.makedirs(os.path.dirname(self.frontend_data_file), exist_ok=True)

    def _get_api_key(self) -> str:
        """Get API key from environment file"""
        try:
            api_key = get_key('.env', 'HuggingFaceAPIKey')
            if not api_key:
                raise ImageGenerationError("HuggingFace API key not found in .env file")
            return api_key
        except Exception as e:
            logger.error(f"Failed to get API key: {e}")
            raise ImageGenerationError(f"API key error: {e}")

    def _sanitize_filename(self, prompt: str) -> str:
        """Sanitize prompt for use as filename"""
        # Remove or replace invalid characters
        sanitized = re.sub(r'[<>:"/\\|?*]', '_', prompt)
        # Remove extra spaces and limit length
        sanitized = re.sub(r'\s+', '_', sanitized.strip())
        return sanitized[:50]  # Limit length to prevent path issues

    async def query_api(self, payload: dict, timeout: int = 60) -> bytes:
        """Make API request with proper error handling"""
        try:
            response = await asyncio.to_thread(
                requests.post, 
                self.api_url, 
                headers=self.headers, 
                json=payload,
                timeout=timeout
            )
            
            if response.status_code != 200:
                logger.error(f"API request failed with status {response.status_code}: {response.text}")
                raise ImageGenerationError(f"API request failed: {response.status_code}")
                
            return response.content
            
        except requests.exceptions.Timeout:
            logger.error("API request timed out")
            raise ImageGenerationError("API request timed out")
        except requests.exceptions.RequestException as e:
            logger.error(f"API request failed: {e}")
            raise ImageGenerationError(f"API request failed: {e}")

    async def generate_images(self, prompt: str, num_images: int = 4) -> List[str]:
        """Generate multiple images asynchronously"""
        if not prompt.strip():
            raise ImageGenerationError("Prompt cannot be empty")
            
        logger.info(f"Generating {num_images} images for prompt: {prompt}")
        
        tasks = []
        generated_files = []
        sanitized_prompt = self._sanitize_filename(prompt)

        for i in range(num_images):
            payload = {
                "inputs": f"{prompt}, quality=4k, sharpness=maximum, Ultra High details, High Resolution, seed = {randint(0, 1000000)}"
            }
            task = asyncio.create_task(self.query_api(payload))
            tasks.append(task)
        
        try:
            image_bytes_list = await asyncio.gather(*tasks, return_exceptions=True)
            
            for i, result in enumerate(image_bytes_list):
                if isinstance(result, Exception):
                    logger.error(f"Failed to generate image {i+1}: {result}")
                    continue
                    
                filename = f"{sanitized_prompt}_{i + 1}.jpg"
                filepath = os.path.join(self.data_folder, filename)
                
                try:
                    with open(filepath, "wb") as f:
                        f.write(result)
                    generated_files.append(filepath)
                    logger.info(f"Generated image: {filepath}")
                except IOError as e:
                    logger.error(f"Failed to save image {i+1}: {e}")
                    
        except Exception as e:
            logger.error(f"Error during image generation: {e}")
            raise ImageGenerationError(f"Image generation failed: {e}")
            
        return generated_files

    def open_images(self, generated_files: List[str]):
        """Open generated images with proper resource management"""
        if not generated_files:
            logger.warning("No images to open")
            return
            
        logger.info(f"Opening {len(generated_files)} images")
        
        for filepath in generated_files:
            try:
                if os.path.exists(filepath):
                    img = Image.open(filepath)
                    logger.info(f"Opening image: {filepath}")
                    img.show()
                    sleep(1)  # Brief pause between images
                else:
                    logger.warning(f"Image file not found: {filepath}")
            except IOError as e:
                logger.error(f"Unable to open image {filepath}: {e}")
            except Exception as e:
                logger.error(f"Unexpected error opening {filepath}: {e}")

    def generate_images_sync(self, prompt: str, num_images: int = 4) -> List[str]:
        """Synchronous wrapper for image generation"""
        try:
            return asyncio.run(self.generate_images(prompt, num_images))
        except Exception as e:
            logger.error(f"Image generation failed: {e}")
            raise

    def read_frontend_data(self) -> tuple[Optional[str], bool]:
        """Read data from frontend file with error handling"""
        try:
            if not os.path.exists(self.frontend_data_file):
                return None, False
                
            with open(self.frontend_data_file, "r") as f:
                data = f.read().strip()
                
            if not data or ',' not in data:
                return None, False
                
            prompt, status = data.split(",", 1)
            return prompt.strip(), status.strip().lower() == "true"
            
        except Exception as e:
            logger.error(f"Error reading frontend data: {e}")
            return None, False

    def write_frontend_status(self, prompt: str = "", status: bool = False):
        """Write status to frontend file"""
        try:
            with open(self.frontend_data_file, "w") as f:
                f.write(f"{prompt},{status}")
        except Exception as e:
            logger.error(f"Error writing frontend status: {e}")

    def run(self):
        """Main loop with proper error handling and exit conditions"""
        logger.info("Starting image generation service...")
        
        try:
            while True:
                try:
                    prompt, should_generate = self.read_frontend_data()
                    
                    if should_generate and prompt:
                        logger.info(f"Processing image generation request: {prompt}")
                        
                        try:
                            generated_files = self.generate_images_sync(prompt)
                            if generated_files:
                                self.open_images(generated_files)
                                logger.info(f"Successfully generated {len(generated_files)} images")
                            else:
                                logger.warning("No images were generated successfully")
                            
                            # Update status to indicate completion
                            self.write_frontend_status(prompt, False)
                            logger.info("Image generation completed successfully")
                            
                        except ImageGenerationError as e:
                            logger.error(f"Image generation failed: {e}")
                            self.write_frontend_status(prompt, False)
                        except Exception as e:
                            logger.error(f"Unexpected error during image generation: {e}")
                            self.write_frontend_status(prompt, False)
                    else:
                        sleep(1)  # Wait before checking again
                        
                except KeyboardInterrupt:
                    logger.info("Received interrupt signal, shutting down...")
                    break
                except Exception as e:
                    logger.error(f"Unexpected error in main loop: {e}")
                    sleep(5)  # Wait before retrying
                    
        except Exception as e:
            logger.error(f"Critical error in image generation service: {e}")
            sys.exit(1)

def main():
    """Entry point for the image generation service"""
    generator = ImageGenerator()
    generator.run()

if __name__ == "__main__":
    main()

