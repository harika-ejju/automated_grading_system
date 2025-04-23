import streamlit as st
import requests
import pandas as pd
from config import API_KEY

# --- Streamlit UI ---
st.set_page_config(page_title="AI Essay Grader", layout="wide")
st.title("📝 AI-Powered Essay Grading System")

# Input field for essay
user_input = st.text_area("✍️ Paste your essay here:", height=250)

# Function to send request to Google Gemini API
def grade_essay(essay):
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateText"
    headers = {"Content-Type": "application/json"}
    prompt = f"Grade the following essay on a scale of 1-100 based on content, coherence, grammar, vocabulary, and structure. Provide a detailed breakdown:\n\n{essay}"
    
    data = {"prompt": {"text": prompt}, "temperature": 0.7}
    response = requests.post(f"{url}?key={API_KEY}", json=data, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        return None

# Grade Essay Button
if st.button("🚀 Grade My Essay"):
    if not user_input.strip():
        st.warning("⚠️ Please enter an essay before grading.")
    else:
        st.info("⏳ Grading your essay... Please wait.")
        result = grade_essay(user_input)

        if result:
            # Extract AI-generated response
            ai_output = result.get("candidates", [{}])[0].get("output", "Error: No response from AI.")
            
            # Display AI feedback
            st.subheader("📊 Essay Evaluation Breakdown")
            st.write(ai_output)

            # Simulating extracted scores (Modify this based on actual API response)
            sample_scores = {
                "Criteria": ["Content Relevance", "Coherence", "Grammar", "Vocabulary", "Structure"],
                "Score": [85, 80, 90, 88, 85]  # Placeholder scores
            }
            df_scores = pd.DataFrame(sample_scores)
            st.table(df_scores)

            # Export as Excel
            df_scores.to_excel("graded_essay.xlsx", index=False)
            with open("graded_essay.xlsx", "rb") as f:
                st.download_button("📥 Download Grade Report (Excel)", f, file_name="graded_essay.xlsx", mime="application/vnd.ms-excel")
        else:
            st.error("❌ Failed to retrieve essay evaluation. Please check API Key & Internet connection.")
