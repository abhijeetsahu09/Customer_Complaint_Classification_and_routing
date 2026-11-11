import pandas as pd
import re
from googletrans import Translator

def load_feedback_from_csv(file):

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

    translator = Translator()

    def translate_if_needed(text):
        detected = translator.detect(text)
        if detected.lang in ['hi', 'mr', 'te']:
            translation = translator.translate(text, dest='en')
            return translation.text
        else:
            return text
        
    df['feedback'] = df['feedback'].apply(translate_if_needed)

    feedback_list = df['feedback'].tolist()
    return feedback_list


