"""Shared configuration loaded from environment and optional ``backend/.env``."""

import os
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv

_backend_dir = Path(__file__).resolve().parent
load_dotenv(_backend_dir / ".env")
load_dotenv()


def openai_api_key() -> Optional[str]:
    key = os.environ.get("OPENAI_API_KEY", "").strip()
    return key or None


def openai_model() -> str:
    return os.environ.get("OPENAI_MODEL", "gpt-4o").strip() or "gpt-4o"


def openai_design_detector_model() -> str:
    return (
        os.environ.get("OPENAI_DESIGN_DETECTOR_MODEL", "").strip()
        or openai_model()
    )


def pmd_bin_dir() -> Optional[str]:
    path = os.environ.get("PMD_BIN", "").strip()
    return path or None


def checkstyle_config_path() -> Optional[str]:
    path = os.environ.get("CHECKSTYLE_CONFIG", "").strip()
    return path or None


def jplag_jar_path() -> Optional[str]:
    path = os.environ.get("JPLAG_JAR", "").strip()
    return path or None
