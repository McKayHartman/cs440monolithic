from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import sqlite3
from datetime import datetime

# initalize the service
app = Flask(__name__)

# initalize the cconnection to the datbase
def get_db_connection():
    conn = sqlite3.connect('reviews.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    connection = get_db_connection()
    with open('books.sql', 'r') as f:
        connection.executescript(f.read())
    connection.commit()
    connection.close()




# API review endpoints

# get all review for a book
@app.route('/api/reviews/<int:book_id>', methods=['GET'])
def 


# post a review to the table
@app.route('/api/reviews', methods=['POST'])


# update a review (full replacment via PUT)
@app.route('/api/reviews/<int:review_id>', methods=['PUT'])


# delete a review from the table
@app.route('/api/reviews/<int:review_id>', methods=['DELETE'])


if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5002)