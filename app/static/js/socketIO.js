const allMessages = document.querySelector(".all-messages")
const chatSpace = document.querySelector(".chat-space")

let selectedchat = undefined

window.addEventListener("load",()=>{
    //Add socketio events as needed corresponding to how it is on the server side
    const socket = io.connect('http://127.0.0.1:5000/' );

    socket.on('connect', function() {
        socket.emit('message', {data: 'I\'m connected!'});

        let current_user = document.getElementById('userId').innerHTML;
        socket.emit('getChats', {userId:current_user});  // or we can get user_id from session in the server side

        // helpful if user initiated a chat using the message button, auto select that chat in the list
        let saved = document.getElementById('chat-roomId-saved').innerHTML;
        if (saved){
            socket.emit('getChat', {rid:saved, userId:current_user});
        }
    });

    socket.on('error', data=>{
        let username = document.getElementById('username');
        if (data['username']== username.innerHTML){
            alert(data['msg'])
        }
    });

    socket.on('message', data => {
        if (data.conf_id == "1"){
            console.log(data.msg);
        }
    });

    socket.on('receiveMessageJS', data=>{
        let roomId = document.getElementById('chat-roomId-saved').innerHTML;
        if (data['room_id']==roomId){
            const userName = document.querySelector(".user-name")
            const statusText = document.querySelector(".status-text")
            const statusColor = document.querySelector(".status-color")

            //change the status and username and profile image to that of the selected chat
            userName.innerHTML = data["name"] // Still have to work on this, maybe the chat database model
            statusText.innerHTML = data["status"] // This too

            let chatMessages = document.querySelector(".chat-messages")
            let chatImageUploader = document.querySelector("#chat-image")
            removeAllChildNodes(chatMessages)
            let chats = data['chats']
            let userId = document.getElementById('userId').innerHTML;

            if(data["status"] === "online"){
                statusColor.style.backgroundColor = "green"
            }
            else{
                statusColor.style.backgroundColor = "darkgray"
            }

            for (let i = 0; i < chats.length; i++){
                if (userId == chats[i][i].sender_id){
                    if (chats[i][i].image == 0){
                        let messageCont = document.createElement("div")
                        let messageBubble = document.createElement("div")
                        messageCont.classList.add("sent-by-you")
                        messageBubble.classList.add("bubble-sent-by-you")

                        messageBubble.innerHTML = chats[i][i].message
                        messageCont.appendChild(messageBubble)

                        chatMessages.appendChild(messageCont)
                    }
                    else if (chats[i][i].image == 1){
                        let messageCont = document.createElement("div")
                        messageCont.classList.add("sent-by-you")

                        let image = document.createElement("img")
                        image.setAttribute("src", chats[i][i].message)
                        //image.src = URL.createObjectURL(chatImageUploader.files[i])
                        image.classList.add("uploaded-images")
                        messageCont.appendChild(image)
                        chatMessages.appendChild(messageCont)
                    }
                }
                else{
                    if (chats[i][i].image == 0){
                        let messageCont = document.createElement("div")
                        let messageBubble = document.createElement("div")
                        messageCont.classList.add("sent-by-other")
                        messageBubble.classList.add("bubble-sent-by-other")

                        messageBubble.innerHTML = chats[i][i].message
                        messageCont.appendChild(messageBubble)

                        chatMessages.appendChild(messageCont)
                    }
                    else if (chats[i][i].image == 1){
                        let messageCont = document.createElement("div")
                        messageCont.classList.add("sent-by-other")

                        let image = document.createElement("img")
                        image.setAttribute("src", chats[i][i].message)
                        //image.src = URL.createObjectURL(chatImageUploader.files[i])
                        image.classList.add("uploaded-images")
                        messageCont.appendChild(image)
                        chatMessages.appendChild(messageCont)
                    }
                }
            }
            //console.log(data)
            chatMessages.scrollBy(0,chatMessages.scrollHeight)
        }

    })

    socket.on('receiveMessage', data=>{
        let roomId = document.getElementById('chat-roomId-saved').innerHTML;
        if (data['rid']==roomId){
            const userName = document.querySelector(".user-name")
            const statusText = document.querySelector(".status-text")
            const statusColor = document.querySelector(".status-color")

            //change the status and username and profile image to that of the selected chat
            userName.innerHTML = data["name"] // Still have to work on this, maybe the chat database model
            statusText.innerHTML = data["status"] // This too

            let chatMessages = document.querySelector(".chat-messages")
            let chatImageUploader = document.querySelector("#chat-image")
            removeAllChildNodes(chatMessages)
            let chats = data['chats']
            let userId = document.getElementById('userId').innerHTML;

            if(data["status"] === "online"){
                statusColor.style.backgroundColor = "green"
            }
            else{
                statusColor.style.backgroundColor = "darkgray"
            }

            if (userId == data["sender_id"]){
                if (data["image"] == 0){
                    let messageCont = document.createElement("div")
                    let messageBubble = document.createElement("div")
                    messageCont.classList.add("sent-by-you")
                    messageBubble.classList.add("bubble-sent-by-you")

                    messageBubble.innerHTML = data["message"]
                    messageCont.appendChild(messageBubble)

                    chatMessages.appendChild(messageCont)
                }
                else if (data["image"] == 1){
                    let messageCont = document.createElement("div")
                    messageCont.classList.add("sent-by-you")

                    let image = document.createElement("img")
                    image.setAttribute("src", data["message"])
                    //image.src = URL.createObjectURL(chatImageUploader.files[i])
                    image.classList.add("uploaded-images")
                    messageCont.appendChild(image)
                    chatMessages.appendChild(messageCont)
                }
            }
            else{
                if (data["image"] == 0){
                    let messageCont = document.createElement("div")
                    let messageBubble = document.createElement("div")
                    messageCont.classList.add("sent-by-other")
                    messageBubble.classList.add("bubble-sent-by-other")

                    messageBubble.innerHTML = data["message"]
                    messageCont.appendChild(messageBubble)

                    chatMessages.appendChild(messageCont)
                }
                else if (data["image"] == 1){
                    let messageCont = document.createElement("div")
                    messageCont.classList.add("sent-by-other")

                    let image = document.createElement("img")
                    image.setAttribute("src", data["message"])
                    //image.src = URL.createObjectURL(chatImageUploader.files[i])
                    image.classList.add("uploaded-images")
                    messageCont.appendChild(image)
                    chatMessages.appendChild(messageCont)
                }
            }
            //console.log(data)
            chatMessages.scrollBy(0,chatMessages.scrollHeight)
        }

    })

    socket.on('getChatJS', data=>{
        let list = document.getElementById('chats-list');
        removeAllChildNodes(list);
        let chat = data['chat']

        const li = document.createElement("li");
        const div = document.createElement("div");
        const h1 = document.createElement("h1");
        const p = document.createElement("p");
        const img = document.createElement("img");
        const span = document.createElement("span");

        li.classList.add('spec-chat')

        div.classList.add('user-det-cont');
        h1.innerHTML = chat.name;
        p.innerHTML = "";
        div.appendChild(h1);
        div.appendChild(p);

        img.src = chat.user_img;
        img.classList.add('user-profile-image');

        span.classList.add('cid');
        span.innerHTML = chat.room_id;

        li.appendChild(div);
        li.appendChild(img);
        li.appendChild(span);

        socket.emit('join-chat',{rid: chat.room_id});
        socket.emit('getMessages', {rid: chat.room_id});

        list.appendChild(li);

    })

    socket.on('getChatsJS', data=>{
        let list = document.getElementById('chats-list');
        removeAllChildNodes(list);
        let chats = data['chats']
        for (let i = 0; i < data['chatCount']; i++){
            const li = document.createElement("li");
            const div = document.createElement("div");
            const h1 = document.createElement("h1");
            const p = document.createElement("p");
            const img = document.createElement("img");
            const span = document.createElement("span");

            li.classList.add('spec-chat')

            div.classList.add('user-det-cont');
            h1.innerHTML = chats[i][i].name;
            p.innerHTML = chats[i][i].last_message;
            div.appendChild(h1);
            div.appendChild(p);

            img.src = chats[i][i].user_img;
            img.classList.add('user-profile-image');

            span.classList.add('cid');
            span.innerHTML = chats[i][i].id;

            li.appendChild(div);
            li.appendChild(img);
            li.appendChild(span);

            li.addEventListener('click', function(){
                let saved = document.getElementById('chat-roomId-saved');
                saved.innerHTML = this.childNodes[2].innerHTML; // span cid
                //console.log(saved.innerHTML)

                socket.emit('join-chat',{rid: this.childNodes[2].innerHTML});
                socket.emit('getMessages', {rid: this.childNodes[2].innerHTML});
            })
            list.appendChild(li);
        }
    })

    let chats = document.querySelectorAll('.cid');
    let sendMessage = document.getElementById('send-message');

    sendMessage.addEventListener('click', function(){
        let chatMessageInput = document.querySelector(".chat-input")
        let msg = chatMessageInput.value;
        let saved = document.getElementById('chat-roomId-saved').innerHTML;
        let userId = document.getElementById('userId').innerHTML;
        let timestamp = Date.now() / 1000

        //socket.emit('join-chat',{rid: saved});
        socket.emit('handle_message', {message: msg, rid: saved, sender_id:userId, timestamp:timestamp})

        chatMessageInput.value = "";
    });

    // When a chat is clicked, dynamically update chat-roomId-saved to the room id of the selected chat
    for (let c =0; c<chats.length;c++){
        let el = chats[c].parentNode
        //console.log(el.childNodes);
        el.addEventListener('click', function(){
            let saved = document.getElementById('chat-roomId-saved');
            //console.log(saved.innerHTML);

            saved.innerHTML=this.childNodes[5].innerHTML;
            console.log(saved.innerHTML)
            selectedchat = saved.innerHTML;
            //chatMessages.replaceChildren("")
            check_chat_status()

            //console.log(this.childNodes[5].innerHTML)
            //console.log(saved.innerHTML)
        })
    }

})
/*
    check_chat_status()
    const chatList = document.querySelector(".chats-list")
    const chatMessages = document.querySelector(".chat-messages")
    chats.forEach((chat)=>{
        //Add the chats list inbox
        let newchatelem = document.createElement("li")
        newchatelem.classList.add("spec-chat")
        newchatelem.addEventListener("click",()=>{
            //selected chat is the chat the user is currently looking at
            selectedchat = chat
            chatMessages.replaceChildren("") 
            check_chat_status()

            const userName = document.querySelector(".user-name")
            const statusText = document.querySelector(".status-text")
            const statusColor = document.querySelector(".status-color")

            //change the status and username and profile image to that of the selectedchat
            userName.innerHTML = selectedchat.user_name
            statusText.innerHTML = selectedchat.status
            if(selectedchat.status === "online"){
                statusColor.style.backgroundColor = "green"
            }
            else{
                statusColor.style.backgroundColor = "darkgray"
            }

            //display all messages of selected chat
            selectedchat.messages.forEach((message)=>{
                let messagecont = document.createElement("div")
                let messagebubble = document.createElement("div")

                if(message.sent_from === "you"){
                    messagecont.classList.add("sent-by-you")
                    messagebubble.classList.add("bubble-sent-by-you")
                }
                if(message.sent_to === "you"){
                    messagecont.classList.add("sent-by-other")
                    messagebubble.classList.add("bubble-sent-by-other")
                }

                messagebubble.innerHTML = message.message
                messagecont.appendChild(messagebubble)

                chatMessages.appendChild(messagecont)
                chatMessages.scrollBy(0,chatMessages.scrollHeight)
            })
        })

        let username = document.createElement("h1")
        username.innerHTML = chat.user_name

        let user_profile_image = document.createElement("img")
        user_profile_image.classList.add("user-profile-image")
        user_profile_image.src = chat.user_profile_image

        let lastmessage = document.createElement("p")
        lastmessage.innerHTML = cutstr(chat.messages[chat.messages.length - 1].message)

        let userdetcont = document.createElement("div")
        userdetcont.classList.add("user-det-cont")
        userdetcont.appendChild(username)
        userdetcont.appendChild(lastmessage)

        newchatelem.appendChild(user_profile_image)
        newchatelem.appendChild(userdetcont)
        chatList.appendChild(newchatelem)
    })
})
*/
function check_chat_status(){
    let noMessagesSpace = document.querySelector(".no-messages-space")
    let chatMessagesSpace = document.querySelector(".chat-messages-space")
    if(selectedchat){
        noMessagesSpace.style.display = "none"
        chatMessagesSpace.style.display = "inline-block"
    }
    else{
        noMessagesSpace.style.display = "flex"
        chatMessagesSpace.style.display = "none"
    }
}

