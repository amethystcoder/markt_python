function appendMessage(img, msg, side = "left") {
    const time = formatDate(new Date());
    const date = msg.time || time; // Use provided time or current time

    const displayName = side === 'right' ? 'You' : msg.name;

    const msgHTML = `
        <div class="msg ${side}-msg">
            <div class="msg-img" style="background-image: url(${img})"></div>
            <div class="msg-bubble">
                <div class="msg-info">
                    <div class="msg-info-name ${side}-name">${displayName}</div>
                    <div class="msg-info-time">${date}</div>
                </div>
                <div class="msg-text">${msg.message}</div>
            </div>
        </div>
    `;

    const msgerChat = document.getElementById("messages");
    msgerChat.insertAdjacentHTML("beforeend", msgHTML);
    msgerChat.scrollTop += 500;
}

// Utils
function get(selector, root = document) {
  return root.querySelector(selector);
}

function formatDate(date) {
  const h = "0" + date.getHours();
  const m = "0" + date.getMinutes();

  return `${h.slice(-2)}:${m.slice(-2)}`;
}

document.addEventListener('DOMContentLoaded', function () {
    // Connect to the WebSocket server
    const socket = io.connect('http://127.0.0.1:5000');

    // Replace these variables with actual user information when integrated
    const currentUser = {
        unique_id: 'user123',
        username: 'John Doe', // Change to actual username
        profile_picture: 'https://example.com/profile.jpg' // Change to actual profile picture URL
    };

    // Function to display a message in the chat
    function displayMessage(message) {
        const msgContainer = document.getElementById('messages');
        const side = currentUser.unique_id === message.sender ? 'right' : 'left';
        appendMessage(currentUser.profile_picture, { name: message.sender_name, time: message.timestamp, message: message.message }, side);
    }

    // Event listener for receiving a message
    socket.on('message', function (data) {
        displayMessage(data);
    });

    // Event listener for a user connecting
    socket.on('connect', function (data) {
        console.log('Connected to server:', data);
    });

    // Event listener for a user disconnecting
    socket.on('disconnect', function (data) {
        console.log('Disconnected from server:', data);
    });

    // Event listener for typing notification
    socket.on('typing', function (data) {
        console.log(`${data.sender_name} is typing...`);
    });

    // Event listener for read notification
    socket.on('read', function (data) {
        console.log(`${data.sender_name} has read your message.`);
    });

    // Function to handle sending a message
    function sendMessage(message) {
        // Replace with actual logic to send a message
        const messageData = {
            type: 'message',
            sent_from: currentUser.unique_id,
            sent_to: 'recipient123', // Replace with actual recipient ID
            message: message,
            send_date_and_time: new Date().toISOString()
        };

        // Send the message to the server
        socket.emit('message', JSON.stringify(messageData));

        // Display the sent message
        displayMessage({
            sender: currentUser.unique_id,
            sender_name: 'You',
            timestamp: messageData.send_date_and_time,
            message: messageData.message
        });
    }

    // Replace this with actual logic to handle form submission
    const form = document.querySelector('.msger-inputarea');
    form.addEventListener('submit', function (event) {
        event.preventDefault();
        const input = document.querySelector('.msger-input');
        const message = input.value.trim();

        if (message !== '') {
            // Call the function to send the message
            sendMessage(message);
            input.value = '';
        }
    });
});
