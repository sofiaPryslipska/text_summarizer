import streamlit as st
from google import genai
from google.genai import types

st.set_page_config(page_title="Text Summarizer")
st.title("Text Summarizer")

with st.sidebar:
    st.header("Configuration")
    api_key = st.text_input("Enter API Key", type="password")
    
    summary_style = st.selectbox(
        "Output Format",
        ["Short Paragraph", "Bullet Points", "Detailed Analysis"]
    )

text = st.text_area("Source Text", height=200)

prompts = {
    "Short Paragraph": "Summarize the text into one concise paragraph. Return only the summary text without any greetings, introductions, or conversational filler.",
    "Bullet Points": "Extract the main points from the text as a bulleted list. Return only the list without any greetings, introductions, or conversational filler.",
    "Detailed Analysis": "Perform a structured analysis of the text. Identify the main idea, key arguments, and conclusions. Use Markdown headings. Return only the analysis."
}

if st.button("Summarize"):
    if not api_key:
        st.error("API Key is required.")
    elif not text:
        st.warning("Source text is required.")
    else:
        try:
            with st.spinner("Processing..."):
                client = genai.Client(
                    api_key=api_key, 
                    http_options={'api_version': 'v1beta'}
                )
                
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=text,
                    config=types.GenerateContentConfig(
                        system_instruction=prompts[summary_style],
                        temperature=0.2
                    )
                )
                
                st.success("Result:")
                st.write(response.text)
                
        except Exception as e:
            st.error(f"Error: {str(e)}")
