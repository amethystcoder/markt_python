from .chat_model import Chat
from .user_model import User


def group_chats(user_id):
    """Groups all ungrouped chats of a particular user into bundles of messages.

    Args:
        user_id (str): The unique_id of the chat sender.

    Returns:
        list: List of dictionaries representing chat bundles.
    """
    grouped_messages = []

    # Fetch chats from the database using SQLAlchemy query
    chats = Chat.query.filter((Chat.sender == user_id) | (Chat.recipient == user_id)).all()

    if chats:
        for chat in chats:
            # A flag that determines whether a message has been added to the grouped_messages
            added = False

            if isinstance(chat, Chat):
                for grouped_message in grouped_messages:
                    if grouped_message['user_id'] == chat.recipient or grouped_message['user_id'] == chat.sender:
                        grouped_message['messages'].append(
                            {
                                "sent_to": chat.recipient,
                                "sent_from": chat.sender,
                                "status": "",
                                "send_date_and_time": chat.date_created,
                                "message": chat.message
                            }
                        )
                        added = True
                        break

                if not added:
                    # Fetch other data like `username`, `user_profile_image`, and `user_type` from the User model
                    user = User.query.filter_by(unique_id=new_message_bundle['user_id']).first()

                    new_message_bundle = {
                        'user_id': user.unique_id,
                        'user_name': user.username,
                        'user_profile_image': user.profile_picture,
                        'user_type': user.user_type,
                        'messages': [
                            {
                                "sent_to": chat.recipient,
                                "sent_from": chat.sender,
                                "status": "",
                                "send_date_and_time": chat.date_created,
                                "message": chat.message
                            }
                        ]
                    }

                    grouped_messages.append(new_message_bundle)
                    added = True

    return grouped_messages
