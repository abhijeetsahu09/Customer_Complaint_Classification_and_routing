import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle
import numpy as np


# model = joblib.load("model/tfidf_model.pkl")   
with open('model/tfidf_model.pkl', 'rb') as file:
    best_model, tfidf_vectorizer = pickle.load(file)

routing_rules = {
    "complaint": "Customer Support",
    "praise": "Public Relations",
    "inquiry": "Sales",
    "suggestion": "Product Development"
}

def classify_and_route(feedback_list):
    # print(feedback_list)

    # final_list = model.predict(X_test_tfidf)
    # print(final_list)
    X_input_tfidf = tfidf_vectorizer.transform(feedback_list)
    prediction = best_model.predict(X_input_tfidf)

    results = []
    for feedback, prediction in zip(feedback_list, prediction):
        # prediction = model.predict(X_test_tfidf)[0]  # Assuming model outputs a label directly
        # department = routing_rules.get(prediction, "General")
        results.append({
            "feedback": feedback,
            "category": prediction,
            # "department": department
        })
    return results
