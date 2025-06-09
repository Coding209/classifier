import streamlit as st

st.set_page_config(page_title="University Chatbot", layout="centered")

st.title("🎓 University Application Chatbot")

st.markdown("Ask me about application deadlines, documents, or how to apply.")

# Keep chat history in session
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Mock function to simulate bot response (replace with Rasa API call)
def get_bot_response(user_message):
    if "deadline" in user_message.lower():
        return "The application deadline for Fall 2025 is January 15."
    elif "documents" in user_message.lower():
        return "You will need transcripts, letters of recommendation, and your personal statement."
    elif "how to apply" in user_message.lower():
        return "Visit our admissions page and fill out the online application form."
    else:
        return "I'm sorry, I didn't understand that. Can you please rephrase?"

# Input box for user message
user_input = st.text_input("You:", key="user_input")

# On submit
if st.button("Send"):
    if user_input:
        st.session_state.chat_history.append(("You", user_input))
        bot_response = get_bot_response(user_input)
        st.session_state.chat_history.append(("Bot", bot_response))
        st.session_state.user_input = ""

# Display chat history
for sender, message in st.session_state.chat_history:
    if sender == "You":
        st.markdown(f"**{sender}:** {message}")
    else:
        st.markdown(f"<div style='text-align:right'><b>{sender}:</b> {message}</div>", unsafe_allow_html=True)


        # Create download link for the ZIP file
        href = f'<a href="data:application/zip;base64,{b64_zip}" download="{zip_filename}">Download 150 PDFs</a>'
        st.markdown(href, unsafe_allow_html=True)
        st.success("50 PDFs for each year generated successfully!")

if __name__ == "__main__":
    main()
