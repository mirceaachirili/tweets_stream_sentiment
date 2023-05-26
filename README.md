# Twitter Sentiment Tracker

This application streams real-time Twitter data, performs sentiment analysis, and displays the results in an interactive dashboard. It uses Python, Dash, Tweepy, Textblob, NLTK, and Plotly, among other libraries.

## Features

- Stream real-time Twitter data based on user-defined keywords
- Perform sentiment analysis on the streamed data
- Display the results in an interactive dashboard with multiple tabs
- Provide a breakdown of tweet polarity (negative, neutral, positive)
- Show the frequency of top words in the tweets

## Setup

1. Clone the repository
2. Install the required Python packages: `pip install -r requirements.txt`
3. Set up your Twitter API credentials in a `credentials.py` file
4. Run the application: `python dash_app/app.py`

## Usage

1. Enter your search keywords in the input field
2. Click "Submit" to start streaming and analyzing tweets
3. Navigate between the tabs to view different analytics

## Note

This project was completed when Twitter offered free API access. Please ensure you have the necessary access before running the application.

## Demo

A demo of the application can be found [here](https://tw-mnt.alexmircea.dev/).

## License

This project is licensed under the terms of the MIT license.
