"""
This module contains functions for performing the codelab tasks
"""
import logging
import os
import re

import pandas as pd
from googleapiclient.http import MediaFileUpload


def combine_dataframes(df1, df2):
    """
    Combine two DataFrames and return the combined result.
    :param df1: First DataFrame
    :param df2: Second DataFrame
    :return: Combined DataFrame
    """
    combined_df = pd.concat([df1, df2], ignore_index=True)
    return combined_df


def generate_email(name):
    """
    Generate an email from the student's name.
    Takes the first letter of the first name and combines it with the last name.
    :param name: student name
    :return: email
    """
    name_parts = re.split(r'[\s,]+', name)
    email_name = name_parts[0][0].lower() + name_parts[-1].lower()

    # Remove any special characters
    email_name = re.sub(r'[^a-zA-Z]', '', email_name)
    return f"{email_name}@gmail.com"


def make_unique(emails):
    """
    Make email addresses unique by appending a number if duplicates exist.
    :param emails: list of email addresses
    :return: unique list of email addresses
    """
    seen = {}
    unique_emails = []

    for email in emails:
        if email not in seen:
            seen[email] = 0
            unique_emails.append(email)
        else:
            seen[email] += 1
            unique_email = f"{email.split('@')[0]}{seen[email]}@gmail.com"
            unique_emails.append(unique_email)

    return unique_emails


def get_students_by_gender(df, gender):
    """
    Get all students of a specified gender.
    :param df: DataFrame containing student names and genders
    :param gender: The student gender
    :return: DataFrame containing students of the specified gender
    """
    for index, row in df.iterrows():
        if row['Gender'] == gender:
            yield row


def build_jsonl(shuffled_df, special_char_names):
    """
    Build data of shuffled students from the shuffled dataframe for jsonl
    conversion
    :param shuffled_df: The shuffled dataframe
    :param special_char_names: the list of names with special characters
    :return: A list of dictionaries containing shuffled student information
    """
    shuffled_students = []
    id_count = 0

    for index, row in shuffled_df.iterrows():
        student_name = row["Student Name"]
        if student_name in special_char_names:
            has_special_character = "['yes']"
        else:
            has_special_character = "['no']"

        student_details = {
            "id": id_count,
            "student_number": row["Student Number"],
            "additional_details": [
                {
                    "dob": row["DoB"].strftime("%Y-%m-%d"),
                    "gender": row["Gender"],
                    "special_character": has_special_character,
                }
            ]
        }

        shuffled_students.append(student_details)
        id_count += 1

    return shuffled_students


def create_folder(service, folder_name, parent_folder_id=None):
    """
    Create a folder in Google Drive.
    :param parent_folder_id: ID of the parent folder
    :param service: The Google Drive service
    :param folder_name: The name of the folder
    :return: the ID of the created folder
    """

    folder_metadata = {
        "name": folder_name,
        "mimeType": "application/vnd.google-apps.folder",
        "parents": [parent_folder_id],
    }

    folder = service.files().create(body=folder_metadata, fields='id').execute()

    return folder['id']


def upload_files(output_folder, service, parent_folder_id=None):
    files_to_upload = [
        (os.path.join(root, file), file)
        for root, dirs, files in os.walk(output_folder)
        for file in files
    ]

    for file_path, file_name in files_to_upload:
        file_metadata = {
            "name": file_name,
            "parents": [parent_folder_id],
        }

        media = MediaFileUpload(file_path)
        file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
        logging.info(f"Uploaded {file_name} to Google Drive.")
