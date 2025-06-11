import streamlit as st

# Page config
st.set_page_config(layout="wide")

# Layout
col1, col2 = st.columns([1, 2])

# Left: Static image
with col1:
    st.image("image.png")

# Right: Simple chatbot
with col2:
    st.title("Chatbot")

    if "chat" not in st.session_state:
        st.session_state.chat = []

    user_input = st.text_input("You:", key="input")

    if user_input:
        st.session_state.chat.append(("You", user_input))
        bot_reply = f"You said: {user_input}"
        st.session_state.chat.append(("Bot", bot_reply))

    for sender, msg in st.session_state.chat:
        st.write(f"**{sender}:** {msg}")
