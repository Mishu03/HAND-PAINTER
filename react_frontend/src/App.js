import React, { useEffect } from "react";
import Canvas from "./Canvas";
import wsService from "./WebSocketService";

function App() {
  useEffect(() => {
    wsService.connect("ws://localhost:8765"); // Make sure this matches your Python WS server
  }, []);

  return (
    <div>
      <h1>Hand Gesture Painter</h1>
      <Canvas />
    </div>
  );
}

export default App;