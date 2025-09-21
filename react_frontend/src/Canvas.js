import React, { useRef, useEffect, useState } from "react";
import wsService from "./WebSocketService";

const Canvas = () => {
  const canvasRef = useRef(null);
  const [strokes, setStrokes] = useState([]);

  useEffect(() => {
    const canvas = canvasRef.current;
    const ctx = canvas.getContext("2d");

    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;

    // Draw all strokes
    const drawStrokes = () => {
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      strokes.forEach((stroke) => {
        ctx.beginPath();
        ctx.arc(stroke.x, stroke.y, stroke.brushSize / 2, 0, 2 * Math.PI);
        ctx.fillStyle = "blue"; // Change color dynamically if needed
        ctx.fill();
      });
    };

    drawStrokes();
  }, [strokes]);

  // Listen to WebSocket messages
  useEffect(() => {
    wsService.onMessage((data) => {
      setStrokes((prev) => [...prev, data]);
    });
  }, []);

  return <canvas ref={canvasRef} style={{ display: "block" }} />;
};

export default Canvas;