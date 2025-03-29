import PyPDF2
import textwrap
import ollama
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Function to extract text from PDF
def extract_text_from_pdf(pdf_path):
    with open(pdf_path, "rb") as file:
        pdf_reader = PyPDF2.PdfReader(file)
        text = " ".join(page.extract_text() or "" for page in pdf_reader.pages)
    return text

# Function to clean text
def clean_text(text):
    text = text.lower()
    text = re.sub(r'\W+', ' ', text)  # Remove special characters
    return text

# Function to generate summary using DeepSeek-R1
def generate_summary(text, mode):
    prompt = f"""
    Summarize the following financial document in {mode} mode:
    - Beginner: Simple language, key insights.
    - Intermediate: More details, explanations.
    - Expert: In-depth analysis, financial jargon.

    Document:
    {text}
    """
    try:
        response = ollama.chat(model="deepseek-r1:1.5b", messages=[{"role": "user", "content": prompt}])
        return response["message"]["content"]
    except Exception as e:
        return f"Error generating summary: {str(e)}"

# Function to check summary accuracy using cosine similarity
def verify_summary(original_text, summary):
    vectorizer = TfidfVectorizer(stop_words="english")
    vectors = vectorizer.fit_transform([clean_text(original_text), clean_text(summary)])
    similarity_score = cosine_similarity(vectors[0], vectors[1])[0][0]
    
    if similarity_score > 0.7:
        return f"✅ High similarity ({similarity_score:.2f}): Summary is accurate."
    elif 0.4 < similarity_score <= 0.7:
        return f"⚠️ Moderate similarity ({similarity_score:.2f}): Some details might be missing."
    else:
        return f"❌ Low similarity ({similarity_score:.2f}): Possible hallucinations."

# Main execution
if __name__ == "__main__":
    pdf_path = input("Enter the path to your financial PDF: ")
    mode = input("Select summary mode (Beginner/Intermediate/Expert): ").capitalize()

    print("\nExtracting text from PDF...")
    full_text = extract_text_from_pdf(pdf_path)

    print("\nGenerating summary with DeepSeek-R1...")
    summary = generate_summary(full_text, mode)

    print("\nGenerated Summary:")
    print("-" * 80)
    print(summary)
    print("-" * 80)

    # Verify Summary Accuracy
    print("\nVerifying summary accuracy...")
    verification_report = verify_summary(full_text, summary)

    print("\nVerification Report:")
    print(verification_report)
