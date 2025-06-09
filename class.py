import streamlit as st

def get_bot_response(user_message):
    user_message = user_message.lower()
    if "deadline" in user_message:
        return "📅 The application deadline for Fall 2025 is January 15."
    elif "documents" in user_message:
        return "📝 You'll need transcripts, a personal statement, and recommendation letters."
    elif "how to apply" in user_message or "apply" in user_message:
        return "🧭 To apply, visit our website, choose your program, and fill out the online application form."
    elif "thank" in user_message:
        return "You're welcome! 😊"
    else:
        return "🤖 Sorry, I didn't quite get that. Could you rephrase your question?"

def main():
    st.set_page_config(page_title="University Chatbot", layout="centered")
    st.title("🎓 University Application Chatbot")
    st.markdown("Ask me anything about applying to the university!")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Input field
    user_input = st.text_input("You:", key="user_input")

    # Handle input
    if st.button("Send"):
        if user_input:
            st.session_state.chat_history.append(("You", user_input))
            bot_reply = get_bot_response(user_input)
            st.session_state.chat_history.append(("Bot", bot_reply))

            # Clear input using rerun
            del st.session_state["user_input"]
            st.experimental_rerun()

    # Display chat
    for sender, message in st.session_state.chat_history:
        if sender == "You":
            st.markdown(f"**{sender}:** {message}")
        else:
            st.markdown(f"<div style='text-align:right'><b>{sender}:</b> {message}</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
