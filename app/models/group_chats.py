from .chat_model import Chat
    
def group_chats(chats, user_id):
    '''arranges all unarranged chats of a particular user into bundles of 
        messages
        `chats` is a list of objects of type chat
        user_id is the unique_id of the chat sender
        '''
    #extract the users(recipents) of user_id
    present_user_recipents = []
    for rec in chats:
        if rec.recipent is not user_id:
            present_user_recipents.append(rec.recipent)
        elif rec.sender is not user_id:
            present_user_recipents.append(rec.sender)

    #remove duplicates
    unduplicated_user_rep = list(set(present_user_recipents))
    
    #TODO: We need to get the other data like `username`,`user_profile_image` and `user_type`
    #from the other classes/models. For now, empty strings would be assigned to them.
    
    #group users(recipents into bundles)
    grouped_chats = []
    [grouped_chats.append({'user_id':grp_ch,'user_name':'','user_profile_image':'','messages':[]}) for grp_ch in unduplicated_user_rep]
    
    #arrange each message in those bundles
    for msgs in grouped_chats:
        msgs["messages"] = [{"sent_to":chat.recipent,"sent_from":chat.sender,"status":"","send_date_and_time":chat.date_created,"message":chat.message} for chat in filter(lambda x:x.recipent == msgs["user_id"] or x.sender == msgs["user_id"],chats)]
    
    return grouped_chats