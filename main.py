import pandas as pd
import matplotlib.pyplot as plt


def load_csv(filepath):
    return pd.read_csv(filepath)


def top_music(df, column_name, top_n=50):
    return df[column_name].value_counts().head(top_n)


def daily_counts(df):
    daily_counts = (
        df["Day of Week"]
        .value_counts()
        .reindex(
            [
                "Monday",
                "Tuesday",
                "Wednesday",
                "Thursday",
                "Friday",
                "Saturday",
                "Sunday",
            ]
        )
    )
    return daily_counts


def add_datetime_columns(df):
    df["Listened At"] = pd.to_datetime(df["Listened At"], format="%d %b %Y %H:%M")
    df["YearMonth"] = df["Listened At"].dt.to_period("M")
    df["Day of Week"] = df["Listened At"].dt.dayofweek.map(
        {
            0: "Monday",
            1: "Tuesday",
            2: "Wednesday",
            3: "Thursday",
            4: "Friday",
            5: "Saturday",
            6: "Sunday",
        }
    )


def count_songs_by_period(df, period_column):
    if period_column != "Day of Week":
        return df[period_column].value_counts().sort_values()
    else:
        return daily_counts(df)


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
    1) Top 50 Artists
    2) Top 50 Albums
    3) Top 50 Songs
    4) Number of Songs Per Month
    5) Number of Songs Per Week
    6) Number of Songs Per Hour
    7) Cumulative Plays per Artist over Time
    """)

    choice = int(input())

    if choice == 1:
        data = top_music(df, "Artist", top_n=50)
        plot_horizontal_bar_graph(data, "Plays", "Artist", "Top 50 Artists")

    elif choice == 2:
        data = top_music(df, "Album", top_n=50)
        plot_horizontal_bar_graph(data, "Plays", "Album", "Top 50 Albums")

    elif choice == 3:
        data = top_music(df, "Song", top_n=50)
        plot_horizontal_bar_graph(data, "Plays", "Song", "Top 50 Songs")

    elif choice == 4:
        data = count_songs_by_period(df, "YearMonth")
        plot_bar_graph(data, "Month", "Number of Plays", "Number of Songs Per Month")

    elif choice == 5:
        data = count_songs_by_period(df, "Day of Week")
        plot_bar_graph(data, "Week", "Number of Plays", "Number of Songs Per Week")

    elif choice == 6:
        data = count_songs_by_period(df, "Hour")
        plot_bar_graph(data, "Hour", "Number of Plays", "Number of Songs Per Hour")

    elif choice == 7:
        top_25_songs = top_music(df, "Song", top_n=25).index
        df = df.sort_values(by="Listened At")
        df["Cumulative Count"] = df.groupby("Song").cumcount() + 1
        plot_cumulative_trend(df, top_25_songs)

    else:
        print("Wrong Choice. Rerun the Program")


if __name__ == "__main__":
    main()
