import json
import mysql.connector
import numpy as np
import pandas as pd
import plotly.express as px
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import datetime
import myloginpath

# Database connection configuration
db_config = {
    "user": "rmukai",
    "password": "your_mysql_password",
    "host": "localhost",
    "database": "testbase",
}

db_config = myloginpath.parse('client')
db_config['database'] = 'testbase'

# Connect to the MySQL database
def connect_to_db():
    return mysql.connector.connect(**db_config)


# Save query details to the MySQL table
def save_query(query, params, columns):
    conn = connect_to_db()
    cursor = conn.cursor()
    query_to_save = "INSERT INTO saved_queries (query, params, columns) VALUES (%s, %s, %s)"
    cursor.execute(query_to_save, (query, json.dumps(params), json.dumps(columns)))
    conn.commit()
    cursor.close()
    conn.close()

# Execute a MySQL query and return the result as a DataFrame
def execute_query(query, params):
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute(query, params)
    result = cursor.fetchall()
    columns = [col[0] for col in cursor.description]
    cursor.close()
    conn.close()
    return pd.DataFrame(result, columns=columns)

# Initialize the Dash app
app = dash.Dash(__name__)
app.layout = html.Div([
    # Input components for the MySQL query and parameters
    dcc.Input(id="query-input", type="text", placeholder="Enter MySQL query", style={"width": "100%"}),
    dcc.Input(id="params-input", type="text", placeholder="Enter query parameters as a comma-separated list"),
    html.Button("Submit", id="submit-query"),

    # Dropdown components for selecting X and Y columns
    dcc.Dropdown(id="xaxis-dropdown", placeholder="Select X-axis column"),
    dcc.Dropdown(id="yaxis-dropdown", placeholder="Select Y-axis columns", multi=True),

    # Checkboxes for Y-scale options
    dcc.Checklist(
        id="yscale-checklist",
        options=[
            {"label": "Use logarithmic scale", "value": "log"},
        ],
    ),

    # The output plot
    dcc.Graph(id="output-plot"),

    # Hidden div to store the DataFrame as JSON
    html.Div(id="dataframe-json", style={"display": "none"}),
])

@app.callback(
    [Output("dataframe-json", "children"), Output("xaxis-dropdown", "options"), Output("yaxis-dropdown", "options")],
    [Input("submit-query", "n_clicks")],
    [State("query-input", "value"), State("params-input", "value")],
)
def update_data(n_clicks, query, params):
    if not query:
        return dash.no_update, dash.no_update, dash.no_update

    params = [param.strip() for param in params.split(",")] if params else []
    df = execute_query(query, params)
    options = [{"label": col, "value": col} for col in df.columns]

    return df.to_json(date_format="iso", orient="split"), options, options

@app.callback(
    Output("output-plot", "figure"),
    [Input("xaxis-dropdown", "value"), Input("yaxis-dropdown", "value"), Input("yscale-checklist", "value")],
    [State("dataframe-json", "children")],
)
def update_plot(x_axis, y_axis, y_scale, dataframe_json):
    if not x_axis or not y_axis or not dataframe_json:
        return dash.no_update

    df = pd.read_json(dataframe_json, orient="split")

    # Configure the plot's Y-axis scale
    yaxis_config = {"type": "log"} if (y_scale is not None and "log" in y_scale) else {}

    # Create the plot
    fig = px.scatter(
        df,
        x=x_axis,
        y=y_axis,
        title="Plotting MySQL Query Results",
        labels={col: col for col in df.columns},
    )
    fig.update_yaxes(**yaxis_config)

    return fig

def create_dummy_data():

    conn = connect_to_db()
    cursor = conn.cursor()

    sql_command = (
        "REPLACE INTO \n" +
        "   TIME_SERIES_DATA \n" +
        "   SET \n" +
        "       THE_TIMESTAMP = %s, \n" +
        "       VAR_1 = %s, \n" +
        "       VAR_2 = %s, \n" +
        "       VAR_3 = %s"
    )

    baseline_datetime = datetime.datetime.utcnow()

    N = 101

    tuple_list = []

    for n in range(N):
        current_timedelta = datetime.timedelta(seconds=12 * n)
        current_datetime = baseline_datetime+current_timedelta
        y1 = float(n) / (N - 1)
        y2 = np.sin(2 * np.pi * y1)
        y3 = np.sin(4 * np.pi * y1)
        data_tuple = (current_datetime, y1, y2, y3)

        tuple_list.append(data_tuple)

    result = cursor.executemany(sql_command, tuple_list)

    conn.commit()

    cursor.close()
    conn.close()


# Run the Dash app
if __name__ == "__main__":
    create_dummy_data()
    app.run_server(debug=True)
