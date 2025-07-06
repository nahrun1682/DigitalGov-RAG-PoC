"""
Central configuration for DigitalGov-RAG-PoC
Loads environment variables and defines project constants
"""
from dotenv import load_dotenv
import os
from pathlib import Path

# Load .env
load_dotenv()

# Project root directory
PROJECT_ROOT = Path(__file__).parent

# Data directories
RAW_DIR = PROJECT_ROOT / "data_pipeline" / "data" / "raw"
RAW_DIR.mkdir(parents=True, exist_ok=True)

# Base URL for scraping
BASE_URL = os.getenv(
    "BASE_URL",
    "https://cio.go.jp/guides/index.html#main-content"
)

# Langfuse configuration
LANGFUSE_SECRET_KEY = os.getenv("LANGFUSE_SECRET_KEY")
LANGFUSE_PUBLIC_KEY = os.getenv("LANGFUSE_PUBLIC_KEY")
LANGFUSE_HOST = os.getenv("LANGFUSE_HOST_URL")
