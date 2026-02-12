"""
Configuration file for database connections
Easily switch between SQLite, Databricks, or other databases
"""

import os
from dotenv import load_dotenv

load_dotenv()

# Database Configuration
DB_CONFIG = {
    "type": "sqlite",  # Options: "sqlite", "databricks", "postgresql", "mysql"
    "sqlite": {
        "database": "insurance.db"
    },
    "databricks": {
        "server_hostname": os.getenv("DATABRICKS_SERVER_HOSTNAME"),
        "http_path": os.getenv("DATABRICKS_HTTP_PATH"),
        "access_token": os.getenv("DATABRICKS_TOKEN"),
        "catalog": os.getenv("DATABRICKS_CATALOG", "main"),
        "schema": os.getenv("DATABRICKS_SCHEMA", "default")
    }
}

# Gemini AI Configuration
GEMINI_CONFIG = {
    "api_key": os.getenv("GOOGLE_API_KEY"),
    "model": "gemini-2.5-flash"
}

# App Configuration
APP_CONFIG = {
    "title": "🔍 Smart Data Analytics Assistant",
    "icon": "🔍",
    "layout": "wide",
    "theme": {
        "primaryColor": "#1f77b4",
        "backgroundColor": "#ffffff",
        "secondaryBackgroundColor": "#f0f2f6",
        "textColor": "#262730"
    }
}