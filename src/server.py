from flask import Flask, request, jsonify, make_response

app = Flask(__name__)

rooms = {}
users = {}

# Index


@app.route('/')
def index():
    return make_response(jsonify({
        "success": True
    }), 200)


# Users


# List all the users


@app.route('/users', methods=['GET'])
def get_users():
    return make_response(jsonify(users), 200)

# Create a user with a given name


@app.route('/users/<name>', methods=['POST'])
def create_user(name):
    if (len(name) >= 3 and len(name) <= 16):
        if name in users.keys():
            return make_response(jsonify({
                "success": False,
                "error": "User name is taken."
            }), 200)
        else:
            users[name] = {
                "name": name,
                "current_room": ""
            }

            return make_response(jsonify({
                "success": True,
                "user": users[name]
            }), 200)
    else:
        return make_response(jsonify({
            "success": False,
            "error": "User name must be between 3 and 16 characters."
        }), 400)


# Rooms


# List all the rooms
@app.route('/rooms', methods=['GET'])
def get_rooms():
    return make_response(jsonify(rooms), 200)


# Create a room with a given name
@app.route('/rooms/<name>', methods=['POST'])
def create_room(name):
    if (len(name) >= 3 and len(name) <= 16):
        if name in rooms.keys():
            return make_response(jsonify({
                "success": False,
                "error": "Room name is taken."
            }), 200)
        else:
            rooms[name] = {
                "name": name,
                "users": {}
            }

            return make_response(jsonify({
                "success": True,
                "room": rooms[name]
            }), 200)
    else:
        return make_response(jsonify({
            "success": False,
            "error": "Room name must be between 3 and 16 characters."
        }), 400)


# Joining


@app.route('/join/<name>', methods=['POST'])
def join_room(name):
    data = request.json
    return make_response(jsonify(data), 200)


@app.route('/leave/<name>', methods=['POST'])
def leave_room(name):
    print("Leaving room named: " + name)
    return make_response(jsonify({}), 200)
