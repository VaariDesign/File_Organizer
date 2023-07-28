import os
import re
import shutil

def extract_date_from_filename(filename):
    pattern = r"(\d{4})(\d{2})(\d{2})_(\d{2})(\d{2})(\d{2})" # example name: 20230101_000000
    match = re.match(pattern, filename)
    if match:
        year, month, day, hour, minute, second = match.groups()
        return year, month, day, hour, minute, second
    return None

def organize_files(folder_path, naming_format, organization_criteria):
    if not os.path.exists(folder_path):
        print("Folder not found.")
        return

    for filename in os.listdir(folder_path):
        filepath = os.path.join(folder_path, filename)

        # Skip directories and non-files
        if not os.path.isfile(filepath):
            continue

        date_info = extract_date_from_filename(filename)
        if not date_info:
            print(f"Skipping file '{filename}' as it doesn't match the expected naming format.")
            continue

        year, month, day, hour, minute, second = date_info
        new_folder_name = naming_format.format(
            year=year,
            month=month,
            day=day,
            hour=hour,
            minute=minute,
            second=second,
            filename=filename
        )

        # Move the file to the corresponding folder
        new_folder_path = os.path.join(folder_path, new_folder_name)
        os.makedirs(new_folder_path, exist_ok=True)
        shutil.move(filepath, os.path.join(new_folder_path, filename))

if __name__ == "__main__":
    folder_path = input("Enter the folder path to organize files: ")
    naming_format = input("Enter the naming format (use {year}, {month}, etc. as placeholders): ")
    organization_criteria = input("Enter the organization criteria (e.g., {month} to organize by month): ")

    organize_files(folder_path, naming_format, organization_criteria)
    print("File organization complete.")
