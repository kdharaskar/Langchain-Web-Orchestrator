import os
import time
import config
from .load_data import load_rows
from .content_generator import generate_personalized_content
from .email_scheduler import email_scheduler

def main_orchestrator_script():
    print("Starting the professor cold emailing process...")
    if not config.check_essential_configs():
        print("Essential configurations missing or placeholders detected. Please check .env and config.py.")

    print(f"\nLoading professors from: {os.path.abspath(config.CSV_FILE_PATH)}")
    professors = load_rows(config.CSV_FILE_PATH)

    for i, professor_details in enumerate(professors):
        
        email_body = generate_personalized_content(
            professor_details=professor_details,
            user_name=config.NAME,
            user_mobile_number=config.MOBILE_NUMBER
        )

        print(f"\nEmail content generated for {i}: {professor_details['prof_name']}.")
        print(f"Scheduling email to {i}: {professor_details['prof_name']}...")

        # Print the email body for debugging
        print(f"Email Body:\n{email_body}")

        # response = email_scheduler(
        #     professor_details=professor_details,
        #     email_body=email_body,
        #     user_name=config.NAME,
        #     user_mobile_number=config.MOBILE_NUMBER,
        #     schedule = config.EMAIL_SCHEDULE
        # )

        # if response == "success":
        #     print(f"Email scheduled for {professor_details['prof_name']}.")
        #     print(f"Sleeping for {config.SLEEP_TIME} seconds to avoid rate limits...")
        #     time.sleep(config.SLEEP_TIME)
        # else:
        #     print(f"Failed to schedule email for {professor_details['prof_name']}.")
        #     print(f"Response: {response}")

    print("All emails have been scheduled. Process completed.")
    print("Please check your email client for the scheduled emails.")

if __name__ == '__main__':
    
    # Run the main orchestrator script
    main_orchestrator_script()