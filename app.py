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
st.subheader("Analiza przyjmowanych strategii w edukacyjnej grze interaktywnej | Analysis of adopted strategies in an educational interactive game")

# Lista nazw zakładek
tab_names = ["Home", "Wszystkie Tory | All Tracks"] + [f"Tor | Track {i}" for i in range(1, 8)]

# Tworzenie zakładek
tabs = st.tabs(tab_names)


# Zawartość zakładki Główna
with tabs[0]:
    st.header("Wprowadzenie | Introduction")
    st.markdown("""
        Witamy w interaktywnej analizie gry edukacyjnej **OЯTHO**, dostępnej w Centrum Nauki Kopernik. OЯTHO to kooperacyjna gra dla dwóch graczy, której celem jest wspólne przeprowadzenie kulki przez wirtualny tor. Jeden z graczy kontroluje ruch w osi **X**, a drugi w osi **Y** — sukces wymaga współpracy, komunikacji oraz koordynacji. 
        Welcome to the interactive analysis of the educational game **OЯTHO**, available at the Copernicus Science Centre. OЯTHO is a cooperative game for two players, where the goal is to jointly guide a ball through a virtual track. One player controls movement along the **X** axis, while the other controls movement along the **Y** axis — success requires collaboration, communication, and coordination.
    
        Gra stanowi świetne wprowadzenie do **pojęcia układu współrzędnych** i rozwija umiejętności miękkie, takie jak **cierpliwość i współpraca**. 
        The game serves as an excellent introduction to the **concept of the coordinate system** and develops soft skills such as **patience and collaboration**.
    
        ### 🔍 Cel analizy | Analysis Purpose
        Celem tej analizy jest lepsze zrozumienie, jak użytkownicy radzą sobie z grą, oraz jakie strategie prowadzą do skutecznej współpracy i ukończenia poziomu. Sprawdzamy w jaki sposób dobór strategii poruszania się wpływa na szybkość przejścia poziomu oraz szansę na przejście go do końca. 
        The purpose of this analysis is to better understand how users cope with the game and which strategies lead to effective collaboration and level completion. We examine how the choice of movement strategies affects the speed of level completion and the chances of completing it successfully.
       
    
        ### 📊 Co badamy? | What are we investigating?
        Nasza analiza koncentruje się na **poziomie trudności 0**, czyli podstawowym wariancie gry, w którym każdy gracz manualnie steruje ruchem wyłącznie w jednej osi. 
        Our analysis focuses on **difficulty level 0**, which is the basic variant of the game where each player manually controls movement in only one axis.

                   
        Analizujemy m.in.:
        - **metryki przejścia toru** – takie jak płynność ruchu (`smoothness`) czy stosunek schodkowych ruchów (`stair_ratio`),
        - **różnice między torami** – jak strategie zmieniają się w zależności od typu toru,
        - **strategie na poszczególnych odcinkach toru** – szukamy optymalnej strategii i ścieżki dla danego toru.  
                
                
        We analyze, among other things:
        - **track traversal metrics** – such as movement *smoothness* (`*smoothness*`) and the ratio of stair-like movements (`*stair_ratio*`),
        - **differences between tracks** – how strategies change depending on the type of track,
        - **strategies on individual track segments** – we search for the optimal strategy and path for a given track.

    
        
                 
        ### 📈 Metryki | Metrics
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
    *Measures the ratio of stair-like movements to total movements. Values close to 0 indicate smooth movement, while values close to 1 indicate "stair-like" movement.*
    $$
    \\text{stair\_ratio} = \\frac{\\text{liczba kroków ze zmianą tylko współrzędnej X lub tylko współrzędnej Y}}{\\text{liczba wszystkich kroków}} \\\\
    \\text{stair\_ratio} = \\frac{\\text{number of steps changing only X or only Y coordinate}}{\\text{total number of steps}}
    $$


    """)

    st.markdown(r"""
   - `trajectory_strategy_bias`: Mierzy względną trudność danego fragmentu toru Y dla konkretnej strategii M 
    (połączenia `stair_ratio_group` i `smoothness_group`) w porównaniu do innych strategii. Obliczana jako iloraz udziału 
    danej strategii w przedziale toru Y do udziału pozostałych strategii na tym samym przedziale toru 
    (liczone wśród próbek z completion ≥ Y).  
    *Measures the relative difficulty of a given track segment Y for a specific strategy M* 
    *(combination of `stair_ratio_group` and `smoothness_group`) compared to other strategies. Calculated as the ratio* 
    *of the share of the given strategy in the track segment Y to the share of other strategies in the same segment* 
    *(counted among samples with completion ≥ Y).* 

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

    ### ❓ Pytania badawcze | Research Questions:
    - W jaki sposób dwie metryki ruchu – smoothness i stair_ratio – wpływają na prawdopodobieństwo ukończenia oraz czas przejścia toru? | In what way do the two movement metrics – smoothness and stair_ratio – affect the probability of completion and the time taken to complete the track?
    - Czy optymalna kombinacja tych metryk - trajectory_strategy_bias - zmienia się w zależności od odcinka trasy? | Does the optimal combination of these metrics - trajectory_strategy_bias - change depending on the segment of the track?
                
    #### Literatura | Literature:
    K. Potęga vel Żabik, D. Abrahamson, I. Iłowiecka-Tańska, "It Takes Two to OЯTHO: A Tabletop Action-Based Embodied Design for the Cartesian System",  [Link](https://link.springer.com/article/10.1007/s40751-024-00139-8)       
                      
    ##### Autorzy | Authors:
    Natalia Choszczyk, Mateusz Deptuch, Aleksandra Samsel 
    """)
    calculate_toggle = st.toggle("oblicz wszystko od nowa | recalculate everything")

