import streamlit as st
import pandas as pd
from funcs import (generate_metrics_plots, get_metrics_plots, generate_all_tracks_plots, get_all_tracks_plots,
                   generate_correlation_analysis_plots, get_correlation_analysis_plots, generate_route_plots,
                   get_route_plots, best_strategy)
import matplotlib.pyplot as plt
import os
print("Current working directory:", os.getcwd())
# Ustawienia strony
st.set_page_config(page_title="OЯTHO", layout="wide")

# Tytuł główny
st.title("💡 OЯTHO")
st.subheader("Analiza przyjmowanych strategii w edukacyjnej grze interaktywnej.")

# Lista nazw zakładek
tab_names = ["Home", "Wszystkie Tory"] + [f"Tor {i}" for i in range(1, 8)]

# Tworzenie zakładek
tabs = st.tabs(tab_names)


# Zawartość zakładki Główna
with tabs[0]:
    st.header("Wprowadzenie")
    st.markdown("""
        Witamy w interaktywnej analizie gry edukacyjnej **OЯTHO**, dostępnej w Centrum Nauki Kopernik. OЯTHO to kooperacyjna gra dla dwóch graczy, której celem jest wspólne przeprowadzenie kulki przez wirtualny tor. Jeden z graczy kontroluje ruch w osi **X**, a drugi w osi **Y** — sukces wymaga współpracy, komunikacji oraz dobrej koordynacji.
    
        Gra stanowi świetne wprowadzenie do **pojęcia układu współrzędnych** i rozwija umiejętności miękkie, takie jak **cierpliwość i współpraca**.
    
        ### 🔍 Cel analizy
        Celem tej analizy jest lepsze zrozumienie, jak użytkownicy radzą sobie z grą, oraz jakie strategie prowadzą do skutecznej współpracy i ukończenia poziomu. Sprawdzamy w jaki sposób dobór strategii poruszania się wpływa na szybkość przejścia poziomu oraz szansę na przejście go do końca.
       
    
        ### 📊 Co badamy?
        Nasza analiza koncentruje się na **poziomie trudności 0**, czyli podstawowym wariancie gry, w którym każdy gracz manualnie steruje ruchem wyłącznie w jednej osi.

                   
        Analizujemy m.in.:
        - **strategie ruchu** – np. czy gracze poruszają się płynnie, czy "schodkowo",
        - **metryki przejścia toru** – takie jak płynność ruchu (`smoothness`) czy stosunek schodkowych ruchów (`stair_ratio`),
        - **różnice między torami** – jak strategie zmieniają się w zależności od typu toru.
    
        
                 
        ### 📈 Metryki
        - `smoothness`: Mierzy płynność ruchu gracza. Wartości bliskie 0 oznaczają płynny ruch, podczas gdy większe wartości wskazują ruch z ostrymi zmianami kierunku.
    """)
    st.markdown(r"""
                $$
                \text{smoothness} = \frac{\sum_{i} (\arccos(\cos(\theta_i)))^2}{\sum_{j} \text{długość}_j} \\
                \text{gdzie } \theta_i \text{ to kąt pomiędzy wektorami kolejnych odcinków ruchu.}
                $$
    """)
    st.markdown("""

    - `stair_ratio`: Mierzy stosunek schodkowych ruchów do całkowitych ruchów. Wartości bliskie 0 oznaczają płynny ruch, podczas gdy wartości bliskie 1 wskazują na "schodkowy" ruch.
        $$
      \\text{stair\\_ratio} = \\frac{\\text{liczba kroków ze zmianą tylko wsółrzędnej X lub tylko współrzędnej Y}}{\\text{liczba wszystkich kroków}}
      $$

    """)

    st.markdown(r"""
    - `trajectory_strategy_bias`: Mierzy względną trudność danego fragmentu toru Y dla konkretnej strategii M
    (połączenia `stair_ratio_group` i `smoothness_group`) w porównaniu do innych strategii. Obliczana jako iloraz udziału 
    danej strategii w przedziale toru Y do udziału pozostałych strategii na tym samym przedziale toru 
    (liczone wśród próbek z completion ≥ Y).
    
    $$
    \text{trajectory\_strategy\_bias}(M,Y) \;=\;
    \frac{\displaystyle 
        \frac{\#\{m = M,\,y = Y\}}{\#\{m = M,\,y \geq Y\}}
    }
    {
        \displaystyle
        \frac{\#\{m \neq M,\,y = Y\}}{\#\{m \neq M,\,y \geq Y\}}
    }
    $$  
    ### ❓ Pytania badawcze:
    - W jaki sposób dwie metryki ruchu – smoothness i stair_ratio – wpływają na prawdopodobieństwo ukończenia oraz czas przejścia toru?
    - Czy optymalna kombinacja tych metryk - trajectory_strategy_bias - zmienia się w zależności od odcinka trasy?
                
    #### Literatura:
    K. Potęga vel Żabik, D. Abrahamson, I. Iłowiecka-Tańska, "It Takes Two to OЯTHO: A Tabletop Action-Based Embodied Design for the Cartesian System",  [Link](https://link.springer.com/article/10.1007/s40751-024-00139-8)       
                      
    ##### Autorzy:
    Natalia Choszczyk, Mateusz Deptuch, Aleksandra Samsel 
    """)
    calculate_toggle = st.toggle("oblicz wszystko od nowa")

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

