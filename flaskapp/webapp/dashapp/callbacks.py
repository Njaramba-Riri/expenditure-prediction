from dash import Input, Output, State
import plotly.graph_objs as go
import plotly.express as px
from .layouts import train 

def dash_callbacks(app):
    @app.callback(
            Output("graph", "figure"),
            Input("candidate", "value")
    )
    def display_cholopleth(candidate):
        df = px.data.gapminder().query("year == 2007")
        #df = px.data.election()
        geoson = px.data.election_geojson()
        fig = px.choropleth(
            df, locations='lifeExp', hover_name="country", color=candidate, range_color=[0, 3000]
        )

        fig.update_geos(fitbounds="locations", visible=False)
        fig.update_layout(
            title_text='2014 GLobal GDP',
            geo = dict(
                showFrame=False,
                showCoatLines=False,
                projection_type='equirectangular'
            )
        )

        return fig

    @app.callback(
        Output("histogram-chart", "figure"),
        Output("line-chart", "figure"),
        Input("country-filter", "value"),
        Input("age-filter", "value"),
        Input("purpose-filter", "value"),
        Input("activity-filter", "value"),
        prevent_initial_call=True,
    )     
    def update_charts(country, age_group, purpose, activity):
        filtered_data = train.query(
            "country == @country and age_group == @age_group and purpose == @purpose and main_activity == @activity"
            )
        
        histogram_chart =  {
            "data": [
                {
                    "x": filtered_data["purpose"],
                    "y": filtered_data['cost_category'],
                    "type": "histogram"
                }
            ],
            "layout": {
                "title": "Cost Category vs Travel Purpose.",

            }
        }

        line_chart =  {
            "data": [
                {
                    "x": filtered_data["age_group"],
                    "y": filtered_data["cost_category"],
                    "type": "line"
                }
            ],
            "layout": {
                "title": "Cost Category Vs Tourist Age Group"
            }
        }

        return line_chart, histogram_chart

    @app.callback(
            Output("scatter-plot", "figure"),
            Input("slider", "value")
    )
    def update_scatter_chart(range_slider):
        low, high = range_slider
        mask = (train['total_male'].values > low) & (train['total_male'].values < high)
        
        # Assuming 'x_column' and 'y_column' are the names of the columns you want to plot
        fig = go.Figure(
            data=go.Scatter(
                x=train.loc[mask, 'country'], 
                y=train.loc[mask, 'purpose'],
                mode='markers'  # This adds the markers to the plot
            )
        )

        return fig
