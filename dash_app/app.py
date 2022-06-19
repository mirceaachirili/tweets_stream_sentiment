from dash import Dash, Input, Output, callback, dash_table, dcc, html
from datetime import date, datetime
import dash_bootstrap_components as dbc
from mentions import mentions_layout, df
from sentiment import sentiment_layout

app = Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.LUX],
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}]
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
    dbc.Row(dbc.Col(html.H1('Twitter sentiment tracker',
            style={'textAlign': 'center'}), width=12)),
    html.Hr(),
    html.P('Select date range:'),
    html.Div([
        dcc.DatePickerRange(
            id='my-date-picker-range',
            min_date_allowed=date(2021, 7, 1),
            max_date_allowed=date.today(),
            initial_visible_month=date(2021, 7, 1),
            start_date=date(2021,7,17),
            end_date=date.today()
        )
        ]),
    dbc.Row(dbc.Col(app_tabs, width=12), className='mb-3'),
    html.Div(id='content', children=[])

])


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
        return 'Tab in developement'
    return html.P("This shouldn't be displayed for now...")


# Date range callback
# Filter datatable by date range
@app.callback(
    Output('tbl', 'data'),
    Input('my-date-picker-range', 'start_date'),
    Input('my-date-picker-range', 'end_date'))

def update_table(start_date, end_date):
    mask = (df['datetime'] > start_date) & (df['datetime'] <= end_date)
    return df[mask].to_dict('records')

# Dropdown callback
@app.callback(
    Output('tbl', 'page_size'),
    [Input('count-mentions', 'value')]
)

def table_count(no_results):
    if no_results == 5:
        return 5
    elif no_results == 10:
        return 10
    elif no_results == 15:
        return 15

if __name__ == '__main__':
    app.run_server(debug=True)






