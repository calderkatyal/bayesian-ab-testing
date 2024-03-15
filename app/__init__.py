from flask import Flask
from flask_session import Session

app = Flask(__name__, static_folder='static', template_folder='templates')
app.secret_key = 'your_very_secret_key_here'

# Configure server-side session storage
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

from app import views