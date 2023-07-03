
                        // chatbox display


class Chatbox {
    constructor() {
        this.args = {
            openButton: document.querySelector('.chatbox__button'),
            chatBox: document.querySelector('.chatbox__support'),
            sendButton: document.querySelector('.send__button')
        
        }

        this.state = false;
        this.messages =[];
      
    }

    display() {
        const { openButton, chatBox, sendButton } = this.args;

        openButton.addEventListener('click', () => this.toggleState(chatBox))
        openButton.addEventListener('click', () => this.onSendButton(chatBox))

        const node = chatBox.querySelector('input');
        node.addEventListener("keyup",({key})=>{
            if (key === "Enter"){
                this.onSendButton(chatBox)
            }
        })

      

     
    }

    toggleState(chatbox) {
        this.state = !this.state;

        // show or hides the box
        if (this.state) {
            chatbox.classList.add('chatbox--active')
        } else {
            chatbox.classList.remove('chatbox--active')
        }
    }

   
   
    
}
const chatbox = new Chatbox();
chatbox.display();


                          // Function to highlight code using highlight.js library

setInterval(highlightAll,1000);

function highlightAll() {
  document.querySelectorAll("pre code").forEach(block => {
    hljs.highlightBlock(block);
  });
}

    const chatBox = document.querySelector(".chat-box");
    const messageInput = document.querySelector("#message-input");
    const sendBtn = document.querySelector("#send-btn");

    function addMessage(message, isUserMessage) {
      const messageDiv = document.createElement("div");



      messageDiv.innerHTML = `
        <p class="messages__item messages__item--operator ">${message}</p>
        `;

      chatBox.appendChild(messageDiv);
      chatBox.scrollTop = chatBox.scrollHeight;
    }




    function sendMessage() {
      const message = messageInput.value.trim();

      if (message !== "") {
        addMessage(message, true);

        fetch("/api", {
          method: "POST",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify({ message })
        })
          .then(response => response.json())
          .then(data => {
                      messageInput.value = "";
            const messageDiv = document.createElement("div");
            const content = data.content;
            
            // Check if the content has code block
            const hasCodeBlock = content.includes("```");
            if (hasCodeBlock) {
              // If the content has code block, wrap it in a <pre><code> element
              const codeContent = content.replace(/```([\s\S]+?)```/g, '</p><pre><code>$1</code></pre><p>');

              messageDiv.innerHTML = `<p class="messages__item messages__item--visitor ">${codeContent}</p>`
            }
            else{
              messageDiv.innerHTML = `<p class="messages__item messages__item--visitor ">${content}</p>`
            }
            chatBox.appendChild(messageDiv);
            chatBox.scrollTop = chatBox.scrollHeight;

          })
          .catch(error => console.error(error));
      }
    }

    
    sendBtn.addEventListener("click", sendMessage);
    messageInput.addEventListener("keydown", event => {
      if (event.keyCode === 13 && !event.shiftKey) {
        event.preventDefault();
        sendMessage();
      }
    });



    // pagination


var currentPage = 1;
var itemsPerPage = 9;
var views = document.querySelectorAll("#pub-uni .view1 ");
var totalPages = Math.ceil(views.length / itemsPerPage);

function showPage(page) {
  var startIndex = (page - 1) * itemsPerPage;
  var endIndex = startIndex + itemsPerPage;

  for (var i = 0; i < views.length; i++) {
    if (i >= startIndex && i < endIndex) {
      views[i].style.display = "block";
    } else {
      views[i].style.display = "none";
    }
  }
}

function previousPage() {
  if (currentPage > 1) {
    currentPage--;
    showPage(currentPage);
  }
}

function nextPage() {
  if (currentPage < totalPages) {
    currentPage++;
    showPage(currentPage);
  }
}
showPage(currentPage);










// *********************display images from input in page
function afficherImages(event) {
  var input = event.target;
  var imagesDiv = document.getElementById('images');

  imagesDiv.innerHTML = '';

  for (var i = 0; i < input.files.length; i++) {
      var file = input.files[i];
      var reader = new FileReader();

      reader.onload = function(e) {
          var img = document.createElement('img');
          img.classList.add('imageclass')
          img.src = e.target.result;
          img.alt = file.name;
          imagesDiv.appendChild(img);
          
      }

      reader.readAsDataURL(file);
  }
}

  // **************************add new program
  var count=1;
function addNewInputs() {
  count ++
  const inputContainer = document.getElementById('inputContainer');

  // add diploma
  const newInput5Label = document.createElement('label');
  newInput5Label.textContent = 'Diploma:';
  newInput5Label.className = "form-label col";
  const newInput5 = document.createElement('input');
  newInput5.type = 'text';
  newInput5.name = 'diploma' + count;
  newInput5.className = "form-control col";

  const newInput5Div = document.createElement('div');
  const newInput6Div=document.createElement('div');
  newInput5Div.appendChild(newInput5Label);
  newInput5Div.appendChild(newInput6Div);
  newInput6Div.appendChild(newInput5);
  newInput5Div.className = "row my-4"
  newInput6Div.className ="col-9"

  // add program tittle
  const newInput1Label = document.createElement('label');
  newInput1Label.textContent = 'Program tittle:';
  newInput1Label.className = "form-label col";
  const newInput1 = document.createElement('input');
  newInput1.type = 'text';
  newInput1.name = 'program_tittle' + count;
  newInput1.className = "form-control col";

  const newInput1Div = document.createElement('div');
  const newInput3Div=document.createElement('div');
  newInput1Div.appendChild(newInput1Label);
  newInput1Div.appendChild(newInput3Div);
  newInput3Div.appendChild(newInput1);
  newInput1Div.className = "row my-4"
  newInput3Div.className ="col-9"

  // add description
  const newInput2Label = document.createElement('label');
  newInput2Label.textContent = 'Description:';
  newInput2Label.className = 'form-label col';
  const newInput2 = document.createElement('textarea');
  newInput2.type = 'text';
  newInput2.name = 'description'+count;
  newInput2.className = 'form-control col';

  const newInput2Div = document.createElement('div');
  const newInput4Div = document.createElement('div');
  newInput2Div.appendChild(newInput2Label);
  newInput2Div.appendChild(newInput4Div);
  newInput4Div.appendChild(newInput2);
  newInput2Div.className = "row my-4"
  newInput4Div.className ="col-9"

  // add new input in countainer
  inputContainer.appendChild(newInput5Div);
  inputContainer.appendChild(newInput1Div);
  inputContainer.appendChild(newInput2Div);
  
}








