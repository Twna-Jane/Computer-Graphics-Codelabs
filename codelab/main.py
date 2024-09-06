import pandas as pd

from codelab.functions import build_jsonl
from functions import generate_email, make_unique, combine_dataframes, get_students_by_gender
import logging

# Logging configuration
logging.basicConfig(
    filename='computations.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
)

# Excel sheets
df1 = pd.read_excel("File_A.xlsx")
df2 = pd.read_excel("File_B.xlsx")
df = combine_dataframes(df1, df2)

# Generating unique student emails
df["Email Address"] = df["Student Name"].apply(generate_email)
df["Email Address"] = make_unique(df["Email Address"])

# Logging generated emails
logging.info("----- Generated Email Addresses -----")
for index, row in df.iterrows():
    logging.info(f"Student Email {index + 1}: {row['Email Address']}")

# Combined DataFrame saved as CSV and TSV
df.to_csv("output/students.csv", index=False)
df.to_csv("output/students.tsv", sep='\t', index=False)

# Male students
male_df = pd.DataFrame(get_students_by_gender(df, "M"))
male_df.to_csv("output/male_students.csv", index=False)
logging.info(f"No of male students: {len(male_df)}")

# Female students
female_df = pd.DataFrame(get_students_by_gender(df, "F"))
female_df.to_csv("output/female_students.csv", index=False)
logging.info(f"No of female students: {len(female_df)}")

# Students with special characters
pattern = r"[^\w\s,]"
special_char_students = df[df["Student Name"].str.contains(pattern, regex=True)]

special_char_names = []
logging.info(f"Students with special characters in their names: {len(special_char_students)}")
for student_name in special_char_students["Student Name"]:
    logging.info(f" - {student_name}")
    special_char_names.append(student_name)

# Save to CSV
special_char_students.to_csv("output/special_char_students.csv", index=False)

# One-time shuffle
shuffled_df = df.sample(frac=1)

# Output shuffled data to JSON
shuffled_df.to_json("output/shuffled_students.json", orient="records")

# Building data to convert to JSONL
shuffled_students = build_jsonl(shuffled_df, special_char_names)

shuffled_df = pd.DataFrame(shuffled_students)
shuffled_df.to_json("output/shuffled_students.jsonl", orient="records", lines=True)
