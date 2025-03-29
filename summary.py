import streamlit as st
import PyPDF2
import textwrap
import ollama

# Function to extract text from PDF in chunks
def extract_text_from_pdf(uploaded_file, chunk_size=3000):
    pdf_reader = PyPDF2.PdfReader(uploaded_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text() + "\n"
    
    # Split text into manageable chunks
    chunks = textwrap.wrap(text, chunk_size)
    return chunks

# Function to generate summary using DeepSeek-R1 7B
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

# Streamlit UI
st.title("Financial Document Story Generator (DeepSeek-R1 1.5B)")

uploaded_file = st.file_uploader("Upload a financial PDF", type=["pdf"])
mode = st.selectbox("Select Summary Mode", ["Beginner", "Intermediate", "Expert"])

if uploaded_file:
    st.write("Extracting text from PDF...")
    text_chunks = extract_text_from_pdf(uploaded_file)

    if st.button("Generate Summary"):
        st.write("Processing document with DeepSeek-R1 1.5B...")

        all_summaries = []
        for i, chunk in enumerate(text_chunks):
            st.write(f"Summarizing chunk {i+1}/{len(text_chunks)}...")
            summary = generate_summary(chunk, mode)
            all_summaries.append(summary)

        final_summary = "\n".join(all_summaries)

        st.subheader("Final Summary")
        st.write(final_summary)
