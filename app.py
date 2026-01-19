import os
import pandas as pd
import numpy as np 
import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI

# Lets get the api key from the environment
gemini_api_key = os.getenv('TestProject1')

# Lets configure the model
model = ChatGoogleGenerativeAI(
    model = 'gemini-2.5-flash-lite' ,
    api_key = gemini_api_key
)

#Design the UI of application
st.title(":orange[HealthifyMe:] :blue[You Personal Health Assistant]")
st.markdown(''' This applicaions will assist you to get better and customized Health Advice. You can ask your health related 
            issues and get the personalized guidance.''')

st.write(
'''
Follow These Steps:
* Enter your details in sidebar.
* Rate your activity and fitness on the sclae of 0-5.
* Submit your Details
* Ask your question on the main page
* Click on Generate button and relax !! 
'''
)
# Design the sidebar for all the user parameters
st.sidebar.header(':red[ENTER YOUR DETAILS]')
name = st.sidebar.text_input("Enter Your Name:")
gender = st.sidebar.selectbox("Select Your Gender:",['Male','Female'])
age = st.sidebar.text_input("Enter Your Age:")
weight = st.sidebar.text_input("Ente your weight in Kgs:")
height = st.sidebar.text_input("Ente your height in Cms:")
bmi = pd.to_numeric(weight) / (( pd.to_numeric(height)/100)**2)
active = st.sidebar.slider("Rate Your Activity (0-5):",0,5,step=1)
fit = st.sidebar.slider("Rate Your Fitness (0-5):",0,5,step=1)
if st.sidebar.button('Submit'):
    st.sidebar.write(f"{name}, your BMI is: {round(bmi,2)} Kg/m^2")
    
# Lets use the Gemini Model to generate the report 
user_input = st.text_input("Ask me your Question, I'm here to help you:")
prompt = f''' 
<Role> You are an expert in health and wellness and has 10+ years experince in guiding people.
<Goal> Generate the customized report addressing the problem the user have asked Here is the question that user have asked: {user_input}.
<Context> Here are the detils of the user which is provide by the user name = {name} 
age = {age} 
gender= {gender}
height = {height} 
weight = {weight} 
activity_rate(0-5) = {active} 
fittness_rate(0-5) = {fit}
<Instruction>
* Use bullets points where ever possible *
*Create Tables to represent any data whenever possible*
*Strictly do not advise any medicine, what may come.*
<Format> Following should be the outline of the report, in the sequence
* Start with 2-3 lines of comments which user have givenin the user_input * 
*Explain what the real probelm could be on the bsis of input the user have provided *
*Sugest the possible reasons for the problems *
*What are the possible solutions *
*Mention the Doctor from  what specilzation can be visited if required *
*Memntion ny chage in the diet which is required. *
*In last create a final summary of the things that has been discussed in the report *
'''

if st.button('Generate'):
    response = model.invoke(prompt)
    st.write(response.content)
    