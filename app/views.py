#
# +-- THIS WOULD BE WORKED ON, AS IT WAS TREATED WITH FULL RENDERING IN MIND --+
# +-- IT COULD CONTRIBUTE TO TESTING IN THE FUTURE, NEVERTHELESS --+

from flask import Blueprint, render_template, request, url_for, redirect, session, flash, jsonify
from app.models import *
from functools import wraps

from db import db
from app import socketio

views = Blueprint('views', __name__, static_folder='static', template_folder='templates')


# NOTE, we create a new chat list for any newly registered user (the register route)


# Login decorator to ensure user is logged in before accessing certain routes
def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if "user" not in session:
            return redirect(url_for("views.login"))
        return f(*args, **kwargs)

    return decorated


# Register a new user and hash password
@views.route("/register", methods=["GET", "POST"])
def register():
    """
    Handles user registration and password hashing.

    Returns:
        Response: Flask response object.
    """
    pass


@views.route("/login", methods=["GET", "POST"])
def login():
    """
    Handles user login and session creation.

    Returns:
        Response: Flask response object.
    """
    pass


@views.route('/')
def landing_page():
    """
    Renders landing page interface.

    Returns:
        Response: Flask response object.
    """


# Serves as api for initiating/creating chat
@views.route("/new-chat/", methods=["GET"])
@login_required
def new_chat():
    """
    Creates a new chat room and adds users to the chat list.

    Returns:
        Response: Flask response object.
    """
    user_id = session["user"]["id"]
    # Get the other user in the URL or set to None
    recipient_user_id = request.args.get("recipient_id", None)

    recipient_user = User.query.filter_by(id=recipient_user_id).first()

    existing_chat = Chat.query.filter_by(user_id=user_id).first()

    # Check if the new chat is already in the chat list
    if recipient_user.id not in [user_chat["user_id"] for user_chat in existing_chat.chat_list]:
        # Generate a room_id
        room_id = Chat.generate_unique_id()

        # Add the new chat to the chat list of the current user
        updated_chat_list = existing_chat.chat_list + [{"user_id": recipient_user.id, "room_id": room_id}]
        existing_chat.chat_list = updated_chat_list

        # Save the changes to the database
        existing_chat.save_to_db()

        # Create a new chat list for the recipient user if it doesn't exist
        recipient_chat = Chat.query.filter_by(user_id=recipient_user.id).first()
        if not recipient_chat:
            recipient_chat = Chat(user_id=recipient_user.id, chat_list=[])
            recipient_chat.save_to_db()

        # Add the new chat to the chat list of the recipient user
        updated_chat_list = recipient_chat.chat_list + [{"user_id": user_id, "room_id": room_id}]
        recipient_chat.chat_list = updated_chat_list
        recipient_chat.save_to_db()

        # Create a new message entry for the chat room
        new_message = Message(room_id=room_id)
        new_message.save_to_db()

    room_id = None
    for user_chat in existing_chat.chat_list:
        if user_chat["user_id"] == recipient_user.id:
            room_id = user_chat["room_id"]
            break

    return redirect(url_for("views.chat", rid=room_id))


@views.route("/chat")
@login_required
def chat():
    """
    Renders the chat interface and displays chat messages.

    Returns:
        Response: Flask response object.
    """
    # Get the room id in the URL or set to None
    room_id = request.args.get("rid", None)  # To auto select that chat in the list --> UI

    # Get the chat list for the user
    current_user_id = session["user"]["id"]
    current_user_chats = Chat.query.filter_by(user_id=current_user_id).first()
    chat_list = current_user_chats.chat_list if current_user_chats else []

    # Initialize context that contains information about the chat room
    data = []

    for chat in chat_list:
        # Query the database to get the username of users in a user's chat list
        username = User.query.get(chat["user_id"]).username
        user_image = User.query.get(chat["user_id"]).profile_image
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
            "user_image": user_image,
            "room_id": chat["room_id"],
            "is_active": is_active,
            "last_message": last_message_content,
        })

    # Get all the message history in a certain room
    messages = Message.query.filter_by(room_id=room_id).first().messages if room_id else []

    return render_template(
        "chat.html",
        user_data=session["user"],
        room_id=room_id,
        data=data,
        messages=messages,
    )


@views.route("/imageUploadChat", methods=["POST"])
@login_required
def upload_image():
    """
    The route expects an image file in the request (assuming the file input in the form has the name attribute set to 'image').
    TODO
    - Get chat's room id e.g rid = request.form.get('imagerid')
    - The image is then uploaded to a cloud storage or any method we would utilize(maybe the upload folder or storage bucket)
    - A thumbnail URL can be generated using the cloud service (or functions from ImageSaver class).
    - This URL is then stored in the message entry for the chat room, and the fact that it's an image (set image to 1).
    - Set the session variable 'imageid' to the ID of chatMessage entry the newly created image

    """
    # Redirect to the 'chat' route after image upload
    return redirect(url_for('views.chat'))
