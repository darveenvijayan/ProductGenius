%%writefile ProductGenius.py
import streamlit as st
import tiktoken
from datetime import datetime, timedelta
import json
import requests
import time
import os

CHATBOT_API = os.environ["chat_api"]

left_co, cent_co,last_co = st.columns(3)
with cent_co:
    st.image("/content/AIA-Logo.png")

st.markdown("<h1 style='text-align: center;'>AIA Product Genius</h1>", unsafe_allow_html=True)
st.markdown("<h5 style='text-align: center; color: grey;'>AI chatbot capable of answering queries related to specific AIA products</h2>", unsafe_allow_html=True)
st.divider()

def get_with_json_body(url, json_data):
    # Encode the JSON data as a string
    encoded_data = json.dumps(json_data)
    # Set the headers to specify JSON content type
    headers = {"Content-Type": "application/json"}
    # Send the GET request with the JSON data in the body
    response = requests.get(url, headers=headers, data=encoded_data)
    # Return the response object
    return response

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Hello! Welcome to AIA. Before we get started, may I ask which product you are interested in learning about?"
        }
    ]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask me about AIA products"):


    #TODO: add prompt to st.session_state.messages

    json_data = {
        "query": prompt,
        "memory": st.session_state.messages
    }


    response = get_with_json_body(url=CHATBOT_API+'/product_genius/', json_data=json_data)

    # Check for successful response
    if response.status_code == 200:
        # Process the response data
        data = response.json()
        print(data)
    else:
        print(f"Error: {response.status_code}")

    answer = data['Answer']

    ####################################################################################



    print(len(st.session_state.messages))
    #print(st.session_state.messages)

    # write user text
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""

        # Simulate stream of response with milliseconds delay
        for chunk in answer.split():
            full_response += chunk + " "
            time.sleep(0.05)
            # Add a blinking cursor to simulate typing
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)

        # Calculate the number of input tokens
        encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
        input_token_count = len(encoding.encode(str(st.session_state.messages)))
        input_token_cost = (0.0005/1000)*input_token_count

        # Calculate the number of completions tokens
        completion_token_count = len(encoding.encode(str({"role": "assistant", "content": full_response})))
        completion_token_cost = (0.0015/1000)*completion_token_count
        tot_cost = input_token_cost*4.63 + completion_token_cost*4.63
        message_placeholder.markdown(full_response)#+f"\n\n[ OpenAI Cost: RM{tot_cost} ]")
        # message_placeholder.markdown(full_response)+f"\n\n[ OpenAI Cost: RM{tot_cost} ]")



    # Calculate the number of input tokens
    encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
    input_token_count = len(encoding.encode(str(st.session_state.messages)))
    input_token_cost = (0.0005/1000)*input_token_count

    # Calculate the number of completions tokens
    completion_token_count = len(encoding.encode(str({"role": "assistant", "content": full_response})))
    completion_token_cost = (0.0015/1000)*completion_token_count

    print('Question:',prompt)
    print('Answer:',full_response)
    print(f"Input tokens: {input_token_count} | Cost: RM{input_token_cost*4.63}")
    print(f"Completion tokens: {completion_token_count} | Cost: RM{completion_token_cost*4.63}")
    print(f"Total Cost: RM{input_token_cost*4.63 + completion_token_cost*4.63}")
    print("======")

    st.session_state.messages = data['memory']
    #print(st.session_state.messages)

