"""
config/settings.py — Load and expose environment variables.
"""

import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
MODEL_NAME: str = os.getenv("MODEL_NAME", "gpt-4o-mini")
TEMPERATURE: float = float(os.getenv("TEMPERATURE", "0"))

if not OPENAI_API_KEY:
    raise EnvironmentError(
        "OPENAI_API_KEY is not set. "
        "Add it to your .env file or export it as an environment variable."
    )

# Expose the key to the OpenAI SDK
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
