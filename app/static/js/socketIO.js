const allMessages = document.querySelector(".all-messages")
const chatSpace = document.querySelector(".chat-space")
let chats = document.querySelectorAll('.cid');

let selectedchat = undefined

window.addEventListener("load",()=>{
    //Add socketio events as needed corresponding to how it is on the server side
    const socket = io.connect('http://127.0.0.1:5000/' );

    socket.on('connect', function() {
        socket.emit('message', {data: 'I\'m connected!'});

        /*
        let current_user = document.getElementById('userId').innerHTML;
        socket.emit('getChats', {userId:current_user});  // or we can get user_id from session in the server side
        */

        // helpful if user initiated a chat using the message button, auto select that chat in the list
        let saved = document.getElementById('chat-roomId-saved').innerHTML;
        if (saved){
            socket.emit('getMessages', {rid:saved});
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

    socket.on('getChatsJS', data=>{
        var list = document.getElementById('chats-list');
        removeAllChildNodes(list);
        var channels = data['chats']
        for (var i = 0; i < data['chatCount']; i++){
            const li = document.createElement("li");
            const div = document.createElement("div");
            const h1 = document.createElement("h1");
            const p = document.createElement("p");
            const img = document.createElement("img");
            const span = document.createElement("span");

            li.classList.add('spec-chat')

            div.classList.add('user-det-cont');
            h1.innerHTML = chats[i][i].name;
            p.innerHTML = chats[i][i].last_message; // Not implemented in the server side yet
            div.appendChild(h1);
            div.appendChild(p);

            img.src = chats[i][i].user_img;
            img.classList.add('user-profile-image');

            span.classList.add('cid');
            span.innerHTML = chats[i][i].id;

            li.appendChild(div);
            li.appendChild(img);
            li.appendChild(span);

            div.addEventListener('click', function(){

                socket.emit('join-chat',{rid: chats[i][i].id});
                socket.emit('getMessages', {rid:chats[i][i].id});
            })
            list.appendChild(li);
        }
    })


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