# Zakładki Tor 1 – Tor 7
stats_by_track = {
    1: {
        "Liczba wszystkich gier / Total games": 19631,
        "Liczba ukończonych gier / Completed games": 7936,
        "Procent ukończonych gier / Completion rate": "40.43%",
        "Średni czas gry (s) / Average game time (s)": 24.7,
        "Średni czas ukończonej gry (s) / Average completed game time (s)": 45.44,
        "Średni procent ukończenia gry / Average completion percentage": "62.16%"
    },
    2: {
        "Liczba wszystkich gier / Total games": 22999,
        "Liczba ukończonych gier / Completed games": 8079,
        "Procent ukończonych gier / Completion rate": "35.13%",
        "Średni czas gry (s) / Average game time (s)": 21.66,
        "Średni czas ukończonej gry (s) / Average completed game time (s)": 44.4,
        "Średni procent ukończenia gry / Average completion percentage": "52.58%"
    },
    3: {
        "Liczba wszystkich gier / Total games": 20679,
        "Liczba ukończonych gier / Completed games": 8842,
        "Procent ukończonych gier / Completion rate": "42.76%",
        "Średni czas gry (s) / Average game time (s)": 15.4,
        "Średni czas ukończonej gry (s) / Average completed game time (s)": 27.71,
        "Średni procent ukończenia gry / Average completion percentage": "61.85%"
    },
    4: {
        "Liczba wszystkich gier / Total games": 418,
        "Liczba ukończonych gier / Completed games": 168,
        "Procent ukończonych gier / Completion rate": "40.19%",
        "Średni czas gry (s) / Average game time (s)": 18.22,
        "Średni czas ukończonej gry (s) / Average completed game time (s)": 38.31,
        "Średni procent ukończenia gry / Average completion percentage": "56.37%"
    },
    5: {
        "Liczba wszystkich gier / Total games": 291,
        "Liczba ukończonych gier / Completed games": 152,
        "Procent ukończonych gier / Completion rate": "52.23%",
        "Średni czas gry (s) / Average game time (s)": 21.29,
        "Średni czas ukończonej gry (s) / Average completed game time (s)": 33.11,
        "Średni procent ukończenia gry / Average completion percentage": "65.67%"
    },
    6: {
        "Liczba wszystkich gier / Total games": 262,
        "Liczba ukończonych gier / Completed games": 182,
        "Procent ukończonych gier / Completion rate": "69.47%",
        "Średni czas gry (s) / Average game time (s)": 12.47,
        "Średni czas ukończonej gry (s) / Average completed game time (s)": 15.47,
        "Średni procent ukończenia gry / Average completion percentage": "77.33%"
    },
    7: {
        "Liczba wszystkich gier / Total games": 424,
        "Liczba ukończonych gier / Completed games": 174,
        "Procent ukończonych gier / Completion rate": "41.04%",
        "Średni czas gry (s) / Average game time (s)": 16.54,
        "Średni czas ukończonej gry (s) / Average completed game time (s)": 30.65,
        "Średni procent ukończenia gry / Average completion percentage": "58.42%"
    }
}


all_stats = {
    "Liczba wszystkich gier / Total games": 64704,
    "Liczba ukończonych gier / Completed games": 25533,
    "Procent ukończonych gier / Completion rate": "39.46%",
    "Średni czas gry (s) / Average game time (s)": 20.49,
    "Średni czas ukończonej gry (s) / Average completed game time (s)": 38.54,
    "Średni procent ukończenia gry / Average completion percentage": "58.67%"
}


