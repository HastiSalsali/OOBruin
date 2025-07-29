# Team name: OOBruin
Team members: **[Edwin Lin](https://www.linkedin.com/in/edwlin7279/)**, **[Tyler Newton](https://www.linkedin.com/in/newton-tyler/)**, **[Hasti Salsali](www.linkedin.com/in/hastisalsali)**, **[Alex Lopez](https://www.linkedin.com/in/alexlopez1159/)**

-> This repository contains the code, circuit diagram, and CAD files for our project, created for **UCLA 2025 HAcK**. Our spy gadgets includes a watch and a bowtie, designed to communicate to and be controlled by our website.

### Electronics and Schematics:
[Circuit diagram](https://github.com/HastiSalsali/OOBruin/blob/master/Electronics_and_Schematics%3A/Circuit_Diagram.jpg)

### Meachanical Components:
[CAD files](https://github.com/HastiSalsali/OOBruin/tree/master/Mechanical_Components%3A)

### Presentation:
[Slides (pdf)](https://github.com/HastiSalsali/OOBruin/blob/master/Presentation/00Bruin%20Design%20Review%20Presentation.pdf)

[Slides (Google Slides)](https://docs.google.com/presentation/d/19XGPjU8Jk1XB0TQxRVJp7M6kx2x2rjpt80H7BGjiUeA/edit?usp=sharing)

[Video Presentation (Youtube)](https://youtu.be/FFLzoeuouuA)

### Our Gadgets:
<img width="308" height="412" alt="00Bruin Agent" src="https://github.com/user-attachments/assets/b0b73ab2-cbcf-4caf-ad66-36ee8f8a5d82" />
<img width="306" height="411" alt="00Bruin Bowtie" src="https://github.com/user-attachments/assets/8317234a-a462-4a76-a629-db986fc865df" />
<img width="306" height="411" alt="00Bruin Bowtie" src="https://github.com/user-attachments/assets/618f893e-669a-4140-b2d4-d2991203e54d" />

## How to run code:

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
