import json
import os
from datetime import datetime, timedelta

# --- Configuration ---
DATA_FILE = 'library_data.json'

# --- Book Class ---
class Book
    def __init__(self, title, author, isbn, quantity=1)
        self.title = title
        self.author = author
        self.isbn = isbn  # International Standard Book Number - unique identifier
        self.quantity = quantity
        self.available_copies = quantity

    def __str__(self)
        return fTitle {self.title}, Author {self.author}, ISBN {self.isbn}, Available {self.available_copies}{self.quantity}

    def to_dict(self)
        return {
            'title' self.title,
            'author' self.author,
            'isbn' self.isbn,
            'quantity' self.quantity,
            'available_copies' self.available_copies
        }

    @classmethod
    def from_dict(cls, data)
        book = cls(data['title'], data['author'], data['isbn'], data['quantity'])
        book.available_copies = data['available_copies']
        return book

# --- Member Class ---
class Member
    def __init__(self, name, member_id)
        self.name = name
        self.member_id = member_id # Unique identifier for the member
        self.borrowed_books = {}  # {isbn {'borrow_date' 'YYYY-MM-DD', 'due_date' 'YYYY-MM-DD'}}

    def __str__(self)
        return fName {self.name}, Member ID {self.member_id}, Books Borrowed {len(self.borrowed_books)}

    def to_dict(self)
        return {
            'name' self.name,
            'member_id' self.member_id,
            'borrowed_books' self.borrowed_books
        }

    @classmethod
    def from_dict(cls, data)
        member = cls(data['name'], data['member_id'])
        member.borrowed_books = data['borrowed_books']
        return member

# --- Library Class ---
class Library
    def __init__(self, data_file=DATA_FILE)
        self.books = {}     # {isbn Book_object}
        self.members = {}   # {member_id Member_object}
        self.data_file = data_file
        self._load_data()

    def _load_data(self)
        Loads library data from a JSON file.
        if os.path.exists(self.data_file)
            try
                with open(self.data_file, 'r') as f
                    data = json.load(f)
                    self.books = {isbn Book.from_dict(b_data) for isbn, b_data in data.get('books', {}).items()}
                    self.members = {mid Member.from_dict(m_data) for mid, m_data in data.get('members', {}).items()}
                print(Library data loaded successfully.)
            except json.JSONDecodeError
                print(Error Could not decode JSON. Starting with empty library.)
                self.books = {}
                self.members = {}
            except Exception as e
                print(fAn unexpected error occurred while loading data {e})
                self.books = {}
                self.members = {}
        else
            print(No existing library data file found. Starting with empty library.)

    def _save_data(self)
        Saves current library data to a JSON file.
        data = {
            'books' {isbn book.to_dict() for isbn, book in self.books.items()},
            'members' {mid member.to_dict() for mid, member in self.members.items()}
        }
        try
            with open(self.data_file, 'w') as f
                json.dump(data, f, indent=4)
            print(Library data saved successfully.)
        except Exception as e
            print(fError saving data {e})

    def add_book(self, title, author, isbn, quantity=1)
        Adds a new book or increases quantity of an existing book.
        if isbn in self.books
            self.books[isbn].quantity += quantity
            self.books[isbn].available_copies += quantity
            print(fIncreased quantity for book '{title}'. New quantity {self.books[isbn].quantity})
        else
            book = Book(title, author, isbn, quantity)
            self.books[isbn] = book
            print(fBook '{title}' added to the library.)
        self._save_data()

    def remove_book(self, isbn)
        Removes a book from the library by ISBN.
        if isbn in self.books
            # Check if any copies are currently borrowed
            for member in self.members.values()
                if isbn in member.borrowed_books
                    print(fCannot remove book '{self.books[isbn].title}'. Copies are currently borrowed by members.)
                    return False
            
            del self.books[isbn]
            print(fBook with ISBN '{isbn}' removed from the library.)
            self._save_data()
            return True
        else
            print(fBook with ISBN '{isbn}' not found.)
            return False

    def list_books(self)
        Lists all books in the library.
        if not self.books
            print(No books in the library.)
            return
        print(n--- Current Books in Library ---)
        for book in self.books.values()
            print(book)
        print(--------------------------------)

    def add_member(self, name, member_id)
        Adds a new member to the library.
        if member_id in self.members
            print(fMember with ID '{member_id}' already exists.)
        else
            member = Member(name, member_id)
            self.members[member_id] = member
            print(fMember '{name}' (ID {member_id}) added.)
        self._save_data()

    def remove_member(self, member_id)
        Removes a member from the library by Member ID.
        if member_id in self.members
            if self.members[member_id].borrowed_books
                print(fCannot remove member '{self.members[member_id].name}'. They still have borrowed books.)
                return False
            del self.members[member_id]
            print(fMember with ID '{member_id}' removed.)
            self._save_data()
            return True
        else
            print(fMember with ID '{member_id}' not found.)
            return False

    def list_members(self)
        Lists all members in the library.
        if not self.members
            print(No members registered.)
            return
        print(n--- Registered Members ---)
        for member in self.members.values()
            print(member)
        print(--------------------------)

    def borrow_book(self, isbn, member_id, loan_period_days=14)
        Allows a member to borrow a book.
        book = self.books.get(isbn)
        member = self.members.get(member_id)

        if not book
            print(fBook with ISBN '{isbn}' not found.)
            return False
        if not member
            print(fMember with ID '{member_id}' not found.)
            return False

        if book.available_copies  0
            if isbn in member.borrowed_books
                print(fMember '{member.name}' has already borrowed '{book.title}'.)
                return False

            book.available_copies -= 1
            borrow_date = datetime.now()
            due_date = borrow_date + timedelta(days=loan_period_days)
            member.borrowed_books[isbn] = {
                'borrow_date' borrow_date.strftime('%Y-%m-%d'),
                'due_date' due_date.strftime('%Y-%m-%d')
            }
            print(f'{book.title}' borrowed by '{member.name}'. Due on {due_date.strftime('%Y-%m-%d')})
            self._save_data()
            return True
        else
            print(f'{book.title}' is currently out of stock.)
            return False

    def return_book(self, isbn, member_id)
        Allows a member to return a book.
        book = self.books.get(isbn)
        member = self.members.get(member_id)

        if not book
            print(fBook with ISBN '{isbn}' not found.)
            return False
        if not member
            print(fMember with ID '{member_id}' not found.)
            return False

        if isbn in member.borrowed_books
            book.available_copies += 1
            del member.borrowed_books[isbn]
            print(f'{book.title}' returned by '{member.name}'.)
            self._save_data()
            return True
        else
            print(fMember '{member.name}' did not borrow '{book.title}'.)
            return False

    def search_book(self, query, search_by='title')
        Searches for books by title, author, or ISBN.
        results = []
        query = query.lower()
        if search_by == 'title'
            results = [book for book in self.books.values() if query in book.title.lower()]
        elif search_by == 'author'
            results = [book for book in self.books.values() if query in book.author.lower()]
        elif search_by == 'isbn'
            results = [book for book in self.books.values() if query == book.isbn.lower()]
        else
            print(Invalid search_by parameter. Use 'title', 'author', or 'isbn'.)
            return []

        if results
            print(fn--- Search Results for '{query}' by {search_by} ---)
            for book in results
                print(book)
            print(------------------------------------------)
        else
            print(fNo books found matching '{query}' by {search_by}.)
        return results

    def display_member_borrowed_books(self, member_id)
        Displays books currently borrowed by a specific member.
        member = self.members.get(member_id)
        if not member
            print(fMember with ID '{member_id}' not found.)
            return

        if not member.borrowed_books
            print(fMember '{member.name}' has no borrowed books.)
            return

        print(fn--- Books borrowed by {member.name} (ID {member.member_id}) ---)
        for isbn, details in member.borrowed_books.items()
            book = self.books.get(isbn)
            if book
                borrow_date = details['borrow_date']
                due_date = details['due_date']
                print(f  - Title {book.title}, Author {book.author}, ISBN {book.isbn}, Borrow Date {borrow_date}, Due Date {due_date})
            else
                print(f  - Unknown book (ISBN {isbn}) - Data inconsistency)
        print(-------------------------------------------------)

    def check_overdue_books(self)
        Checks and lists any overdue books.
        overdue_found = False
        print(n--- Overdue Books ---)
        for member_id, member in self.members.items()
            for isbn, details in member.borrowed_books.items()
                due_date_str = details['due_date']
                due_date = datetime.strptime(due_date_str, '%Y-%m-%d')
                if datetime.now()  due_date
                    book = self.books.get(isbn)
                    if book
                        print(f  - Member {member.name} (ID {member_id}), Book {book.title} (ISBN {isbn}), Due Date {due_date_str})
                        overdue_found = True
                    else
                        print(f  - Member {member.name} (ID {member_id}), Unknown Book (ISBN {isbn}) is overdue.)
                        overdue_found = True
        if not overdue_found
            print(No overdue books found.)
        print(---------------------)

