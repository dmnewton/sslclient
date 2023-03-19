from flask import Flask, redirect, url_for, session
from authlib.integrations.flask_client import OAuth
import yaml

from functools import wraps

app = Flask(__name__)

# Read YAML file
with open("config.yaml", 'r') as stream:
    data_loaded = yaml.safe_load(stream)

app.secret_key = data_loaded['secret_key']
#configuraciones de oauth
oauth = OAuth(app)
github = oauth.register(
    name='github',
    client_id=data_loaded['client_id'],
    client_secret=data_loaded['client_secret'],
    access_token_url='https://github.com/login/oauth/access_token',
    access_token_params=None,
    authorize_url='https://github.com/login/oauth/authorize',
    authorize_params=None,
    api_base_url='https://api.github.com/',
    client_kwargs={'scope': 'user:email'},
)

def logged_in(f):
    @wraps(f)
    def decorated_func(*args, **kwargs):
        if session.get("logged_in"):
            return f(*args, **kwargs)
        else:
            return redirect("/login")
    return decorated_func

@app.route("/")
def index():
    if session.get("logged_in"):
        return f"Hello! you are logged in as {session.get('login')}"
    else:
        return f'Hello! Stranger'

@app.route("/abc")
@logged_in
def abc():
    return f'abc!'

@app.route('/login')
def registro():
   github = oauth.create_client('github')
   redirect_uri = url_for('authorize', _external=True)
   return github.authorize_redirect(redirect_uri)

@app.route('/authorize')
def authorize():
    github = oauth.create_client('github')
    token = github.authorize_access_token()
    resp = github.get('user', token=token)
    profile = resp.json()
    # Begin user session by logging the user in
    session['logged_in'] = True
    session['login'] = profile['login']
    # do something with the token and profile
    #print(profile, token)
   
    return redirect('/')


if __name__ == "__main__":
    app.run(host='0.0.0.0',port=3000,debug=True)