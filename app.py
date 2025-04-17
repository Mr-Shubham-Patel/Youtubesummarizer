from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

prompt = """You are a Youtube video summarizer. You will be taking the transcript text and
summarizing the entire video and provide the important summary in points withing 250-300
words. Please provide the summary of the text given here in 2 languages English and Hindi. 
Please translate it accordingly: """

def extract_transcript_details(video_url):
    try:
        video_id = video_url.split("=")[1]
        transcript_text = YouTubeTranscriptApi.get_transcript(video_id,languages=["en","hi"])
        transcript = ""
        for i in transcript_text:
            transcript += " " + i['text']
        return transcript
    except Exception as e:
        raise e
    
st.set_page_config(page_title="Youtube Video Summarizer")
st.header("Youtube Video Summarizer Web Application")

youtube_link = st.text_input("Enter Youtube Video Link")

if youtube_link:
    video_id = youtube_link.split("=")[1]
    st.image(f"https://img.youtube.com/vi/pSVk-5WemQ0/0.jpg",use_column_width=True)

submit = st.button("Submit")

def gemini_model_response(transcript_text,prompt):
    model = genai.GenerativeModel("gemini-2.0-flash")
    reponse = model.generate_content(prompt+transcript_text)
    return reponse.text

if submit:
    transcript_text = extract_transcript_details(youtube_link)
    if transcript_text:
        summary = gemini_model_response(transcript_text,prompt)
        st.markdown("### Summary of the video:")
        st.write(summary)
    else:
        st.write("No summary found")