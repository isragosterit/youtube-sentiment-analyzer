from flask import Flask, render_template, request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from textblob import TextBlob

DEVELOPER_KEY = "AIzaSyBjXI7DHqtD3qyvJt6sxvegSIzVCkYKxos"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

app = Flask(__name__, template_folder='templates')

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        video_id = request.form["video_id"]
        max_results = 100

        try:
            youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)
            video = youtube.videos().list(
                part="snippet",
                id=video_id
            ).execute()
            if not video["items"]:
                error_message = "Video not found. Please provide a valid YouTube video ID."
                return render_template("index.html", error_message=error_message)
            video_title = video["items"][0]["snippet"]["title"]

            comments = []
            results = youtube.commentThreads().list(
                part="snippet",
                videoId=video_id,
                textFormat="plainText",
                maxResults=max_results
            ).execute()
            while results:
                for item in results["items"]:
                    comment = item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
                    comments.append(comment)
                if "nextPageToken" in results:
                    results = youtube.commentThreads().list(
                        part="snippet",
                        videoId=video_id,
                        textFormat="plainText",
                        maxResults=max_results,
                        pageToken=results["nextPageToken"]
                    ).execute()
                else:
                    break
        except HttpError as e:
            if e.resp.status == 400:
                error_message = "Invalid video ID. Please provide a valid YouTube video ID."
                return render_template("index.html", error_message=error_message)
            else:
                error_message = "An HTTP error occurred:\n%s" % e.content
                return render_template("index.html", error_message=error_message)

        def analyze_sentiment(comment):
            testimonial = TextBlob(comment)
            return testimonial.sentiment.polarity

        positive_comments = []
        negative_comments = []
        neutral_comments = []
        for comment in comments:
            sentiment_score = analyze_sentiment(comment)
            if sentiment_score > 0:
                positive_comments.append(comment)
            elif sentiment_score < 0:
                negative_comments.append(comment)
            else:
                neutral_comments.append(comment)

        num_comments = len(comments)
        num_positive = len(positive_comments)
        num_negative = len(negative_comments)
        num_neutral = len(neutral_comments)
        percent_positive = round(100 * num_positive / num_comments, 1)
        percent_negative = round(100 * num_negative / num_comments, 1)
        percent_neutral = round(100 * num_neutral / num_comments, 1)

        return render_template("index.html", comments=comments, video_id=video_id, video_title=video_title,
            num_comments=num_comments, num_positive=num_positive, percent_positive=percent_positive,
            num_negative=num_negative, percent_negative=percent_negative, num_neutral=num_neutral,
            percent_neutral=percent_neutral)

    else:
        return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
