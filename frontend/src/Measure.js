import React, { useState } from "react";

export function Measure() {
  const [text, setText] = useState("This is a text block.");

  const handleClick = () => {
    setText("Button was clicked!");
  };

  return (
    <div style={{ border: "1px solid #ccc", padding: "24px", borderRadius: "8px", maxWidth: "400px", margin: "24px auto" }}>
      <h2>Header</h2>
      <button onClick={handleClick}>Click Me</button>
      <div style={{ marginTop: "16px" }}>{text}</div>
    </div>
  );
}