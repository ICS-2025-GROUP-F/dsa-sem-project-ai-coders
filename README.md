# Student Performance Tracker System

A GUI-based system for managing student details, grades, and generating basic reports.

## Features

- Add/View/Edit/Delete student records
- Input marks for multiple subjects
- Compute average & rank
- View top performers
- Search students by name or ID
- Sort students by score or name
- Generate performance analytics

## Data Structures Used

1. **List**: To store all student objects temporarily (runtime DB)
2. **Dictionary**: To store individual student data (ID, name, marks per subject)
3. **Set**: To ensure no duplicate student IDs
4. **Queue/Stack**: To manage recent actions for undo functionality

## Installation

1. Make sure you have Python 3.7+ installed
2. Install the required packages:

```bash
pip install -r requirements.txt
```

## Running the Application

```bash
python main.py
```

## Project Structure

- `/data`: Data management modules
  - `database.py`: SQLite database interface
  - `student.py`: Student model class
  - `student_manager.py`: Core data operations
  - `report.py`: Analytics and reports
  - `store.py`: Wrapper for easier data access

- `/dsa`: Data structures and algorithms
  - `search.py`: Search algorithms (linear, binary)
  - `sort.py`: Sorting algorithms (bubble, merge)
  - `undo_stack.py`: Stack for undo functionality

- `/ui`: User interface components
  - `/layouts`: Screen layouts
  - `/themes`: Visual themes
  - `/widgets`: Reusable UI components

## Usage

1. Register new students with their details and marks
2. View all students in a table format
3. Search for specific students
4. Analyze performance metrics
5. View top performers 