from .chat_model import Chat
from .user_model import User
from sqlalchemy.orm import aliased
from db import db


def group_chats(user_id):
    """Groups all ungrouped chats of a particular user into bundles of messages.

    Args:
        user_id (str): The unique_id of the chat sender.

    Returns:
        list: List of dictionaries representing chat bundles.
    """
    # Create aliases for sender and recipient
    sender_alias = aliased(User)
    recipient_alias = aliased(User)

    # Fetch distinct sender-recipient pairs
    pairs = (
        db.session.query(Chat.sender, Chat.recipient)
        .filter((Chat.sender == user_id) | (Chat.recipient == user_id))
        .distinct()
        .all()
    )

    grouped_messages = []

    for sender, recipient in pairs:
        # Fetch user data using aliases
        sender_data = sender_alias.query.filter_by(unique_id=sender).first()
        recipient_data = recipient_alias.query.filter_by(unique_id=recipient).first()

        # Fetch messages between the sender and recipient
        messages = (
            Chat.query.filter(
                (
                        (Chat.sender == sender) & (Chat.recipient == recipient) |
                        (Chat.sender == recipient) & (Chat.recipient == sender)
                )
            )
            .order_by(Chat.date_created)
            .all()
        )

        # Create a bundle
        new_message_bundle = {
            'user_id': sender_data.unique_id if user_id != sender_data.unique_id else recipient_data.unique_id,
            'user_name': sender_data.username if user_id != sender_data.unique_id else recipient_data.username,
            'user_profile_image': sender_data.profile_picture if user_id != sender_data.unique_id else recipient_data.profile_picture,
            'user_type': sender_data.user_type if user_id != sender_data.unique_id else recipient_data.user_type,
            'messages': [
                {
                    "sent_to": chat.recipient,
                    "sent_from": chat.sender,
                    "status": "",
                    "send_date_and_time": chat.date_created,
                    "message": chat.message
                }
                for chat in messages
            ]
        }

        grouped_messages.append(new_message_bundle)

    return grouped_messages
