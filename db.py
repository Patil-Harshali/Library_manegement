import secrets

# Simulated database
books = [
    {"id": 1, "title": "1984", "author": "George Orwell"},
    {"id": 2, "title": "To Kill a Mockingbird", "author": "Harper Lee"}
]
 # To store book details
# Simulated Members Database
members = [
    {"id": 1, "name": "Alice", "email": "alice@example.com"},
    {"id": 2, "name": "Bob", "email": "bob@example.com"}
]


 # To store member details
tokens = {"admin": secrets.token_hex(16)}  # Token storage



