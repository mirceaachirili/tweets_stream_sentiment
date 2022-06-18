from dash import Dash, Input, Output, callback, dash_table, dcc, html
from datetime import date
import pandas as pd
import psycopg2
import credentials
import dash_bootstrap_components as dbc
from mentions import mentions_layout

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
    html.Div([
        dcc.DatePickerRange(
            id='my-date-picker-range',
            min_date_allowed=date(1995, 8, 5),
            max_date_allowed=date(2017, 9, 19),
            initial_visible_month=date(2017, 8, 5),
            end_date=date(2017, 8, 25)
        ),
    html.Div(id='output-container-date-picker-range')
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
        return 'Tab in developement'
    elif tab_chosen == "tab-other":
        return 'Tab in developement'
    return html.P("This shouldn't be displayed for now...")


# Date range callback
@app.callback(
    Output('output-container-date-picker-range', 'children'),
    Input('my-date-picker-range', 'start_date'),
    Input('my-date-picker-range', 'end_date'))

def update_output(start_date, end_date):
    string_prefix = 'You have selected: '
    if start_date is not None:
        start_date_object = date.fromisoformat(start_date)
        start_date_string = start_date_object.strftime('%B %d, %Y')
        string_prefix = string_prefix + 'Start Date: ' + start_date_string + ' | '
    if end_date is not None:
        end_date_object = date.fromisoformat(end_date)
        end_date_string = end_date_object.strftime('%B %d, %Y')
        string_prefix = string_prefix + 'End Date: ' + end_date_string
    if len(string_prefix) == len('You have selected: '):
        return 'Select a date to see it displayed here'
    else:
        return string_prefix


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






