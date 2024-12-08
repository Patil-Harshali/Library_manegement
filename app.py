from flask import Flask, request, jsonify, render_template, redirect, url_for
from db import books, members, tokens  # Simulated database
import secrets

# Simulated database
books = []  # Store book details as dictionaries
next_id = 1  # To assign unique IDs to books

app = Flask(__name__)  # Initialize the Flask app
# Define your routes and logic here
@app.route('/books/add', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        global books
        new_id = max(book['id'] for book in books) + 1 if books else 1
        books.append({'id': new_id, 'title': title, 'author': author})
        return redirect(url_for('view_books', added=True))  # Pass 'added' flag
    return render_template('add_book.html')


@app.route('/books/edit/<int:book_id>', methods=['GET', 'POST'])
def edit_book(book_id):
    if request.method == 'POST':
        data = request.get_json()
        title = data.get('title')
        author = data.get('author')

        # Update the book in the database
        for book in books:
            if book['id'] == book_id:
                book['title'] = title
                book['author'] = author
                return jsonify({"message": "Book updated"}), 200

        return jsonify({"message": "Book not found"}), 404

    # If the request method is GET, render the edit page
    book = next((book for book in books if book['id'] == book_id), None)
    if book:
        return render_template('edit_book.html', book=book)

    return "Book not found", 404

@app.route('/books/delete/<int:book_id>', methods=['POST'])
def delete_book(book_id):
    global books
    books = [book for book in books if book['id'] != book_id]
    return redirect(url_for('view_books', deleted=True))

@app.route('/books/paginated', methods=['GET'])
def get_books_paginated():
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 5))
    start = (page - 1) * per_page
    end = start + per_page
    return jsonify(books[start:end]), 200

@app.route('/books/view')
def view_books():
    # Pagination logic
    per_page = 5  # Display 5 books per page
    page = request.args.get('page', 1, type=int)  # Get the current page from the URL (defaults to 1)

    

    # Calculate start and end index for slicing the books list
    start = (page - 1) * per_page
    end = start + per_page

    # Get the books for the current page
    books_page = books[start:end]

    # Calculate total pages
    total_books = len(books)
    total_pages = (total_books + per_page - 1) // per_page  # Ceiling division to get the number of pages

    # Determine if the page is the first or last one
    is_first_page = page == 1
    is_last_page = page == total_pages

    added = request.args.get('added', False)  # Check if a book was recently added
    deleted = request.args.get('deleted', False)  # Check if a book was recently deleted
    #return render_template('view_books.html', books=books, added=added,deleted=deleted)
    return render_template('view_books.html', books=books_page, total_pages=total_pages, current_page=page, 
                           is_first_page=is_first_page, is_last_page=is_last_page,dded=added,deleted=deleted)


@app.route('/books/search', methods=['GET'])
def search_books():
    query = request.args.get('q', '').lower()  # Get search query
    # Search for books where either title or author matches the query
    results = [book for book in books if query in book['title'].lower() or query in book['author'].lower()]

    # Check if any results are found
    if results:
        message = "Book(s) found in the library!"
    else:
        message = "No books found in the library with that search term."

    # Return search results and message
    return render_template('view_books.html', books=results, search_query=query, message=message)





@app.route('/members/add', methods=['GET', 'POST'])
def add_member():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']

        # Add the member to the list
        global members
        new_id = max(member['id'] for member in members) + 1 if members else 1
        members.append({'id': new_id, 'name': name, 'email': email})

        # Redirect with the 'added' flag
        return redirect(url_for('add_member', added=True))

    # Check for the 'added' flag in the query parameters
    added = request.args.get('added', False)
    return render_template('add_member.html', added=added)


@app.route('/members/view')
def view_members():
    page = int(request.args.get('page', 1))  # Get the current page number
    members_per_page = 5  # Number of members per page
    start = (page - 1) * members_per_page
    end = start + members_per_page

    total_pages = (len(members) // members_per_page) + (1 if len(members) % members_per_page > 0 else 0)

    deleted = request.args.get('deleted', False)  # Check if a member was deleted

    return render_template('view_members.html', 
                           members=members[start:end], 
                           current_page=page, 
                           total_pages=total_pages, 
                           deleted=deleted)

@app.route('/members/edit/<int:member_id>', methods=['GET', 'POST'])
def edit_member(member_id):
    if request.method == 'POST':
        data = request.get_json()
        name = data.get('name')
        email = data.get('email')

        # Update the member in the database (assuming a `members` list)
        for member in members:
            if member['id'] == member_id:
                member['name'] = name
                member['email'] = email
                return jsonify({"message": "Member updated"}), 200

        return jsonify({"message": "Member not found"}), 404

    # If the request method is GET, render the edit page
    member = next((member for member in members if member['id'] == member_id), None)
    if member:
        return render_template('edit_member.html', member=member)

    return "Member not found", 404


@app.route('/members/delete/<int:member_id>', methods=['POST'])
def delete_member(member_id):
    global members
    members = [member for member in members if member['id'] != member_id]
    return redirect(url_for('view_members', deleted=True))  # Pass deleted flag to show success message

@app.route('/token', methods=['GET'])
def get_token():
    user = request.args.get('user')
    if user == 'admin':
        return jsonify({"token": tokens[user]}), 200
    return jsonify({"error": "Invalid user"}), 403


@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
