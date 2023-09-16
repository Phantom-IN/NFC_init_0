from webbrowser import BackgroundBrowser
import streamlit as st
from streamlit_option_menu import option_menu
import base64
import pandas as pd
from flask import Flask, request, jsonify
from sentiment import get_sentiment
from predict import classify_text
import matplotlib.pyplot as plt
from youtube_transcript_api import YouTubeTranscriptApi
import re
import joblib
import string
 
app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    heading = data['heading']
    description = data['description']
    sentiment = get_sentiment(heading)
    department = classify_text(description)
    first_label = department["labels"][0]
    
    if first_label == "finance":
        first_label = "Ministry of Finance"
    
    if first_label == "agriculture":
        first_label = "Ministry of Agriculture"
    
    if first_label == "defence":
        first_label = "Ministry of Defence"

    if first_label == "environment":
        first_label = "Ministry of Environment, Forest and Climate Change"

    if first_label == "health":
        first_label = "Ministry of Health and Family Welfare"

    if first_label == "water":
        first_label = "Ministry of Jal Shakti"

    if first_label == "science":
        first_label = "Ministry of Science & Technology"
        
    if first_label == "technology":
        first_label = "Ministry of Science & Technology"

    if first_label == "family":
        first_label = "Ministry of Health and Family Welfare"

    if first_label == "others":
        first_label = "Others"
        
    if first_label == "information and broadcasting":
        first_label = "Ministry of Information & Broadcasting"
        
    if first_label == "prime minister":
        first_label = "Prime Minister's Office"

    to_add = {
        "Title": [heading],
        "Description": [description],
        "Sentiment": [sentiment],
        "Department": [first_label]
    }
    to_add_df = pd.DataFrame(to_add)
    to_add_df.to_csv("Salary_Data.csv", mode='a', header=False, index=False)

    # Convert DataFrame to dictionary
    to_add_dict = to_add_df.to_dict(orient='records')
    response = {"label": first_label}
    return jsonify(response)

# @app.route("/classify", methods=["POST"])
# def classify():
#     data = request.get_json()
#     text = data.get("heading")
#     result = classify_text(text)
#     first_label = result["labels"][0]
#     return jsonify(first_label)

