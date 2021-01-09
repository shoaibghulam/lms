//set Constant Variable
const msgerForm = get(".msger-inputarea");//form class
const msgerInput = get(".msger-input");//input class
const msgerChat = get(".msger-chat");//chat window

// Chat Bot Default Message Display 
const BOT_MSGS = [
  "Hi, how are you?",
  "Ohh... I can't understand what you trying to say. Sorry!",
  "I like to play games... But I don't know how to play!",
  "Sorry if my answers are not relevant. :))",
  "I feel sleepy! :("
];

// Icons made by Freepik from www.flaticon.com

const BOT_IMG = "https://image.flaticon.com/icons/svg/327/327779.svg";
const PERSON_IMG = "https://image.flaticon.com/icons/svg/145/145867.svg";
const BOT_NAME = "BOT";
const PERSON_NAME = "Sajad";

// Firing Event On Submit Click
msgerForm.addEventListener("submit", event => {
  
  //this prevent Defualt revoke default submit button functionality 
  event.preventDefault();

// we create another const Var and Takes above var value 
  const msgText = msgerInput.value;
  if (!msgText) return;

// here we are append our ui with sender name image and his text which was taken from input
  appendMessage(PERSON_NAME, PERSON_IMG, "right", msgText);
// after appending successfully we are clear our input field 
  msgerInput.value = "";

// here we call our botresponce function to display bots default messages which is store above in string
  botResponse();
});
var channel = pusher.subscribe('chat');
function appendMessage(name, img, side, text) {
  //   Simple solution for small apps
  const msgHTML = `
    <div class="msg ${side}-msg">
      <div class="msg-img" style="background-image: url(${img})"></div>

      <div class="msg-bubble">
        <div class="msg-info">
          <div class="msg-info-name">${name}</div>
          <div class="msg-info-time">${formatDate(new Date())}</div>
        </div>

        <div class="msg-text">${text}</div>
      </div>
    </div>
  `;

  msgerChat.insertAdjacentHTML("beforeend", msgHTML);
  msgerChat.scrollTop += 500;
}
// if you like to play with bots then remove comment from function
function botResponse() {
  const r = random(0, BOT_MSGS.length - 1);
  const msgText = BOT_MSGS[r];
  const delay = msgText.split(" ").length * 100;

  setTimeout(() => {
    appendMessage(BOT_NAME, BOT_IMG, "left", msgText);
  }, delay);
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

function random(min, max) {
  return Math.floor(Math.random() * (max - min) + min);
}
