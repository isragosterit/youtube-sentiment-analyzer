# youtube-sentiment-analysis
Youtube Sentiment Analyzer

A web application that performs sentiment analysis on YouTube comments using the YouTube Data API and TextBlob.

## Installation
1. Clone the repository:
git clone https://github.com/isragosterit/youtube-sentiment-analysis

2. Install the required dependencies:
Flask==2.0.2
google-api-python-client==2.19.1
google-auth==2.3.0
textblob==0.15.3

3. Obtain a YouTube Data API key from the Google Cloud Console.

4. Insert your API key in the code (`app.py`) by replacing the value of the `ENTER_YOUR_DEVELOPER_KEY` variable.

## Usage
1. Run the application:

2. Access the web application in your browser at `http://localhost:5000`.

3. Enter a valid YouTube video ID in the input field and click the "Analyze" button.

4. The tool will analyze the sentiment of the comments for the specified video and display the results.

## Screenshots

![screenshot](https://github.com/isragosterit/youtube-sentiment-analysis/assets/82115269/56a0a3d8-5a74-4a21-ba7f-a56e6753d4cd)

## Limitations
- The YouTube Data API has rate limits for API requests, so there may be restrictions on the number of comments that can be analyzed within a certain timeframe.
- The sentiment analysis is based on TextBlob's sentiment scoring, which may not capture the nuances of certain languages or specific contexts.
