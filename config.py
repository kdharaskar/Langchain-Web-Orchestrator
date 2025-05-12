import os
from dotenv import load_dotenv

EMAIL_SCHEDULE = False # Set to True if you want to schedule emails, False for drafting

SLEEP_TIME = 1 # Time to sleep between sending emails (in seconds)

BASE_URL = "https://www.isb.edu"
OUTPUT_FILE = "../data/isb_faculty_directory.csv"

# Add headers to mimic a browser visit
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

# Delay between fetching individual profile pages (be polite to the server)
REQUEST_DELAY_SECONDS = 1 # Increase if you encounter issues like temporary blocks
# Delay between fetching directory pages
PAGE_REQUEST_DELAY_SECONDS = 1

# Get the absolute path of the directory where this config file is located
# This is typically the project root.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Load environment variables from .env file located in the project root
# If your .env is elsewhere, you can specify its path: load_dotenv(dotenv_path=os.path.join(BASE_DIR, '.my-env-file'))
dotenv_path = os.path.join(BASE_DIR, '.env')
load_dotenv(dotenv_path=dotenv_path)

# --- LLM Configuration ---
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
LLM_MODEL_NAME = os.getenv("LLM_MODEL_NAME", "gpt-4o-mini")  # Default model
LLM_TEMPERATURE = float(os.getenv("LLM_TEMPERATURE", 0.6)) # Default temperature

# --- Email Sender Configuration (loaded from .env, with defaults) ---
APP_EMAIL_ADDRESS = os.getenv("APP_EMAIL_ADDRESS")
APP_EMAIL_PASSWORD = os.getenv("APP_EMAIL_PASSWORD") # For Gmail, this should be an App Password
SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587)) # Common port for TLS; 465 for SSL

# --- Application Paths and File Names ---
# Path to the data directory, relative to the project root (BASE_DIR)
DATA_DIR = os.path.join(BASE_DIR, "data")
CSV_FILENAME = os.getenv("CSV_FILENAME")
CSV_FILE_PATH = os.path.join(DATA_DIR, CSV_FILENAME)

# --- User-Specific Information (User MUST customize these) ---

NAME = os.getenv("NAME_CONFIG")
CV_FILENAME = os.getenv("CV_FILENAME")
CV_FILE_PATH = os.getenv("CV_FILE_PATH", os.path.join(DATA_DIR, CV_FILENAME))

# --- Sanity Checks for Essential Configurations ---
def check_essential_configs():
    """
    Checks if essential configurations are set and not using default placeholder values.
    Prints warnings if configurations are missing or seem like placeholders.
    Returns True if basic checks pass, False otherwise (indicating critical issues).
    """
    print("\n--- Configuration Check ---")
    all_good = True
    warnings = []

    # Critical configurations that MUST be set
    critical_vars = {
        "OPENAI_API_KEY": OPENAI_API_KEY,
        "APP_EMAIL_ADDRESS": APP_EMAIL_ADDRESS,
        "APP_EMAIL_PASSWORD": APP_EMAIL_PASSWORD,
    }
    for key, value in critical_vars.items():
        if not value:
            warnings.append(f"CRITICAL: '{key}' is not set in your .env file. Application might not work.")
            all_good = False

    # Configurations that should be customized by the user
    user_custom_vars = {
        "NAME": (NAME, "Your Name"), # (variable, placeholder_value)
        "YOUR_CV_FILENAME": (CV_FILENAME, "Your_CV.pdf"),
        "YOUR_CV_PATH": (CV_FILE_PATH, os.path.join(BASE_DIR, "Your_CV.pdf")) # Compare against default constructed placeholder
    }
    for key, (value, placeholder) in user_custom_vars.items():
        if value == placeholder:
            warnings.append(f"NOTICE: '{key}' is using a default placeholder value ('{value}'). Please customize it in config_settings.py or your .env file.")
        elif key == "YOUR_CV_PATH" and not os.path.exists(value):
             warnings.append(f"NOTICE: CV file for '{key}' not found at '{value}'. Please ensure the path is correct.")

    if not os.path.exists(CSV_FILE_PATH):
        warnings.append(f"NOTICE: CSV data file not found at '{CSV_FILE_PATH}'. Data loading will fail.")
        all_good = False

    if warnings:
        print("Configuration Issues Found:")
        for warning in warnings:
            print(f"- {warning}")
    else:
        print("All checked configurations seem to be in order or customized.")

    print("--- End Configuration Check ---\n")
    return all_good

# This block allows you to run `python config_settings.py` to see your loaded settings
if __name__ == "__main__":
    print("Current Configuration Settings:")
    print(f"  Project Base Directory (BASE_DIR): {BASE_DIR}")
    print(f"  .env file path used: {dotenv_path} (exists: {os.path.exists(dotenv_path)})")
    print("-" * 30)
    print("  LLM Settings:")
    print(f"    OpenAI API Key Loaded: {'Yes (hidden for security)' if OPENAI_API_KEY else 'No - PLEASE SET THIS IN .env'}")
    print(f"    LLM Model Name: {LLM_MODEL_NAME}")
    print(f"    LLM Temperature: {LLM_TEMPERATURE}")
    print("-" * 30)
    print("  Email Settings:")
    print(f"    App Email Address: {APP_EMAIL_ADDRESS if APP_EMAIL_ADDRESS else 'Not Set - PLEASE SET THIS IN .env'}")
    print(f"    App Email Password Loaded: {'Yes (hidden for security)' if APP_EMAIL_PASSWORD else 'No - PLEASE SET THIS IN .env'}")
    print(f"    SMTP Host: {SMTP_HOST}")
    print(f"    SMTP Port: {SMTP_PORT}")
    print("-" * 30)
    print("  File Paths:")
    print(f"    Data Directory: {DATA_DIR}")
    print(f"    CSV Filename: {CSV_FILENAME}")
    print(f"    Full CSV Path: {CSV_FILE_PATH} (exists: {os.path.exists(CSV_FILE_PATH)})")
    print("-" * 30)
    print("  User Customization:")
    print(f"    Name: {NAME}")
    print(f"    Your CV Filename: {CV_FILENAME}")
    print(f"    Your CV Path: {CV_FILE_PATH} (exists: {os.path.exists(CV_FILE_PATH)})")
    print("-" * 30)

    check_essential_configs()

    # Example of how other modules would use these:
    # from config_settings import OPENAI_API_KEY, CSV_FILE_PATH
    # print(f"\nExample usage: CSV Path is {CSV_FILE_PATH}")