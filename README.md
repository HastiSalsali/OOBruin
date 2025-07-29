# Team name: OOBruin
Team members: *Edwin Lin*, *Tyler Newton*, *Hasti Salsali*, *Alex Lopez*
-> This repo holds the code, circuit diagram, and CAD for our project for the **UCLA HAcK Hackathon 2025**. Our spy gadgets included a watch and a bowtie, which both communicated and were controlled with our website.  

### [Circuit diagram](https://drive.google.com/file/d/10QwgVS3xziQsNO_BHqdusI0C0zyzDuw0/view?usp=sharing)

### [CAD files]()

### [Slides]()

### [Video Presentation]()

## Our Gadgets:
![alt text](image.jpg)

## To run code:

### AI Setup:
-add a my_secrets.py file in the OOBruin/AI folder, containing your OpenAI "`API_KEY`".

### Backend and Frontend setup

- In the backend directory, create a file named '.env', and add the following:

- CONNECT_URL=mqtts://(your URL):(your port)

- MQTT_USER=(your user)

- MQTT_PASS=(your pass)

- Then, while in the backend directory, install the dependencies by running
 `npm install` 
- You can start the backend by running 
  `node index.js`

- In a separate terminal, in the frontend directory, install the dependencies by running
 `npm install`
- You can start the frontend by running 
 `npm start`
