import os
import time
import config
import sys
from pathlib import Path

# Add the parent directory to sys.path to allow importing config
sys.path.append(str(Path(__file__).parent.parent))

from utils.load_data import load_rows
from utils.content_generator import generate_personalized_content
from utils.email_scheduler import email_scheduler

def main_orchestrator_script():
    print("Starting the professor cold emailing process...")
    if not config.check_essential_configs():
        print("Essential configurations missing or placeholders detected. Please check .env and config.py.")
        return False

    print(f"\nLoading professors from: {os.path.abspath(config.CSV_FILE_PATH)}")
    professors = load_rows(config.CSV_FILE_PATH)
    
    if not professors:
        print("No professor data loaded. Please check the CSV file.")
        return False

    for i, professor_details in enumerate(professors):
        try:
            email_body = generate_personalized_content(
                professor_details=professor_details,
                user_name=config.NAME,
                user_mobile_number=config.MOBILE_NUMBER
            )

            print(f"\nEmail content generated for {i}: {professor_details['prof_name']}.")
            print(f"Scheduling email to {i}: {professor_details['prof_name']}...")

            # Print the email body for debugging
            print(f"Email Body:\n{email_body}")

            response = email_scheduler(
                professor_details=professor_details,
                email_body=email_body,
                user_name=config.NAME,
                user_mobile_number=config.MOBILE_NUMBER,
                schedule=config.EMAIL_SCHEDULE
            )

            if response == "success":
                print(f"Email {'scheduled' if config.EMAIL_SCHEDULE else 'saved as draft'} for {professor_details['prof_name']}.")
                print(f"Sleeping for {config.SLEEP_TIME} seconds to avoid rate limits...")
                time.sleep(config.SLEEP_TIME)
            else:
                print(f"Failed to {'schedule' if config.EMAIL_SCHEDULE else 'save'} email for {professor_details['prof_name']}.")
                print(f"Response: {response}")
        except Exception as e:
            print(f"Error processing professor {professor_details.get('prof_name', 'Unknown')}: {str(e)}")
            continue

    print("All emails have been processed. Process completed.")
    print("Please check your email client for the scheduled emails." if config.EMAIL_SCHEDULE else "Please check data/email_data.json for saved drafts.")
    return True

if __name__ == '__main__':
    main_orchestrator_script()