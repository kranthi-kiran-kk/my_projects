function sendMessage() {
  var userInput = document.getElementById("user-input").value;
  var chatMessages = document.getElementById("chat-messages");
  var chatMessage = document.createElement("div");
  chatMessage.textContent = "User: " + userInput;
  chatMessages.appendChild(chatMessage);

  // Call chatbot API or logic to get response
  var botResponse = "Chatbot: This is a dummy response.";
  var botMessage = document.createElement("div");
  botMessage.textContent = botResponse;
  chatMessages.appendChild(botMessage);
  
  // Clear input field
  document.getElementById("user-input").value = "";

  // Scroll to bottom of chat messages
  chatMessages.scrollTop = chatMessages.scrollHeight;
}
