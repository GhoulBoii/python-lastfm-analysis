import sys

import matplotlib.pyplot as plt
import pandas as pd


# Ask the user for input
print("🎉 Welcome to SpotPlot! 🎉")
print("By Kshamendra, Aaditya & Srikar ")
print("─" * 31)
print("Please select an option from the menu below:")
print("\n 1) Top 10 Songs")
print(" 2) Number of Songs Per Month")
print(" 3) Cumulative Plays per Artist over Time")
choice = int(input("\nEnter your choice (1-3): "))

# Defining vars
df = pd.read_csv(
    "data.csv", names=["Artist", "Album", "Song", "Listened At"]
)
xlabel = ""
ylabel = ""
title = ""


print("─" * 50)
print("🖨 Printing the DataFrame...\n")
print(df)
print("─" * 50)
# Formatting Listened At and adding months column
df["Listened At"] = pd.to_datetime(df["Listened At"], format="%d %b %Y %H:%M")
df["Months"] = df["Listened At"].dt.to_period("M")

if choice == 1:
    # Get top 10 songs
    print("\n🎵 You've chosen: Top 10 Songs!")
    data = df["Song"].value_counts().head(10)[::-1]
    data.plot(kind="barh")
    xlabel = "Plays"
    ylabel = "Songs"
    title = "Top 10 Songs"

elif choice == 2:
    # Get number of songs listened to per month
    print("\n📅 You've chosen: Number of Songs Per Month!")
    data = df["Months"].value_counts().sort_values()
    data.plot(kind="bar")
    ylabel = "Months"
    xlabel = "Plays"
    title = "Monthly Listening Activity"

elif choice == 3:
    # Getting top 25 songs to find cumulative count of
    print("\n📈 You've chosen: Cumulative Plays per Artist over Time!")
    data = df["Song"].value_counts().head(10).index

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

print("📊 Plottting the Graph...")
plt.savefig("graph2.png", bbox_inches="tight")
plt.show()

print("\n👋 Bye!")
