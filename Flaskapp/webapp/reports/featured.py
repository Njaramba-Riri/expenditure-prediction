import os
from io import BytesIO
import base64
import warnings
warnings.filterwarnings("ignore")
warnings.simplefilter("ignore")

from ..mainapp.models import Features, Feedback
from webapp import db


import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns


from dash import Dash, html, dcc, Input, Output, dash_table
import plotly.express as px
import plotly
import plotly.graph_objs as go
import json

from sklearn.metrics import confusion_matrix, roc_auc_score, classification_report, f1_score, precision_score
from sklearn.preprocessing import LabelEncoder, OneHotEncoder

train = pd.read_csv('~/desktop/expenditure/Datasets/train.csv', encoding='iso-8859-1', on_bad_lines='skip')
train.drop("Tour_ID", axis=1, inplace=True)

PROJECT_DIR="."
CHAPTER_ID="Visualizations"
IMAGES_PATH= os.path.join(PROJECT_DIR, "Images", CHAPTER_ID)
os.makedirs(IMAGES_PATH, exist_ok=True)

def save_fig(fig_id, tight_layout=True, fig_extension="png", resolution=300):
    path=os.path.join(IMAGES_PATH, fig_id + "." + fig_extension)
    print(f" Figure '{fig_id}' Saved.")
    if tight_layout:
        plt.tight_layout()
    plt.savefig(path, format=fig_extension, dpi=resolution)


def create_plots():
    data = go.Bar(
        x=train['cost_category'],
        y=train['purpose']
    )

    graphjson = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)
    return graphjson


def plot_categorical(x, y, title=None, xlabel=None, ylabel=None):
    ct=pd.crosstab(train[x], train[y])
    
    fig, axes=plt.subplots(nrows=1,ncols=2, figsize=(12,8))
    
    sns.heatmap(ct, cmap='viridis', annot=True, cbar=True, fmt='g', ax=axes[0])
    axes[0].set_title('Heatmap' if title is None else title)
    axes[0].set_xlabel(''if xlabel is None else xlabel)
    axes[0].set_ylabel('' if ylabel is None else ylabel)
    
    ct.plot(kind='bar', stacked=True, ax=axes[1])
    axes[1].set_title('Bar Chart' if title is None else title)
    axes[1].set_xlabel(f"{x}" if xlabel is None else xlabel)
    axes[1].set_ylabel('counts' if ylabel is None else ylabel)
    axes[1].legend(title=y)
    
    fig.suptitle(f"Relationship between {x} and {y}", fontsize=16, weight='bold')


from dash import Dash, html, dash_table, dcc


def init_dashboard(server):
    """Create a Plotly Dash dashboard."""
    dash_app = Dash(
        server=server,
        routes_pathname_prefix='/letsgo/admin/dashapp/',
        external_stylesheets=[
            '/static/dash/style.css',
        ]
    )

    # Create Dash Layout
    dash_app.layout = html.Div(id='dash-container')

    # Create Layout
    dash_app.layout = html.Div(
        children=[
            dcc.Graph(
                id="histogram-graph",
                figure={
                    "data": [
                        {
                            "x": train["cost_category"],
                            "text": train["cost_category"],
                            "customdata": train["purpose"],
                            "name": "311 Calls by region.",
                            "type": "histogram",
                        }
                    ],
                    "layout": {
                        "title": "NYC 311 Calls category.",
                        "height": 500,
                        "padding": 150,
                    },
                },
            ),
        ],
        id="dash-container",
    )

    return dash_app.server

