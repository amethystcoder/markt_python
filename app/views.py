from flask import Blueprint, render_template

chat_test_blp = Blueprint('example', __name__)


@chat_test_blp.route('/chat')
def chat_page():
    return render_template('index.html')
