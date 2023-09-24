from db import db

class Chat(db.Model):
    """Controls all database crud operations related to user chats 
      """
    
    __tablename__ = "chats"

    #An incremental id for the specified chat
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    #a unique identifier for a specific chat SHA256 Encoded
    unique_id = db.Column(db.String(400), nullable=False, unique=True)
    #The message sent 
    message = db.Column(db.String(400), nullable=False)
    date_created = db.Column(db.TIMESTAMP, nullable=False)
    recipent = db.Column(db.String(400), nullable=False)
    #The user who sent the chat
    sender = db.Column(db.String(400), nullable=False)

    def __init__(self,user_id):
        pass

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
    
    def arrange_chats(self, chats, user_id):
        '''arranges all unarranged chats of a particular user into bundles of 
        messages
        chats is (usually) a tuple containing the chat data gotten from the database
        apparently, chat[5] is the recipent and chat[6] would be the sender. If you have 
        any revisions or optimizations, please notify and make them.
        user_id is the unique_id of the chat sender
        '''
        arranged_messages = []
        
        if type(chats) == list:
            for chat in chats:
                #A flag that determines whether a message has been added to the arranged_messages
                added = False
                if type(chat) == tuple:
                    ''' The message bundle is a packet of a particular user(buyer/seller) the 
                            user with the user_id in the function arg has messaged or chatted with.
                            The bundle contains details about that particular user, and an array of 
                            the messages between the user and the user with the user_id in the function arg'''
                    for arranged_message in arranged_messages:
                        if arranged_message['user_id'] == chat[5] or arranged_message['user_id'] == chat[6]:
                            arranged_message['messages'].append(
                                {
                                    "sent_to":chat[5],
                                    "sent_from":chat[6],
                                    "status":"",
                                    "send_date_and_time":chat[4],
                                    "message":chat[3]
                                }
                            )
                            added = True
                            break
                    if not added:
                        #TODO: We need to get the other data like `username`,`user_profile_image` and `user_type`
                        #from the other classes/models. For now, empty strings would be assigned to them.
                        
                        new_message_bundle = {
                            'user_id':'',
                            'user_name':'',
                            'user_profile_image':'',
                            'user_type':'',
                            'messages':[]
                        }
                        
                        #setting the user_id of the dictionary chat bundle
                        if user_id == chat[5]:
                            new_message_bundle['user_id'] = chat[6]
                        elif user_id == chat[6]:
                            new_message_bundle['user_id'] = chat[5]
                            
                        new_message_bundle['messages'].append(
                            {
                                "sent_to":chat[5],
                                "sent_from":chat[6],
                                "status":"",
                                "send_date_and_time":chat[4],
                                "message":chat[3]
                            }
                        )
                        arranged_messages.append(new_message_bundle)
                        added = True
                            
        return arranged_messages

    def retrieve_all_chats_using_user_id(self,user_id):
        """Gets all messages connected to a user(buyer or seller).
        gets all messages, chats e.t.c from the database where the 
        sender or recipent of the chat is the user with the `user_id`

        Args:
            user_id (String): _description_
            The specified unique_id of the user(buyer/seller)
        """
        return self.arrange_chats(db.session.query(Chat).get({'sender':user_id}))
    
    def retrieve_chats_in_date_packets_using_user_id(self,user_id):
        return db.session.query(Chat).get({'sent_from':user_id})

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
