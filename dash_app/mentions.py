from dash import dash_table, dcc, html
import pandas as pd
import psycopg2
import credentials
import dash_bootstrap_components as dbc

conn = psycopg2.connect(database='TwitterDB', 
							user=credentials.pg_user, 
							password=credentials.pg_pass)
query = '''
		    SELECT t.*, tu.user_location FROM tweets AS t
		    LEFT JOIN twitter_user AS tu ON tu.user_id = t.user_id;
        	'''

df = pd.read_sql(query, conn)

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
            html.Div(
				dash_table.DataTable(
                    data=df.to_dict('records'),
                    columns=[{"name": i, "id": i} for i in df.columns], 
					id='tbl', 
					style_data={
						'whiteSpace': 'normal',
						'height': 'auto',
						'lineHeight': '17px'
								},
                    page_size=5
									)
					)
		)
	]	
)
