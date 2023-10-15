from flask import Blueprint, render_template

chat_test_blp = Blueprint('example', __name__)


@chat_test_blp.route('/chat')
def chat_page():
    return render_template('index.html')


@chat_test_blp.route('/get_user')
def get_user():
    """

    :return: json object with current user
    """
    pass


@chat_test_blp.route('/new_chat')
def new_chat():
    """

    :return: json object with room_id
    """
    pass


@chat_test_blp.route('/get_messages/', methods=["GET", "POST"])
def get_messages():
    """

    :return: all messages in a particular room_id
    """
    pass
