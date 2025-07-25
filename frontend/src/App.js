import React, { useState, useEffect } from "react";
import io from 'socket.io-client';
import './App.css';
import { Header } from "./header";

const socket = io('http://localhost:8000');

function App() {
  const [pictureStatus, setPictureStatus] = useState("");
  const [pictureAvail, setPictureAvail] = useState(false)


  useEffect(() => {
    socket.on('connect', () => console.log('Connected:', socket.id));
    socket.on('picture_taken', data => {
      setPictureStatus(data.message);

      setTimeout(() => setPictureStatus(""), 3000); // Clear status after 3 seconds
    });
    console.log('STARTED PROGRAM')
    return () => {
      socket.off('picture_taken');
    };
  }, []);


  

   

  //measurements:
  const [tempRes, settempRes] = useState("No measurements done yet!");
  const [humidRes, sethumidRes] = useState("No measurements done yet!");
  const [lightRes, setlightRes] = useState("No measurements done yet!");
  const [distRes, setdistRes] = useState("No measurements done yet!");

  socket.on('temp', (latestTemp) => {
    settempRes(latestTemp);
    //console.log("got temp measurements" + latestTemp)
  })
  socket.on('humidity', (latestHumidity) => {
    sethumidRes(latestHumidity);
    //console.log("got Humidity measurements" + latestHumidity);
  })
  socket.on('light', (latestLight) => {
    setlightRes(latestLight);
    //console.log("got light measurements" + latestLight);
  })
  socket.on('ultrasonic', (latestUltrasonic) => {
    setdistRes(latestUltrasonic);
    //console.log("got distance measurements" + latestUltrasonic);
  })

  //Take photo

  function Camera(prop) {
    let handleClick = () => {
      socket.emit('take_picture')
          console.log('taking photo')

    }
    return (
      <div style={{ padding: "24px", borderRadius: "8px", maxWidth: "400px", margin: "24px auto" }}>
        <h2 className="Heading1">Camera:</h2>
        <button onClick={handleClick} className="Button">Take photo</button >
        {prop.pictureAvail ? (
          <div style={{ marginTop: "16px" }}>
            <img src="/downloaded_image.jpg" alt="Taken" style={{ width: "100%", borderRadius: "8px" }} />
          </div>
        ) :
          (<div className="Result">No image captured yet</div>)}
      </div>
    );
  }


  ////////
  return (
    <div className="app">
      <Header />
      <div style={{ padding: "24px", borderRadius: "8px", maxWidth: "400px", margin: "24px auto" }}>
        <h2 className="Heading1">Measurements:</h2>
        <p className="Result"> Temp value: {tempRes ? tempRes : "No measurements done yet!"} </p>
        <p className="Result"> Humidity value: {humidRes ? humidRes : "No measurements done yet!"} </p>
        <p className="Result"> Light value: {lightRes ? lightRes : "No measurements done yet!"} </p>
        <p className="Result"> Distance value: {distRes ? distRes : "No measurements done yet!"} </p>
      </div>
      <Camera pictureAvail = {pictureAvail}/>
    </div>

  );
}

export default App;
