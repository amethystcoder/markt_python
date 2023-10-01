// main.js

document.addEventListener('DOMContentLoaded', () => {
    const socket = io.connect('http://' + document.domain + ':' + location.port);

    // Connect Event
    socket.on('connect', () => {
        console.log('Connected to WebSocket');
    });

    // Custom Event (you can add more as needed)
    socket.on('message', (data) => {
        console.log('Received message:', data);
        // Handle the received message on the client side
    });

    // Add more event handlers as needed

    // Disconnect Event
    socket.on('disconnect', () => {
        console.log('Disconnected from WebSocket');
    });
});
