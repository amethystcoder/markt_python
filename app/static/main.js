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
        const msgContainer = document.querySelector('.msger-chat');
        const msgWrapper = document.createElement('div');
        msgWrapper.classList.add('msg', message.sender === currentUser.unique_id ? 'right-msg' : 'left-msg');

        const msgImage = document.createElement('div');
        msgImage.classList.add('msg-img');
        msgImage.style.backgroundImage = `url(${message.sender === currentUser.unique_id ? currentUser.profile_picture : 'https://example.com/default-profile.jpg'})`;

        const msgBubble = document.createElement('div');
        msgBubble.classList.add('msg-bubble');

        const msgInfo = document.createElement('div');
        msgInfo.classList.add('msg-info');

        const msgInfoName = document.createElement('div');
        msgInfoName.classList.add('msg-info-name');
        msgInfoName.textContent = message.sender === currentUser.unique_id ? 'You' : message.sender_name;

        const msgInfoTime = document.createElement('div');
        msgInfoTime.classList.add('msg-info-time');
        msgInfoTime.textContent = new Date(message.timestamp).toLocaleTimeString();

        const msgText = document.createElement('div');
        msgText.classList.add('msg-text');
        msgText.textContent = message.message;

        msgInfo.appendChild(msgInfoName);
        msgInfo.appendChild(msgInfoTime);

        msgBubble.appendChild(msgInfo);
        msgBubble.appendChild(msgText);

        msgWrapper.appendChild(msgImage);
        msgWrapper.appendChild(msgBubble);

        msgContainer.appendChild(msgWrapper);
        msgContainer.scrollTop = msgContainer.scrollHeight;
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
