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
    with open('review_service.sql', 'r') as f:
        connection.executescript(f.read())
    connection.commit()
    connection.close()

# API review endpoints

# get all review for a book
@app.route('/api/reviews/<int:book_id>', methods=['GET'])
def get_reviews(book_id):
    conn = get_db_connection()
    reviews = conn.execute('SELECT * FROM reviews WHERE book_id = ?', (book_id,)).fetchall()
    conn.close()
    return jsonify([dict(review) for review in reviews])


# post a review to the table
@app.route('/api/reviews', methods=['POST'])
def add_review():
    if not request.json:
        return jsonify({'error': 'No data provided'}), 400
    
    required_fields = ['book_id', 'rating', 'reviewer']
    if not all(field in request.json for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400
    
    conn = get_db_connection()
    cursor = conn.execute(
        'INSERT INTO reviews (book_id, rating, comment, reviewer, date) VALUES (?, ?, ?, ?, ?)',
        (request.json['book_id'], request.json['rating'], request.json.get('comment', ''), request.json['reviewer'], datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    )
    review_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    return jsonify({'id': review_id, 'message': 'Review added successfully'}), 201


# update a review (full replacment via PUT)
@app.route('/api/reviews/<int:review_id>', methods=['PUT'])
def update_review(review_id):
    if not request.json:
        return jsonify({'error': 'No data provided'}), 400
        
    conn = get_db_connection()
    review = conn.execute('SELECT * FROM reviews WHERE id = ?', (review_id,)).fetchone()
    if review is None:
        conn.close()
        return jsonify({'error': 'Review not found'}), 404
        
    rating = request.json.get('rating', review['rating'])
    comment = request.json.get('comment', review['comment'])
    
    conn.execute('UPDATE reviews SET rating = ?, comment = ? WHERE id = ?',
                 (rating, comment, review_id))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Review updated successfully'})


# delete a review from the table
@app.route('/api/reviews/<int:review_id>', methods=['DELETE'])
def delete_review(review_id):
    conn = get_db_connection()
    review = conn.execute('SELECT * FROM reviews WHERE id = ?', (review_id,)).fetchone()
    if review is None:
        conn.close()
        return jsonify({'error': 'Review not found'}), 404
        
    conn.execute('DELETE FROM reviews WHERE id = ?', (review_id,))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Review deleted successfully'})


if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5002)