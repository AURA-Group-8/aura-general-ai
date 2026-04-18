import os
from dotenv import dotenv_values
from pathlib import Path

# Carregar SOMENTE do .env (não do SO)
env_path = Path(__file__).parent / ".env"
ENV = dotenv_values(dotenv_path=env_path)

# MySQL
MYSQL_HOST = ENV.get("MYSQL_HOST", "localhost")
MYSQL_USER = ENV.get("MYSQL_USER", "root")
MYSQL_PASSWORD = ENV.get("MYSQL_PASSWORD", "")
MYSQL_DATABASE = ENV.get("MYSQL_DATABASE", "clinic")

# Gemini
GEMINI_API_KEY = ENV.get("GEMINI_API_KEY")

# Cache
CACHE_TTL_MINUTES = 60