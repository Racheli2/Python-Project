
# Python-Project 📚

A simple desktop application for managing books using Python, Tkinter, and SQLite.

## 🧰 Features

* Add new books with title, author, year, and ISBN
* View all books in the database
* Search for specific entries
* Update and delete existing records
* Built with `Tkinter` for the GUI and `sqlite3` for data storage

## 🖼️ Screenshot

*(You can add a screenshot of the UI here if available)*

## 📁 Project Structure

| File          | Description                              |
| ------------- | ---------------------------------------- |
| `frontend.py` | Main GUI logic using Tkinter             |
| `backend.py`  | Database interaction (CRUD using SQLite) |
| `main.py`     | Script to launch the app                 |
| `README.md`   | Project documentation (this file)        |

## ▶️ Getting Started

### Prerequisites

Make sure Python 3 is installed. No external libraries are required – uses only standard library.

### Run the Application

```bash
python main.py
```

The GUI window will open, and you can start adding or managing books.

## 🛠️ How It Works

* `backend.py` manages the SQLite database and performs operations like insert, update, delete, and search.
* `frontend.py` builds the interface and interacts with the backend.
* `main.py` connects it all and starts the application.

## ✅ To Do / Future Improvements

* Add export/import functionality (CSV, JSON)
* Add error handling and input validation
* Improve UI design
* Package the app into a standalone executable (with PyInstaller or similar)

## 📄 License

This project is open source under the MIT License.
