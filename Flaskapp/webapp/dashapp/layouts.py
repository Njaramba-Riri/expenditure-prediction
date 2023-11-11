from dash import dcc, html, dash_table
import pandas as pd 
import plotly.express as px
import plotly.graph_objs as go
from plotly.subplots import make_subplots
from ..auth.models import User, Role
from ..mainapp.models import Features, Feedback

train = pd.read_csv('~/desktop/expenditure/Datasets/train.csv', encoding='iso-8859-1', on_bad_lines='skip')
train.drop("Tour_ID", axis=1, inplace=True)
sample_train = train.head(10)

countries = train['country'].sort_values().unique()
age_group = train['age_group'].sort_values().unique()
purpose = train['purpose'].sort_values().unique()
main_activity = train['main_activity'].sort_values().unique()

def dash_layout(app):
    data = Features.query.all()
    df = pd.DataFrame(data)

    app.layout =  html.Div(
        children=[
            html.H1("Model Schemas."),
            html.P("System databases."),
            html.Div(
                children=[
                    html.Div(
                        children=[
                            dash_table.DataTable(
                                id="sample-dataset",
                                columns=[
                                    {"name":i, "id":i}
                                    for i in train.columns
                                ],
                                data=sample_train.to_dict("records"),
                                style_cell=dict(textAlign='left'),
                                style_header=dict(backgroundColor='turquoise'),
                                style_data=dict(backgroundColor='lavender'),
                                sort_action="native",
                                sort_mode="native",
                                page_size=300,
                            )
                        ],
                        id='table'
                    ),
                ],
                id="row"
            )

        ],
        id="dash-tables"
    )

    app.layout = html.Div(
        children=[
            html.H1(children="Insights Drawn From Training Data", className="header"),
            html.P("During model training, the following visualizations summarizes key influences of individual tourist spending"),
            html.Div(
                    children= [
                            html.Div(
                                children=[
                                    html.Div("Most frequented.", className="section-title"),
                                    dcc.RadioItems(
                                        id='candidate',
                                        options=["Joly", "Coderre", "Bergeron"],
                                        value="Coderre",
                                        inline=True
                                    ),
                                    dcc.Graph(
                                        id="graph",
                                        figure={
                                            "data": [
                                                go.Figure(
                                                    data=go.Choropleth(
                                                        locations=train['country'],
                                                        z=train['total_male'],
                                                        text=train['country'],
                                                        colorscale='Blues',
                                                        reversescale=True,
                                                        marker_line_color='darkgray',
                                                        marker_line_width=0.5,
                                                        colorbar_title= 'Cost Category per country'
                                                    )
                                                )                                    
                                            ]
                                        },
                                        config={"displayModeBar": False}
                                    )
                                ],
                                id="country",
                                className="col-md-4"
                            ),
                            html.Div(
                                children=[
                                    html.Div("Featured Visualizations", className="section-title"),
                                    html.Div(
                                        children=[
                                            html.Div(
                                                children=[
                                                    html.Div(children="Country", className="menu-title"),
                                                    dcc.Dropdown(
                                                        id="country-filter",
                                                        options=[
                                                            {"label": country, "value": country}
                                                            for country in countries
                                                        ],
                                                        value="UNITED KINGDOM",
                                                        clearable=False,
                                                        className="dropdown",                                       
                                                    ),
                                                ],
                                                className="dropdown"
                                            ),
                                            html.Div(
                                                children=[
                                                    html.Div(children="Tourist Age Group", className="menu-title"),
                                                    dcc.Dropdown(
                                                        id="age-filter",
                                                        options=[
                                                            {"label":age, "value":age}
                                                            for age in age_group
                                                        ],
                                                        value="25-44",
                                                        clearable=False,
                                                        searchable=False,
                                                        className="dropdown",
                                                    ),
                                                    
                                                ],
                                                className="dropdown"
                                            ),
                                            html.Div(
                                                children=[
                                                    html.Div(children="Travel Purpose", className="menu-title"),
                                                    dcc.Dropdown(
                                                        id="purpose-filter",
                                                        options=[
                                                            {"label": purp, "value": purp}
                                                            for purp in purpose
                                                        ],
                                                        value="Leisure and Holidays",
                                                        searchable=True,
                                                        clearable=False,
                                                        className="dropdown",
                                                    ),
                                                ],
                                                className="dropdown"
                                            ),
                                            html.Div(
                                                children=[
                                                    html.Div(children="Main Activity of the Trip", className="menu-title"),
                                                    dcc.Dropdown(
                                                        id="activity-filter",
                                                        options=[
                                                            {"label":activity, "value":activity}
                                                            for activity in main_activity
                                                        ],
                                                        value="Wildlife Tourism",
                                                        searchable=True,
                                                        clearable=False,
                                                        placeholder="Activity",
                                                        className="dropdown",
                                                    ),
                                                ],
                                                className="dropdown"
                                            ),
                                        ],
                                        className="menu",
                                    ),
                                    html.Div(
                                        children=[
                                            html.Div(
                                                children=dcc.Graph(
                                                    id="histogram-chart",
                                                    config={"displayModeBar": False},       
                                                ),
                                                className="card"
                                            ),
                                            html.Div(
                                                children=dcc.Graph(
                                                    id="line-chart",
                                                    config={"displayModeBar": False}
                                                ),
                                                className="card"
                                            ),
                                        ],
                                        className="big-card",
                                    ),
                                ],
                                id="interactive",
                                className="col-md-6"
                            ),                                

                        ],
                    id="dash-intro",
                ), 
            html.Div(children=[
                html.H1("Donut Charts."),
                html.Div(
                    children=[
                        html.Div(
                            children=[
                                html.Div(
                                    children=[
                                        dcc.Graph(
                                            id="donut-chart",
                                            config={"displayModeBar": False},
                                            figure={
                                                "data": [
                                                    go.Pie(
                                                        labels=train['cost_category'],
                                                        values=train['cost_category'].value_counts(),
                                                        hole=.3
                                                    ),
                                                ],
                                                "layout": {
                                                    "title": "The proportion of cost category"
                                                }
                                            },
                                            className="col-mddd-5"
                                        ), 
                                        go.Sunburst(
                                            labels=train['purpose'],
                                            values=train['purpose'].value_counts()
                                        )                                       
                                    ],
                                    id="col-md-5"
                                ),
                                dcc.Graph(
                                    id="scatter-plot",
                                    config={"displayModeBar": False},
                                    figure={
                                        "data": [
                                            go.Scatter(
                                                x=train[train["cost_category"]==i]["total_male"],
                                                y=train[train["cost_category"]==i]["total_female"],
                                                text=train[train["cost_category"] == i]["country"],
                                                mode='markers',
                                                opacity=.8,
                                                marker={
                                                    'size':10,
                                                    'line':{'width':.5, 'color':'white'}
                                                },
                                                name=i
                                            ) for i in train.cost_category.unique()
                                           
                                        ],
                                        "layout":{
                                            "title":"Combined total people per country vs cost category",
                                            "xaxis": {"title":"Total number of men."},
                                            "yaxis": {"title": "Total number of women"},
                                            "margin":{"l":40, "r":40, "t":40, "b":40},
                                            "legend":{"x":.5, "y":1},
                                            "hovermode":"closest"
                                        }
                                    },
                                    className="col-md-5"
                                ),
                                dcc.RangeSlider(
                                    id="slider",
                                    min=0, max=100, step=1,
                                    value=[0, 20],
                                    marks={'0':0, '100':100},
                                )                            
                                
                            ],
                            id="donuts"
                        ),

                    ]),

            ]),
            dcc.Graph(
                id="histogram-graph",
                config={"displayModeBar": False},
                figure={
                    "data": [
                        {
                            "x": train["cost_category"],
                            "text": train["cost_category"],
                            "customdata": train["purpose"],
                            "name": "Cost Category by Travel Purpose.",
                            "type": "histogram",
                        }
                    ],
                    "layout": {
                        "title": "NYC 311 Calls category.",
                        "height": 500,
                        "padding": 150,
                        "colorway": ["#17b897"],
                    },
                },
            ),
            dcc.Graph(
                id="bar-chart",
                config={"displayModeBar": False},
                figure={
                    "data": [
                        go.Bar(
                            x=train[train['cost_category']==i]['country'],
                            y=train[train['cost_category']==i]['info_source'],
                            name=i
                        ) for i in train.cost_category.unique()
                    ],
                }
            ),
            html.Div(
                children=[
                    html.P("Filter by number."),
                    dcc.RangeSlider(
                        id="range-slider",
                        min=0, max=100, step=1,
                        marks={0:'0', 100:'100'},
                        value=[0, 20]
                    ),                     
                ]
            ),
            dcc.Graph(
                id = 'bar',
                config={"displayModeBar": False},
                figure={
                    "data": [
                        {
                            'x': train['main_activity'],
                            #'y': train['cost_category'],
                            'type': 'bar'
                        }
                    ],
                    "layout": {
                            'title': 'Total male',
                            'height': 400,
                            'padding': 200,
                            'xanchor': "left",
                    },
                    "xaxis": {"fixedrange": True}
                },
            ),
            dcc.Graph(
                id='bar-plot',
                config={"displayModeBar": False},
                figure={
                    "data": [
                        {
                            "x": train['total_male'],
                            "y": train["total_female"],
                            "type": "scatter"
                        }
                    ],
                    "layout":{
                        "title": "Total Male vs Total Female",
                        "height": 500,
                    }
                }
            ),
            html.Div(
                children= [
                    html.H1("Sample Training Dataset."),
                    html.P(children=["The Below sample dataset was used for training the model."]),
                    dash_table.DataTable(
                        id="sample-dataset",
                        columns=[
                            {"name":i, "id":i}
                            for i in df.columns
                        ],
                        data=sample_train.to_dict("records"),
                        style_cell=dict(textAlign='left'),
                        style_header=dict(backgroundColor='turquoise'),
                        style_data=dict(backgroundColor='lavender'),
                        sort_action="native",
                        sort_mode="native",
                        page_size=300,
                    ), 
                ],
            ),                   
 
        ],
        id="dash-container",   
    )


    return app.layout