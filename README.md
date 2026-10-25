# BMI Calculator

A Python BMI calculator with a Tkinter graphical interface. It stores every calculation in a SQLite database so you can review your history, see a trend chart, and delete old records. A command-line version is included too.

## Features

- Enter name, weight (kg) and height (feet and inches, e.g. `5.7`)
- Calculates BMI and shows the BMI category
- Input validation for weight and height
- Saves each record (name, weight, height, BMI, category, date) in a local SQLite database
- BMI history window with the option to delete records
- BMI trend chart drawn with Matplotlib
- Command-line version in `main.py`

## Tech Stack

- Python 3
- Tkinter
- SQLite (`sqlite3`)
- Matplotlib

## Project Structure

```text
python_project/
├── main.py       # command-line version
├── gui.py        # Tkinter GUI (main application)
├── database.py   # SQLite create / save / read / delete functions
└── .gitignore
```

## How to Run

1. Clone the repository:

   ```bash
   git clone https://github.com/Mrabdulla17/python_project.git
   cd python_project
   ```

2. Install Matplotlib (Tkinter and SQLite come with most Python installs):

   ```bash
   pip install matplotlib
   ```

3. Start the GUI:

   ```bash
   python gui.py
   ```

   Or use the command-line version:

   ```bash
   python main.py
   ```

The database file `bmi_records.db` is created automatically on first run.

## What I Learned

- Building a desktop GUI with Tkinter
- Designing a small SQLite database and writing CRUD functions
- Separating UI, logic and data code into different files
