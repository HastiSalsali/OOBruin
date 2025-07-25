import React, { useState } from "react";

export function Camera() {
      const [photo , setPhoto] = useState(null);
      let handleClick = () => {

      }
  return (
    <div style={{  padding: "24px", borderRadius: "8px", maxWidth: "400px", margin: "24px auto" }}>
      <h2 className="Heading1">Camera:</h2>
      <button onClick={handleClick} className= "Button">Take photo</button >
      
    </div>
  );
}