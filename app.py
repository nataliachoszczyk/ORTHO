import streamlit as st
import pandas as pd
from funcs import generate_plots

# Ustawienia strony
st.set_page_config(page_title="ORTHO", layout="wide")

# Tytuł główny
st.title("💡 ORTHO")
st.subheader("Analiza przyjmowanych strategii w edukacyjnej grze interaktywnej.")

# Lista nazw zakładek
tab_names = ["Home", "Wszystkie Tory"] + [f"Tor {i}" for i in range(1, 8)]

# Tworzenie zakładek
tabs = st.tabs(tab_names)

# Zawartość zakładki Główna
with tabs[0]:
    st.header("Wprowadzenie")
    st.markdown("""
    Witamy w interaktywnej analizie gry edukacyjnej **ORTHO**, dostępnej w Centrum Nauki Kopernik. ORTHO to kooperacyjna gra dla dwóch graczy, której celem jest wspólne przeprowadzenie kulki przez wirtualny tor. Jeden z graczy kontroluje ruch w osi **X**, a drugi w osi **Y** — sukces wymaga współpracy, komunikacji oraz dobrej koordynacji.

    Gra stanowi świetne wprowadzenie do **pojęcia układu współrzędnych** i rozwija umiejętności miękkie, takie jak **cierpliwość i współpraca**.

    ### 🔍 Cel analizy

    Nasza analiza koncentruje się na **poziomie trudności 0**, czyli podstawowym wariancie gry, w którym każdy gracz manualnie steruje ruchem wyłącznie w jednej osi.

    ### 📊 Co badamy?

    Analizujemy m.in.:
    - **strategie ruchu** – np. czy gracze poruszają się płynnie, czy "schodkowo",
    - **metryki przejścia toru** – takie jak płynność ruchu (`smoothness`) czy stosunek schodkowych ruchów (`stair ratio`),
    - **różnice między torami** – jak strategie zmieniają się w zależności od typu toru.

    Celem tej analizy jest lepsze zrozumienie, jak użytkownicy radzą sobie z grą, oraz jakie strategie prowadzą do skutecznej współpracy i ukończenia poziomu.
    """)

# Zawartość zakładki Wszystkie Tory
with tabs[1]:
    st.header("Wszystkie Tory")
    st.markdown("Tutaj znajdują się zbiorcze dane lub wizualizacje dotyczące wszystkich torów.")
    st.image(f"app_plots/tory.png", caption=f"Tory w grze ORTHO", use_container_width=True)

# Zakładki Tor 1 – Tor 7
stats_by_track = {
    1: {"Liczba wszystkich gier": 19631, "Liczba ukończonych gier": 7936, "Procent ukończonych gier": "40.43%", "Średni czas gry (s)": 24.7, "Średni czas ukończonej gry (s)": 45.44, "Średni procent ukończenia gry": "62.16%"},
    2: {"Liczba wszystkich gier": 22999, "Liczba ukończonych gier": 8079, "Procent ukończonych gier": "35.13%", "Średni czas gry (s)": 21.66, "Średni czas ukończonej gry (s)": 44.4, "Średni procent ukończenia gry": "52.58%"},
    3: {"Liczba wszystkich gier": 20679, "Liczba ukończonych gier": 8842, "Procent ukończonych gier": "42.76%", "Średni czas gry (s)": 15.4, "Średni czas ukończonej gry (s)": 27.71, "Średni procent ukończenia gry": "61.85%"},
    4: {"Liczba wszystkich gier": 418, "Liczba ukończonych gier": 168, "Procent ukończonych gier": "40.19%", "Średni czas gry (s)": 18.22, "Średni czas ukończonej gry (s)": 38.31, "Średni procent ukończenia gry": "56.37%"},
    5: {"Liczba wszystkich gier": 291, "Liczba ukończonych gier": 152, "Procent ukończonych gier": "52.23%", "Średni czas gry (s)": 21.29, "Średni czas ukończonej gry (s)": 33.11, "Średni procent ukończenia gry": "65.67%"},
    6: {"Liczba wszystkich gier": 262, "Liczba ukończonych gier": 182, "Procent ukończonych gier": "69.47%", "Średni czas gry (s)": 12.47, "Średni czas ukończonej gry (s)": 15.47, "Średni procent ukończenia gry": "77.33%"},
    7: {"Liczba wszystkich gier": 424, "Liczba ukończonych gier": 174, "Procent ukończonych gier": "41.04%", "Średni czas gry (s)": 16.54, "Średni czas ukończonej gry (s)": 30.65, "Średni procent ukończenia gry": "58.42%"}
}


for i in range(2, 9):  # Indeksy tabs[2] do tabs[8]
    with tabs[i]:
        tor_num = i - 1
        st.header(f"Tor {tor_num} – Analiza i Obraz")

        col1, col2, col3 = st.columns([1, 1, 1])

        with col1:
            st.image(f"app_plots/tor{tor_num}.png", caption=f"Tor {tor_num}", width=300, use_container_width="auto")
        with col2:
            st.image(f"app_plots/tor{tor_num}_ex.png", caption=f"Tor {tor_num} – przykładowa gra", use_container_width=True)
        with col3:
            selected_stats = stats_by_track[i-1]
            df_stats = pd.DataFrame({
                "Statystyka": list(selected_stats.keys()),
                "Wartość": list(selected_stats.values())
            })

            st.subheader(f"📊 Podstawowe statystyki")
            st.dataframe(df_stats, use_container_width=True)

        col4, col5 = st.columns([1, 1])
        with col4:
            st.image(f"app_plots/min_smoothness_{tor_num}.png", caption=f"Najbardziej gładki tor", use_container_width=True)
            st.image(f"app_plots/min_stair_ratio_{tor_num}.png", caption=f"Tor z najmniejszym stair_ratio", use_container_width=True)

        with col5:
            st.image(f"app_plots/max_smoothness_{tor_num}.png", caption=f"Najmniej gładki tor", use_container_width=True)
            st.image(f"app_plots/max_stair_ratio_{tor_num}.png", caption=f"Tor z największym stair_ratio", use_container_width=True)
        st.markdown("Wykresy zostały wykonane na podstawie gier wykonanych w minimum 50%")
        with st.spinner("Wykresy metryk", show_time=True):
            metrics_plots = generate_plots(f"data/filtered_records_{tor_num}_metrics.jsonl")
        st.subheader("📈 Wykresy metryk")
        col6, col7 = st.columns([1, 1])
        with col6:
            st.pyplot(metrics_plots["hist_smoothness"])
            st.pyplot(metrics_plots["smoothness_time_plot"])
            st.pyplot(metrics_plots["scatter_plot"])   
        with col7:  
            st.pyplot(metrics_plots["hist_stair_ratio"])
            st.pyplot(metrics_plots["stair_ratio_time_plot"])
         
