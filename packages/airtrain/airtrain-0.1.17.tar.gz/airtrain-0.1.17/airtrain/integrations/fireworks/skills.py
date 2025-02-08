from typing import List, Optional, Dict, Any
from pydantic import Field
import requests
from loguru import logger

from airtrain.core.skills import Skill, ProcessingError
from airtrain.core.schemas import InputSchema, OutputSchema
from .credentials import FireworksCredentials
from .models import FireworksMessage, FireworksResponse


class FireworksInput(InputSchema):
    """Schema for Fireworks AI chat input"""

    user_input: str = Field(..., description="User's input text")
    system_prompt: str = Field(
        default="You are a helpful assistant.",
        description="System prompt to guide the model's behavior",
    )
    conversation_history: List[Dict[str, str]] = Field(
        default_factory=list,
        description="List of previous conversation messages in [{'role': 'user|assistant', 'content': 'message'}] format",
    )
    model: str = Field(
        default="accounts/fireworks/models/deepseek-r1",
        description="Fireworks AI model to use",
    )
    temperature: float = Field(
        default=0.7, description="Temperature for response generation", ge=0, le=1
    )
    max_tokens: Optional[int] = Field(
        default=None, description="Maximum tokens in response"
    )
    context_length_exceeded_behavior: str = Field(
        default="truncate", description="Behavior when context length is exceeded"
    )


class FireworksOutput(OutputSchema):
    """Schema for Fireworks AI output"""

    response: str = Field(..., description="Model's response text")
    used_model: str = Field(..., description="Model used for generation")
    usage: Dict[str, int] = Field(default_factory=dict, description="Usage statistics")


class FireworksChatSkill(Skill[FireworksInput, FireworksOutput]):
    """Skill for interacting with Fireworks AI models"""

    input_schema = FireworksInput
    output_schema = FireworksOutput

    def __init__(self, credentials: Optional[FireworksCredentials] = None):
        """Initialize the skill with optional credentials"""
        super().__init__()
        self.credentials = credentials or FireworksCredentials.from_env()
        self.base_url = "https://api.fireworks.ai/inference/v1"

    def _build_messages(self, input_data: FireworksInput) -> List[Dict[str, str]]:
        """
        Build messages list from input data including conversation history.

        Args:
            input_data: The input data containing system prompt, conversation history, and user input

        Returns:
            List[Dict[str, str]]: List of messages in the format required by Fireworks AI
        """
        messages = [{"role": "system", "content": input_data.system_prompt}]

        # Add conversation history if present
        if input_data.conversation_history:
            messages.extend(input_data.conversation_history)

        # Add current user input
        messages.append({"role": "user", "content": input_data.user_input})

        return messages

    def process(self, input_data: FireworksInput) -> FireworksOutput:
        """Process the input using Fireworks AI API"""
        try:
            logger.info(f"Processing request with model {input_data.model}")

            # Build messages using the helper method
            messages = self._build_messages(input_data)

            # Prepare request payload
            payload = {
                "messages": messages,
                "model": input_data.model,
                "context_length_exceeded_behavior": input_data.context_length_exceeded_behavior,
                "temperature": input_data.temperature,
                "n": 1,
                "response_format": {"type": "text"},
                "stream": False,
            }

            if input_data.max_tokens:
                payload["max_tokens"] = input_data.max_tokens

            # Make API request
            response = requests.post(
                f"{self.base_url}/chat/completions",
                json=payload,
                headers={
                    "Authorization": f"Bearer {self.credentials.fireworks_api_key.get_secret_value()}",
                    "Content-Type": "application/json",
                },
            )

            response.raise_for_status()
            response_data = FireworksResponse(**response.json())

            logger.success("Successfully processed Fireworks AI request")

            return FireworksOutput(
                response=response_data.choices[0]["message"]["content"],
                used_model=response_data.model,
                usage={
                    "prompt_tokens": response_data.usage.prompt_tokens,
                    "completion_tokens": response_data.usage.completion_tokens,
                    "total_tokens": response_data.usage.total_tokens,
                },
            )

        except Exception as e:
            logger.exception(f"Fireworks AI processing failed: {str(e)}")
            raise ProcessingError(f"Fireworks AI processing failed: {str(e)}")
