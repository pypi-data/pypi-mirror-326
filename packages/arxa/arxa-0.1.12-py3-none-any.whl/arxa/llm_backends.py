#!/usr/bin/env python3
import os
import logging
import requests
import anthropic
import openai
import traceback
from tenacity import retry, retry_if_exception_type, wait_exponential, stop_after_attempt
from typing import Optional
import json

logger = logging.getLogger(__name__)

def truncate_text_to_token_limit(text: str, max_tokens: int, encoding_name: str = "cl100k_base") -> str:
    """
    Truncate text so that its token count is less than or equal to max_tokens.
    Uses the tiktoken library.
    """
    import tiktoken
    enc = tiktoken.get_encoding(encoding_name)
    tokens = enc.encode(text)
    if len(tokens) <= max_tokens:
        return text
    truncated_tokens = tokens[:max_tokens]
    return enc.decode(truncated_tokens)

class OpenAIAPIError(Exception):
    pass

@retry(
    retry=retry_if_exception_type((openai.RateLimitError, OpenAIAPIError)),
    wait=wait_exponential(multiplier=1, min=4, max=60),
    stop=stop_after_attempt(5),
)
def openai_generate(client: openai.OpenAI, prompt: str, model: str = "o3-mini") -> str:
    """
    Send a prompt to OpenAI’s API with rate-limit handling.
    """
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "user", "content": prompt}
            ],
            max_completion_tokens=8192
        )
        logger.debug("OpenAI response: %s", response)
        return response.choices[0].message.content
    except Exception as e:
        logger.debug("Exception in openai_generate:\n%s", traceback.format_exc())
        logger.error("openai_generate encountered an exception of type %s with details: %s", type(e).__name__, str(e))
        status_code = getattr(e, "status_code", None)
        if status_code and status_code in [429, 500]:
            raise OpenAIAPIError(f"OpenAI API rate limit or server error: {e}")
        else:
            logger.error("An unexpected error occurred in openai_generate. Exception details: %s", e, exc_info=True)
            raise

class DeepseekAPIError(Exception):
    pass

@retry(
    retry=retry_if_exception_type(DeepseekAPIError),
    wait=wait_exponential(multiplier=1, min=4, max=60),
    stop=stop_after_attempt(5),
)
def deepseek_generate(client: openai.OpenAI, prompt: str, model: str = "deepseek-chat") -> str:
    """
    Send a prompt to DeepSeek’s API by using the OpenAI client with a custom base_url.
    """
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "user", "content": prompt}
            ],
            max_completion_tokens=8192,
            stream=False
        )
        logger.debug("DeepSeek response: %s", response)
        return response.choices[0].message.content
    except Exception as e:
        logger.debug("Exception in deepseek_generate:\n%s", traceback.format_exc())
        logger.error("deepseek_generate encountered an exception: %s", str(e))
        status_code = getattr(e, "status_code", None)
        if status_code and status_code in [429, 500]:
            raise DeepseekAPIError(f"DeepSeek API rate limit or server error: {e}")
        else:
            raise

class FireworksAPIError(Exception):
    pass

@retry(
    retry=retry_if_exception_type(FireworksAPIError),
    wait=wait_exponential(multiplier=1, min=4, max=60),
    stop=stop_after_attempt(5),
)
def fireworks_generate(prompt: str, model: str = "accounts/fireworks/models/deepseek-v3") -> str:
    """
    Send a prompt to the Fireworks API.
    """
    url = "https://api.fireworks.ai/inference/v1/chat/completions"
    payload = {
        "model": model,
        "max_tokens": 65536,
        "top_p": 1,
        "top_k": 40,
        "presence_penalty": 0,
        "frequency_penalty": 0,
        "temperature": 0.6,
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }
    api_key = os.getenv("FIREWORKS_API_KEY")
    if not api_key:
        raise FireworksAPIError("FIREWORKS_API_KEY environment variable not set.")
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        response.raise_for_status()
        data = response.json()
        logger.debug("Fireworks response: %s", data)
        # Assumes the API returns a structure with choices->[{'message': {'content': ...}}]
        return data["choices"][0]["message"]["content"]
    except Exception as e:
        logger.error("Error in fireworks_generate: %s", str(e))
        raise FireworksAPIError(str(e))

class AnthropicAPIError(Exception):
    pass

@retry(
    retry=retry_if_exception_type((anthropic.RateLimitError, AnthropicAPIError)),
    wait=wait_exponential(multiplier=1, min=4, max=60),
    stop=stop_after_attempt(5),
)
def anthropic_generate(client: anthropic.Anthropic, prompt: str, model: Optional[str] = None) -> str:
    """
    Send a prompt to an Anthropic (Claude) model with rate-limit handling.
    """
    if not model:
        model = "claude-3-5-sonnet-latest"  # Default model.
    try:
        response = client.messages.create(
            model=model,
            max_tokens=8192,
            temperature=0.5,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        return response.content[0].text if response.content else ""
    except anthropic.APIError as e:
        if e.status_code in [429, 529]:
            raise AnthropicAPIError(f"Anthropic API rate limit or server error: {e}")
        raise

class OllamaAPIError(Exception):
    pass

@retry(
    retry=retry_if_exception_type(OllamaAPIError),
    wait=wait_exponential(multiplier=1, min=4, max=60),
    stop=stop_after_attempt(5),
)
def ollama_generate(prompt: str, model: str = "llama3:6b") -> str:
    """
    Send a prompt to an Ollama local inference server.
    """
    OLLAMA_API_URL = "http://localhost:11434/api/generate"
    try:
        print(prompt)
        response = requests.post(OLLAMA_API_URL, json={
            "model": model,
            "prompt": prompt,
            "stream": False
        })
        response.raise_for_status()
        data = response.json()
        return data.get("response", "")
    except requests.RequestException as e:
        status_code = e.response.status_code if e.response else 0
        raise OllamaAPIError(f"Ollama API Error {status_code} - {str(e)}")
