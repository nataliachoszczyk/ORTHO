import streamlit as st

# Ustawienia strony
st.set_page_config(page_title="ORTHO", layout="wide")

# Tytuł główny
st.title("💡 ORTHO")
st.subheader("Analiza przyjmowanych strategii w grze interaktywnej.")

# Lista nazw zakładek
tab_names = ["Home", "Wszystkie Tory"] + [f"Tor {i}" for i in range(1, 8)]

# Tworzenie zakładek
tabs = st.tabs(tab_names)

# Zawartość zakładki Główna
with tabs[0]:
    st.header("Wprowadzenie")
    st.markdown("""
    tutaj sobie opisszemy czym jest ortho i co robimy w tej aplikacji.
    """)

# Zawartość zakładki Wszystkie Tory
with tabs[1]:
    st.header("Wszystkie Tory")
    st.markdown("Tutaj znajdują się zbiorcze dane lub wizualizacje dotyczące wszystkich torów.")
    st.image(f"app_plots/tory.png", caption=f"Tory w grze ORTHO", use_container_width=True)

# Zakładki Tor 1 – Tor 7
for i in range(2, 9):  # Indeksy tabs[2] do tabs[8]
    with tabs[i]:
        tor_num = i - 1
        st.header(f"Tor {tor_num} – Analiza i Obraz")

        col1, col2, col3 = st.columns([2, 1, 3])

        with col1:
            st.image(f"app_plots/tor{tor_num}.png", caption=f"Tor {tor_num}", width=300, use_container_width="auto")
        with col3:
            st.image(f"app_plots/tor{tor_num}_ex.png", caption=f"Tor {tor_num} – przykładowa gra", use_container_width=True)
