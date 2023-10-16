from flask import (
    render_template,
    request,
    session,
    Blueprint,
    jsonify
)
from db import db
from models import (
    User,
    Chat,
    Message,
    ChatMessage,
    get_messages_in_bundles_of_timestamp)

chat_test_blp = Blueprint('chat_test', __name__)


@chat_test_blp.route('/chat')
def chat_page():
    return render_template('index.html')


"""
During user registration we create a chat entry for that user, For example (line 32-35):
@views.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form["email"].strip().lower()
        username = request.form["username"].strip().lower()
        password = request.form["password"]

        # Check if the user already exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash("User already exists with that username.")
            return redirect(url_for("views.login"))

        # Create a new user
        new_user = User(username=username, email=email, password=password)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        # Create a new chat list for the newly registered user
        new_chat = Chat(user_id=new_user.id, chat_list=[])
        db.session.add(new_chat)
        db.session.commit()

        flash("Registration successful.")
        return redirect(url_for("views.login"))

    return render_template("auth.html")
"""

"""
When user logs in, we create a session for that user. for example (line 62-67):
@views.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"].strip().lower()
        password = request.form["password"]

        # Query the database for the inputted email address
        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            # Create a new session for the newly logged-in user
            session["user"] = {
                "id": user.id,
                "username": user.username,
                "email": user.email,
            }
            return redirect(url_for("views.chat"))
        else:
            flash("Invalid login credentials. Please try again.")
            return redirect(url_for("views.login"))

    return render_template("auth.html")
"""


@chat_test_blp.route('/get_user')
def get_user():
    """

    :return: json object with current user
    """
    return jsonify(session["user"])


@chat_test_blp.route('/new_chat/<string:seller_email>', methods=["POST"])
def new_chat(seller_email):
    """

    :return: json object with room_id
    """
    user_id = session["user"]["id"]  # This would obv be a buyer, since only a buyer can initiate a convo
    new_chat_email = seller_email.lower()  # Could be any info from the seller's page whose message
    # icon was clicked, Here I'm using the seller's email

    # Get the recipient user
    recipient_user = User.query.filter_by(email=new_chat_email).first()

    # Check if the chat already exists
    existing_chat = Chat.query.filter_by(user_id=user_id).first()
    if not existing_chat:
        existing_chat = Chat(user_id=user_id, chat_list=[])
        db.session.add(existing_chat)
        db.session.commit()

    data = {'room_id': ''}
    # Check if the new chat is already in the chat list
    if recipient_user.id not in [chat["user_id"] for chat in existing_chat.chat_list]:
        # Generate a room_id
        room_id = Chat.generate_unique_id()
        data = {'room_id': room_id}

        # Add the new chat to the chat list of the current user
        existing_chat.chat_list.append({"user_id": recipient_user.id, "room_id": room_id})

        # Save the changes to the database
        db.session.add(existing_chat)
        db.session.commit()

        # Create a new chat list for the recipient user if it doesn't exist
        recipient_chat = Chat.query.filter_by(user_id=recipient_user.id).first()
        if not recipient_chat:
            recipient_chat = Chat(user_id=recipient_user.id, chat_list=[])
            db.session.add(recipient_chat)
            db.session.commit()

        # Add the new chat to the chat list of the recipient user
        recipient_chat.chat_list.append({"user_id": user_id, "room_id": room_id})
        db.session(recipient_chat)
        db.session.commit()

        # Create a new message entry for the chat room
        new_message = Message(room_id=room_id)
        db.session.add(new_message)
        db.session.commit()

    return jsonify(data)


@chat_test_blp.route('/get_messages/', methods=["GET", "POST"])
def get_messages():
    """
    Gets all the message history in a certain room, in bundles of timestamp, indexed and paginated.
    :return: all messages in a particular room_id
    """
    # Get the room id in the URL or set to None
    room_id = request.args.get("rid", None)

    # Get all the message history in a certain room

    # Get the Message object for the chat room
    message = Message.query.filter_by(room_id=room_id).first()

    # Using the function in group_chats to get message in bundles
    messages = get_messages_in_bundles_of_timestamp(message, bundle_size=100, page=1)

    return jsonify(messages)


@chat_test_blp.route('/get_last_message/', methods=["GET", "POST"])
def get_last_messages():
    """
    can be used for the chat inbox UI window
    :return: json object with list of last messages of a user
    """
    # Get the room id in the URL or set to None
    room_id = request.args.get("rid", None)

    # Get the chat list for the user
    current_user_id = session["user"]["id"]
    current_user_chats = Chat.query.filter_by(user_id=current_user_id).first()
    chat_list = current_user_chats.chat_list if current_user_chats else []

    # Initialize context that contains information about the chat room
    data = []

    for chat in chat_list:
        # Query the database to get the username of users in a user's chat list
        username = User.query.get(chat["user_id"]).username
        is_active = room_id == chat["room_id"]

        try:
            # Get the Message object for the chat room
            message = Message.query.filter_by(room_id=chat["room_id"]).first()

            # Get the last ChatMessage object in the Message's messages relationship
            last_message = message.messages[-1]

            # Get the message content of the last ChatMessage object
            last_message_content = last_message.content

        except (AttributeError, IndexError):
            # Set variable to this when no messages have been sent to the room
            last_message_content = "This place is empty. No messages ..."

        data.append({
            "username": username,
            "room_id": chat["room_id"],
            "is_active": is_active,
            "last_message": last_message_content,
        })

    return jsonify(data)
