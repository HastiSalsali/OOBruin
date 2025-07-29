# Team name: OOBruin
Team members: *Edwin Lin*, *Tyler Newton*, *Hasti Salsali*, *Alex Lopez*

-> This repository contains the code, circuit diagram, and CAD files for our project, created for **UCLA 2025 HAcK**. Our spy gadgets includes a watch and a bowtie, designed to communicate to and be controlled by our website.

### Electronics and Schematics:
[Circuit diagram](https://github.com/HastiSalsali/OOBruin/blob/master/Electronics_and_Schematics%3A/Circuit_Diagram.jpg)

### Meachanical Components:
[CAD files](https://github.com/HastiSalsali/OOBruin/tree/master/Mechanical_Components%3A)

### Presentation:
[Pdf of Slides](https://github.com/HastiSalsali/OOBruin/blob/master/Presentation/00Bruin%20Design%20Review%20Presentation.pdf)

[Google Slides](https://docs.google.com/presentation/d/19XGPjU8Jk1XB0TQxRVJp7M6kx2x2rjpt80H7BGjiUeA/edit?usp=sharing)

[Video Presentation]()


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
