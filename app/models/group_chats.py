from .chat_model import Chat


def group_chats(chats, user_id):
    """Arranges all unarranged chats of a particular user into bundles of messages.

    `chats` is a list of objects of type chat.
    `user_id` is the unique_id of the chat sender.
    """
    group_messages = []

    if isinstance(chats, list):
        for chat in chats:
            added = False
            if isinstance(chat, Chat):
                for group_message in group_messages:
                    if group_message['user_id'] == chat.recipent or group_message['user_id'] == chat.sender:
                        group_message['messages'].append(
                            {
                                "sent_to": chat.recipent,
                                "sent_from": chat.sender,
                                "status": "",
                                "send_date_and_time": chat.date_created,
                                "message": chat.message
                            }
                        )
                        added = True
                        break
                if not added:
                    new_message_bundle = {
                        'user_id': '',
                        'user_name': '',  # You can fill in these details from the user model
                        'user_profile_image': '',  # You can fill in these details from the user model
                        'user_type': '',  # You can fill in these details from the user model
                        'messages': []
                    }

                    if user_id == chat.recipent:
                        new_message_bundle['user_id'] = chat.sender
                    elif user_id == chat.sender:
                        new_message_bundle['user_id'] = chat.recipent

                    new_message_bundle['messages'].append(
                        {
                            "sent_to": chat.recipent,
                            "sent_from": chat.sender,
                            "status": "",
                            "send_date_and_time": chat.date_created,
                            "message": chat.message
                        }
                    )
                    group_messages.append(new_message_bundle)
                    added = True

    return group_messages
