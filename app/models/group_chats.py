from .chat_model import Chat
from .user_model import User
from sqlalchemy import or_


def group_chats(user_id, page=1, messages_per_page=10):
    """Groups all ungrouped chats of a particular user into bundles of messages.

    Args:
        user_id (str): The unique_id of the chat sender.
        page (int): Page number for pagination.
        messages_per_page (int): Number of messages to fetch per page.

    Returns:
        list: List of dictionaries representing chat bundles.
    """
    grouped_messages = []

    # Calculate offset for pagination
    offset = (page - 1) * messages_per_page

    # Fetch chats from the database using SQLAlchemy query
    chats = (
        Chat.query
        .filter(or_(Chat.sender == user_id, Chat.recipient == user_id))
        .order_by(Chat.timestamp.desc())  # Change to use timestamp for ordering
        .offset(offset)
        .limit(messages_per_page)
        .all()
    )

    if chats:
        for chat in chats:
            # Fetch other data like `username`, `user_profile_image`, and `user_type` from the User model
            user = User.query.filter_by(unique_id=chat.sender).first()

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
                        "send_date_and_time": chat.timestamp,  # Change to use timestamp
                        "message": chat.message
                    }
                ]
            }

            grouped_messages.append(new_message_bundle)

    return grouped_messages
