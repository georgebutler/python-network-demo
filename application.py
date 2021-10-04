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
            # Moves: 0 = Empty space, 1 = first player, 2 = second player
            # Turn: 0 = Game Over, 1 = first player, 2 = second player

            rooms[name] = {
                "name": name,
                "users": {},
                "moves": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                "turn": 1
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


@application.route('/act/<room>', methods=['POST'])
def act_room(room):
    data = request.json

    if room in rooms.keys():
        if "name" in data.keys():
            if "position" in data.keys():
                if data["name"] in users.keys():
                    userRoom = users[data["name"]]["current_room"]

                    if room == userRoom:
                        key = -1

                        for k, v in rooms[room]["users"].items():
                            if v == data["name"]:
                                key = k

                        if rooms[room]["turn"] == key + 1:
                            position = int(data["position"])
                            symbol = key + 1

                            if rooms[room]["moves"][position] == 0:
                                rooms[room]["moves"][position] = symbol
                                rooms[room]["turn"] = 1 if rooms[room]["turn"] != 1 else 2

                                # Check win condition

                                # Across the top
                                if rooms[room]["moves"][0] == rooms[room]["moves"][1] == rooms[room]["moves"][2] != 0:
                                    rooms[room]["turn"] = 0
                                    print("WINNER: " +
                                          str(rooms[room]["turn"]) + "!!!!!!!")
                                    return make_response(jsonify(rooms[room]), 200)
                                # Across the middle
                                elif rooms[room]["moves"][3] == rooms[room]["moves"][4] == rooms[room]["moves"][5] != 0:
                                    rooms[room]["turn"] = 0
                                    print("WINNER: " +
                                          str(rooms[room]["turn"]) + "!!!!!!!")
                                    return make_response(jsonify(rooms[room]), 200)
                                # Across the bottom
                                elif rooms[room]["moves"][6] == rooms[room]["moves"][7] == rooms[room]["moves"][8] != 0:
                                    rooms[room]["turn"] = 0
                                    print("WINNER: " +
                                          str(rooms[room]["turn"]) + "!!!!!!!")
                                    return make_response(jsonify(rooms[room]), 200)

                                # TODO: Check win condition and set turn to 0.
                                # TODO: Don't let them make a turn if room doesn't have two players.

                                return make_response(jsonify(rooms[room]), 200)
                            else:
                                return make_response(jsonify({
                                    "success": False,
                                    "error": "The position index: " + str(position) + " is taken."
                                }), 400)
                        else:
                            return make_response(jsonify({
                                "success": False,
                                "error": "Not your turn."
                            }), 400)
                    else:
                        return make_response(jsonify({
                            "success": False,
                            "error": "User not allowed to move in that room."
                        }), 400)
                else:
                    return make_response(jsonify({
                        "success": False,
                        "error": "User name not found in 'users'"
                    }), 400)
            else:
                return make_response(jsonify({
                    "success": False,
                    "error": "Must include 'position' as JSON data."
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
