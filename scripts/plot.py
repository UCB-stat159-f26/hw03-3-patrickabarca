import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


# formatting axes
def format_axes(ax, player_df):
    ax.set_frame_on(False)

    # plotting x-axis on top
    ax.tick_params(top=True, labeltop=True, bottom=False, labelbottom=False)

    # y-axis labels
    age_diff = ['-20', '-10', 'Same age', '+10', '+20 years']
    plt.yticks(np.arange(-20, 30, 10), age_diff, color='grey')

    # adjusting x-axis to player's career
    start_age = int(player_df['age'].min()) // 2 * 2
    end_age = int(player_df['age'].max()) + 3
    plt.xticks(np.arange(start_age, end_age, 2), color='grey')

    plt.tick_params(axis='y', length=0)
    plt.tick_params(axis='x', color='gainsboro')
    plt.ylabel('')
    plt.xlabel('')


# formatting plot
def format_plot(ax):
    plt.grid(axis='both', linestyle='-', linewidth=1, color='gainsboro')
    plt.axhline(y=0, linestyle='-', linewidth=0.8, color='darkgrey')

    # legend
    ax.legend(loc=[0.3, 1.07], ncols=2, frameon=False,
              labels=['Matches won', 'Match lost'])

    # title
    plt.title("Professional Matches by Age",
              fontsize=12, loc='center', y=1.12, weight='bold')


# Main plotting function
def plot_career(player_df):
    fig, ax = plt.subplots(figsize=(11, 6))

    sns.scatterplot(data=player_df, x='age',
                    y='age_difference',
                    hue='wl', hue_order=['W', 'L'],
                    palette={"W": "deepskyblue", "L": "purple"},
                    alpha=0.7, s=20, ax=ax)

    format_axes(ax, player_df)
    format_plot(ax)

    plt.show()