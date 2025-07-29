import React, { useState, useEffect } from "react";
import io from 'socket.io-client';
import './App.css';
import { Header } from "./header";

const socket = io('http://localhost:8000');

function App() {
  const [pictureStatus, setPictureStatus] = useState("");
  const [pictureAvail, setPictureAvail] = useState(false)
  const [cameraKey, setCameraKey] = useState(0);


  useEffect(() => {
    socket.on('connect', () => console.log('Connected:', socket.id));

    socket.on('picture_taken', data => {
      setPictureStatus(data.message);
      console.log('GOT PHOTO')
      setTimeout(() => setPictureStatus(""), 3000); // Clear status after 3 seconds
    });

    console.log('STARTED PROGRAM at', Date.now()) //To check when page reloads

    return () => {
      socket.off('picture_taken');
    };
  }, []);

  //UPDATING MEASUREMENTS:

  const [tempRes, settempRes] = useState("No measurements done yet!");
  const [humidRes, sethumidRes] = useState("No measurements done yet!");
  const [lightRes, setlightRes] = useState("No measurements done yet!");
  const [distRes, setdistRes] = useState("No measurements done yet!");

  //geting values from backend:

  socket.on('temp', (latestTemp) => {
    settempRes(latestTemp); //changing usestate variable so value rerenders in website
    console.log("got temp measurements" + latestTemp)
  })
  socket.on('humidity', (latestHumidity) => {
    sethumidRes(latestHumidity); //changing usestate variable so value rerenders in website
    console.log("got Humidity measurements" + latestHumidity);
  })
  socket.on('light', (latestLight) => {
    setlightRes(latestLight); //changing usestate variable so value rerenders in website
    console.log("got light measurements" + latestLight);
  })
  socket.on('ultrasonic', (latestUltrasonic) => {
    setdistRes(latestUltrasonic); //changing usestate variable so value rerenders in website
    console.log("got distance measurements" + latestUltrasonic);
  })


  //TAKING PHOTO:

  function Camera(prop) {  //camera component holding the captured photo, button to take photo and audio description

    let handleClick = () => {
      socket.emit('take_picture') //when "Take photo" button is click send message to backend to take photo
      console.log('taking photo')
    }

    return (
      <div className="camera-section">
        <h2 className="Heading1">Camera:</h2>
        <button onClick={handleClick} className="Button">Take photo</button >  {/*take photo button*/}
        <div className="media-container">
          <img src={`/downloaded_image.jpg?${Math.floor(Date.now() / 500)}`} alt="No photo to display" className="camera-image" /> {/*added the time as a query string so website rerenders image every few seconds*/}
          <audio controls className="audio-player">
            <source src={`/image_to_speach.mp3?${Math.floor(Date.now() / 500)}`} type="audio/mpeg" /> {/*added the time as a query string so website rerenders audio every few seconds*/}
            Your browser does not support the audio element.
          </audio>
        </div>
      </div>
    );
  }


  //SENDING MESSAGES TO AGENT:

  const [text, setText] = useState(null);
  const handleChange = e => setText(e.target.value); //change text value when something is typed into chatbox

  const handleSubmit = e => {
    console.log("Frontend sending message: " + text);
    e.preventDefault(); // prevent page from refreshing
    //React -> Node
    socket.emit('display', text);
    setText("");
  };


  return (
    <div className="app">
      <Header />
      <div className="main-container">
        <div className="measurements-section">
          <h2 className="Heading1">Measurements:</h2>
          <p className="Result"> Temp value: {tempRes ? `${tempRes} °F` : "No measurements done yet!"} </p>
          <p className="Result"> Humidity value: {humidRes ? `${humidRes} %` : "No measurements done yet!"} </p>
          <p className="Result"> Light value: {lightRes ? `${lightRes} lm` : "No measurements done yet!"} </p>
          <p className="Result"> Distance value: {distRes ? `${distRes} cm` : "No measurements done yet!"} </p>
        </div>
        <Camera />
      </div>
      <div className="talk-to-agent-section">
        <h2 className="Heading1">Talk to agent</h2>
        <div className="text-input-container">
          <input
            type="text"
            placeholder="Enter your message..."
            value={text}
            onChange={handleChange} 
            className="text-input"
            maxLength={32} //max number of digits that can be sent to agent at a time
            required
          />
          <button onClick={handleSubmit} className="Button send-button">Send</button>
        </div>
      </div>
    </div>

  );
}

//
export default App;



