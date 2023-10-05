import json
import concurrent.futures
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def preprocess_ocr_data(ocr_data):
    #this removes the commas from the txt files to not cause bloated percentage
    return [word.strip() for word in ocr_data.split(',') if word.strip()]

def read_file_content(file_path):
    # just what it says
    try:
        with open(file_path, 'r') as file:
            content = file.read()
            return preprocess_ocr_data(content) 
    except Exception as exc:
        print(f"Error reading file '{file_path}': {exc}")
        return []

def calculate_similarity(uploaded_file_content, other_file_content):

    uploaded_text = ' '.join(uploaded_file_content)
    other_text = ' '.join(other_file_content)
    
    tfidf_matrix = TfidfVectorizer().fit_transform([uploaded_text, other_text])
    similarity = cosine_similarity(tfidf_matrix[0], tfidf_matrix[1])
    return similarity[0][0]

def compare_file_similarity(uploaded_file_content, other_file_data):

    try:
        uploaded_text = ' '.join(uploaded_file_content)
        other_text = ' '.join(other_file_data.read_file_content())

        tfidf_matrix = TfidfVectorizer().fit_transform([uploaded_text, other_text])
        similarity = cosine_similarity(tfidf_matrix[0], tfidf_matrix[1])

        return other_file_data.filename, similarity[0][0]
    

    except Exception as exc:
        print(f"Error calculating similarity for '{other_file_data.filename}': {exc}")
        return other_file_data.filename, None

