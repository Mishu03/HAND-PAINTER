class WebSocketService {
  constructor() {
    this.ws = null;
    this.callbacks = [];
  }

  connect(url) {
    this.ws = new WebSocket(url);

    this.ws.onopen = () => {
      console.log("WebSocket connected");
    };

    this.ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        this.callbacks.forEach((cb) => cb(data));
      } catch (e) {
        console.error("Invalid JSON:", event.data);
      }
    };

    this.ws.onclose = () => {
      console.log("WebSocket disconnected. Reconnecting in 2s...");
      setTimeout(() => this.connect(url), 2000);
    };
  }

  onMessage(callback) {
    this.callbacks.push(callback);
  }
}

export default new WebSocketService();