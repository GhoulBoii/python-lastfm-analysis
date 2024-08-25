import pandas as pd
import matplotlib.pyplot as plt

csv = None
with open("data/ghoulboii.csv") as file:
    csv = pd.read_csv(file)

print("""What do you want?
1) Top 50 Artists
2) Top 50 Albums
3) Top 50 Songs
4) Number of Songs Per Month
5) Number of Songs Per Week
6) Number of Songs Per Hour
7) Cumulative Plays per Artist over Time
""")
# inp = int(input())


# Get Top Songs/Artists/Albums
def top_music(csv, column_name):
    return csv[column_name].value_counts().sort_values(ascending=False)


def count_songs_alltime(csv, column_name):
    csv["Listened At"] = pd.to_datetime(csv["Listened At"], format="%d %b %Y %H:%M")
    csv["YearMonth"] = csv["Listened At"].dt.to_period("M")
    csv["YearWeek"] = csv["Listened At"].dt.to_period("W")
    return csv["YearWeek"].value_counts().sort_index()


def count_songs_week(csv):
    csv["Listened At"] = pd.to_datetime(csv["Listened At"], format="%d %b %Y %H:%M")
    csv["Day of Week"] = csv["Listened At"].dt.dayofweek
    csv["Day of Week"] = csv["Day of Week"].map(
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

    daily_counts = (
        csv["Day of Week"]
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


def count_songs_hour(csv):
    csv["Listened At"] = pd.to_datetime(csv["Listened At"], format="%d %b %Y %H:%M")
    csv["Hour"] = csv["Listened At"].dt.hour
    return csv["Hour"].value_counts().sort_index()


def plot_top_music_bargraph(csv, column_name):
    csv[25::-1].plot(kind="barh")
    plt.xlabel(column_name)
    plt.ylabel("Number of Plays")
    plt.title(f"Top 25 Most Played {column_name}")
    plt.show()


def plot_count_songs_bargraph(csv, column_name):
    csv.plot(kind="bar")
    plt.ylabel("Number of Plays")
    plt.title(f"Number of songs played per {column_name}")
    plt.show()


def cum_songs(csv):
    sorted_csv = top_music(csv, column_name="Song")
    csv["Listened At"] = pd.to_datetime(csv["Listened At"], format="%d %b %Y %H:%M")
    csv = csv.sort_values(by="Listened At")
    csv["Cumulative Count"] = csv.groupby("Song").cumcount() + 1
    top_25_songs = sorted_csv.index[:25]
    for song in top_25_songs:
        song_data = csv[csv["Song"] == song]
        plt.plot(song_data["Listened At"], song_data["Cumulative Count"], label=song)
    plt.title("Song Trends Over Time")
    plt.xlabel("Date")
    plt.ylabel("Cumulative Count")
    plt.xticks(rotation=45)
    plt.legend(title="Songs", bbox_to_anchor=(1.05, 1), loc="upper left")
    plt.show()


# sorted_csv = top_music(csv, column_name="Song")
# print(sorted_csv)
# plot_top_music_bargraph(sorted_csv, column_name="Song")

# sorted_csv = count_songs_time(csv, column_name="Week")
# plot_count_songs_bargraph(sorted_csv, column_name="Month")

# sorted_csv = count_songs_week(csv)
# plot_count_songs_bargraph(sorted_csv, column_name="Month")

# sorted_csv = count_songs_hour(csv)
# plot_count_songs_bargraph(sorted_csv, column_name="Hour")

cum_songs(csv)
