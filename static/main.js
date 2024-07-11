var socket = io.connect('http://' + document.domain + ':' + location.port);
var room = "main_room";  // Example room

function sendMessage() {
    var username = document.getElementById('username').value;
    var message = document.getElementById('message').value;
    socket.emit('message', {'username': username, 'message': message, 'room': room});
    document.getElementById('message').value = '';
}

socket.on('connect', function() {
    var username = document.getElementById('username').value;
    socket.emit('join', {'username': username, 'room': room});
});

socket.on('message', function(data) {
    var chatBox = document.getElementById('chat-box');
    var newMessage = document.createElement('div');
    newMessage.innerHTML = '<strong>' + data.username + ':</strong> ' + data.message + ' <em>(' + data.sentiment + ')</em>';
    chatBox.appendChild(newMessage);
    chatBox.scrollTop = chatBox.scrollHeight;  // Scroll to the bottom
});
