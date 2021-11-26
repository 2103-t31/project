# Code source: https://dash-bootstrap-components.opensource.faculty.ai/examples/simple-sidebar/
import dash
import dash_bootstrap_components as dbc

from dash import html, dcc, dash_table
import plotly.express as px
from dash.dependencies import Input, Output, State
import pandas as pd
import plotly.express as px

from flask import Flask

import db

# data source: https://www.kaggle.com/chubak/iranian-students-from-1968-to-2017
# data owner: Chubak Bidpaa
df = pd.read_csv(
    "https://raw.githubusercontent.com/Coding-with-Adam/Dash-by-Plotly/master/Bootstrap/Side-Bar/iranian_students.csv"
)
server = Flask(__name__)

app = dash.Dash(
    __name__,
    title="Team 31 BBFA - Disney",
    server=server,
    suppress_callback_exceptions=True,
    update_title=None,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
)
server = app.server


# styling the sidebar
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

# padding for the page content
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

sidebar = html.Div(
    [
        html.H2("Team 31  bbfa", className="display-4"),
        html.Hr(),
        html.P("Disney", className="lead"),
        dbc.Nav(
            [
                dbc.NavLink("Products", href="/", active="exact"),
                dbc.NavLink("Top sale", href="/top-sale", active="exact"),
                dbc.NavLink("Average Order", href="/avg-order", active="exact"),
                dbc.NavLink("Market Channel", href="/mkt-channel", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

content = html.Div(id="page-content", children=[], style=CONTENT_STYLE)

app.layout = html.Div([dcc.Location(id="url"), sidebar, content])


@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname == "/":
        return [
            html.H2("Products", style={"textAlign": "center"}),
            dcc.Interval(
                id="interval_sqlite", interval=86400000 * 7, n_intervals=0
            ),  # activated once/week or when page refreshed
            html.Div(id="sqlite_datatable"),
            html.Button("Add Row", id="editing-rows-button", n_clicks=0),
            html.Button("Save to SQLite", id="save_to_sqlite", n_clicks=0),
            html.Div(id="placeholder", children=[]),
            html.H2("Stock Count", style={"textAlign": "center"}),
            dcc.Graph(id="my_graph"),
            # Create notification when saving to excel
            dcc.Store(id="store", data=0),
        ]
    elif pathname == "/top-sale":
        return [
            html.H2("Top Selling Products", style={"textAlign": "center"}),
            dcc.Interval(id="interval_sqlite", interval=86400000 * 7, n_intervals=0),
            dcc.Graph(id="top-selling-graph"),
        ]
    elif pathname == "/avg-order":
        return [
            dcc.Interval(id="interval_sqlite", interval=86400000 * 7, n_intervals=0),
            html.H2("Average Order", style={"textAlign": "center"}),
            dcc.Dropdown(
                id="total_type_dropdown",
                options=[
                    {"label": "Total Order", "value": "Total Order"},
                    {"label": "Total Value", "value": "Total Value"},
                ],
                value="Total Order",
                multi=False,
                clearable=False,
                style={"width": "50%"},
            ),
            html.Div([dcc.Graph(id="average-order")]),
        ]
    elif pathname == "/mkt-channel":
        return [
            dcc.Interval(id="interval_sqlite", interval=86400000 * 7, n_intervals=0),
            html.Div(
                [
                    html.H2("Overall", style={"textAlign": "center"}),
                    html.P("Variable"),
                    dcc.Dropdown(
                        id="overall_total_type_dropdown",
                        options=[
                            {
                                "label": "Total Order Value",
                                "value": "Total Order Value",
                            },
                            {"label": "Order Count", "value": "Order Count"},
                            {
                                "label": "Average Order Value",
                                "value": "Average Order Value",
                            },
                        ],
                        value="Total Order Value",
                        multi=False,
                        clearable=False,
                        style={"width": "50%"},
                    ),
                    dcc.Graph(id="overall"),
                ]
            ),
            html.H2("Device Type", style={"textAlign": "center"}),
            html.Div(
                [
                    html.P("Device"),
                    dcc.Dropdown(
                        id="device_type_dropdown",
                        options=[
                            {"label": "Android", "value": "Android"},
                            {"label": "Iphone", "value": "Iphone"},
                            {"label": "Mac", "value": "Mac"},
                            {"label": "Windows", "value": "Windows"},
                        ],
                        value="Android",
                        multi=False,
                        clearable=False,
                        style={"width": "50%"},
                    ),
                    html.P("Variable"),
                    dcc.Dropdown(
                        id="total_type_dropdown",
                        options=[
                            {
                                "label": "Total Order Value",
                                "value": "Total Order Value",
                            },
                            {"label": "Order Count", "value": "Order Count"},
                            {
                                "label": "Average Order Value",
                                "value": "Average Order Value",
                            },
                        ],
                        value="Total Order Value",
                        multi=False,
                        clearable=False,
                        style={"width": "50%"},
                    ),
                ],
                style=dict(display="flex"),
            ),
            html.Div([dcc.Graph(id="device-type")]),
        ]
    # If the user tries to reach a different page, return a 404 message
    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ]
    )


@app.callback(
    Output("sqlite_datatable", "children"), [Input("interval_sqlite", "n_intervals")]
)
def populate_datatable(n_intervals):
    df = db.run_query(
        "SELECT productID, productName as 'Product name', unitPrice, stockCount as 'Stock count' FROM products;"
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
                for c in ["unitPrice", "Stock count"]
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
    fig = px.bar(df_fig, x="Product name", y="Stock count", color="Stock count")
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
        "SELECT t.productID, t.productName as 'Product name' ,SUM(t.quantity) as 'Total sold' FROM (SELECT c.cartID,c.productID, c.quantity, p.productName FROM contains c left join products p on p.productID = c.productID WHERE c.cartID in (SELECT cartID from purchasedcart )) t GROUP BY t.productID order by SUM(t.quantity) desc;"
    )
    fig = px.bar(df_fig, x="Product name", y="Total sold", color="Total sold")
    return fig


@app.callback(
    Output(component_id="average-order", component_property="figure"),
    [Input(component_id="total_type_dropdown", component_property="value")],
)
def update_graph(my_dropdown):
    df_fig = db.run_query(
        "SELECT COUNT(*) as 'Total Order',SUM(q.value) 'Total Value', Quarter FROM (SELECT pc.cartID, sc.value,(STRFTIME('%m', pc.datePurchased) + 2) / 3 as Quarter FROM shoppingCarts sc INNER JOIN purchasedCart pc ON sc.cartID = pc.cartID WHERE sc.value < (SELECT AVG(sc.value) FROM shoppingCarts sc INNER JOIN purchasedCart pc ON sc.cartID = pc.cartID)) q GROUP BY quarter"
    )
    figure = px.bar(
        df_fig, x="Quarter", y=my_dropdown, color=my_dropdown, title="Average Order"
    )

    return figure


@app.callback(
    [
        Output(component_id="device-type", component_property="figure"),
        Output(component_id="overall", component_property="figure"),
    ],
    [
        Input(component_id="overall_total_type_dropdown", component_property="value"),
        Input(component_id="device_type_dropdown", component_property="value"),
        Input(component_id="total_type_dropdown", component_property="value"),
    ],
)
def update_graph(
    overall_total_type_dropdown, device_type_dropdown, total_type_dropdown
):
    df_fig = db.run_query(
        "SELECT v.deviceType as 'Device Type', v.Mchannel as 'Marketing Channel', SUM(sc.value) as 'Total Order Value', COUNT(*) as 'Order Count', printf(\"%.2f\",(SUM(sc.value)/Count(*))) as 'Average Order Value' FROM visits v INNER JOIN makes m ON v.visitID = m.visitID INNER JOIN has h ON m.custID = h.custID INNER JOIN purchasedcart p ON h.cartID = p.cartID INNER JOIN shoppingCarts sc ON p.cartID = sc.cartID GROUP BY v.deviceType, v.Mchannel"
    )
    df_total_type = df_fig[["Device Type", "Marketing Channel", total_type_dropdown]]
    df_device_filter = df_fig["Device Type"].str.contains(device_type_dropdown)
    figure2 = px.bar(
        df_fig,
        x="Marketing Channel",
        y=overall_total_type_dropdown,
        color=overall_total_type_dropdown,
        hover_data=["Device Type"],
        title="Average Order",
    )
    figure1 = px.bar(
        df_total_type[df_device_filter],
        x="Marketing Channel",
        y=total_type_dropdown,
        color=total_type_dropdown,
        title="Average Order",
    )
    return figure1, figure2


if __name__ == "__main__":
    app.run_server(port=3000)
