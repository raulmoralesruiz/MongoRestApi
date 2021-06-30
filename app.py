# Importar librerías 
from flask import Flask, jsonify, request, Response
from flask.wrappers import Request #, jsonify, request
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash
from bson import json_util
from bson.objectid import ObjectId

# Ejecutar aplicación Flask
app = Flask(__name__)
app.config['MONGO_URI']='mongodb://test:test@127.0.0.1:27017/test?authSource=admin'
mongo = PyMongo(app)


# Ruta para crear usuarios
@app.route('/users', methods=['POST'])

# Método para crear usuarios
def create_user():
    # recibir datos
    username = request.json['username']
    password = request.json['password']
    email = request.json['email']

    if username and password and email:
        hashed_pass = generate_password_hash(password)

        # si no existe la conexión, la crea
        id = mongo.db.users.insert(
            {
                'username': username,
                'password': hashed_pass,
                'email': email,
            }
        )
        response = {
            'id': str(id),
            'username': username,
            'password': hashed_pass,
            'email': email,
        }
        return response
    else:
        return not_found()


# Ruta para obtener usuarios
@app.route('/users', methods=['GET'])

# Método para obtener usuarios
def get_users():
    # obtener datos de mongodb (formato bson originalmente)
    users = mongo.db.users.find()
    # convertir los datos anteriores, de bson a json
    response = json_util.dumps(users)
    # enviar datos convertidos al cliente
    return Response(response, mimetype='application/json')


# Ruta para obtener usuarios
@app.route('/users/<id>', methods=['GET'])

# Método para obtener usuarios
def get_user(id):
    user = mongo.db.users.find_one({'_id': ObjectId(id)})
    response = json_util.dumps(user)
    return Response(response, mimetype='application/json')


# Ruta para eliminar usuarios
@app.route('/users/<id>', methods=['DELETE'])

# Método para eliminar usuarios
def delete_user(id):
    mongo.db.users.delete_one({'_id': ObjectId(id)})
    response = jsonify({'response': 'User (' + id + ') was deleted successfully'})
    return response


# Ruta para actualizar usuarios
@app.route('/users/<id>', methods=['PUT'])

# Método para actualizar usuarios
def update_user(id):
    username = request.json['username']
    password = request.json['password']
    email = request.json['email']
    
    if username and password and email:
        hashed_pass = generate_password_hash(password)
        mongo.db.users.update_one({'_id': ObjectId(id)}, {'$set': {
            'username': username,
            'password': hashed_pass,
            'email': email
        }})
        response = jsonify({'response': 'User (' + id + ') was updated successfully'})
        return response


# Ruta para controlar errores
@app.errorhandler(404)

# Método para controlar errores
def not_found(error = None):
    response = jsonify({
        'response': 'Resource not found ' + request.url,
        'status': 404,
    })
    response.status_code = 404
    return response 


if __name__ == '__main__':
    app.run(debug=True, port=4000)