import streamlit as st

from memory import (
    add_relation,
    find_relations,
)

from brain.knowledge import (
    add_knowledge,
    find_knowledge,
    add_structured_knowledge,
    find_structured_knowledge,
    find_contradictions,
    find_duplicate,
)


st.title("🧠 Мой ИИ")


# ============================================================
# 📚 ПРОСТОЕ ЗНАНИЕ
# ============================================================

st.header("📚 Память")

subject = st.text_input(
    "Понятие",
    key="simple_subject"
)

fact = st.text_input(
    "Факт",
    key="simple_fact"
)

if st.button("Сохранить знание"):
    if subject and fact:
        add_knowledge(subject, fact)
        st.success("🟢 Знание сохранено!")
    else:
        st.warning("Введите понятие и факт.")


# ============================================================
# 🧩 СТРУКТУРИРОВАННОЕ ЗНАНИЕ
# ============================================================

st.header("🧩 Структурированное знание")

structured_subject = st.text_input(
    "Объект",
    key="structured_subject"
)

structured_property = st.text_input(
    "Свойство / отношение",
    key="structured_property"
)

structured_value = st.text_input(
    "Значение",
    key="structured_value"
)

confidence = st.slider(
    "Уверенность",
    min_value=0.0,
    max_value=1.0,
    value=1.0,
    step=0.1
)

if st.button("Сохранить структурированное знание"):

    if (
        structured_subject
        and structured_property
        and structured_value
    ):

        duplicate = find_duplicate(
            structured_subject,
            structured_property,
            structured_value
        )

        if duplicate:
            st.warning(
                "🟡 Это знание уже есть в моей памяти."
            )

        else:

            contradictions = find_contradictions(
                structured_subject,
                structured_property,
                structured_value
            )

            if contradictions:

                st.error(
                    "🔴 Обнаружено противоречие!"
                )

                st.write(
                    "Существующее знание:"
                )

                for item in contradictions:

                    st.write(
                        f"**{item['subject']}** → "
                        f"{item['property']} → "
                        f"{item['value']} "
                        f"(уверенность: "
                        f"{item.get('confidence', 1.0)})"
                    )

                st.info(
                    "Новое знание не сохранено, "
                    "потому что оно противоречит "
                    "существующему."
                )

            else:

                add_structured_knowledge(
                    structured_subject,
                    structured_property,
                    structured_value,
                    confidence
                )

                st.success(
                    "🟢 Структурированное знание сохранено!"
                )

    else:

        st.warning(
            "Заполните все поля."
        )


# ============================================================
# 🔗 СВЯЗИ МЕЖДУ ЗНАНИЯМИ
# ============================================================

st.header("🔗 Связь между знаниями")

relation_subject = st.text_input(
    "Объект 1",
    key="relation_subject"
)

relation = st.text_input(
    "Отношение",
    key="relation"
)

relation_object = st.text_input(
    "Объект 2",
    key="relation_object"
)

relation_confidence = st.slider(
    "Уверенность связи",
    min_value=0.0,
    max_value=1.0,
    value=1.0,
    step=0.1,
    key="relation_confidence"
)

if st.button("Сохранить связь"):

    if (
        relation_subject
        and relation
        and relation_object
    ):

        add_relation(
            relation_subject,
            relation,
            relation_object,
            relation_confidence
        )

        st.success(
            "🟢 Связь сохранена!"
        )

    else:

        st.warning(
            "Заполните все поля."
        )


# ============================================================
# 🔎 ПОИСК В ПАМЯТИ
# ============================================================

st.header("🔎 Поиск в памяти")

search_subject = st.text_input(
    "Что найти?",
    key="search_subject"
)

if st.button("Найти"):

    if search_subject:

        simple_results = find_knowledge(
            search_subject
        )

        structured_results = find_structured_knowledge(
            search_subject
        )

        relation_results = find_relations(
            search_subject
        )

        if (
            not simple_results
            and not structured_results
            and not relation_results
        ):

            st.info(
                "Ничего не найдено."
            )

        else:

            if simple_results:

                st.subheader(
                    "📚 Простые знания"
                )

                for item in simple_results:

                    st.write(
                        f"**{item['subject']}** → "
                        f"{item['fact']}"
                    )

            if structured_results:

                st.subheader(
                    "🧩 Структурированные знания"
                )

                for item in structured_results:

                    st.write(
                        f"**{item['subject']}** → "
                        f"{item['property']} → "
                        f"{item['value']} "
                        f"(уверенность: "
                        f"{item.get('confidence', 1.0)})"
                    )

            if relation_results:

                st.subheader(
                    "🔗 Связи"
                )

                for item in relation_results:

                    st.write(
                        f"**{item['subject']}** → "
                        f"{item['relation']} → "
                        f"{item['object']} "
                        f"(уверенность: "
                        f"{item.get('confidence', 1.0)})"
                    )

    else:

        st.warning(
            "Введите понятие для поиска."
        )