# --- Main Application Logic (CLI) ---
def display_menu()
    print(n--- Library Management System Menu ---)
    print(1. Add Book)
    print(2. Remove Book)
    print(3. List All Books)
    print(4. Search Book)
    print(5. Add Member)
    print(6. Remove Member)
    print(7. List All Members)
    print(8. Borrow Book)
    print(9. Return Book)
    print(10. View Member's Borrowed Books)
    print(11. Check Overdue Books)
    print(12. Exit)
    print(------------------------------------)

def main()
    library = Library()

    while True
        display_menu()
        choice = input(Enter your choice )

        if choice == '1'
            title = input(Enter book title )
            author = input(Enter book author )
            isbn = input(Enter book ISBN )
            try
                quantity = int(input(Enter quantity (default 1) ) or 1)
                if quantity = 0
                    raise ValueError
            except ValueError
                print(Invalid quantity. Quantity must be a positive integer.)
                continue
            library.add_book(title, author, isbn, quantity)
        
        elif choice == '2'
            isbn = input(Enter ISBN of book to remove )
            library.remove_book(isbn)

        elif choice == '3'
            library.list_books()

        elif choice == '4'
            search_type = input(Search by (titleauthorisbn) ).lower()
            query = input(fEnter {search_type} to search )
            library.search_book(query, search_type)

        elif choice == '5'
            name = input(Enter member name )
            member_id = input(Enter member ID )
            library.add_member(name, member_id)

        elif choice == '6'
            member_id = input(Enter member ID to remove )
            library.remove_member(member_id)

        elif choice == '7'
            library.list_members()

        elif choice == '8'
            isbn = input(Enter ISBN of book to borrow )
            member_id = input(Enter member ID )
            library.borrow_book(isbn, member_id)

        elif choice == '9'
            isbn = input(Enter ISBN of book to return )
            member_id = input(Enter member ID )
            library.return_book(isbn, member_id)

        elif choice == '10'
            member_id = input(Enter member ID to view borrowed books )
            library.display_member_borrowed_books(member_id)

        elif choice == '11'
            library.check_overdue_books()

        elif choice == '12'
            print(Exiting Library Management System. Goodbye!)
            break
        else
            print(Invalid choice. Please try again.)

if __name__ == __main__
    main()