####################### WSZYSTKIE TORY #######################
with tabs[1]:
    st.header("Wszystkie Tory | All Tracks")
    st.markdown("""Wykresy zostały wykonane na podstawie gier wykonanych w minimum 25%. Pozwala nam to wykluczyć gry, które ledwo zostały rozpoczęte i nie jesteśmy w stanie wyciągnąć na ich podstawie istotnych wniosków.  
                Plots were created based on games completed in at least 25%. This allows us to exclude games that were barely started, from which we cannot draw significant conclusions.""")
    st.image(f"app_plots/tory.png", caption=f"Tory w grze OЯTHO", use_container_width=True)

    with st.spinner("Wykresy metryk | Metrics Plots", show_time=True):
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
            "Statystyka | Stat": list(all_stats.keys()),
            "Wartość | Value": list(all_stats.values())
        })

        st.subheader(f"📊 Podstawowe statystyki | Basic Stats")
        st.dataframe(df_stats, use_container_width=True)
    with col2:
        st.pyplot(all_metrics_plots["hist_smoothness"])
    with col3:
        st.pyplot(all_metrics_plots["hist_stair_ratio"])
    
    st.subheader("Analiza ukończenia gry w zależności od wartości metryk | Analysis of game completion based on metric values")
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

    st.markdown("""Jak widać, metryki 'smoothness' i 'stair_ratio' wykazują znaczącą korelację z czasem ukończenia gry (Im bardziej gładki ruch, tym krótszy czas ukończenia gry, im mniej schodkowy ruch, tym krótszy czas ukończenia gry). Jednakże, żadna z metryk nie jest skorelowana z procentem ukończenia gry. Oznacza to, że gracze mogą ukończyć grę nawet przy dużych wartościach metryk, ale ich czas przejścia będzie dłuższy.  
                As we can see, the metrics 'smoothness' and 'stair_ratio' show a significant correlation with the time taken to complete the game (the smoother the movement, the shorter the completion time; the less stair-like the movement, the shorter the completion time). However, none of the metrics is correlated with the percentage of game completion. This means that players can complete the game even with high metric values, but their completion time will be longer.""")


    
####################### POSZCZEGÓLNE TORY #######################
for i in range(2, 9):
    with tabs[i]:
        tor_num = i - 1
        st.header(f"Tor {tor_num} – Analiza i Obraz | Track {tor_num} – Analysis and Image")

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

            st.subheader(f"📊 Podstawowe statystyki | Basic stats")
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

        st.markdown("Dalej porównajmy rozkład metryk `smoothness` i `stair_ratio` dla gier ukończonych i nieukończonych. \nLet's further compare the distribution of the metrics `smoothness` and `stair_ratio` for completed")

        _, row4_2, row4_3, _ = st.columns([1, 3, 3, 1])
        with row4_2:
            st.markdown("**Gry ukończone**")
            st.pyplot(all_tracks_plots["hist_smoothness_true"])
            st.pyplot(all_tracks_plots["hist_stair_ratio_true"])
        with row4_3:
            st.markdown("**Gry nieukończone**")
            st.pyplot(all_tracks_plots["hist_smoothness_false"])
            st.pyplot(all_tracks_plots["hist_stair_ratio_false"])

        st.markdown("""Dotakowo spójrzmy na rozkład metryk w stosunku do ukończenia toru.  
                    Additionally, let's look at the distribution of metrics in relation to track completion.""")

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
        
        _, col_s13, col_s14, _ = st.columns([1, 8, 4, 1])
        with col_s13:
            st.pyplot(best_strategy(tor_num))
        with col_s14:
            if calculate_toggle:
                routes_plot = generate_route_plots(tor_num)
            else:
                routes_plot = get_route_plots(tor_num)
            st.image(routes_plot)

        _, col_s15, col_s16, _ = st.columns([1, 8, 4, 1])
        with col_s15:
            st.markdown(
                "Powyższy wykres wizualizuje trasę podzieloną na odcinki, gdzie kolor odcinka odpowiada najskuteczniejszej strategii"
                " na tym właśnie fragmencie. Najlepsza strategia jest wybrana na podstawie metryki trajectory_strategy_bias. "
                "Im mniejsza wartość tej metryki, tym lepsza strategia dla danego fragmentu toru.\n\n"
                "This plot visualizes the track divided into segments, where the color of each segment corresponds to the most effective strategy"
                " for that particular part. The best strategy is selected based on the trajectory_strategy_bias metric."
                " The lower the value of this metric, the better the strategy for a given segment of the track.\n"
            )
        with col_s16:
            st.markdown("""Powyższy wykres przedstawia wszystkie trasy (ukończone w przynajmniej 25%), które zostały wykonane przez graczy.  
                        The above plot shows all the routes (completed at least 25%) that players have taken.""")


        _, col_s10, col_s11, _ = st.columns([1, 4, 4, 1])
        with col_s10:
            st.pyplot(correlation_analysis_plots["spearman_correlation_matrix_completed"])
        with col_s11:
            st.pyplot(correlation_analysis_plots["spearman_correlation_matrix_not_completed"])



