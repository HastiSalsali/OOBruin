import React, { useState } from "react";

export function Measure() {
let temp, humid, light, dist;
  const [tempRes, settempRes] = useState("No measurements done yet!");
    const [humidRes, sethumidRes] = useState("No measurements done yet!");
    const [lightRes, setlightRes] = useState("No measurements done yet!");
    const [distRes, setdistRes] = useState("No measurements done yet!");
  const handleClickTemp = () => {
    settempRes("Temp:" + temp);
  };
  const handleClickHumid = () => {
    sethumidRes("Humid:" + temp);
  };
  const handleClickLight = () => {
    setlightRes("Light:" + temp);
  };
  const handleClickDist = () => {
    setdistRes("Distance:" + temp);
  };

  return (
    <div style={{  padding: "24px", borderRadius: "8px", maxWidth: "400px", margin: "24px auto" }}>
      <h2 className="Heading1">Measurements:</h2>
      <button onClick={handleClickTemp} className= "Button">Measure tempereature</button>
      <div className="Result">{tempRes}</div>

      <button onClick={handleClickHumid} className= "Button">Measure humidity</button>
      <div className="Result">{humidRes}</div>

      <button onClick={handleClickLight} className= "Button">Measure light intensity</button>
      <div className="Result">{lightRes}</div>

      <button onClick={handleClickDist} className= "Button">Measure distance</button>
      <div className="Result">{distRes}</div>
    </div>
  );
}