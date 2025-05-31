import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import pickle


# @st.cache_data
def generate_metrics_plots(tor_num, completed=True):
    data = pd.read_json(f"data/filtered_records_{tor_num}_metrics.json", lines=True)
    smoothnesses = data['smoothness']
    stair_ratios = data['stair_ratio']

    plots = {}

    # Completed games data
    completed_games = data[data['track_Completed'] == True]
    completed_smoothnesses = completed_games['smoothness']
    completed_stair_ratios = completed_games['stair_ratio']
    completed_times = completed_games['track_Time'] /1000 # to minutes
    completed_times = completed_times.round(2)

    if completed:
        hist_smoothnesses = completed_smoothnesses
        hist_stair_ratios = completed_stair_ratios
    else:
        filtered = data[data['track_Completion_percent'] >= 0.25]
        hist_smoothnesses = filtered['smoothness']
        hist_stair_ratios = filtered['stair_ratio']

    # Smoothness histogram
    fig1, ax1 = plt.subplots()
    sns.histplot(hist_smoothnesses, bins=30, kde=True, ax=ax1, color='#f5dd09')
    ax1.set_title('Rozkład smoothness')
    ax1.set_xlabel('Smoothness')
    ax1.set_ylabel('Liczba wystąpień')
    plots["hist_smoothness"] = fig1

    # Stair ratio histogram
    fig2, ax2 = plt.subplots()
    sns.histplot(hist_stair_ratios, bins=30, kde=True, ax=ax2, color='#f5dd09')
    ax2.set_title('Rozkład stair ratio')
    ax2.set_xlabel('Stair Ratio')
    ax2.set_ylabel('Liczba wystąpień')
    plots["hist_stair_ratio"] = fig2

    # Scatter plot: stair ratio vs smoothness
    fig3, ax3 = plt.subplots()
    sns.scatterplot(x=completed_smoothnesses, y=completed_stair_ratios, ax=ax3, color='#f5dd09')
    ax3.set_title('Stair Ratio vs Smoothness')
    ax3.set_xlabel('Smoothness')
    ax3.set_ylabel('Stair Ratio')
    plots["scatter_plot"] = fig3

    # Smoothness vs time
    fig4, ax4 = plt.subplots()
    sns.scatterplot(x=completed_times, y=completed_smoothnesses, ax=ax4, color='#f5dd09')
    ax4.set_title('Smoothness vs Time')
    ax4.set_xlabel('Czas (s)')
    ax4.set_ylabel('Smoothness')
    plots["smoothness_time_plot"] = fig4

    # Stair ratio vs time
    fig5, ax5 = plt.subplots()
    sns.scatterplot(x=completed_times, y=completed_stair_ratios, ax=ax5, color='#f5dd09')
    ax5.set_title('Stair Ratio vs Time')
    ax5.set_xlabel('Czas (s)')
    ax5.set_ylabel('Stair Ratio')
    plots["stair_ratio_time_plot"] = fig5


    path = "app_plots/" + str(tor_num) + "_metrics_plots.pkl"
    with open(path, 'wb') as f:
        pickle.dump(plots, f)
    return plots



def get_metrics_plots(tor_num):
    path = "app_plots/" + str(tor_num) + "_metrics_plots.pkl"
    with open(path, 'rb') as f:
        plots = pickle.load(f)
    return plots

def generate_route_plots(tor_num):
    data = pd.read_json(f"data/filtered_records_{tor_num}_metrics.json", lines=True)
    data = data[data["track_Completion_percent"] >= 0.25]

    num_tracks = len(data)
    alpha = min(1.0, 35 / num_tracks)

    fig, ax = plt.subplots(figsize=(6, 6))

    for _, row in data.iterrows():
        points_dict = row['Points']
        cols = points_dict['columns']
        points_data = points_dict['data']

        points_df = pd.DataFrame(points_data, columns=cols)
        ax.plot(points_df['X'], points_df['Y'], alpha=alpha, color="#f5b209", linewidth=0.5)

    ax.set_title("Najczęstsze ścieżki ruchu (zagęszczenie torów)")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.grid(True)
    ax.set_aspect('equal')


    # Save as PNG image (not pickle!)
    path = f"app_plots/route_plots_{tor_num}.png"
    fig.savefig(path, dpi=300, bbox_inches='tight')

    plt.close(fig)  # Close the figure to free memory if used in a loop

    return fig  # or return fig if needed for display

