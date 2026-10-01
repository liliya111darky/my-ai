import streamlit as st
from memory import add_knowledge, find_knowledge


st.set_page_config(
    page_title="My AI",
    page_icon="🧠",
)

st.title("🧠 My AI")
st.write("Мой собственный искусственный интеллект")

st.divider()

st.subheader("📚 Память")

subject = st.text_input("Тема")
fact = st.text_area("Что должен запомнить ИИ?")

if st.button("💾 Запомнить"):
    if subject and fact:
        add_knowledge(subject, fact)
        st.success("Знание сохранено в памяти!")
    else:
        st.warning("Заполни тему и знание.")

st.divider()

st.subheader("🔎 Поиск в памяти")

search_subject = st.text_input("Что найти в памяти?")

if st.button("🔍 Найти"):
    if search_subject:
        results = find_knowledge(search_subject)

        if results:
            for item in results:
                st.write(f"**{item['subject']}** — {item['fact']}")
        else:
            st.info("Я пока ничего не знаю об этом.")
    else:
        st.warning("Напиши тему для поиска.")
