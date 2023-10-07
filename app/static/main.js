document.addEventListener("DOMContentLoaded", function() {
    var socket = io.connect("http://127.0.0.1:5000");

    socket.on('connect', function() {
        console.log('Connected to the server!');
    });

    socket.on('message', function(data) {
        displayMessage(data.sender, data.content);
    });

    function displayMessage(sender, content) {
        var messageContainer = document.getElementById('messages');
        var messageElement = document.createElement('div');
        messageElement.innerHTML = `<strong>${sender}:</strong> ${content}`;
        messageContainer.appendChild(messageElement);
    }

    window.sendMessage = function() {
        var messageInput = document.getElementById('messageInput');
        var messageContent = messageInput.value;

        socket.emit('message', {
            type: 'text',
            content: messageContent,
            sender: 'your_user_id',  // Replace with actual user ID
            recipient: 'recipient_user_id'  // Replace with actual recipient user ID
        });

        messageInput.value = '';
    };
});
