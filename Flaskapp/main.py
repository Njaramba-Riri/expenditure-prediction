import os 
from webapp import create_app, db

env = os.environ.get("LETSGO_ENV", 'dev')
app = create_app('config.%sConfig' % env.capitalize())
os.environ.get('OAUTHLIB_INSECURE_TRANSPORT')

if __name__ == "__main__":
    create_app = app
    create_app.run(debug=True)
else:
    gunicorn_app = app