def get_route_plots(tor_num):
    path = f"app_plots/route_plots_{tor_num}.png"
    with open(path, 'rb') as f:
        plot= pickle.load(f)
    return plot

def generate_all_tracks_plots():
    data_path = "data/filtered_records_1_to_7_noXY_metrics.json"
    data = pd.read_json(data_path, lines=True)
    plots = {}

    # Podział danych
    completed = data[data['track_Completed'] == True]
    not_completed = data[(data['track_Completed'] == False) & (data['track_Completion_percent'] >= 0.25)]

    # Histogram smoothness - ukończone
    fig1, ax1 = plt.subplots()
    sns.histplot(completed['smoothness'], bins=30, kde=True, ax=ax1, color='#f5dd09')
    ax1.set_title('Rozkład smoothness (ukończone)')
    ax1.set_xlabel('Smoothness')
    ax1.set_ylabel('Liczba wystąpień')
    plots["hist_smoothness_true"] = fig1

    # Histogram smoothness - nieukończone
    fig2, ax2 = plt.subplots()
    sns.histplot(not_completed['smoothness'], bins=30, kde=True, ax=ax2, color='#f5dd09')
    ax2.set_title('Rozkład smoothness (nieukończone)')
    ax2.set_xlabel('Smoothness')
    ax2.set_ylabel('Liczba wystąpień')
    plots["hist_smoothness_false"] = fig2

    # Histogram stair_ratio - ukończone
    fig3, ax3 = plt.subplots()
    sns.histplot(completed['stair_ratio'], bins=30, kde=True, ax=ax3, color='#f5dd09')
    ax3.set_title('Rozkład stair ratio (ukończone)')
    ax3.set_xlabel('Stair Ratio')
    ax3.set_ylabel('Liczba wystąpień')
    plots["hist_stair_ratio_true"] = fig3

    # Histogram stair_ratio - nieukończone
    fig4, ax4 = plt.subplots()
    sns.histplot(not_completed['stair_ratio'], bins=30, kde=True, ax=ax4, color='#f5dd09')
    ax4.set_title('Rozkład stair ratio (nieukończone)')
    ax4.set_xlabel('Stair Ratio')
    ax4.set_ylabel('Liczba wystąpień')
    plots["hist_stair_ratio_false"] = fig4

    # Scatter plot smoothness vs stair_ratio z kolorem wg track_Completed
    fig5, ax5 = plt.subplots()
    sns.scatterplot(
        data=data,
        x="smoothness",
        y="stair_ratio",
        hue="track_Completed",
        palette={True: '#f5dd09', False: '#999999'},
        ax=ax5
    )
    ax5.set_title('Smoothness vs Stair Ratio (kolor: ukończenie)')
    ax5.set_xlabel('Smoothness')
    ax5.set_ylabel('Stair Ratio')
    ax5.legend(title="Ukończono")
    plots["scatter_smoothness_vs_stair_ratio_colored"] = fig5

    # Scatter plot smoothness vs stair_ratio (kolor wg track_Completion_percent)
    fig6, ax6 = plt.subplots()
    scatter = ax6.scatter(
        data["smoothness"],
        data["stair_ratio"],
        c=data["track_Completion_percent"],
        cmap="YlOrRd",
        s=50,
        edgecolor='k'
    )
    ax6.set_title('Smoothness vs Stair Ratio (kolor: Completion %)')
    ax6.set_xlabel('Smoothness')
    ax6.set_ylabel('Stair Ratio')
    cbar = fig6.colorbar(scatter, ax=ax6)
    cbar.set_label('Completion Percent')
    plots["scatter_smoothness_vs_stair_ratio_gradient"] = fig6

    # Zapis wykresów
    path = "app_plots/all_tracks_metrics_plots.pkl"
    with open(path, 'wb') as f:
        pickle.dump(plots, f)

    return plots

def get_all_tracks_plots():
    path = "app_plots/all_tracks_metrics_plots.pkl"
    with open(path, 'rb') as f:
        plots = pickle.load(f)
    return plots

