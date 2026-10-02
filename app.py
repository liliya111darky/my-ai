import streamlit as st
from memory import (
    add_knowledge,
    find_knowledge,
    add_structured_knowledge,
    find_structured_knowledge,
    add_relation,
    find_relations
)


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

st.subheader("🧩 Структурированное знание")

structured_subject = st.text_input("Объект")
structured_property = st.text_input("Свойство")
structured_value = st.text_input("Значение")

structured_confidence = st.slider(
    "Уверенность",
    min_value=0.0,
    max_value=1.0,
    value=1.0,
    step=0.1
)

if st.button("🧠 Сохранить структурированное знание"):
    if structured_subject and structured_property and structured_value:
        add_structured_knowledge(
            structured_subject,
            structured_property,
            structured_value,
            structured_confidence
        )
        st.success("Структурированное знание сохранено!")
    else:
        st.warning("Заполни объект, свойство и значение.")


st.divider()

st.subheader("🔗 Связь между знаниями")

relation_subject = st.text_input(
    "Объект 1",
    key="relation_subject"
)

relation_type = st.text_input(
    "Отношение",
    key="relation_type"
)

relation_object = st.text_input(
    "Объект 2",
    key="relation_object"
)

relation_confidence = st.slider(
    "Уверенность в связи",
    min_value=0.0,
    max_value=1.0,
    value=1.0,
    step=0.1,
    key="relation_confidence"
)

if st.button("🔗 Сохранить связь"):
    if relation_subject and relation_type and relation_object:
        add_relation(
            relation_subject,
            relation_type,
            relation_object,
            relation_confidence
        )
        st.success("Связь сохранена в памяти!")
    else:
        st.warning("Заполни оба объекта и отношение.")


st.divider()

st.subheader("🔎 Поиск в памяти")

search_subject = st.text_input("Что найти в памяти?")

if st.button("🔍 Найти"):
    if search_subject:
        results = find_knowledge(search_subject)
        structured_results = find_structured_knowledge(search_subject)
        relation_results = find_relations(search_subject)

        if results:
            for item in results:
                if "fact" in item:
                    st.write(
                        f"**{item['subject']}** — {item['fact']}"
                    )

        if structured_results:
            for item in structured_results:
                st.write(
                    f"**{item['subject']}** → "
                    f"{item['property']} → "
                    f"{item['value']} "
                    f"(уверенность: {item['confidence']})"
                )

        if relation_results:
            for item in relation_results:
                st.write(
                    f"**{item['subject']}** → "
                    f"{item['relation']} → "
                    f"{item['object']} "
                    f"(уверенность: {item['confidence']})"
                )

        if not results and not structured_results and not relation_results:
            st.info("Я пока ничего не знаю об этом.")
    else:
        st.warning("Напиши тему для поиска.")
