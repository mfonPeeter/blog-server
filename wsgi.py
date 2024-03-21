from flask import Flask
from dotenv import load_dotenv
from views.blog import blog_blueprint
import os

app = Flask(__name__)

app.register_blueprint(blog_blueprint, url_prefix='/blog')

load_dotenv()

with app.app_context():
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


if __name__ == '__main__':
    app.run(debug=True)
