import streamlit as st

from brain.knowledge import (
    add_knowledge,
    find_knowledge,
    add_structured_knowledge,
    find_structured_knowledge,
    find_contradictions,
    find_duplicate,
)

from brain.relations import (
    add_relation,
    find_relations,
    infer_from_relations,
)

from brain.reasoning import (
    build_reasoning_chain,
    explain_reasoning,
)


st.title("🧠 Мой ИИ")


# ==========================================
# 📚 ПРОСТАЯ ПАМЯТЬ
# ==========================================

st.header("📚 Память")

subject = st.text_input(
    "О чём запомнить?",
    key="simple_subject"
)

fact = st.text_input(
    "Что нужно запомнить?",
    key="simple_fact"
)

if st.button("Запомнить", key="save_simple"):

    if subject and fact:

        add_knowledge(
            subject,
            fact
        )

        st.success(
            "Я запомнил это."
        )


# ==========================================
# 🧩 СТРУКТУРИРОВАННОЕ ЗНАНИЕ
# ==========================================

st.header(
    "🧩 Структурированное знание"
)

structured_subject = st.text_input(
    "Объект",
    key="structured_subject"
)

structured_property = st.text_input(
    "Свойство",
    key="structured_property"
)

structured_value = st.text_input(
    "Значение",
    key="structured_value"
)

if st.button(
    "Сохранить знание",
    key="save_structured"
):

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
                "🟡 Это знание уже есть "
                "в моей памяти."
            )

        else:

            contradictions = (
                find_contradictions(
                    structured_subject,
                    structured_property,
                    structured_value
                )
            )

            if contradictions:

                st.error(
                    "🔴 Обнаружено "
                    "противоречие!"
                )

                for item in contradictions:

                    st.write(
                        f"{item['subject']} → "
                        f"{item['property']} → "
                        f"{item['value']} "
                        f"(уверенность: "
                        f"{item.get('confidence', 1.0)})"
                    )

                st.info(
                    "Новое знание "
                    "не сохранено."
                )

            else:

                add_structured_knowledge(
                    structured_subject,
                    structured_property,
                    structured_value
                )

                st.success(
                    "Знание сохранено."
                )


# ==========================================
# 🔗 СВЯЗЬ МЕЖДУ ЗНАНИЯМИ
# ==========================================

st.header(
    "🔗 Связь между знаниями"
)

relation_subject = st.text_input(
    "Откуда",
    key="relation_subject"
)

relation_type = st.text_input(
    "Связь",
    key="relation_type"
)

relation_object = st.text_input(
    "К чему",
    key="relation_object"
)

if st.button(
    "Сохранить связь",
    key="save_relation"
):

    if (
        relation_subject
        and relation_type
        and relation_object
    ):

        add_relation(
            relation_subject,
            relation_type,
            relation_object
        )

        st.success(
            "Связь сохранена."
        )


# ==========================================
# 🔎 ПОИСК
# ==========================================

st.header(
    "🔎 Поиск в памяти"
)

search_subject = st.text_input(
    "Что найти?",
    key="search_subject"
)

if st.button(
    "Найти",
    key="search_button"
):

    if search_subject:

        # ----------------------------------
        # Простые факты
        # ----------------------------------

        simple_results = find_knowledge(
            search_subject
        )

        if simple_results:

            st.subheader(
                "📚 Простые факты"
            )

            for item in simple_results:

                st.write(
                    f"{item['subject']} — "
                    f"{item['fact']}"
                )


        # ----------------------------------
        # Структурированные знания
        # ----------------------------------

        structured_results = (
            find_structured_knowledge(
                search_subject
            )
        )

        if structured_results:

            st.subheader(
                "🧩 Структурированные знания"
            )

            for item in structured_results:

                st.write(
                    f"{item['subject']} → "
                    f"{item['property']} → "
                    f"{item['value']} "
                    f"(уверенность: "
                    f"{item.get('confidence', 1.0)})"
                )


        # ----------------------------------
        # Прямые связи
        # ----------------------------------

        relation_results = find_relations(
            search_subject
        )

        if relation_results:

            st.subheader(
                "🔗 Связи"
            )

            for item in relation_results:

                st.write(
                    f"{item['subject']} → "
                    f"{item['relation']} → "
                    f"{item['object']} "
                    f"(уверенность: "
                    f"{item.get('confidence', 1.0)})"
                )


        # ----------------------------------
        # Старый механизм вывода
        # ----------------------------------

        inferred_results = (
            infer_from_relations(
                search_subject
            )
        )

        if inferred_results:

            st.subheader(
                "🧠 Выводы"
            )

            for item in inferred_results:

                st.write(
                    f"{item['subject']} → "
                    f"{item['relation']} → "
                    f"{item['object']} "
                    f"(через: {item['via']}, "
                    f"уверенность: "
                    f"{item['confidence']})"
                )


        # ----------------------------------
        # Новый механизм рассуждения
        # ----------------------------------

        reasoning_results = (
            build_reasoning_chain(
                search_subject
            )
        )

        if reasoning_results:

            st.subheader(
                "🧠 Цепочки рассуждения"
            )

            for chain in reasoning_results:

                st.write(
                    f"➡️ Результат: "
                    f"{chain['result']}"
                )

                st.write(
                    f"Уверенность: "
                    f"{chain['confidence']}"
                )

                st.write(
                    "Основания:"
                )

                for step in chain["path"]:

                    st.write(
                        f"{step['subject']} → "
                        f"{step['relation']} → "
                        f"{step['object']}"
                    )


        if (
            not simple_results
            and not structured_results
            and not relation_results
            and not inferred_results
            and not reasoning_results
        ):

            st.info(
                "Я пока ничего не нашёл."
            )