function cutstr(str){
    if(str.length > 18)
        return str.slice(0,21)+"..."
    return str
}

function remove_selected_chat(){
    selectedchat = undefined
    check_chat_status()
    const userName = document.querySelector(".user-name")
    const statusText = document.querySelector(".status-text")
    const statusColor = document.querySelector(".status-color")

    userName.innerHTML = ""
    statusText.innerHTML = ""
    statusColor.style.backgroundColor = "darkgray"
}

/*
function send_message(){
    const chatMessages = document.querySelector(".chat-messages")
    let chatInput = document.querySelector(".chat-input")
    let text = chatInput.value
    if(text){
        selectedchat.messages.push(
            {sent_to:selectedchat.user_id,sent_from:"you",status:"unread",
            send_date_and_time:"00:04",message:text})
        let messagecont = document.createElement("div")
        let messagebubble = document.createElement("div")

        messagecont.classList.add("sent-by-you")
        messagebubble.classList.add("bubble-sent-by-you")

        messagebubble.innerHTML = text
        messagecont.appendChild(messagebubble)

        chatMessages.appendChild(messagecont)
        chatMessages.scrollBy(0,chatMessages.scrollHeight)
        chatInput.value = ""
    }
}

function handle_image_uploads(){
    const chatMessages = document.querySelector(".chat-messages")
    let chatImageUploader = document.querySelector("#chat-image")
    for(i=0;i<chatImageUploader.files.length;i++){
        let messagecont = document.createElement("div")
        messagecont.classList.add("sent-by-you")

        let image = document.createElement("img")
        image.src = URL.createObjectURL(chatImageUploader.files[i])
        image.classList.add("uploaded-images")
        messagecont.appendChild(image)
        chatMessages.appendChild(messagecont)
    }
    chatMessages.scrollBy(0,chatMessages.scrollHeight)
}
//this is another function that depends on how the data from the socketio events would look like
function handle_incoming_messages(incoming_message){}

//PS: These values are just for tests, please remove them incase you want to get the socketio stuff set
let chats = [{
    user_id:"john",user_name:"john",user_profile_image:"cdvnvhjhihnyhb",user_type:"buyer",status:"online",
    messages:[
        {sent_to:"john",sent_from:"you",status:"read",send_date_and_time:"00:04",message:"hello"},
        {sent_to:"john",sent_from:"you",status:"read",send_date_and_time:"00:04",message:"hello"},
        {sent_to:"you",sent_from:"john",status:"read",send_date_and_time:"00:04",message:"hello"},
        {sent_to:"john",sent_from:"you",status:"read",send_date_and_time:"00:04",message:"hello"},
        {sent_to:"you",sent_from:"john",status:"read",send_date_and_time:"00:04",message:"goat"},
        {sent_to:"john",sent_from:"you",status:"read",send_date_and_time:"00:04",message:"hello"},
        {sent_to:"john",sent_from:"you",status:"read",send_date_and_time:"00:04",message:"hello"},
        {sent_to:"you",sent_from:"john",status:"read",send_date_and_time:"00:04",message:"hello"},
        {sent_to:"you",sent_from:"john",status:"read",send_date_and_time:"00:04",message:"bat"},
    ]
},
{
    user_id:"maze",user_name:"maze",user_profile_image:"cdvnvhjhihnyhb",user_type:"buyer",status:"online",
    messages:[
        {sent_to:"maze",sent_from:"you",status:"read",send_date_and_time:"00:04",message:"hello"},
        {sent_to:"maze",sent_from:"you",status:"read",send_date_and_time:"00:04",message:"hello"},
        {sent_to:"you",sent_from:"maze",status:"read",send_date_and_time:"00:04",message:"hello"},
        {sent_to:"maze",sent_from:"you",status:"read",send_date_and_time:"00:04",message:"hello"},
        {sent_to:"you",sent_from:"maze",status:"read",send_date_and_time:"00:04",message:"courterrr"},
        {sent_to:"maze",sent_from:"you",status:"read",send_date_and_time:"00:04",message:"hello"},
        {sent_to:"maze",sent_from:"you",status:"read",send_date_and_time:"00:04",message:"hello"},
        {sent_to:"you",sent_from:"maze",status:"read",send_date_and_time:"00:04",message:"hello"},
        {sent_to:"you",sent_from:"maze",status:"read",send_date_and_time:"00:04",message:"hello"},
    ]
}]
*/