if __name__ == '__main__':
    
    st.set_page_config(page_title="NewsRakshak", page_icon=":memo:", layout="wide")

    data = pd.read_csv("Salary_Data.csv")
    st.set_option('deprecation.showPyplotGlobalUse', False)

    def add_bg_from_local(image_file):
        with open(image_file, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read())
        st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url(data:image/{"png"};base64,{encoded_string.decode()});
            background-size: cover
        }}
        </style>
        """,
        unsafe_allow_html=True
        )
    add_bg_from_local('bg2.jpg')

    # Define columns
    col1, col2 = st.columns([2, 4])
    st.markdown("##")
    st.markdown("##")
    st.markdown("##")

    # Title in the first column
    with col1:
        st.header(":memo: NewsRakshak")

    # Option menu in the second column
    with col2:
        selected = option_menu(
            menu_title=None,
            options=["Home","Ministry", "YouTube Check", "Contact", "FakeNews"],
            icons=["house","buildings","youtube","phone","youtube"],
            menu_icon="cast",
            default_index=0,
            orientation="horizontal",
            styles={
                "container": {"background-color": "#fafafa"},
                "icon": {"color": "orange", "font-size": "18px"},
                "nav-link": {
                    "font-size": "15px",
                    "text-align": "left",
                    "margin": "0px",
                    "--hover-color": "#eee",
                },

            },
        )


    if selected == "Home":
        st.header("Home Page")
        textarea_input = st.text_area("Enter your feedback here", "")
        if st.button("Submit"):
            if textarea_input == '':
                st.write("Textbox cannot be empty!!!")
            else:
                sentiment = get_sentiment(textarea_input)
                department = classify_text(textarea_input)
                first_label = department["labels"][0]
        
                if first_label == "finance":
                    first_label = "Ministry of Finance"
                
                if first_label == "agriculture":
                    first_label = "Ministry of Agriculture"
                
                if first_label == "defence":
                    first_label = "Ministry of Defence"

                if first_label == "environment":
                    first_label = "Ministry of Environment, Forest and Climate Change"

                if first_label == "health":
                    first_label = "Ministry of Health and Family Welfare"

                if first_label == "water":
                    first_label = "Ministry of Jal Shakti"

                if first_label == "science":
                    first_label = "Ministry of Science & Technology"
                    
                if first_label == "technology":
                    first_label = "Ministry of Science & Technology"

                if first_label == "family":
                    first_label = "Ministry of Health and Family Welfare"

                if first_label == "others":
                    first_label = "Others"
                    
                if first_label == "information and broadcasting":
                    first_label = "Ministry of Information & Broadcasting"
                    
                if first_label == "prime minister":
                    first_label = "Prime Minister's Office"
                st.write(f"The given text is associated with {first_label} and has {sentiment} sentiment.")

    if selected == "Ministry":
        valid_admin_username = 'admin'
        valid_admin_password = 'password'

        username = st.text_input("Username:")
        password = st.text_input("Password:", type="password")

        if st.button("Login"):
            if username == valid_admin_username and password == valid_admin_password:
                st.success("Logged in as: {}".format(username))
                st.header("Ministry Page")
                selected_option = st.selectbox("Select an option", ['Prime Minister Office', 'Ministry of Health and Family Welfare', 'Ministry of Defence', 'Ministry of Finance', 'Ministry of Commerce & Industry', 'Ministry of Science & Technology', 'Ministry of Jal Shakti', 'Ministry of Information & Broadcasting', 'Ministry of Agriculture & Farmers Welfare', 'Ministry of Environment, Forest and Climate Change', 'Others'])
                st.write(f"You selected: {selected_option}")
                filtered_df = data[data["Department"] == selected_option]
                st.write("Filtered Data:")
                if st.checkbox("Show Table"):
                    st.dataframe(filtered_df,width = 1000 , height = 500)
                sentiment_counts = filtered_df["Sentiment"].value_counts()
                st.subheader("Sentiment Distribution:")
                fig, ax = plt.subplots(figsize=(8, 8))
                ax.pie(sentiment_counts, labels=sentiment_counts.index, autopct='%1.1f%%', startangle=90)
                ax.axis('equal')
                st.pyplot(fig)
                if st.button("Download Filtered Data as CSV"):
                    csv_file = filtered_df.to_csv(index=False)
                    b64 = base64.b64encode(csv_file.encode()).decode()
                    href = f'<a href="data:file/csv;base64,{b64}" download="filtered_data.csv">Download CSV</a>'
                    st.markdown(href, unsafe_allow_html=True)
            else:
                st.error("Invalid username or password")
                st.stop()
    
    if selected == "YouTube Check":
        st.subheader("YouTube URL Checker")
        youtube_url = st.text_input("Enter a YouTube URL:", placeholder="https://www.youtube.com/watch?v=VIDEO_ID")
        if st.button("Check YouTube URL"):
            match = re.search(r"v=([A-Za-z0-9_-]+)", youtube_url)
            if match:
                video_id = match.group(1)
            else:
                raise ValueError("Invalid YouTube URL")
            transcript = YouTubeTranscriptApi.get_transcript(video_id)
            transcript_text = ""
            for segment in transcript:
                transcript_text += segment["text"] + " "
            sentiment = get_sentiment(transcript_text)
            st.write(f"The given YouTube video link has {sentiment} sentiment.")

    if selected == "Contact":
        st.header("Contact Us")
        def validate_input(username, phone_number, email, subject, message):
            if not username:
                return "Username is required!"
            elif not phone_number:
                return "Phone number is required!"
            elif not email:
                return "Please give your Email!"
            elif not is_valid_email(email):
                return "Give a valid Email!"
            elif not subject:
                return "Please give your Subject!"
            elif not message:
                return "Message is required!"
            else:
                return None
        username = st.text_input("Your Name")
        phone_number = st.text_input("Phone Number")
        email = st.text_input("Email")
        subject = st.text_input("Subject")
        message = st.text_area("Message", height=200)

        def is_valid_email(email):
            import re
            pattern = r'^\w+([-]?\w+)*@\w+([-]?\w+)*(\.\w{2,3})+$'
            return re.match(pattern, email.lower())
        if st.button("Send Message"):
            err_msg = validate_input(username, phone_number, email, subject, message)
            if err_msg:
                st.error(err_msg)
            else:
                success_msg = f"Thank you dear {username}, Your message has been sent successfully!"
                st.success(success_msg)

    if selected == "FakeNews":
        st.header("Fake News Detector")
        textarea_input = st.text_area("Enter the news you want to verify", "")
        if st.button("Submit"):
            if textarea_input == '':
                st.write("Textbox cannot be empty!!!")
            else:
                Model = joblib.load('fake_news_model.pkl')
                def wordpre(text):
                    text = text.lower()
                    text = re.sub(r'\[.*?\]', '', text)
                    text = re.sub("\\W"," ",text)
                    text = re.sub(r'https?://\S+|www\.\S+', '', text)
                    text = re.sub('<.*?>+', '', text)
                    text = re.sub('[%s]' % re.escape(string.punctuation), '', text)
                    text = re.sub('\n', '', text)
                    text = re.sub(r'\w*\d\w*', '', text)
                    return text
                
                txt = wordpre(textarea_input)
                txt = pd.Series(txt)
                result = Model.predict(txt)
                if result == 0:
                    st.write(f"The given news is FAKE.")
                else:
                    st.write(f"The given news is REAL.")


    hide_st_style = """
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                header {visibility: hidden;}
                </style>
                """
    st.markdown(hide_st_style, unsafe_allow_html=True)
    app.run()