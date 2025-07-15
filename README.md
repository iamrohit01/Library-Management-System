# Library Management System

A simple console-based Library Management System built with Python, featuring basic functionalities to manage books, members, and book borrowing/returning. The system uses JSON files for data persistence, ensuring that data is saved and loaded across sessions.

## Features

* **Book Management:**
    * Add new books (including quantity).
    * Increase quantity of existing books.
    * Remove books (only if not currently borrowed).
    * List all books with their availability.
    * Search for books by title, author, or ISBN.
* **Member Management:**
    * Add new library members.
    * Remove members (only if they have no borrowed books).
    * List all registered members.
* **Borrowing & Returning:**
    * Borrow books with automatic due date calculation (14 days default).
    * Return borrowed books.
    * View all books borrowed by a specific member.
    * Check for overdue books.
* **Data Persistence:**
    * Automatically saves all library data (books, members, borrowed records) to `library_data.json` upon any modification.
    * Loads data from `library_data.json` when the system starts.

## How to Run

1.  **Save the code:** Save the provided Python code into a file named `library_system.py`.
2.  **Open Terminal/Command Prompt:** Navigate to the directory where you saved `library_system.py`.
3.  **Run the application:** Execute the following command:
    ```bash
    python library_system.py
    ```
4.  **Interact:** Follow the on-screen menu prompts to perform library operations.

## Data Storage

The system automatically creates and manages a file named `library_data.json` in the same directory as `library_system.py`. This file stores all book, member, and borrowing information. **Do not manually edit this file unless you understand JSON format and potential data inconsistencies.**

## Project Structure