def generate_correlation_analysis_plots(track_num):
    # Load data
    path_to_data = f"data/filtered_records_{track_num}_metrics.json"
    data = pd.read_json(path_to_data, lines=True)

    # Prepare numerical columns
    data['track_Completed_numeric'] = data['track_Completed'].astype(int)
    data['track_Time_seconds'] = data['track_Time'] / 1000  # ms -> s

    numeric_cols_completed = ['smoothness', 'stair_ratio', 'track_Time_seconds', 'track_Completed_numeric']
    numeric_cols_not_completed = ['smoothness', 'stair_ratio', 'track_Time_seconds', 'track_Completion_percent', 'track_Completed_numeric']
    corr_data_completed = data[numeric_cols_completed]
    corr_data_not_completed = data[numeric_cols_not_completed]
    corr_data_completed = corr_data_completed[corr_data_completed['track_Completed_numeric'] == 1].drop(columns=['track_Completed_numeric'])
    corr_data_not_completed = corr_data_not_completed[
    (corr_data_not_completed['track_Completed_numeric'] == 0) &
    (corr_data_not_completed['track_Completion_percent'] >= 0.25)
].drop(columns=['track_Completed_numeric'])

    plots = {}

    label_map = {
    'smoothness': 'Smoothness',
    'stair_ratio': 'Stair Ratio',
    'track_Time_seconds': 'Time (s)',
    'track_Completion_percent': 'Completion rate',
    }

    
    # Spearman correlation matrix - completed
    spearman_corr = corr_data_completed.corr(method='spearman')
    display_labels = [label_map.get(col, col) for col in spearman_corr.columns]
    fig_spearman, ax_spearman = plt.subplots(figsize=(8, 6))
    sns.heatmap(spearman_corr, annot=True, cmap='YlOrRd', fmt=".2f", ax=ax_spearman, xticklabels=display_labels,
    yticklabels=display_labels)
    ax_spearman.set_xticklabels(ax_spearman.get_xticklabels(), rotation=0, ha='center')
    ax_spearman.set_yticklabels(ax_spearman.get_yticklabels(), rotation=90, va='center')
    
    ax_spearman.set_title("Macierz korelacji (Spearmana) - ukończone")
    plots["spearman_correlation_matrix_completed"] = fig_spearman

    # Spearman correlation matrix - not completed
    spearman_corr = corr_data_not_completed.corr(method='spearman')
    display_labels = [label_map.get(col, col) for col in spearman_corr.columns]
    fig_spearman, ax_spearman = plt.subplots(figsize=(8, 6))
    sns.heatmap(spearman_corr, annot=True, cmap='YlOrRd', fmt=".2f", ax=ax_spearman, xticklabels=display_labels,
    yticklabels=display_labels)
    ax_spearman.set_xticklabels(ax_spearman.get_xticklabels(), rotation=0, ha='center')
    ax_spearman.set_yticklabels(ax_spearman.get_yticklabels(), rotation=90, va='center')
    ax_spearman.set_title("Macierz korelacji (Spearmana) - nieukończone")
    plots["spearman_correlation_matrix_not_completed"] = fig_spearman

    # Boxplot smoothness vs track_Completed
    fig_smooth, ax_smooth = plt.subplots()
    sns.boxplot(x='track_Completed', y='smoothness', data=data, ax=ax_smooth,  boxprops=dict(facecolor='#f5dd09', color='#f5dd09'))
    ax_smooth.set_yscale('log')
    ax_smooth.set_title("Smoothness vs track_Completed (skala logarytmiczna)")
    plots["boxplot_smoothness"] = fig_smooth

    # Boxplot stair_ratio vs track_Completed
    fig_stair, ax_stair = plt.subplots()
    sns.boxplot(x='track_Completed', y='stair_ratio', data=data, ax=ax_stair,  boxprops=dict(facecolor='#f5dd09', color='#f5dd09'))
    ax_stair.set_title("Stair Ratio vs track_Completed")
    plots["boxplot_stair_ratio"] = fig_stair

    # Boxplot time vs track_Completed
    fig_time, ax_time = plt.subplots()
    sns.boxplot(x='track_Completed', y='track_Time_seconds', data=data, ax=ax_time,  boxprops=dict(facecolor='#f5dd09', color='#f5dd09'))
    ax_time.set_yscale('log')
    ax_time.set_title("Time (sekundy) vs track_Completed (skala logarytmiczna)")
    plots["boxplot_time"] = fig_time

    # Save all plots
    output_path = f"app_plots/correlation_analysis_plots_{track_num}.pkl"
    with open(output_path, 'wb') as f:
        pickle.dump(plots, f)

    return plots



def get_correlation_analysis_plots(track_num):
    with open(f"app_plots/correlation_analysis_plots_{track_num}.pkl", 'rb') as f:
        plots = pickle.load(f)
    return plots