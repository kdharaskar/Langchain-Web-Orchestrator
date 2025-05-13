import csv
import os

def load_rows(file_path: str) -> list[dict]:
    """
    Loads professor data from a CSV file.

    Args:
        file_path (str): The path to the CSV file.

    Returns:
        list[dict]: A list of dictionaries, where each dictionary
                    represents a professor and contains data from a row.
                    Returns an empty list if the file is not found or is empty.
    """

    professors = []

    if not os.path.exists(file_path):
        print(f"Error: CSV file not found at {file_path}")
        return professors
    if os.path.getsize(file_path) == 0:
        print(f"Error: CSV file is empty at {file_path}")
        return professors

    try:

        with open(file_path, mode='r', encoding='utf-8-sig') as csvfile:  # 'utf-8-sig' handles potential BOM
            reader = csv.DictReader(csvfile)
            # Check if essential columns are present in the header
            required_columns = ['Sr.No.', 'Name', 'Email', 'Academic-Area',
                                'Research-Speciality', 'Biography']  # Add others if critical
            
            if not reader.fieldnames:
                print("Error: CSV file has no headers")
                return professors

            if not all(col in reader.fieldnames for col in required_columns):
                missing = [col for col in required_columns if col not in reader.fieldnames]
                print(f"Error: CSV file is missing required columns: {', '.join(missing)}")
                print(f"Available columns: {', '.join(reader.fieldnames)}")
                return professors

            for row in reader:
                # Basic validation: ensure critical fields like 'Email' and 'Name' are not empty
                if not row.get('Name') or not row.get('Email'):
                    print(f"Warning: Skipping row due to missing Name or Email: {row}")
                    continue
                professors.append(row)

        if not professors and reader.fieldnames:  # File had headers but no data rows
            print(f"Warning: CSV file at {file_path} contains headers but no data rows.")

    except Exception as e:
        print(f"An error occurred while reading the CSV file: {e}")
        return []  # Return empty list on other errors

    return professors

if __name__ == '__main__':
    # Example usage (for testing this module directly)
    # Create a dummy professors.csv in the same directory as csv_loader.py for this test
    dummy_csv_path = 'professors.csv'
    if not os.path.exists(dummy_csv_path):
        with open(dummy_csv_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(
                ['Sr.No.', 'Name', 'Email', 'Academic-Area', 'Research-Speciality', 'Biography', 'Profile-URL'])
            writer.writerow(['1', 'Dr. Ada Lovelace', 'ada@example.com', 'Computer Science', 'Analytical Engines',
                             'Pioneering work in computation.', 'http://example.com/ada'])
            writer.writerow(['2', 'Dr. Alan Turing', 'alan@example.com', 'Mathematics', 'Cryptography, AI',
                             'Key contributions to theoretical computer science.', 'http://example.com/turing'])
            writer.writerow(
                ['3', '', 'no_name@example.com', 'Physics', 'Quantum Mechanics', 'Bio here', ''])  # Test missing name
            writer.writerow(
                ['4', 'Dr. No Email', '', 'Chemistry', 'Organic Chemistry', 'Bio here', ''])  # Test missing email

    print(f"Attempting to load professors from: {os.path.abspath(dummy_csv_path)}")

    professor_list = load_rows(dummy_csv_path)

    if professor_list:
        print(f"\nSuccessfully loaded {len(professor_list)} professors:")
        for prof in professor_list:
            print(prof)
    else:
        print("\nNo professors were loaded. Check errors above.")

    # Example of loading a non-existent file
    print("\nAttempting to load non-existent file:")
    load_rows("non_existent.csv")

    # Example of loading an empty file
    empty_csv_path = 'empty_professors.csv'
    with open(empty_csv_path, 'w', encoding='utf-8') as f:
        pass  # Create an empty file
    print("\nAttempting to load an empty file:")
    load_rows(empty_csv_path)
    os.remove(empty_csv_path)  # Clean up

    # Example of loading a file with headers but no data
    header_only_csv_path = 'header_only_professors.csv'
    with open(header_only_csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Sr.No.', 'Name', 'Email', 'Academic-Area', 'Research-Speciality', 'Biography', 'Profile-URL'])
    print("\nAttempting to load a file with only headers:")
    load_rows(header_only_csv_path)
    os.remove(header_only_csv_path)  # Clean up