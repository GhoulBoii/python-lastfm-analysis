import pandas as pd
import matplotlib.pyplot as plt


def load_csv(filepath):
    return pd.read_csv(filepath)


def top_music(df, column_name, top_n=50):
    return df[column_name].value_counts().head(top_n)


def add_datetime_columns(df):
    df["Listened At"] = pd.to_datetime(df["Listened At"], format="%d %b %Y %H:%M")
    df["YearMonth"] = df["Listened At"].dt.to_period("M")


def count_songs_by_period(df, period_column):
    return df[period_column].value_counts().sort_values()


def plot_bar_graph(data, xlabel, ylabel, title):
    data.plot(kind="bar")
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.tight_layout()
    plt.show()


def plot_horizontal_bar_graph(data, xlabel, ylabel, title):
    data.plot(kind="barh")
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.tight_layout()
    plt.show()


def plot_cumulative_trend(df, top_songs):
    """Plot the cumulative plays over time for the top songs."""
    for song in top_songs:
        song_data = df[df["Song"] == song]
        plt.plot(song_data["Listened At"], song_data["Cumulative Count"], label=song)
    plt.title("Cumulative Song Trends Over Time")
    plt.xlabel("Date")
    plt.ylabel("Cumulative Count")
    plt.xticks(rotation=45)
    plt.legend(title="Songs", bbox_to_anchor=(1.05, 1), loc="upper left")
    plt.tight_layout()
    plt.show()


def main():
    # Load data
    df = load_csv("data/ghoulboii.csv")

    # Add necessary datetime columns
    add_datetime_columns(df)

    # Ask the user for input
    print("""What do you want?
    1) Top 50 Songs
    2) Number of Songs Per Month
    3) Cumulative Plays per Artist over Time
    """)

    choice = int(input())

    if choice == 1:
        data = top_music(df, "Song", top_n=50)
        plot_horizontal_bar_graph(data, "Plays", "Song", "Top 50 Songs")

    elif choice == 2:
        data = count_songs_by_period(df, "YearMonth")
        plot_bar_graph(data, "Month", "Number of Plays", "Number of Songs Per Month")

    elif choice == 3:
        top_25_songs = top_music(df, "Song", top_n=25).index
        df = df.sort_values(by="Listened At")
        df["Cumulative Count"] = df.groupby("Song").cumcount() + 1
        plot_cumulative_trend(df, top_25_songs)

    else:
        print("Wrong Choice. Rerun the Program")


if __name__ == "__main__":
    main()
