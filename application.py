from flask import Flask, request, jsonify, make_response

application = Flask(__name__)

rooms = {}
users = {}

# Index


@application.route('/')
def index():
    return make_response(jsonify({
        "success": True
    }), 200)


# Users


# List all the users


@application.route('/users', methods=['GET'])
def get_users():
    return make_response(jsonify(users), 200)

# Create a user with a given name


@application.route('/users/<name>', methods=['POST'])
def create_user(name):
    if len(name) >= 3 and len(name) <= 16:
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
@application.route('/rooms', methods=['GET'])
def get_rooms():
    return make_response(jsonify(rooms), 200)


# Create a room with a given name
@application.route('/rooms/<name>', methods=['POST'])
def create_room(name):
    if len(name) >= 3 and len(name) <= 16:
        if name in rooms.keys():
            return make_response(jsonify({
                "success": False,
                "error": "Room name is taken."
            }), 200)
        else:
            # Moves: 0 = empty space, 1 = first player, 2 = second player

            rooms[name] = {
                "name": name,
                "users": {},
                "moves": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
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


@application.route('/join/<name>', methods=['POST'])
def join_room(name):
    data = request.json

    if name in rooms.keys():
        if len(rooms[name]["users"]) <= 1:
            if "name" in data.keys():
                if data["name"] in users.keys():
                    if len(users[data["name"]]["current_room"]) <= 0:
                        index = len(rooms[name]["users"])

                        rooms[name]["users"][index] = data["name"]
                        users[data["name"]]["current_room"] = name
                        return make_response(jsonify(rooms[name]), 200)
                    else:
                        return make_response(jsonify({
                            "success": False,
                            "error": "You must leave your current room before joining another."
                        }), 400)
                else:
                    return make_response(jsonify({
                        "success": False,
                        "error": "User name not found in 'users'"
                    }), 400)
            else:
                return make_response(jsonify({
                    "success": False,
                    "error": "Must include 'name' as JSON data."
                }), 400)
        else:
            return make_response(jsonify({
                "success": False,
                "error": "Room is full."
            }), 400)
    else:
        return make_response(jsonify({
            "success": False,
            "error": "Room not found in 'rooms'"
        }), 400)

# Moves


@application.route('/act/<name>', methods=['POST'])
def act_room(name):
    data = request.json

    if name in rooms.keys():
        if "name" in data.keys():
            if data["name"] in users.keys():
                if len(users[data["name"]]["current_room"]) > 0:
                    users[data["name"]]["current_room"] = name
                    return make_response(jsonify(data), 200)
            else:
                return make_response(jsonify({
                    "success": False,
                    "error": "User name not found in 'users'"
                }), 400)
        else:
            return make_response(jsonify({
                "success": False,
                "error": "Must include 'name' as JSON data."
            }), 400)
    else:
        return make_response(jsonify({
            "success": False,
            "error": "Room not found in 'rooms'"
        }), 400)
