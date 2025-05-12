import os
import time
import config
from .load_data import load_rows
from .content_generator import generate_personalized_content
from .email_scheduler import email_scheduler

def get_user_core_message_details():
    cv_mention = f"I have attached my CV, '{config.CV_FILENAME}', for your detailed review." \
                 if config.CV_FILENAME else \
                 "I have attached my CV for your detailed review."
    return {
        "introduction": f"""My name is {config.NAME}. I am a [Your Role/Status...].""",
        "alignment_guidance": f"""I am writing to you because... {{prof_research_speciality}}... {{prof_biography_snippet}}...""",
        "call_to_action": f"""{cv_mention} It outlines my qualifications..."""
    }

def main_orchestrator_script():
    print("Starting the professor cold emailing process...")
    if not config.check_essential_configs():
        print("Essential configurations missing or placeholders detected. Please check .env and config.py.")

    print(f"\nLoading professors from: {os.path.abspath(config.CSV_FILE_PATH)}")
    professors = load_rows(config.CSV_FILE_PATH)

    for i, professor_details in enumerate(professors):
        pass

if __name__ == '__main__':
    main_orchestrator_script()