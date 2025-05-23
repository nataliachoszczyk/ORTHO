import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
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

def generate_all_tracks_plots():
    data_path = "data/filtered_records_1_to_7_metrics.json"
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

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import pickle
import numpy as np

def generate_correlation_analysis_plots():
    # Load data
    path_to_data = "data/filtered_records_1_to_7_metrics.json"
    data = pd.read_json(path_to_data, lines=True)

    # Prepare numerical columns
    data['track_Completed_numeric'] = data['track_Completed'].astype(int)
    data['track_Time_seconds'] = data['track_Time'] / 1000  # ms -> s

    numeric_cols = ['smoothness', 'stair_ratio', 'track_Time_seconds', 'track_Completion_percent', 'track_Completed_numeric']
    corr_data = data[numeric_cols]

    plots = {}

    # Pearson correlation matrix
    pearson_corr = corr_data.corr(method='pearson')
    fig_pearson, ax_pearson = plt.subplots(figsize=(8, 6))
    sns.heatmap(pearson_corr, annot=True, cmap='YlOrRd', fmt=".2f", ax=ax_pearson)
    ax_pearson.set_title("Macierz korelacji (Pearsona)")
    plots["pearson_correlation_matrix"] = fig_pearson

    # Spearman correlation matrix
    spearman_corr = corr_data.corr(method='spearman')
    fig_spearman, ax_spearman = plt.subplots(figsize=(8, 6))
    sns.heatmap(spearman_corr, annot=True, cmap='YlOrRd', fmt=".2f", ax=ax_spearman)
    ax_spearman.set_title("Macierz korelacji (Spearmana)")
    plots["spearman_correlation_matrix"] = fig_spearman

    # Boxplot smoothness vs track_Completed
    fig_smooth, ax_smooth = plt.subplots()
    sns.boxplot(x='track_Completed', y='smoothness', data=data, ax=ax_smooth, color='#f5dd09')
    ax_smooth.set_yscale('log')
    ax_smooth.set_title("Smoothness vs track_Completed (skala logarytmiczna)")
    plots["boxplot_smoothness"] = fig_smooth

    # Boxplot stair_ratio vs track_Completed
    fig_stair, ax_stair = plt.subplots()
    sns.boxplot(x='track_Completed', y='stair_ratio', data=data, ax=ax_stair, color='#f5dd09')
    ax_stair.set_title("Stair Ratio vs track_Completed")
    plots["boxplot_stair_ratio"] = fig_stair

    # Boxplot time vs track_Completed
    fig_time, ax_time = plt.subplots()
    sns.boxplot(x='track_Completed', y='track_Time_seconds', data=data, ax=ax_time, color='#f5dd09')
    ax_time.set_yscale('log')
    ax_time.set_title("Time (sekundy) vs track_Completed (skala logarytmiczna)")
    plots["boxplot_time"] = fig_time

    # Save all plots
    output_path = "app_plots/correlation_analysis_plots.pkl"
    with open(output_path, 'wb') as f:
        pickle.dump(plots, f)

    return plots



def get_correlation_analysis_plots():
    with open("app_plots/correlation_analysis_plots.pkl", 'rb') as f:
        plots = pickle.load(f)
    return plots