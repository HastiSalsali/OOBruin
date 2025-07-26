import React, { useState, useEffect } from "react";
import io from 'socket.io-client';
import './App.css';
import { Header } from "./header";

const socket = io('http://localhost:8000');

function App() {
  const [pictureStatus, setPictureStatus] = useState(""); 
  const [NewPic, setNewPic] = useState(()=> (<p className="Result">No pic yet!</p>))
  const [NewAudio, setNewAudio] = useState(()=> (<p className="Result">No pic yet!</p>))


  useEffect(() => {
    socket.on('connect', () => console.log('Connected:', socket.id));
    socket.on('picture_taken', data => {
      setPictureStatus(data.message);
      console.log('GOT PHOTO')

      setTimeout(() => setPictureStatus(""), 3000); // Clear status after 3 seconds
    });
    console.log('STARTED PROGRAM')
    return () => {
      socket.off('picture_taken');
    };
  }, []);

  //measurements:
  const [tempRes, settempRes] = useState(null);
  const [humidRes, sethumidRes] = useState(null);
  const [lightRes, setlightRes] = useState(null);
  const [distRes, setdistRes] = useState(null);

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


  //Take photo:
  let handleCamClick = () => {
    const timestamp = Date.now();
    socket.emit('take_picture')
    console.log('taking photo')
    setNewPic(() => (
      <img src={`/downloaded_image.jpg?${timestamp}`} alt="No photo to display" style={{ width: "100%", borderRadius: "8px" }} />
    ))
    setNewAudio(() => (
      <audio controls style={{ width: "100%", marginTop: "16px" }}>
        <source src={`/image_to_speach.mp3?${timestamp}`}  type="audio/mpeg" />
        Your browser does not support the audio element.
      </audio>
    ))
  }

  //Send message:
  let handleSendClick = () => {

  }


  function Camera() {

    return (
      <div style={{ padding: "24px", borderRadius: "8px", maxWidth: "400px", margin: "24px auto" }}>
        <h2 className="Heading1">Camera:</h2>
        <button onClick={handleCamClick} className="Button">Take photo</button >
        <div style={{ marginTop: "16px" }}>
          {/* {pictureStatus === 'Picture analyzed successfully!' ? (
            NewPic
          ) : (
            <div className="Result">No image captured yet</div>
          )}
          {NewAudio != null ? (NewAudio) : <div className="Result"> No audio messages rendered yet</div>} */}
          {NewPic}
          {NewAudio}
        </div>
      </div>
    );
  }


  //layout
  return (
    <div className="app">
      <Header />
      <div className="main-content">
        {/* Left Column - Measurements */}
        <div className="measurements-section">
          <h2 className="Heading1">Measurements:</h2>
          <p className="Result"> <b>Temp value:</b> {tempRes ? tempRes : "No measurements done yet!"} </p>
          <p className="Result"> <b>Humidity value:</b> {humidRes ? humidRes : "No measurements done yet!"} </p>
          <p className="Result"> <b>Light value:</b> {lightRes ? lightRes : "No measurements done yet!"} </p>
          <p className="Result"> <b>Distance value:</b> {distRes ? distRes : "No measurements done yet!"} </p>
        </div>

        {/* Right Column */}
        <div className="right-section">
          {/* Camera Component */}
          <div className="camera-section">
            <Camera />
          </div>

          {/* Input Box with Send Button */}
          <div className="input-section">
            <input
              type="text"
              placeholder="Enter your message..."
              className="message-input"
            />
            <button className="Button send-button" onClick={handleSendClick} >Send</button>
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
