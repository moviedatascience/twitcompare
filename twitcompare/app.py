from decouple import config
from dotenv import load_dotenv
from flask import Flask, render_template, request
from .model import DB, User

load_dotenv()

def create_app():
    """ Create and configure an instance of the Flask application """
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = config('DATABASE_URL')
    DB.init_app(app)

    @app.route('/')
    def root():
        return render_template('base.html', title='TwitCompare', users=User.query.all())

    @app.route('/user', methods=['POST'])
    @app.route('/user/<name>', methods=['GET'])
    def user(name=None, message=''):
            name = name or request.values['user_name']
            try:
                if request.method == 'POST':
                    add_user(name)
                    message = "User {} sucessfully added!".format(name)
                tweets = User.query.filter(User.name=name).one().tweets
            except Exception as e:
                message = 'Error adding {}: {}'.format(name, e)
                tweets = []
            return render_template('user.html')



    return app
