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

# def compare_file_similarity(uploaded_file_content, other_file_data):

#     try:
#         uploaded_file_path = uploaded_file_content[0] 
#         uploaded_file_content = read_file_content(uploaded_file_path)
        
#         other_file_content = read_file_content(other_file_data['file'])
#         if other_file_content:
#             similarity = calculate_similarity(uploaded_file_content, other_file_content)
#             return other_file_data['filename'], similarity
#         else:
#             print(f"Empty content for file '{other_file_data['filename']}'. Skipping.")
#             return other_file_data['filename'], None
#     except Exception as exc:
#         print(f"Error calculating similarity for '{other_file_data['filename']}': {exc}")
#         return other_file_data['filename'], None
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

def compare_uploaded_file_with_database(uploaded_file_content, file_model_list):
    # Some parallel processing magic which I have no clue of
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_to_filename = {
            executor.submit(compare_file_similarity, uploaded_file_content, file_model): file_model.filename
            for file_model in file_model_list
        }
        for future in concurrent.futures.as_completed(future_to_filename):
            filename = future_to_filename[future]
            try:
                result = future.result()
                if result[1] is not None:
                    print(f"Similarity between uploaded file and '{filename}': {result[1] * 100:.2f}")
                else:
                    print(f"Error processing '{filename}': Unable to calculate similarity.")
            except Exception as exc:
                print(f"Error processing '{filename}': {exc}")


# def compare_uploaded_file_with_database(uploaded_file_content, file_data_list):
#     # some parallel processing magic which I have no clue of
#     with concurrent.futures.ThreadPoolExecutor() as executor:
#         future_to_filename = {executor.submit(compare_file_similarity, uploaded_file_content, file_data): file_data['filename'] for file_data in file_data_list}
#         for future in concurrent.futures.as_completed(future_to_filename):
#             filename = future_to_filename[future]
#             try:
#                 result = future.result()
#                 if result[1] is not None:
#                     print(f"Similarity between uploaded file and '{filename}': {result[1]*100:.2f}")
#                 else:
#                     print(f"Error processing '{filename}': Unable to calculate similarity.")
#             except Exception as exc:
#                 print(f"Error processing '{filename}': {exc}")

# sample_json_data = '''
# {
#     "filename": "QWERTY.pdf",
#     "description": "a file",
#     "file": "/content/drive/MyDrive/BERT/textDetectionOutput/ocrText.txt"
# }'''

# file_data_list_json = '''
# [
#     {
#         "filename": "QWERTY2.pdf",
#         "description": "a file",
#         "file": "/content/drive/MyDrive/BERT/textDetectionOutput/ocrText.txt"
#     },
#     {
#         "filename": "QWERTY3.pdf",
#         "description": "a file",
#         "file": "/content/drive/MyDrive/BERT/textDetectionOutput/ocrText2.txt"
#     },
#     {
#         "filename": "QWERTY4.pdf",
#         "description": "a file",
#         "file": "/content/drive/MyDrive/BERT/textDetectionOutput/hash.txt"
#     }
# ]
# '''

# uploaded_file_data = json.loads(sample_json_data)
# uploaded_file_content = preprocess_ocr_data(uploaded_file_data['file'])

# file_data_list = json.loads(file_data_list_json)

# compare_uploaded_file_with_database(uploaded_file_content, file_data_list) 

