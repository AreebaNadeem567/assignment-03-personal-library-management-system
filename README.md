# Personal Library Manager

## Overview
The **Personal Library Manager** is a command-line application that allows users to manage their book collection. Users can add, remove, and search for books, as well as view statistics on their reading progress. The library is stored as a collection of dictionaries, each containing details about a book.

## Features
### Core Features:
- **Book Details:** Each book entry includes:
  - Title (string)
  - Author (string)
  - Publication Year (integer)
  - Genre (string)
  - Read Status (boolean: True if read, False if unread)

- **Menu System:**
  - Add a book
  - Remove a book
  - Search for a book (by title or author)
  - Display all books
  - Display statistics (total books, percentage read)
  - Exit the program

### Functionality
1. **Add a Book**
   - Prompts the user to enter book details and stores it in the library.
2. **Remove a Book**
   - Allows the user to remove a book by entering its title.
3. **Search for a Book**
   - Enables searching by title or author and displays matching results.
4. **Display All Books**
   - Prints all stored books in a formatted output.
5. **Display Statistics**
   - Shows the total number of books and the percentage of books read.
6. **Exit**
   - Safely terminates the program.

### Optional Features
- File handling: Save and load the book collection from a file to retain data between sessions.
- Improved UI with sorting and filtering options.

## Installation
1. Clone this repository or download the script.
2. Ensure you have Python installed.
3. Run the script using:
   ```bash
   python library_manager.py
   ```

## Usage
Follow the on-screen menu options to interact with your personal library. Add books, remove them, search, and track your reading progress effortlessly.

## License
This project is open-source and available for modification and distribution.

---
Enjoy managing your personal library!
