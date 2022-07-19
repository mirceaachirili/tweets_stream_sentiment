from dash import Dash, Input, Output, State, callback, dash_table, dcc, html
from datetime import date, datetime
import dash_bootstrap_components as dbc
from sentiment import clean_tweet, analyze_polarity, analyze_subjectivity
import pandas as pd
import tweepy
import credentials
import plotly.express as px
import plotly.graph_objects as go


app = Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.LUX],
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}]
                )
server = app.server

auth = tweepy.OAuthHandler(credentials.consumer_key, credentials.consumer_secret)
auth.set_access_token(credentials.access_token, credentials.access_token_secret)

api = tweepy.API(auth)


mentions_layout = html.Div(
    [
        dbc.Row(
                dbc.Col(
                    [
                        html.Label("Number of results per page to return"),
                        dcc.Dropdown(
                            id="count-mentions",
                            multi=False,
                            value=5,
                            options=[
                                {"label": "5", "value": 5},
                                {"label": "10", "value": 10},
                                {"label": "15", "value": 15},
                                {"label": "20", "value": 20},
                                {"label": "25", "value": 25},
                                {"label": "30", "value": 30}
                            ],
                            clearable=False,
                        ),
                    ],
                    width=3,
                )
		),
		html.Br(),
        dbc.Row(
            html.Div(id='table-content')
				)
		])

# Create graph container
sentiment_layout = html.Div([
    dcc.Graph(figure={}, id='bar-plot')]
)

other_layout = html.Div([
    dcc.Graph(figure={}, id='freq-plot')]
)

# Tabs layout
app_tabs = html.Div(
    [
        dbc.Tabs(
            [
                dbc.Tab(label='Mentions', tab_id='tab-mentions'),
                dbc.Tab(label='Sentiment', tab_id='tab-sentiment'),
                dbc.Tab(label='Other', tab_id='tab-other')
            ],
            id='tabs',
            active_tab='tab-mentions'
        )],
        className='mt-3')

# App layout
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1('Twitter sentiment tracker',
            style={'textAlign': 'center'}), width=12)]),
    html.Hr(),
    html.Label("Search keywords"),    
    dbc.Row(
        [
            dbc.Col(
                dcc.Input(
                id="input-handle",
                type="text",
                placeholder="Type here",
                value="twitter"
                ),
                width=3 
                ),
            dbc.Col(html.Button(
                id="hit-button",
                children="Submit",
                style={"background-color": "blue", "color": "white"},
                ))
            ],
        ),
    html.Br(),        
    dbc.Row(dbc.Col(app_tabs, width=12), className='mb-3'),
    html.Div(id='content', children=[]),
    dcc.Store(id='memory-df-filtered', storage_type='memory')
]
)


# Tabs callback
@app.callback(
    Output('content', 'children'),
    [Input('tabs', 'active_tab')]
)
def switch_tab(tab_chosen):
    if tab_chosen == 'tab-mentions':
        return mentions_layout
    elif tab_chosen == "tab-sentiment":
        return sentiment_layout
    elif tab_chosen == "tab-other":
        return other_layout
    return html.P("This shouldn't be displayed for now...")


# Get tweets and store in dataframe 

@app.callback(
    Output('memory-df-filtered', 'data'),
    [Input("hit-button", "n_clicks"),
    State('input-handle', 'value'),
    State('count-mentions', 'value')]
)

def get_table(nclicks, text, tweet_count):
    # Create query method
    tweets = tweepy.Cursor(api.search, q=text, lang='en').items(tweet_count)
    # Pull information from iterable cursor object
    tweets_list = [[tweet.user.screen_name, tweet.user.followers_count, tweet.text, tweet.created_at] for tweet in tweets]
    # Create dataframe for tweets_list
    tweets_df = pd.DataFrame(tweets_list, columns=['account', 'followers', 'text', 'created_at'])
        
    return tweets_df.to_json(date_format='iso', orient='split')


@app.callback(
    Output('table-content', 'children'),
    Input('memory-df-filtered', 'data')
)
def update_table(memory_df):
    df_filtered = pd.read_json(memory_df, orient='split')

    return dash_table.DataTable(
                    data=df_filtered.to_dict('records'),
                    columns=[{"name": i, "id": i} for i in df_filtered.columns], 
					# id='tbl', 
					style_data={
						'whiteSpace': 'normal',
						'height': 'auto',
						'lineHeight': '17px'
								}
        )


# Create dataframe containing the polarity and subjectivity of tweets
@app.callback(
    Output('bar-plot', 'figure'),
    Input('memory-df-filtered', 'data')
)

def update_graph(memory_df):
    df = pd.read_json(memory_df, orient='split')

    df['polarity'] = df['text'].apply(analyze_polarity)

    df_grouped = df.groupby('polarity').count().reset_index()

    df_grouped = df_grouped.rename(columns={
        'created_at': 'count'
    })

    
    # Create plotly graph
    
    fig = px.bar(df_grouped, x='polarity', y='count')


    fig.update_layout(
        title={'text': 'Polarity breakdown',
                'y':0.9,
                'x':0.5,
                'xanchor': 'center',
                'yanchor': 'top'},
        xaxis_title='Polarity', 
        yaxis_title='Count',
        xaxis = dict(
                tickmode = 'array',
                tickvals = [-1, 0, 1],
                ticktext = ['Negative', 'Neutral', 'Positive']
        )
    )
    
    return fig

@app.callback(
    Output('freq-plot', 'figure'),
    Input('memory-df-filtered', 'data')
)

def update_freq(memory_df):
    df = pd.read_json(memory_df, orient='split')

    from nltk.probability import FreqDist
    from utils import process_tweet

    b = process_tweet(' '.join(df['text']))
    freq_b = FreqDist(b)
    top_words = pd.DataFrame(freq_b.most_common(10),
                            columns=['Word', 'Frequency']).drop(0).reset_index(drop=True)
    

    fig = px.bar(top_words, x='Word', y='Frequency')
    
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)






