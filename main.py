from flask import Flask, render_template, request, redirect, url_for
import csv, os
from textblob import TextBlob
import matplotlib.pyplot as plt

app = Flask(__name__)
CSV_FILE = "data/playlist.csv"

def init_csv():
    os.makedirs("data", exist_ok=True)
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Song", "Lyrics", "Mood"])

def analyze_mood(lyrics):
    polarity = TextBlob(lyrics).sentiment.polarity
    if polarity > 0.2:
        return "happy"
    elif polarity < -0.2:
        return "sad"
    else:
        return "neutral"

def log_song(song, lyrics, mood):
    with open(CSV_FILE, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([song, lyrics[:30] + "...", mood])

def get_stats():
    moods = {"happy": 0, "sad": 0, "neutral": 0}
    with open(CSV_FILE, "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            moods[row["Mood"]] += 1

    if sum(moods.values()) == 0:
        return None

    # Pie chart
    plt.pie(moods.values(), labels=moods.keys(), autopct="%1.1f%%")
    plt.title("Playlist Mood Distribution")
    plt.savefig("static/sample.png")
    plt.close()

    return moods

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/add", methods=["POST"])
def add_song():
    song = request.form.get("song")
    lyrics = request.form.get("lyrics")
    mood = analyze_mood(lyrics)
    log_song(song, lyrics, mood)
    return redirect(url_for("stats"))

@app.route("/stats")
def stats():
    stats_data = get_stats()
    return render_template("stats.html", stats=stats_data)

if __name__ == "__main__":
    init_csv()
    app.run(debug=True)
