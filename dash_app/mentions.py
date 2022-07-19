from dash import Dash, Input, Output, callback, dash_table, dcc, html
import pandas as pd
import psycopg2
import credentials
import dash_bootstrap_components as dbc
from app import app

# conn = psycopg2.connect(database='TwitterDB', 
# 							user=credentials.pg_user, 
# 							password=credentials.pg_pass)

# query = '''
# 		    SELECT t.*, tu.user_location FROM tweets AS t
# 		    LEFT JOIN twitter_user AS tu ON tu.user_id = t.user_id;
#         	'''


# df = pd.read_sql(query, conn)

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
                            ],
                            clearable=False,
                        ),
                    ],
                    width=3,
                )
		),
		html.Br(),
        dbc.Row(
            html.Div(id='table-content'

									)
					)
		])


@app.callback(
    Output('table-content', 'children'),
    Input('memory-df-filtered', 'data'),
    Input('count-mentions', 'value')
)

def update_table(memory_df, nb_results):
    df_filtered = pd.read_json(memory_df, orient='split')
    
    return dash_table.DataTable(
                    data=df_filtered.to_dict('records'),
                    columns=[{"name": i, "id": i} for i in df_filtered.columns], 
					# id='tbl', 
					style_data={
						'whiteSpace': 'normal',
						'height': 'auto',
						'lineHeight': '17px'
								},
                    page_size=nb_results)



# # Dropdown callback
# @app.callback(
#     Output('tbl', 'page_size'),
#     [Input('count-mentions', 'value')]
# )

# def table_count(no_results):
#     if no_results == 5:
#         return 5
#     elif no_results == 10:
#         return 10
#     elif no_results == 15:
#         return 15