all_stats = {
    "Liczba wszystkich gier": 64704, "Liczba ukończonych gier": 25533, "Procent ukończonych gier": "39.46%", "Średni czas gry (s)": 20.49, "Średni czas ukończonej gry (s)": 38.54, "Średni procent ukończenia gry": "58.67%"}


####################### WSZYSTKIE TORY #######################
with tabs[1]:
    st.header("Wszystkie Tory")
    st.markdown("Wykresy zostały wykonane na podstawie gier wykonanych w minimum 25%. Pozwala nam to wykluczyć gry, które ledwo zostały rozpoczęte i nie jesteśmy w stanie wyciągnąć na ich podstawie istotnych wniosków.")
    st.image(f"app_plots/tory.png", caption=f"Tory w grze OЯTHO", use_container_width=True)

    with st.spinner("Wykresy metryk", show_time=True):
        if calculate_toggle:
            all_metrics_plots = generate_metrics_plots("1_to_7_noXY", completed=False)
            all_tracks_plots = generate_all_tracks_plots()
            correlation_analysis_plots = generate_correlation_analysis_plots("1_to_7_noXY")
        else:
            all_metrics_plots = get_metrics_plots("1_to_7_noXY")
            all_tracks_plots = get_all_tracks_plots()
            correlation_analysis_plots = get_correlation_analysis_plots("1_to_7_noXY")

    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        df_stats = pd.DataFrame({
            "Statystyka": list(all_stats.keys()),
            "Wartość": list(all_stats.values())
        })

        st.subheader(f"📊 Podstawowe statystyki")
        st.dataframe(df_stats, use_container_width=True)
    with col2:
        st.pyplot(all_metrics_plots["hist_smoothness"])
    with col3:
        st.pyplot(all_metrics_plots["hist_stair_ratio"])
    
    st.subheader("Analiza ukończenia gry w zależności od wartości metryk")
    col_s1, col_s2, col_s3 = st.columns([1, 1, 1])
    with col_s1:
        st.pyplot(all_tracks_plots["hist_smoothness_true"])
    with col_s2:
        st.pyplot(all_tracks_plots["hist_smoothness_false"])
    with col_s3:
        st.pyplot(all_tracks_plots["scatter_smoothness_vs_stair_ratio_colored"])

    col_s4, col_s5, col_s6 = st.columns([1, 1, 1])
    with col_s4:
        st.pyplot(all_tracks_plots["hist_stair_ratio_true"])
    with col_s5:
        st.pyplot(all_tracks_plots["hist_stair_ratio_false"])
    with col_s6:
        st.pyplot(all_tracks_plots["scatter_smoothness_vs_stair_ratio_gradient"])

    col_s7, col_s8, col_s9 = st.columns([1, 1, 1])
    with col_s7:
        st.pyplot(correlation_analysis_plots["boxplot_time"])
    with col_s8:
        st.pyplot(correlation_analysis_plots["boxplot_smoothness"])
    with col_s9:
        st.pyplot(correlation_analysis_plots["boxplot_stair_ratio"])
    
    col7, col8 = st.columns([1, 1])
    with col7:
        st.pyplot(correlation_analysis_plots["spearman_correlation_matrix_completed"])
    with col8:
        st.pyplot(correlation_analysis_plots["spearman_correlation_matrix_not_completed"])

    st.markdown("Jak widać, metryki 'smoothness' i 'stair_ratio' wykazują znaczącą korelację z czasem ukończenia gry (Im bardziej gładki ruch, tym krótszy czas ukończenia gry, im mniej schodkowy ruch, tym krótszy czas ukończenia gry). Jednakże, żadna z metryk nie jest skorelowana z procentem ukończenia gry. Oznacza to, że gracze mogą ukończyć grę nawet przy dużych wartościach metryk, ale ich czas przejścia będzie dłuższy.")


    
