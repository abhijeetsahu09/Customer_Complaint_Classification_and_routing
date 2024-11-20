import pandas as pd
import re


# def preprocess_text(text):
#     text = re.sub(r'\s+', ' ', text)  # Remove extra whitespace
#     text = re.sub(r'[^a-zA-Z0-9\s]', '', text)  # Remove special characters
#     text = text.lower()  # Convert text to lowercase
#     return text

def load_feedback_from_csv(file):
    # df = pd.read_csv(file)

    if file:
        try:
            df = pd.read_csv(file)
        except UnicodeDecodeError:
            file.seek(0)
            try:
                df = pd.read_csv(file, encoding='ISO-8859-1')
            except UnicodeDecodeError:
                file.seek(0)
                df = pd.read_csv(file, encoding='cp1252')

    # df['feedback'] = df['feedback'].apply(preprocess_text)

    feedback_list = df['feedback'].tolist()
    return feedback_list
