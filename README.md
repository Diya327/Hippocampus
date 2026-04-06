# Hippocampus 🧠

A Flask-based adaptive quiz application designed to help students learn through intelligent assessment and progress tracking.

---

## 📌 Overview

Hippocampus is an interactive learning platform that adapts to each student's knowledge level. The application dynamically adjusts question difficulty based on performance, tracks scores over time, and provides instant feedback to enhance the learning experience.

---

## 🚀 Features

- **User Authentication**  
  Secure registration and login system using a lightweight backend

- **Adaptive Difficulty**  
  Questions are selected based on the student's current skill level

- **Level-Based System**  
  Students progress through 5 difficulty levels (1–5)

- **Smart Question Selection**  
  80% of questions match the student's level, while 20% introduce variation

- **Score Tracking**  
  Full quiz history stored per user

- **Progress Analytics**  
  Tracks performance over time (ready for visualisation)

- **Instant Feedback**  
  Immediate response and explanations after each question

- **Customisable Quiz Length**  
  Users can choose how many questions they attempt per quiz

---

## 🛠️ Tech Stack

- **Backend:** Python, Flask  
- **Data Storage:** CSV-based system for user data and quiz content  
- **Architecture:** REST-style backend with templated frontend  

---

## ⚙️ How It Works

1. Users register and log in  
2. The system assigns an initial difficulty level  
3. Questions are selected dynamically:
   - Majority from the user’s level  
   - Minority from other levels to challenge the user  
4. Scores are recorded after each quiz  
5. User progress updates based on performance  

---

## 📂 Project Structure

``` id="proj-struct-updated"
/hippocampus
│── main.py              # Main Flask application
│── quiz.csv             # Quiz questions and answers
│── student.csv          # User login and score data
│
├── templates/           # HTML templates (UI)
├── static/              # CSS and assets
│
├── .vscode/             # Editor configuration
├── __pycache__/         # Python cache files
└── .git/                # Git version control
```

---

## ▶️ Getting Started

### 1. Clone the repository
```bash id="clone"
git clone https://github.com/YOUR_USERNAME/hippocampus.git
cd hippocampus
```

### 2. Install dependencies
```bash id="install"
pip install flask
```

### 3. Run the application
```bash id="run"
python main.py
```

### 4. Open in browser
``` id="url"
http://127.0.0.1:5000/
```

---

## 🔐 Authentication System

- User data is stored in `student.csv`  
- Handles registration and login validation  
- Lightweight alternative to a full database system  

---

## 📊 Data Handling

- `quiz.csv` stores quiz questions, answers, and difficulty levels  
- `student.csv` stores user credentials and scores  
- Data is read and written using Python file handling  

---

## 📈 Future Improvements

- 🔄 Replace CSV storage with a database (e.g. SQLite or MongoDB)  
- 🔑 Add password hashing for improved security  
- 📊 Implement full data visualisation for progress tracking  
- 🌐 Deploy the application online  
- 🎨 Improve UI/UX design  

---

## 🎯 Learning Outcomes

This project demonstrates:
- Backend development with Flask  
- REST-style API design  
- File handling and data persistence in Python  
- Building a basic authentication system  
- Designing adaptive logic for user-based experiences  

---

## 🤝 Contributing

Contributions are welcome! Feel free to fork the repo and submit a pull request.

---

## 📄 License

This project is open-source and available under the MIT License.
