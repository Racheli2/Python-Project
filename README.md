Version-Control Python App 🔄
A simplified version control system built with Python, inspired by Git principles.

📌 Overview
This project simulates a local version control mechanism that allows users to:

Create and manage multiple files

Track changes and save snapshots (commits)

View history of changes

Restore previous versions of each file

All via a graphical interface built with Tkinter, and data stored using SQLite.

🧰 Technologies Used
Python 3.x

Tkinter – for building the GUI

SQLite3 – for storing files, versions and history

OOP principles – for clear code structure and separation of logic

🖼 Features
📁 Add new files and edit existing ones

💾 Save versions ("commits") with timestamps

🕓 Browse history of a file's changes

🔙 Restore to a specific previous version

🎛 Simple and intuitive GUI for interaction

🧠 Project Structure
bash
Copy
Edit
Python-Project/
│
├── backend.py       # Logic for versioning and database
├── frontend.py      # GUI implementation (Tkinter)
├── main.py          # Entry point
└── README.md
🚀 Getting Started
Requirements
Python 3.8+

No external libraries needed

Run the app
bash
Copy
Edit
python main.py
The main window will launch with interface to manage files and versions.

🎯 Use Cases
Educational tool to learn about version control concepts

Personal version tracking for text files

Lightweight alternative to Git for local experiments

📄 License
This project is released under the MIT License.
Use it, modify it, and make it your own.

