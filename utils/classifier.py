import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle
import numpy as np
  
with open('model/tfidf_model_llm.pkl', 'rb') as file:
    best_model, tfidf_vectorizer = pickle.load(file)

routing_rules = {
    "complaint": "Customer Support",
    "praise": "Public Relations",
    "inquiry": "Sales",
    "suggestion": "Product Development"
}

def classify_and_route(feedback_list):
    X_input_tfidf = tfidf_vectorizer.transform(feedback_list)
    prediction = best_model.predict(X_input_tfidf)

    results = []
    for feedback, prediction in zip(feedback_list, prediction):
        results.append({
            "feedback": feedback,
            "category": prediction,
        })
    return results
