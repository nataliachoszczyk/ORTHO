import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
import pickle

# @st.cache_data
def generate_metrics_plots(tor_num):
    data = pd.read_json(f"data/filtered_records_{tor_num}_metrics.json", lines=True)
    smoothnesses = data['smoothness']
    stair_ratios = data['stair_ratio']


    plots = {}

    # Smoothness histogram
    fig1, ax1 = plt.subplots()
    sns.histplot(smoothnesses, bins=30, kde=True, ax=ax1, color='#f5dd09')
    ax1.set_title('Rozkład smoothness')
    ax1.set_xlabel('Smoothness')
    ax1.set_ylabel('Liczba wystąpień')
    plots["hist_smoothness"] = fig1

    # Stair ratio histogram
    fig2, ax2 = plt.subplots()
    sns.histplot(stair_ratios, bins=30, kde=True, ax=ax2, color='#f5dd09')
    ax2.set_title('Rozkład stair ratio')
    ax2.set_xlabel('Stair Ratio')
    ax2.set_ylabel('Liczba wystąpień')
    plots["hist_stair_ratio"] = fig2

    # Scatter plot: stair ratio vs smoothness
    fig3, ax3 = plt.subplots()
    sns.scatterplot(x=smoothnesses, y=stair_ratios, ax=ax3, color='#f5dd09')
    ax3.set_title('Stair Ratio vs Smoothness')
    ax3.set_xlabel('Smoothness')
    ax3.set_ylabel('Stair Ratio')
    plots["scatter_plot"] = fig3

    # Completed games data
    completed_games = data[data['track_Completed'] == True]
    completed_smoothnesses = completed_games['smoothness']
    completed_stair_ratios = completed_games['stair_ratio']
    completed_times = completed_games['track_Time'] / 60  # to minutes
    completed_times = completed_times.round(2)

    # Smoothness vs time
    fig4, ax4 = plt.subplots()
    sns.scatterplot(x=completed_times, y=completed_smoothnesses, ax=ax4, color='#f5dd09')
    ax4.set_title('Smoothness vs Time')
    ax4.set_xlabel('Smoothness')
    ax4.set_ylabel('Czas (min)')
    plots["smoothness_time_plot"] = fig4

    # Stair ratio vs time
    fig5, ax5 = plt.subplots()
    sns.scatterplot(x=completed_times, y=completed_stair_ratios, ax=ax5, color='#f5dd09')
    ax5.set_title('Stair Ratio vs Time')
    ax5.set_xlabel('Stair Ratio')
    ax5.set_ylabel('Czas (min)')
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