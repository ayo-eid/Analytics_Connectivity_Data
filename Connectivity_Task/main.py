import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from modules.Visualization import *
from modules.processing import *

app = dash.Dash(__name__)
server = app.server


# read dataframe from csv and process it
df = pd.read_csv("assets/connectivity_task.csv")
df = clean_df(df)
df = process(df)

# connectivity ratio on different aggregation levels
# 1. aggregated days
days_aggregated = connectivity_ratio(df, "event_day")

# 2. aggregated week days
weekdays_aggregated = connectivity_ratio_ordered(df, "week_day")

# 3. aggregated organisations
org_aggregated = connectivity_ratio_ordered(df, "organisation_name")

# 4. aggregated organisations, places
org_place_aggregated = connectivity_ratio_ordered(df, ["organisation_name", "place_name"])

# 5. aggregated asset types
asset_type_aggregated = connectivity_ratio_ordered(df, "asset_type")

# 6. aggregated organisations, asset types
org_asset_types_aggregated = connectivity_ratio_ordered(df, ["organisation_name", "asset_type"])

# 7. aggregated asset names
asset_names_aggregated = connectivity_ratio_ordered(df, "asset_name")

# 8. aggregated organisations, asset names
org_asset_names_aggregated = connectivity_ratio_ordered(df, ["organisation_name", "asset_name"])

# plots for aggregated Dfs
figs = []

# Line Plot
figs.append(
    plotly_line(
        days_aggregated,
        x="event_day",
        y="count",
        color="event_type",
        title="Connected Vs Disconnected Frequency by Day",
    )
)


# Bar Plots
def plotly_bar(df, x, y, color, title):
    fig = px.bar(df, x=x, y=y, color=color, title=title)
    fig.update_xaxes(type='category')
    figs.append(fig)


bar_aggs = [org_aggregated, asset_names_aggregated, weekdays_aggregated, asset_type_aggregated]
x = ['organisation_name', 'asset_name', 'week_day', 'asset_type']
y = 'count'
color = 'event_type'
bar_titles = ['Organisations Connectivity', 'Assets Connectivity', 'WeekDays Connectivity', 'Asset Type Connectivity']
for i in range(len(bar_aggs)):
    plotly_bar(bar_aggs[i], x[i], y, color, bar_titles[i])

# apply colors on figure layout, #005f69, #001f3f

[fig.update_layout(
    plot_bgcolor="#001f3f", paper_bgcolor="#001f3f", font_color="beige")
    for fig in figs]

# App Layout
# set background color
colors = {"background": "white"}

