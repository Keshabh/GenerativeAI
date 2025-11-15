#Here we will be providing youtube video url
#then we will retrieve videoId from the url
#we will use a lib, where we will pass videoId and get youtube video transcript
#then we will pass this transcript into LLM along with user query,
#uer query could be any doubts regarding the video, maybe to make a notes or to summarize the video.

from dotenv import load_dotenv
load_dotenv()
from youtube_transcript_api import YouTubeTranscriptApi
import os
import google.generativeai as genai
import streamlit as st

genai.configure(api_key = os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-2.5-pro")

def retrieve_video_id(youtube_url):
    return youtube_url.split('=')[1]

def getYoutubeTranscript(videoId):
    api =YouTubeTranscriptApi()
    transcript = api.fetch(video_id = videoId)
    return transcript


def get_gemini_response(prompt, transcript):
    response = model.generate_content(prompt + transcript)
    return response.text


#lets use the model to get the 250 summarise words from the llm
st.session_state.prompt = """You are an expert youtube video summariser. You will be given transcript text
and you will be summarising the entire video and provide me the most important points within 250 words. 
Please provide the summary of the text. Please consider the following transcript: \n"""

st.header("YouTube Doubt Solver: Powered With AI")
url = st.text_input("YouTube Video URL ?", key = "url")
input = st.text_input("Ask your dobts !", key = "doubt")
button = st.button("Get Answer >>")

if button:
    if "summarisedText" not in st.session_state or url != st.session_state.storedUrl:
        st.session_state.storedUrl = url
        data = getYoutubeTranscript(retrieve_video_id(st.session_state.storedUrl))
        allText = ""
        for d in data:
            allText += " " + d.text
        st.session_state.summarisedText = get_gemini_response(st.session_state.prompt,allText)
    prompt = f"""You are an expert in taking user query, and work on the query, and give exactly as asked using the summariseText provided to you.
    Following is the user query:
    {input}
    \n\n Please consider the provided summarised transcript text of a youtube video:\n"""
    ansFetched = get_gemini_response(prompt,st.session_state.summarisedText)
    st.write(ansFetched)



