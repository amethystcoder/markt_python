// Will work iteratively with the frontend team for needed functions and styling

// TODO: Get the seller's email from the user's profile.
var sellerEmail;

async function load_room_id() {
  // TODO: Change the URL to match your backend API.
  const response = await fetch("/new_chat/" + sellerEmail);
  const data = await response.json();
  return data["room_id"];
}

async function load_messages() {
  // TODO: Change the URL to match your backend API.
  const response = await fetch("/get_messages?rid=" + await load_room_id());
  const data = await response.json();
  return data;
}

async function load_user() {
  // TODO: Change the URL to match your backend API.
  const response = await fetch("/get_user");
  const data = await response.json();
  return data["name"];
}

async function load_last_message() {
  // TODO: Change the URL to match your backend API.
  const response = await fetch("/get_last_message?rid=" + await load_room_id());
  const data = await response.json();
  return data;
}

const socket = io.connect('http://' + document.domain + ':' + location.port + '/?rid=' + await load_room_id());

// Sample socket code when connected.
socket.on('connect', function () {
  socket.emit('join-chat', {
    rid: await load_room_id()
  })
});

socket.on('joined-chat', function (msg) {
  console.log(msg);
});

// TODO: Add an event listener to the send message button or other element.
// When the event is triggered, call the following function.
async function sendMessage() {
  // Get the user's input message.
  const user_input = document.getElementById("message-input").value;

  // Get the user's name and ID.
  const user = await load_user();

  // Get the room ID.
  const room_id = await load_room_id();

  // Emit a message to the server.
  socket.emit('outgoing', {
    timestamp: Date.now() / 1000,
    sender_username: user.username,
    sender_id: user.id,
    content: user_input,
    message_type: 'text',
    rid: room_id
  });
}

// TODO: Add an event listener to the send image button or other element.
// When the event is triggered, call the following function.
async function sendImage() {
  // Get the file from the image input field.
  const file = document.getElementById("image-input").files[0];

  // Get the user's name and ID.
  const user = await load_user();

  // Get the room ID.
  const room_id = await load_room_id();

  // Emit an image message to the server.
  socket.emit('imageData', {
    timestamp: Date.now() / 1000,
    sender_username: user.username,
    sender_id: user.id,
    image_url: file,
    message_type: 'image',
    rid: room_id
  });
}

// TODO: Add an event listener to the socket's `message` event.
socket.on('message', function (message) {
  // Get the message object.
  const messageObj = JSON.parse(message);

  // Get the message content.
  const messageContent = messageObj.content;

  // Get the sender's username.
  const senderUsername = messageObj.sender_username;

  // TODO: Display the message in the chat window. For example, you could append the message to a DOM element.
  // Example:
  // const chatWindow = document.getElementById("chat-window");
  // const newMessageElement = document.createElement("div");
  // newMessageElement.innerHTML = `<b>${senderUsername}:</b> ${messageContent}`;
  // chatWindow.appendChild(newMessageElement);

  // **Best practice:** It is best practice to use a different event for displaying text messages and image messages. This will make your code more modular and easier to maintain.

  // Example:
  // socket.on('text-message', function (message) {
  //   // Display the text message.
  // });

  // socket.on('image-message', function (message) {
  //   // Display the image message.
  // });
});
