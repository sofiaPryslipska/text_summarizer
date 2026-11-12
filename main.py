import streamlit as st
from google import genai
from google.genai import types

# Налаштування сторінки для кращого вигляду
st.set_page_config(page_title="Текстовий сумаризатор", page_icon="📝")
st.title("Текстовий сумаризатор 📝")

# Винесення налаштувань у бокову панель
with st.sidebar:
    st.header("Налаштування генерації")
    api_key = st.text_input("Введіть Gemini API Key", type="password")

    # Додавання вибору моделі
    model_choice = st.selectbox(
        "Оберіть модель",
        ["gemini-2.5-flash", "gemini-2.5-pro", "gemini-2.0-flash"]
    )

    # Додавання повзунка для температури
    temperature = st.slider(
        "Температура (креативність)",
        min_value=0.0,
        max_value=2.0,
        value=0.3,  # 0.3 - оптимально для сумаризації
        step=0.1,
        help="Нижчі значення роблять текст більш точним і передбачуваним. Вищі - креативнішим."
    )

    # Додавання вибору формату результату
    summary_style = st.selectbox(
        "Формат результату",
        ["Короткий абзац", "Головні тези (Bullet points)", "Детальний аналіз"]
    )

text = st.text_area("Введіть текст для сумаризації", height=200)

# Словник з розширеними промптами під кожен стиль
prompts = {
    "Короткий абзац": "Ти професійний редактор. Зроби вижимку цього тексту одним коротким абзацом. Пиши лише результат, без привітань та вступних слів.",
    "Головні тези (Bullet points)": "Ти аналітик. Виділи найголовніші думки з наданого тексту у вигляді маркованого списку. Пиши лише результат, без вступних слів.",
    "Детальний аналіз": "Зроби структурований аналіз тексту: виділи головну ідею, ключові аргументи та висновки. Форматуй відповідь за допомогою заголовків markdown."
}

if st.button("Сумаризувати", type="primary"):
    if not api_key:
        st.error("Помилка: Введіть API key у боковій панелі")
    elif not text:
        st.warning("Помилка: Введіть текст для обробки")
    else:
        try:
            # Візуальний індикатор завантаження
            with st.spinner(f"Генерую підсумок за допомогою {model_choice}..."):
                client = genai.Client(api_key=api_key)
                response = client.models.generate_content(
                    model=model_choice,
                    contents=text,
                    config=types.GenerateContentConfig(
                        system_instruction=prompts[summary_style],
                        temperature=temperature
                    )
                )

                st.success("Результат:")
                st.write(response.text)

        except Exception as e:
            st.error(f"Виникла помилка: {str(e)}")
