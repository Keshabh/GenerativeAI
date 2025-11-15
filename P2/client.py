#to build the web application
import streamlit as st
#to send url requests over the internet
import requests

BASE_URL = "http://127.0.0.1:8000"

st.title("LangServe Essay & Poem Generator 🎭")

tab1, tab2 = st.tabs(["✍️ Essay", "📜 Poem"])

with tab1:
    st.header("Essay Generator")
    essay_prompt = st.text_area("Enter your essay topic:", "Impact of AI on education")
    if st.button("Generate Essay"):
        with st.spinner("Generating essay..."):
            response = requests.post(f"{BASE_URL}/essay/invoke", json={"input": essay_prompt})
            if response.status_code == 200:
                result = response.json()
                st.subheader("Generated Essay:")
                st.write(result.get("output", "No output"))
            else:
                st.error("Error: Could not connect to the essay endpoint")

with tab2:
    st.header("Poem Generator")
    poem_prompt = st.text_area("Enter your poem theme:", "Sunrise over the desert")
    if st.button("Generate Poem"):
        with st.spinner("Generating poem..."):
            response = requests.post(f"{BASE_URL}/poem/invoke", json={"input": poem_prompt})
            if response.status_code == 200:
                result = response.json()
                st.subheader("Generated Poem:")
                st.write(result.get("output", "No output"))
            else:
                st.error("Error: Could not connect to the poem endpoint")
