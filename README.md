# TaskFlow 📝

TaskFlow is a modern task management web application built with **Flask** that helps users organize, track, and manage their daily tasks. It provides a secure authentication system, an intuitive dashboard, and a clean, responsive interface that works across desktop and mobile devices.

---

## ✨ Features

- User registration and login
- Secure password hashing
- CSRF protection
- Session-based authentication
- Create new tasks
- Edit existing tasks
- Mark tasks as completed
- Delete tasks with confirmation
- Filter tasks by status
- Responsive design for desktop and mobile
- Modern and minimal user interface

---

## 🛠️ Built With

- Python
- Flask
- SQLite
- HTML5
- CSS3
- JavaScript
- Flask-WTF
- Werkzeug
- Gunicorn
- Python Dotenv

---

## 📂 Project Structure

```text
TaskFlow/
│
├── app.py
├── database.db
├── requirements.txt
├── Procfile
├── .env
│
├── static/
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   └── script.js
│   └── images/
│
├── templates/
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── edit.html
│   ├── 404.html
│   └── 500.html
│
└── README.md
```

---

## 🚀 Installation

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/TaskFlow.git
```

### 2. Navigate into the project

```bash
cd TaskFlow
```

### 3. Create a virtual environment

```bash
python -m venv venv
```

### 4. Activate the virtual environment

**Windows**

```bash
venv\Scripts\activate
```

**macOS/Linux**

```bash
source venv/bin/activate
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

### 6. Create a `.env` file

```env
SECRET_KEY=your_secret_key_here
```

### 7. Run the application

```bash
python app.py
```

Open your browser and visit:

```
http://127.0.0.1:5000
```

---

## 🔐 Security

TaskFlow includes several security best practices:

- Password hashing using Werkzeug
- CSRF protection using Flask-WTF
- Session-based authentication
- Secret key stored in environment variables

---

## 📱 Responsive Design

The application is optimized for:

- Desktop
- Tablet
- Mobile devices

## 🌐 Live Demo

**Live Website**

```
https://taskflow-xrlp.onrender.com
```

---

## 📈 Future Improvements

- Task search
- Due dates
- Categories
- Priority levels
- User profile
- Dark/Light mode toggle
- Email verification
- Password reset
- Notifications
- Dashboard analytics

---

## 👨‍💻 Author

**King Olusuyi**

Software Engineering Student

Backend-focused Full-Stack Developer

## 📄 License

This project is licensed under the MIT License.

Feel free to use, modify, and learn from this project.
