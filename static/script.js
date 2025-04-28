const CONFIG = {
  CAMPAIGN: 'USA_bot_IA',
  LOGOUT_TIMEOUT: 600000, // 10 minutes in milliseconds
  API_ENDPOINTS: {
    LOGIN: '/login',
    CHAT: '/chat',
    LOGOUT: '/logout'
  }
};

let state = {
  currentPrompt: '',
  guid: '',
  name: '',
  mail: '',
  timeoutId: null
};

const SessionManager = {
  initialize() {
    const searchParams = new URLSearchParams(window.location.search);
    state.name = searchParams.get('name');
    state.mail = searchParams.get('mail');
    state.guid = this.generateUUID();
  },

  generateUUID() {
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, c => {
      const r = Math.random() * 16 | 0;
      return (c === 'x' ? r : (r & 0x3 | 0x8)).toString(16);
    });
  },

  startLogoutTimer() {
    if (state.timeoutId) clearTimeout(state.timeoutId);
    state.timeoutId = setTimeout(() => this.logout(), CONFIG.LOGOUT_TIMEOUT);
  },

  async logout() {
    try {
      await fetch(`${CONFIG.API_ENDPOINTS.LOGOUT}?guid=${state.guid}`);
    } catch (error) {
      console.error('Error during logout:', error);
    }
  }
};


// Setup event listeners
document.addEventListener('mousemove keydown click', () => {
  SessionManager.startLogoutTimer();
});

document.getElementById('question').addEventListener('keypress', (event) => {
  if (event.key === 'Enter') {
    ChatManager.sendMessage(event.target.value);
  }
});

document.getElementById('closeButton').addEventListener('click', () => {
  const params = new URLSearchParams({
    name: state.name,
    mail: state.mail,
    guid: state.guid,
    campaign: CONFIG.CAMPAIGN
  });

  SessionManager.logout();
  window.location.href = `/survey?${params}`;
});

document.addEventListener('DOMContentLoaded', () => {
  SessionManager.initialize();
  login();
  ChatManager.initializeTextArea();
});

/**
 * Function that handles user login process.
 *
 * @return {void} No return value
 */
function login() {
  if (!state.name || state.name === "null") {
    window.location.href = '/form';
  } else {
    $.ajax({
      url: CONFIG.API_ENDPOINTS.LOGIN,
      type: "POST",
      contentType: "application/json",
      data: JSON.stringify({ 
        name: state.name, 
        mail: state.mail, 
        guid: state.guid 
      })
    });
  }
}

const ChatManager = {
  async sendMessage(message) {
    if (!message.trim()) return;

    this.disableInput(true);
    
    // Display user message first
    this.displayMessage(message, 'sent');
    
    // Show typing indicator after user message
    this.showTypingIndicator();
    
    try {
      const response = await fetch(CONFIG.API_ENDPOINTS.CHAT, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          question: message,
          conversation: document.getElementById('conversation').value,
          guid: state.guid
        })
      });

      const data = await response.json();
      
      if (data.answer) {
        this.hideTypingIndicator(); // Hide typing indicator before showing response
        this.displayMessage(data.answer, 'received');
      } else if (data.error) {
        this.hideTypingIndicator(); // Hide typing indicator before showing error
        this.showErrorMessage();
      }

    } catch (error) {
      console.error('Error sending message:', error);
      this.hideTypingIndicator(); // Hide typing indicator before showing error
      this.showErrorMessage();
    } finally {
      this.disableInput(false);
      // Clear input after sending
      document.getElementById('question').value = '';
    }
  },

  displayMessage(message, type) {
    const chatCanvas = document.getElementById('chatCanvas');
    const messageHTML = `
            <div class="message ${type}">
                ${type === 'received' ? this.formatMessage(message) : message}
            </div>
            <div class="spacer"></div>
        `;

    chatCanvas.insertAdjacentHTML('beforeend', messageHTML);
    this.scrollToBottom();
  },

  formatMessage(message) {
    return message
      .replace(/### (.*?)(\n|$)/g, '<h3>$1</h3>') // Handle h3 headers
      .replace(/## (.*?)(\n|$)/g, '<h2>$1</h2>') // Handle h2 headers
      .replace(/# (.*?)(\n|$)/g, '<h1>$1</h1>') // Handle h1 headers
      .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
      .replace(/\n/g, '<br>');
  },

  scrollToBottom() {
    const chatElement = document.getElementById('chatCanvas');
    chatElement.scrollTop = chatElement.scrollHeight;
  },

  disableInput(disable) {
    const textarea = document.getElementById("question");
    const sendButton = document.getElementById("send");
    
    textarea.disabled = disable;
    sendButton.disabled = disable;
    
    if (!disable) {
      textarea.style.height = 'auto';
      textarea.style.height = Math.min(textarea.scrollHeight, 150) + 'px';
    }
  },

  showTypingIndicator() {
    if (!document.getElementById("typingMessage")) {
      const chatElement = document.getElementById("chatCanvas");
      const typingHTML = `<div class="message received" id="typingMessage">Escribiendo</div><div class="spacer"></div>`;
      chatElement.insertAdjacentHTML('beforeend', typingHTML);
      this.scrollToBottom();

      // Add animation interval
      this.typingInterval = setInterval(() => {
        const typingMessage = document.getElementById("typingMessage");
        if (typingMessage) {
          const dots = typingMessage.innerHTML.split("Escribiendo")[1] || "";
          typingMessage.innerHTML = dots.length >= 3 
            ? "Escribiendo" 
            : "Escribiendo" + dots + ".";
        }
      }, 500);
    }
  },

  hideTypingIndicator() {
    const typingMessage = document.getElementById("typingMessage");
    if (typingMessage) {
      clearInterval(this.typingInterval); // Clear the animation interval
      typingMessage.remove();
    }
  },

  showErrorMessage() {
    this.displayMessage("Error al enviar el mensaje. Por favor, inténtelo de nuevo.", "received");
  },

  initializeTextArea() {
    const textarea = document.getElementById("question");
    
    // Set initial height
    textarea.style.height = 'auto';
    textarea.style.height = textarea.scrollHeight + 'px';
    
    // Add input event listener for dynamic resizing
    textarea.addEventListener('input', function() {
      this.style.height = 'auto';
      const newHeight = Math.min(this.scrollHeight, 150); // Max height of 150px
      this.style.height = newHeight + 'px';
    });

    // Handle Enter key (Shift+Enter for new line)
    textarea.addEventListener('keydown', (event) => {
      if (event.key === 'Enter' && !event.shiftKey) {
        event.preventDefault();
        this.sendMessage(event.target.value);
      }
    });
  }
};