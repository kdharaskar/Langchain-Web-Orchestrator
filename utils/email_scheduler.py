import json
import os
def email_scheduler(professor_details, email_body, user_name, user_mobile_number, schedule):
    """
    Saves professor details and email body to a JSON file if schedule is False.

    Args:
        professor_details (dict): A dictionary containing professor's details.
                                  It is expected to have a key like 'professor_name'
                                  or 'name'.
        email_body (str): The content of the email.
        user_name (str): Name of the sender.
        user_mobile_number (str): Mobile number of the sender.
        schedule (bool): A boolean indicating whether to schedule the email or
                         save the details.

    Returns:
        str: A message indicating the action taken.
             If schedule is False, returns a message about saving to JSON.
    """
    file_path = "data/email_data.json"

    if not schedule:
        # Try to get professor_name, handling potential KeyError
        professor_name = professor_details.get('prof_name', professor_details.get('Name', 'N/A'))

        data_to_save = {
            "professor_name": professor_name,
            "email_body": email_body,
            "user_name": user_name,
            "user_mobile_number": user_mobile_number
        }
        try:
            if os.path.getsize(file_path) > 0:
                with open(file_path, "r") as json_file:
                    data = json.load(json_file)
                    data.append(data_to_save)
            else:
                data = [data_to_save]

            with open(file_path, "w") as json_file:
                json.dump(data, json_file, indent=4)
            return "success"
        except IOError:
            return "Error: Could not write to email_data.json."
        except TypeError:
            return "Error: Data is not serializable to JSON."
    else:
        # TODO: Implement actual email scheduling logic here
        return "Error: Email scheduling is not implemented yet."

if __name__ == "__main__":

    # Example usage
    professor_details = {
        "professor_name": "Dr. Smith",
        "professor_bio": "Expert in AI and ML",
    }

    email_body = "Hello, this is a test email."
    schedule = False

    result = email_scheduler(professor_details, email_body, "John Doe", "1234567890", schedule)
    print(result)