import pandas as pd
import matplotlib.pyplot as plt
import sys

# Ask the user for input
print("""What do you want?
1) Top 50 Songs
2) Number of Songs Per Month
3) Cumulative Plays per Artist over Time
""")
choice = int(input())

# Defining vars
df = pd.read_csv("data/ghoulboii.csv")
xlabel = ""
ylabel = ""
title = ""

# Formatting Listened At and adding months column
df["Listened At"] = pd.to_datetime(df["Listened At"], format="%d %b %Y %H:%M")
df["Months"] = df["Listened At"].dt.to_period("M")

if choice == 1:
    # Get top 50 songs
    data = df["Song"].value_counts().head(50)
    data.plot(kind="barh")
    xlabel = "Plays"
    ylabel = "Songs"
    title = "Top 50 Songs"

elif choice == 2:
    # Get number of songs listened to per month
    data = df["Months"].value_counts().sort_values()
    data.plot(kind="bar")
    ylabel = "Months"
    xlabel = "Plays"
    title = "Monthly Listening Activity"

elif choice == 3:
    # Getting top 25 songs to find cumulative count of
    data = df["Song"].value_counts().head(25).index

    df = df.sort_values(by="Listened At")
    df["Cumulative Count"] = df.groupby("Song").cumcount() + 1
    for song in data:
        song_data = df[df["Song"] == song]
        plt.plot(song_data["Listened At"], song_data["Cumulative Count"], label=song)
    title = "Cumulative Song Trends Over Time"
    xlabel = "Time"
    ylabel = "Cumulative Count"
    plt.xticks(rotation=45)
    plt.legend(title="Songs", bbox_to_anchor=(1.05, 1), loc="upper left")
else:
    print("Wrong Choice. Rerun the Program")
    sys.exit()

# Output graph
plt.title(title)
plt.xlabel(xlabel)
plt.ylabel(ylabel)
plt.tight_layout()
plt.show()