####################### POSZCZEGÓLNE TORY #######################
for i in range(2, 9):
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


        st.subheader("📉 Wykresy dla metryki `smoothness` i `stair_ratio`")

        with st.spinner("Wykresy metryk", show_time=True):
            if calculate_toggle:
                metrics_plots = generate_metrics_plots(tor_num)
                correlation_analysis_plots = generate_correlation_analysis_plots(tor_num)
            else:
                metrics_plots = get_metrics_plots(tor_num)
                correlation_analysis_plots = get_correlation_analysis_plots(tor_num)

        row1_1, row1_2, row1_3, row1_4 = st.columns([1, 1, 1, 1])

        with row1_1:
            st.image(f"app_plots/min_smoothness_{tor_num}.png", caption=f"Najbardziej gładki tor", use_container_width=True)
        with row1_2:
            st.image(f"app_plots/min_stair_ratio_{tor_num}.png", caption=f"Tor z najmniejszym stair_ratio", use_container_width=True)
        with row1_3:
            st.image(f"app_plots/max_smoothness_{tor_num}.png", caption=f"Najmniej gładki tor", use_container_width=True)
        with row1_4:
            st.image(f"app_plots/max_stair_ratio_{tor_num}.png", caption=f"Tor z największym stair_ratio", use_container_width=True)

        row2_1, row2_2, row2_3, row2_4 = st.columns([1, 3, 3, 1])
        with row2_2:
            st.pyplot(metrics_plots["hist_smoothness"])
        with row2_3:
            st.pyplot(metrics_plots["hist_stair_ratio"])


        col7, col8, col9 = st.columns([1, 1, 1])
        with col7:
            st.pyplot(metrics_plots["smoothness_time_plot"])
        with col8:
            st.pyplot(metrics_plots["stair_ratio_time_plot"])
        with col9:
             st.pyplot(metrics_plots["scatter_plot"])

        st.markdown("Dalej porównajmy rozkład metryk `smoothness` i `stair_ratio` dla gier ukończonych i nieukończonych.")

        _, row4_2, row4_3, _ = st.columns([1, 3, 3, 1])
        with row4_2:
            st.markdown("**Gry ukończone**")
            st.pyplot(all_tracks_plots["hist_smoothness_true"])
            st.pyplot(all_tracks_plots["hist_stair_ratio_true"])
        with row4_3:
            st.markdown("**Gry nieukończone**")
            st.pyplot(all_tracks_plots["hist_smoothness_false"])
            st.pyplot(all_tracks_plots["hist_stair_ratio_false"])

        st.markdown("Dotakowo spójrzmy na rozkład metryk w stosunku do ukończenia toru.")

        _, row5_2, row5_3, _ = st.columns([1, 3, 3, 1])

        with row5_2:
            st.pyplot(all_tracks_plots["scatter_smoothness_vs_stair_ratio_colored"])
        with row5_3:
            st.pyplot(all_tracks_plots["scatter_smoothness_vs_stair_ratio_gradient"])


        col_s7, col_s8, col_s9 = st.columns([1, 1, 1])
        with col_s7:
            st.pyplot(correlation_analysis_plots["boxplot_time"])
        with col_s8:
            st.pyplot(correlation_analysis_plots["boxplot_smoothness"])
        with col_s9:
            st.pyplot(correlation_analysis_plots["boxplot_stair_ratio"])

        col_s12, col_s13, col_s14 = st.columns([1, 5, 1])
        with col_s13:
            st.markdown("Poniższy wykres wizualizuje trasę podzieloną na odcinki, gdzie kolor odcinka odpowiada najskuteczniejszej strategii "
                        "na tym właśnie fragmencie. Najlepsza strategia jest wybrana na podstawie metryki `trajectory_strategy_bias`."
                        "Im mniejsza wartość tej metryki, tym lepsza strategia dla danego fragmentu toru.")
            st.pyplot(best_strategy(tor_num))


        _, col_s10, col_s11, _ = st.columns([1, 4, 4, 1])
        with col_s10:
            st.pyplot(correlation_analysis_plots["spearman_correlation_matrix_completed"])
        with col_s11:
            st.pyplot(correlation_analysis_plots["spearman_correlation_matrix_not_completed"])

            if calculate_toggle:
                routes_plot = generate_route_plots(tor_num)
            else:
                routes_plot = get_route_plots(tor_num)
            with col_s10:
                st.image(routes_plot)
                st.markdown("Powyższy wykres przedstawia wszystkie trasy (ukończone w przynajmjiej 25%), które zostały wykonane przez graczy.")