app.layout = html.Div(
    style={"backgroundColor": colors["background"]},
    children=[
        html.H3(
            children="Analytics Dashboard",
            style={
                "textAlign": "center",
                "fontFamily": "Roboto",
                "fontSize": "1.8rem",
                "color": "#001f3f",
                "marginBottom": "0",
            },
        ),
        html.P(
            children="Connectivity Data",
            style={"textAlign": "center",
                   "fontFamily": "Roboto",
                   "fontSize": "1.2rem",
                   "color": "#444"
                   },
        ),
        html.Div(
            children=[
                html.Div(
                    dcc.Graph(id=figs[0].layout.title.text, figure=figs[0]),
                    style={"width": "50%"},
                ),
                html.Div(
                    dcc.Graph(id=figs[3].layout.title.text, figure=figs[3]),
                    style={"width": "50%"},
                ),
            ],
            style={"display": "flex", " justifyContent": "space-between"},
        ),
        html.Div(
            children=[
                html.Div(
                    dcc.Dropdown(
                        id="slct_org",
                        options=[
                            {"label": i, "value": i}
                            for i in org_place_aggregated["organisation_name"].unique()
                        ],
                        value="Gonzalez-Hancock",
                    ),
                    style={
                        "width": "50%",
                        "marginLeft": "auto",
                        "marginBottom": "1em",
                        "marginTop": "3em"
                        # "display": "flex",
                        # "justifyContent": "flex-end",
                    },
                ),
                html.Div(
                    children=[
                        html.Div(
                            dcc.Graph(
                                id=figs[1].layout.title.text, figure=figs[1], style={},
                            ),
                            style={"width": "50%"},
                        ),
                        html.Div(
                            dcc.Graph(id="places_org", figure={}, style={}),
                            style={"width": "50%"},
                        ),
                    ],
                    style={"display": "flex", " justifyContent": "space-between"},
                ),
            ],
            style={},
        ),
        html.Div(
            children=[
                html.Div(
                    dcc.Dropdown(
                        id="slct_org_2",
                        options=[
                            {"label": i, "value": i}
                            for i in org_asset_types_aggregated["organisation_name"].unique()
                        ],
                        value="Gonzalez-Hancock",
                    ),
                    style={
                        "width": "50%",
                        "marginLeft": "auto",
                        "marginBottom": "1em",
                        "marginTop": "3em"
                        # "display": "flex",
                        # "justifyContent": "flex-end",
                    },
                ),
                html.Div(
                    children=[
                        html.Div(
                            dcc.Graph(
                                id=figs[4].layout.title.text, figure=figs[4], style={},
                            ),
                            style={"width": "50%"},
                        ),
                        html.Div(
                            dcc.Graph(id="asset_type_org", figure={}, style={}),
                            style={"width": "50%"},
                        ),
                    ],
                    style={"display": "flex", " justifyContent": "space-between"},
                ),
            ],
            style={},
        ),
        html.Div(style={"width": "60%", "height": "4px", "backgroundColor": "white"}),
        html.Div(
            children=[
                html.Div(
                    dcc.Dropdown(
                        id="slct_org_3",
                        options=[
                            {"label": i, "value": i}
                            for i in org_asset_names_aggregated["organisation_name"].unique()
                        ],
                        value="Gonzalez-Hancock",
                    ),
                    style={
                        "width": "50%",
                        "marginLeft": "auto",
                        "marginBottom": "1em",
                        "marginTop": "3em"
                        # "display": "flex",
                        # "justifyContent": "flex-end",
                    },
                ),
                html.Div(
                    children=[
                        html.Div(
                            dcc.Graph(
                                id=figs[2].layout.title.text, figure=figs[2], style={},
                            ),
                            style={"width": "50%"},
                        ),
                        html.Div(
                            dcc.Graph(id="asset_name_org", figure={}, style={}),
                            style={"width": "50%"},
                        ),
                    ],
                    style={"display": "flex", " justifyContent": "space-between"},
                ),
            ],
            style={},
        )
    ],
)


@app.callback(
    Output(component_id="places_org", component_property="figure"),
    Input(component_id="slct_org", component_property="value"),
)
def update_graph(selected_organisation):
    filtered_org = org_place_aggregated[
        org_place_aggregated["organisation_name"] == selected_organisation
        ]
    bar_fig = px.bar(
        filtered_org,
        x="place_name",
        y="count",
        color="event_type",
        title=f"Places Connectivity in {selected_organisation} Organization",
    )
    bar_fig.update_layout(
        plot_bgcolor="#001f3f", paper_bgcolor="#001f3f", font_color="beige"
    )
    return bar_fig


@app.callback(
    Output(component_id="asset_type_org", component_property="figure"),
    Input(component_id="slct_org_2", component_property="value"),
)
def update_graph(selected_organisation):
    filtered_org = org_asset_types_aggregated[
        org_asset_types_aggregated["organisation_name"] == selected_organisation
        ]
    bar_fig = px.bar(
        filtered_org,
        x="asset_type",
        y="count",
        color="event_type",
        title=f"Assets Types Connectivity in {selected_organisation} Organization",
    )
    bar_fig.update_xaxes(type='category')
    bar_fig.update_layout(
        plot_bgcolor="#001f3f", paper_bgcolor="#001f3f", font_color="beige"
    )
    return bar_fig


@app.callback(
    Output(component_id="asset_name_org", component_property="figure"),
    Input(component_id="slct_org_3", component_property="value"),
)
def update_graph(selected_organisation):
    filtered_org = org_asset_names_aggregated[
        org_asset_names_aggregated["organisation_name"] == selected_organisation
        ]
    bar_fig = px.bar(
        filtered_org,
        x="asset_name",
        y="count",
        color="event_type",
        title=f"Assets Names Connectivity in {selected_organisation} Organization",
    )
    bar_fig.update_layout(
        plot_bgcolor="#001f3f", paper_bgcolor="#001f3f", font_color="beige"
    )
    return bar_fig


if __name__ == "__main__":
    app.run_server(debug=True)
