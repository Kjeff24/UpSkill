var currentUser = $(".chat-container").data("current-user");
var messageContainer = document.querySelector(".msg-page");

console.log("page chat room")

// Handle form submission
$('#message').submit(function (event) {
  event.preventDefault(); // Prevent default form submission
  console.log("this is forms")
  // Serialize form data
  const formData = $(this).serialize();
  
  // Clear the input fields
  $(this).find('input[type="text"]').val('');

  // Send Ajax request
  $.ajax({
    url: `${window.location.href}send-message`, // Replace with the actual URL to handle form submission
    type: 'POST',
    data: formData,
    error: function(xhr, errmsg, err) {
      // Handle error if the request fails
      console.log(errmsg, xhr, err);
    },
    complete: function() {
      // Clear the textarea value
      $('#msg').val('');
      // Call the displayMessages function to refresh the messages
      displayMessages();

      // Scroll to the bottom of the message container
      const scrollHeight = messageContainer.scrollHeight;
      $(messageContainer).animate({ scrollTop: scrollHeight }, 'slow');

    }
  });
});

function displayMessages() {
  $.ajax({
    url: `${window.location.href}get-messages`, // Replace <room_id> with the actual room ID
    type: "GET",
    dataType: "json",
    success: function (response) {
      // Clear the message container
      $('.msg-page').empty();

      response.forEach((message) => {
        if (message.user === currentUser) {
          messageContainer.innerHTML += `
            <div class="outgoing-chats">
                <div class="outgoing-chats-img">
                    <a href="/profile/${message.user_id}">
                        <img src="${message.avatar}" style="width: 50px; border-radius: 50%; padding: 5px;"/>
                    </a>
                </div>
                <div class="outgoing-msg">
                    <div class="outgoing-chats-msg">
                        
                        <p class="multi-msg">
                            <span style="font-size: 12px;">${message.user}:</span>
                            <br>
                            ${message.body}
                            <span class="time">
                                ${message.created}
                            </span>
                        </p>
                    </div>
                </div>
            </div>
          `
        }
        else {
          messageContainer.innerHTML += `
            <div class="received-chats">
              <div class="received-chats-img">
                  <a href="/profile/${message.user_id}">
                      <img  src="${message.avatar}" style="width: 50px; border-radius: 50%; padding: 5px;"/>  
                  </a>
              </div>
              <div class="received-msg">
                  <div class="received-msg-inbox">
                      <p class="single-msg">
                          <span style="font-size: 12px;">${message.user}:</span>
                          <br>
                          ${message.body}
                          <span class="time">
                          ${message.created}
                          </span>
                      </p>
                  </div>
              </div>
            </div>
          `
        }
        
      });
    },
  });
}

function scrollToBottom() {
  messageContainer.scrollTop = messageContainer.scrollHeight;
}

function scrollToTop() {
  messageContainer.scrollTop = 0;
}

// Call the displayMessages function initially to load the existing messages
displayMessages();

// Call the displayMessages function periodically to update the messages
setInterval(displayMessages, 5000);
