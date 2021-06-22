
# Notychats (whatsapp clone v1.0)

Notychats is a clone of whatsapp having feature to chat between users.
 

## Installation 

Install Notychats project with pip

```bash 
  pip install requirements.txt
```
    
## Environment Variables

To run this project, you will need to add the following  variables to your settings.py

```bash 
`SECRET_KEY`  = "Your project's secret key"

`API_KEY` = os.config['MSG91_Key']
    or 
`API_KEY` = 'Your msg91 key for sending otp'
```


  
## Features

- UI Like Whatsapp
- Real Time Chatting
- OTP Verification
- Edit Profile
- Add Your Friend

  
## Tech Stack

**Back-end:** Python, Django, Django-Channels

**Front-end:** HTML, CSS, BootStrap, JavaScript, Ajax

  
## Run Locally

Clone the project

```bash
  git clone https://github.com/mohitCodepy/NotyChats.git
```

Go to the project directory

```bash
  cd NotyChats
```

Install dependencies

```bash
  pip install -r requirements.txt 
```

In base.html of users users/base.html in side websockets

```bash
  change wss:/ to ws: 
```

Start the server

```bash
  python manage.py runserver
```

  
## Deployment

To deploy this project run

```bash
  yet to update...
```

  
## Developer

- [@mohitCodepy](https://github.com/mohitCodepy)

  
