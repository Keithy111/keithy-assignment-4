from flask import Flask, render_template, request, jsonify
from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import nltk
from nltk.corpus import stopwords

nltk.download('stopwords')

# Initialize the Flask app
app = Flask(__name__)

# Step 1: Fetch dataset and initialize vectorizer
newsgroups = fetch_20newsgroups(subset='all')
stop_words = stopwords.words('english')

# Step 2: Create a term-document matrix using TfidfVectorizer
vectorizer = TfidfVectorizer(stop_words=stop_words, max_features=10000)
X = vectorizer.fit_transform(newsgroups.data)

# Step 3: Apply Singular Value Decomposition (SVD) for dimensionality reduction (LSA)
n_components = 100  # Number of dimensions to reduce to
svd = TruncatedSVD(n_components=n_components)
X_reduced = svd.fit_transform(X)

# Step 4: Define the search engine function
def search_engine(query):
    """
    Function to search for top 5 similar documents given a query
    Input: query (str)
    Output: documents (list), similarities (list), indices (list)
    """
    # Transform the query using the same TF-IDF vectorizer and SVD
    query_vector = vectorizer.transform([query])
    query_reduced = svd.transform(query_vector)

    # Compute cosine similarity between the query and all documents
    similarities = cosine_similarity(query_reduced, X_reduced)[0]
    
    # Get top 5 most similar document indices
    top_indices = np.argsort(similarities)[::-1][:5]
    
    # Retrieve the top 5 documents, similarities, and indices
    top_documents = [newsgroups.data[i] for i in top_indices]
    top_similarities = [similarities[i] for i in top_indices]
    
    return top_documents, top_similarities, top_indices.tolist()

# Flask routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    query = request.form['query']
    documents, similarities, indices = search_engine(query)
    return jsonify({'documents': documents, 'similarities': similarities, 'indices': indices})

if __name__ == '__main__':
    app.run(debug=True)
