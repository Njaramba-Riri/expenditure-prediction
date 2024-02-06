import os 
from webapp import create_app, db
from webapp.cli import register

env = os.environ.get("LETSGO_ENV", 'test')
app = create_app('config.%sConfig' % env.capitalize())
register(app)

if __name__ == "__main__":
    create_app = app
    create_app.run(port=5001, debug=True, use_reloader=True)
else:
    gunicorn_app = app