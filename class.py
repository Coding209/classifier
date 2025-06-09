import streamlit as st

# ---------------- Bot Logic ---------------- #
def get_bot_response(user_message):
    user_message = user_message.lower()
    if "deadline" in user_message:
        return "📅 The application deadline for Fall 2025 is January 15."
    elif "documents" in user_message:
        return "📝 You'll need transcripts, a personal statement, and recommendation letters."
    elif "apply" in user_message:
        return "🧭 To apply, visit our website, choose your program, and fill out the online application form."
    else:
        return "🤖 Sorry, I didn't understand. Could you rephrase your question?"

# ---------------- Main App ---------------- #
def main():
    st.set_page_config(page_title="🎓 University Chatbot", layout="centered")
    st.markdown("<h2 style='text-align: center;'>🎓 University Application Chatbot</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Ask me anything about applying to the university!</p>", unsafe_allow_html=True)

    # Initialize chat history
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Display chat history with avatars
    for sender, message in st.session_state.chat_history:
        if sender == "You":
            st.markdown(f"""
                <div style='display: flex; align-items: center; margin-bottom: 10px;'>
                    <div style='font-size: 20px; margin-right: 8px;'>🧑</div>
                    <div style='background-color: #e1f5fe; padding: 10px; border-radius: 10px;'>{message}</div>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
                <div style='display: flex; align-items: center; margin-bottom: 10px; justify-content: flex-end;'>
                    <div style='background-color: #fce4ec; padding: 10px; border-radius: 10px; margin-right: 8px;'>{message}</div>
                    <div style='font-size: 20px;'>🎓</div>
                </div>
            """, unsafe_allow_html=True)

    # Input box (within form for safe clearing)
    with st.form("chat_form", clear_on_submit=True):
        user_input = st.text_input("Enter your message here...", placeholder="Type here and press Send")
        submitted = st.form_submit_button("Send")

    if submitted and user_input.strip():
        st.session_state.chat_history.append(("You", user_input.strip()))
        bot_reply = get_bot_response(user_input.strip())
        st.session_state.chat_history.append(("Bot", bot_reply))

if __name__ == "__main__":
    main()


