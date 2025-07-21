from flask import Flask, request, jsonify

app = Flask(__name__)

# In-memory data store for users
users = {}

@app.route('/')
def welcome():
    return "Welcome to the User API!"

@app.route('/users', methods=['GET'])
def get_users():
    return jsonify(users)

@app.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    if user_id in users:
        return jsonify({user_id: users[user_id]})
    return jsonify({"error": "User not found"}), 404

@app.route('/users', methods=['POST'])
def add_user():
    data = request.get_json()
    user_id = data.get('id')
    name = data.get('name')

    if not user_id or not name:
        return jsonify({"error": "Please provide id and name"}), 400

    if user_id in users:
        return jsonify({"error": "User ID already exists"}), 400

    users[user_id] = {"name": name}
    return jsonify({"message": "User added", "user": users[user_id]}), 201

@app.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    if user_id not in users:
        return jsonify({"error": "User not found"}), 404

    data = request.get_json()
    name = data.get('name')
    if name:
        users[user_id]['name'] = name
    return jsonify({"message": "User updated", "user": users[user_id]})

@app.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    if user_id not in users:
        return jsonify({"error": "User not found"}), 404

    deleted_user = users.pop(user_id)
    return jsonify({"message": "User deleted", "user": deleted_user})

# Run the app without debug mode
if __name__ == '__main__':
    app.run(debug=False)  # debug is OFF
