import streamlit as st

st.set_page_config(
    page_title="My AI",
    page_icon="🧠",
)

st.title("🧠 My AI")
st.write("Мой собственный искусственный интеллект")

st.divider()

st.subheader("Первый диалог")

message = st.text_input("Напиши что-нибудь:")

if message:
    st.write("Ты сказал(а):")
    st.write(message)
    st.write("Я пока только учусь отвечать. Это моё первое ядро.")
