// OPTION A - if we don't want the client/socketio script linked to all templated related to initiating chat
// Link all html templates with the chat messsage/icon to this script

function createChat(recipientId) {
    $.ajax({
        url: "/new-chat/?recipient_id=" + recipientId,
        type: "GET",  // or "POST" depending on the route definition
        success: function(response) {
            console.log("Chat created successfully");
            // Handle success response if needed
        },
        error: function(error) {
            console.error("Error creating chat", error);
            // Handle error response if needed
        }
    });
}
