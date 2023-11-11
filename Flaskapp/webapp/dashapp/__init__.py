from dash import Dash
import os 

def init_dash(server):

    external_stylesheets = [
        {
            "href": (
                "assets/css/style.css"
                ),
            "rel": "stylesheet"
         }
    ]
    external_scripts = []
    meta_viewport = [
        {
            "name": "viewport",
            "content": "width=device-width, initial-scale=1, shrink-to-fit=no",
        }
    ]

    #curr_dir = os.getcwd() + '/webapp/dashapp/assets'
    dire = os.path.dirname(__file__)
    ass_path = os.path.join(dire, 'assets')

    app = Dash(
        server=server, 
        routes_pathname_prefix='/letsgo/admin/dashboard/',
        assets_folder= ass_path,
        external_stylesheets=external_stylesheets,
        external_scripts=external_scripts,
        meta_tags=meta_viewport)
    
    app.title = "LetsGo | Dashboard"
    app._favicon = 'logo.ico'

    from .layouts import dash_layout
    from .callbacks import dash_callbacks

    with server.app_context():
        
        app.layout = dash_layout(app)

        dash_callbacks(app)

    return app.server