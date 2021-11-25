import dash
from dash.dependencies import Input, Output, State

from dash import html, dcc, dash_table
from flask import Flask

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


import db


server = Flask(__name__)
app = dash.Dash(__name__, server=server, suppress_callback_exceptions=True)
server = app.server


app.layout = html.Div(
    [
        dcc.Interval(
            id="interval_sqlite", interval=86400000 * 7, n_intervals=0
        ),  # activated once/week or when page refreshed
        html.H1("Team 31 Disney", style={"textAlign": "center"}),
        html.Div(id="sqlite_datatable"),
        html.H1("Products", style={"textAlign": "center"}),
        html.Button("Add Row", id="editing-rows-button", n_clicks=0),
        html.Button("Save to SQLite", id="save_to_sqlite", n_clicks=0),
        # Create notification when saving to excel
        html.Div(id="placeholder", children=[]),
        dcc.Store(id="store", data=0),
        dcc.Interval(id="interval", interval=1000),
        dcc.Graph(id="my_graph"),
        html.H1("Top Selling Products", style={"textAlign": "center"}),
        dcc.Graph(id="top-selling-graph"),
    ]
)


@app.callback(
    Output("sqlite_datatable", "children"), [Input("interval_sqlite", "n_intervals")]
)
def populate_datatable(n_intervals):
    df = db.run_query(
        "SELECT productID, productName, unitPrice, stockCount FROM products;"
    )
    return [
        dash_table.DataTable(
            id="our-table",
            columns=[
                {
                    "name": str(x),
                    "id": str(x),
                    "editable": True,
                    "deletable": False,
                    "type": "numeric",
                }
                if x == "productID"
                else {
                    "name": str(x),
                    "id": str(x),
                    "editable": True,
                    "deletable": False,
                }
                for x in df.columns
            ],
            data=df.to_dict("records"),
            editable=True,
            row_deletable=False,
            filter_action="native",
            sort_action="native",  # give user capability to sort columns
            sort_mode="single",  # sort across 'multi' or 'single' columns
            page_action="none",  # render all of the data at once. No paging.
            style_table={"height": "300px", "overflowY": "auto"},
            style_cell={
                "textAlign": "left",
                "minWidth": "100px",
                "width": "100px",
                "maxWidth": "100px",
            },
            style_cell_conditional=[
                {"if": {"column_id": c}, "textAlign": "right"}
                for c in ["unitPrice", "stockCount"]
            ],
        ),
    ]


@app.callback(
    Output("our-table", "data"),
    [Input("editing-rows-button", "n_clicks")],
    [State("our-table", "data"), State("our-table", "columns")],
)
def add_row(n_clicks, rows, columns):
    if n_clicks > 0:
        rows.append({c["id"]: "" for c in columns})
    return rows


@app.callback(Output("my_graph", "figure"), [Input("our-table", "data")])
def display_graph(data):
    df_fig = pd.DataFrame(data)
    # print(df_fig)
    fig = px.bar(df_fig, x="productName", y="stockCount")
    return fig


@app.callback(
    [Output("placeholder", "children"), Output("store", "data")],
    [Input("save_to_sqlite", "n_clicks"), Input("interval", "n_intervals")],
    [State("our-table", "data"), State("store", "data")],
    prevent_initial_call=True,
)
def df_to_csv(n_clicks, n_intervals, dataset, s):
    output = html.Plaintext(
        "The data has been saved to your SQLite database.",
        style={"color": "green", "font-weight": "bold", "font-size": "large"},
    )
    no_output = html.Plaintext("", style={"margin": "0px"})

    input_triggered = dash.callback_context.triggered[0]["prop_id"].split(".")[0]

    if input_triggered == "save_to_sqlite":
        s = 6
        data = pd.DataFrame(dataset)
        # creating column list for insertion
        cols = ",".join([str(i) for i in data.columns.tolist()])
        columns = data.columns.tolist()
        for row in data.itertuples(index=False):
            sql = f"INSERT into Products ({cols}) VALUES {tuple(row)} ON CONFLICT(productID) DO UPDATE SET {columns[1]} = '{row[1]}', {columns[2]} = {row[2]}, {columns[3]} = {row[3]} ;"
            db.run_command(sql)
        return output, s
    elif input_triggered == "interval" and s > 0:
        # Message pop up and disappear after 5s.
        s = s - 1
        if s > 0:
            return output, s
        else:
            return no_output, s
    elif s == 0:
        return no_output, s


@app.callback(
    Output("top-selling-graph", "figure"), [Input("interval_sqlite", "n_intervals")]
)
def display_graph(data):
    df_fig = db.run_query(
        "SELECT t.productID, t.productName ,SUM(t.quantity) as total_sold FROM (SELECT c.cartID,c.productID, c.quantity, p.productName FROM contains c left join products p on p.productID = c.productID WHERE c.cartID in (SELECT cartID from purchasedcart )) t GROUP BY t.productID order by SUM(t.quantity) desc;"
    )
    fig = px.bar(df_fig, x="productName", y="total_sold")
    return fig


if __name__ == "__main__":
    app.run_server(debug=True)
