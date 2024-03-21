from flask import Blueprint, current_app, request, make_response, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from database.read import GetRecord
from database.create import CreateRecord
from datetime import datetime, timedelta
import jwt
import uuid

blog_blueprint = Blueprint('blog', __name__)


@blog_blueprint.route('/register/', methods=['GET', 'POST'])
def register():
    f_name = request.form.get('firstName')
    l_name = request.form.get('lastName')
    email = request.form.get('email')
    user_password = request.form.get('password')

    hash_and_salted_password = generate_password_hash(
        user_password,
        method='pbkdf2:sha256',
        salt_length=8
    )

    user = GetRecord().user(email=email)

    if not user:
        CreateRecord().user(
            public_id=str(uuid.uuid4()),
            f_name=f_name,
            l_name=l_name,
            email=email,
            password=hash_and_salted_password
        )

        return make_response('Successfully registered.', 201)
    return make_response('User already exists. Please Log in.', 409)


@blog_blueprint.route('/login/', methods=['GET', 'POST'])
def login():
    secret_key = current_app.config['SECRET_KEY']
    user = GetRecord().user(email=request.form.get('email'))

    if not user:
        response = make_response(
            'Error fetching auth token!, invalid email or password', 401)
        response.headers['WWW-Authenticate'] = 'Bearer'
        return response

    if check_password_hash(user.user_password, request.form.get('password')):
        expiration_time = datetime.utcnow() + timedelta(minutes=1)
        expiration_timestamp = int(expiration_time.timestamp())
        token = jwt.encode(
            payload={
                'public_id': user.public_id,
                'exp': expiration_timestamp
            },
            key=secret_key,
            algorithm='HS256'
        )
        return jsonify({
            'message': 'Successfully fetched auth token',
            'token': token
        }), 200

    return make_response(
        'Error fetching auth token!, invalid email or password',
        401,
        {'WWW-Authenticate': 'Bearer'}
    )
