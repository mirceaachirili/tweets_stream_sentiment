from textblob import TextBlob
import re
import pandas as pd
from dash import dcc, html

def clean_tweet(tweet):
    # Clean text for TextBlob
    return ' '.join(re.sub(r'''(@[A-Za-z0-9_]+)|     # Remove mentions that start with @
                                ([^0-9A-Za-z \t])    # Remove non-alphanumeric (except space and tab) characters
                                |(\w+:\/\/\S+)''',   # Remove web links
                                " ", tweet).split())
    
def analyze_polarity(tweet):
    '''
    Analyze polarity. Returns 1 for positive, 0 for neutral and -1 for negative.
    '''
    analysis = TextBlob(clean_tweet(tweet))

    if analysis.sentiment.polarity > 0:
        return 1
    elif analysis.sentiment.polarity == 0:
        return 0
    else:
        return -1

def analyze_subjectivity(tweet):
    '''
    Subjectivity analizer. Returns 1 if tweet is subjective or 0 if tweet is objective
    '''
    analysis = TextBlob(clean_tweet(tweet))
    if analysis.sentiment.subjectivity >= 0.5:
        return 1
    else:
        return 0


# # Create dataframe containing the polarity and subjectivity of tweets
# @app.callback(
#     Output('scatter-plot', 'figure'),
#     Input('memory-df-filtered', 'data')
# )

# def update_graph(memory_df):
#     df_updated = pd.read_json(memory_df, orient='split')

#     tweets = df_updated.loc[:, ['tweet', 'datetime']]
#     tweets['polarity'] = tweets['tweet'].apply(analyze_polarity)

#     # Group tweets count by time and polarity
#     tweets_grouped = tweets.groupby([pd.Grouper(key='datetime', freq='2h'), 'polarity']) \
#                             .count().unstack(fill_value=0).stack().reset_index()
#     tweets_grouped = tweets_grouped.rename(columns={
#         'datetime': 'Time in UTC',
#         'tweet': 'Number of mentions'
#     })

#     # Prepare time series data
#     time_series = tweets_grouped['Time in UTC'][tweets_grouped['polarity'] == 0].reset_index(drop=True)

#     negative_polarity = tweets_grouped['Number of mentions'][tweets_grouped['polarity'] == -1].reset_index(drop=True)
#     neutral_polarity = tweets_grouped['Number of mentions'][tweets_grouped['polarity'] == 0].reset_index(drop=True)
#     positive_polarity = tweets_grouped['Number of mentions'][tweets_grouped['polarity'] == 1].reset_index(drop=True)

#     # Create plotly graph
#     import plotly.express as px
#     import plotly.graph_objects as go
#     fig = go.Figure()

#     fig.add_trace(go.Scatter(x=time_series, y=negative_polarity, mode='lines+markers', name='negative'))
#     fig.add_trace(go.Scatter(x=time_series, y=neutral_polarity, mode='lines+markers', name='neutral'))
#     fig.add_trace(go.Scatter(x=time_series, y=positive_polarity, mode='lines+markers', name='positive'))

#     fig.update_layout(title={'text': 'Twitter Sentiment Tracker',
#                             'y':0.9,
#                             'x':0.5,
#                             'xanchor': 'center',
#                             'yanchor': 'top'},
#                     xaxis_title='Time', yaxis_title='Number of mentions')

#     return fig


# # Create graph container
# sentiment_layout = html.Div([
#     dcc.Graph(figure={}, id='scatter-plot')]
# )