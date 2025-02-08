from typing import List, Optional, Dict, Any
from pydantic import Field
import google.generativeai as genai
from loguru import logger

from airtrain.core.skills import Skill, ProcessingError
from airtrain.core.schemas import InputSchema, OutputSchema
from .credentials import Gemini2Credentials


class Gemini2GenerationConfig(InputSchema):
    """Schema for Gemini 2.0 generation config"""

    temperature: float = Field(
        default=1.0, description="Temperature for response generation", ge=0, le=1
    )
    top_p: float = Field(
        default=0.95, description="Top p sampling parameter", ge=0, le=1
    )
    top_k: int = Field(default=40, description="Top k sampling parameter")
    max_output_tokens: int = Field(
        default=8192, description="Maximum tokens in response"
    )
    response_mime_type: str = Field(
        default="text/plain", description="Response MIME type"
    )


class Gemini2Input(InputSchema):
    """Schema for Gemini 2.0 chat input"""

    user_input: str = Field(..., description="User's input text")
    system_prompt: str = Field(
        default="You are a helpful assistant.",
        description="System prompt to guide the model's behavior",
    )
    conversation_history: List[Dict[str, str | List[Dict[str, str]]]] = Field(
        default_factory=list,
        description="List of conversation messages in Gemini's format",
    )
    model: str = Field(default="gemini-2.0-flash", description="Gemini model to use")
    generation_config: Gemini2GenerationConfig = Field(
        default_factory=Gemini2GenerationConfig,
        description="Generation configuration",
    )


class Gemini2Output(OutputSchema):
    """Schema for Gemini 2.0 chat output"""

    response: str = Field(..., description="Model's response text")
    used_model: str = Field(..., description="Model used for generation")
    usage: Dict[str, Any] = Field(default_factory=dict, description="Usage statistics")


class Gemini2ChatSkill(Skill[Gemini2Input, Gemini2Output]):
    """Skill for Gemini 2.0 chat"""

    input_schema = Gemini2Input
    output_schema = Gemini2Output

    def __init__(self, credentials: Optional[Gemini2Credentials] = None):
        super().__init__()
        self.credentials = credentials or Gemini2Credentials.from_env()
        genai.configure(api_key=self.credentials.gemini_api_key.get_secret_value())

    def _convert_history_format(
        self, history: List[Dict[str, str]]
    ) -> List[Dict[str, List[Dict[str, str]]]]:
        """Convert standard history format to Gemini's format"""
        gemini_history = []
        for msg in history:
            gemini_msg = {
                "role": "user" if msg["role"] == "user" else "model",
                "parts": [{"text": msg["content"]}],
            }
            gemini_history.append(gemini_msg)
        return gemini_history

    def process(self, input_data: Gemini2Input) -> Gemini2Output:
        try:
            generation_config = {
                "temperature": input_data.generation_config.temperature,
                "top_p": input_data.generation_config.top_p,
                "top_k": input_data.generation_config.top_k,
                "max_output_tokens": input_data.generation_config.max_output_tokens,
                "response_mime_type": input_data.generation_config.response_mime_type,
            }

            model = genai.GenerativeModel(
                model_name=input_data.model,
                generation_config=generation_config,
            )

            history = (
                input_data.conversation_history
                if input_data.conversation_history
                else self._convert_history_format([])
            )

            chat = model.start_chat(history=history)
            response = chat.send_message(input_data.user_input)

            return Gemini2Output(
                response=response.text,
                used_model=input_data.model,
                usage={
                    "prompt_tokens": 0,
                    "completion_tokens": 0,
                    "total_tokens": 0,
                },
            )

        except Exception as e:
            logger.exception(f"Gemini 2.0 processing failed: {str(e)}")
            raise ProcessingError(f"Gemini 2.0 processing failed: {str(e)}")
