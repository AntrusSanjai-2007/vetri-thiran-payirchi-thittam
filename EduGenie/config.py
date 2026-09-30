import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


def get_bool(name: str, default: bool = False) -> bool:
    value = os.getenv(name)

    if value is None:
        return default

    return value.strip().lower() in {
        "1",
        "true",
        "yes",
        "y",
        "on",
    }


@dataclass(frozen=True)
class Settings:

    app_name: str = os.getenv(
        "APP_NAME",
        "EduGenie",
    )

    gemini_api_key: str = os.getenv(
        "GEMINI_API_KEY",
        "",
    )

    gemini_model: str = os.getenv(
        "GEMINI_MODEL",
        "gemini-3.8-flash",
    )

    explanation_provider: str = os.getenv(
        "EXPLANATION_PROVIDER",
        "gemini",
    ).lower()

    local_model_name: str = os.getenv(
        "LOCAL_MODEL_NAME",
        "MBZUAI/LaMini-Flan-T5-783M",
    )

    debug: bool = get_bool(
        "DEBUG",
        True,
    )

    demo_mode: bool = get_bool(
        "DEMO_MODE",
        False,
    )


settings = Settings()