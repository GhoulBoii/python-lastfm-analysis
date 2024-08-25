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
inp = int(input())


# Get Top songs
def top_songs(csv):
    grouped_csv = csv.groupby(by="Song", as_index=False).size()
    sorted_csv = grouped_csv.sort_values(by="size", ascending=False)
    return sorted_csv


def top_artists(csv):
    grouped_csv = csv.groupby(by="Artist", as_index=False).size()
    sorted_csv = grouped_csv.sort_values(by="size", ascending=False)
    return sorted_csv


def top_albums(csv):
    grouped_csv = csv.groupby(by="Album", as_index=False).size()
    sorted_csv = grouped_csv.sort_values(by="size", ascending=False)
    return sorted_csv


def plot_bargraph(type, sorted_csv):
    plt.bar(sorted_csv[type][:50:], sorted_csv["size"][:50:])
    plt.xlabel(type)
    plt.ylabel("Number of Plays")
    plt.title(f"Top 50 Most Played {type}")


sorted_csv = top_artists(csv)
plot_bargraph("Artist", sorted_csv)

# Rotation needed since song names are not visible
plt.xticks(rotation=90)
plt.show()
