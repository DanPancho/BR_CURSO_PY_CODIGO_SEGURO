from flask import Flask, jsonify, request
import jwt
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'SECRET_KEY'


@app.route('/', methods=['GET'])
def home():
    return jsonify({'response': 'HOLA MUNDO!'})

@app.route('/login', methods=['POST'])
def login():
    auth = request.json
    
    if auth['username'] == 'username' and auth['password'] == 'password':
        token = jwt.encode(
            {
                'user': auth['username'], 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=5)
            },
            app.config['SECRET_KEY']
        )
        return jsonify({'token': token}), 200
    else: 
        return jsonify({'message': 'Credenciales invalidas'})
    

@app.route('/user', methods=['POST'])
def user():
    token = request.headers.get('x-acces-token')
    if not token:
        return jsonify({'message': 'No se ingreso el token'})
    try:
        data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        return jsonify({'message': 'TOKEN OK'}), 200
    except jwt.ExpiredSignatureError:
        return jsonify({'message': 'El token esta caducado'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'message': 'EL token es invalido'}), 401

if __name__ == '__main__':
    app.run(debug=True)