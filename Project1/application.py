#https://www.tutorialspoint.com/flask/flask_sessions.htm
import os, requests, string

from flask import Flask, session, render_template, request, redirect, url_for, jsonify
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)
app.secret_key = os.urandom(24)
# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")
# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
# Create the Session object by passing it the application
#Important: firstly i set up the "app" and then i do Session(app)
Session(app)

# Set up database
#An engine is a common interface from sqlalchemy
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

@app.route("/")
def index():
    if 'user_name' in session:
        user_name = session['user_name']
        return redirect(url_for('home', user_name=user_name))
    return redirect(url_for('login'))

#wherever I can divide each function in GET and POST I do it.
@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        user_name = request.form.get("user_name")
        submitted_user_password = request.form.get("submitted_user_password")
        #fetchone() gives me the whole entry in the database [user_id, user_name, user_password]
        #in order to get just one, I have to select it with the dot operand
        user = db.execute("SELECT * from users WHERE user_name=:user_name",
                            {"user_name": user_name}).fetchone()
        #if user doesnt exist render login page again
        if user is None:
            return redirect(url_for('index'))
        user_password = user.user_password
        #check for correct password
        if user_password == submitted_user_password:
            session['user_name'] = user_name
        return redirect(url_for('index'))

#arguments are passed as part of the url or as post requests from forms
#or get requests with request.args.get without adding them in the url
@app.route('/<user_name>', methods = ['GET', 'POST'])
def home(user_name):
    if request.method == 'GET':
        if 'user_name' in session:
            return render_template('home.html', user_name=user_name)
        else:
            return redirect(url_for('index'))
    else:
        key = int(request.form.get('key'))
        return redirect(url_for('search_results', user_name=user_name, key=key))

@app.route('/logout')
def logout():
   # remove the username from the session if it is there
   session.pop('user_name', None)
   return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        #get form information
        user_name = request.form.get("user_name")
        user_password = request.form.get("user_password")
        #Add user
        db.execute("INSERT INTO users (user_name, user_password) VALUES (:user_name, :user_password)",
                    {"user_name": user_name, "user_password": user_password})
        db.commit()
        return render_template("success.html")

@app.route('/<user_name>/<int:key>') #without the "int:", key will not be int
def search_results(user_name, key):
    results = db.execute("SELECT * FROM books WHERE isbn LIKE '%:key%' ", {"key": key}).fetchall()
    return render_template("search_results.html", user_name=user_name, results=results)

#when I make a get request to the route /username/book_title I get the html file with the desired arguments
#when I submit data to the form (POST request) I do the relevant work but I dont render the template.
#I redirect to the same route meaning I make a get request with the right, new arguments.
@app.route("/<user_name>/<book_title>", methods=['POST', 'GET'])
def book(user_name, book_title):
    book = db.execute("SELECT * from books WHERE title = :book_title", {"book_title": book_title}).fetchone()
    #api get request
    res = requests.get("https://www.goodreads.com/book/review_counts.json",
                        params={"key": API_KEY "isbns": book.isbn})
    data = res.json()
    work_ratings_count = data["books"][0]["work_ratings_count"] #when is have emfwleumena json then i should add
    average_rating = data["books"][0]["average_rating"]         #something like that [0]
    avg = db.execute("SELECT AVG(rating) FROM reviews WHERE book_id = :book_id", {"book_id": book.book_id}).fetchone()
    reviews = db.execute("SELECT * FROM reviews WHERE book_id = :book_id", {"book_id": book.book_id}).fetchall()

    if request.method == 'GET':
        return render_template('book.html', user_name=user_name, book=book, reviews=reviews,
                                avg=avg, average_rating=average_rating, work_ratings_count=work_ratings_count)
    else:
        #dont accept a submittion with no rating
        rating = request.form.get('rating')
        if rating is None:
            return redirect(url_for('book', user_name=user_name, book_title=book_title, book=book, reviews=reviews,
                                    avg=avg, average_rating=average_rating, work_ratings_count=work_ratings_count))
        rating = int(rating)
        review_text = request.form.get("review_text")
        db.execute("INSERT INTO reviews (book_id, rating, review_text) VALUES (:book_id, :rating, :review_text)",
                    {"book_id": book.book_id, "rating": rating, "review_text": review_text})
        db.commit()
        return redirect(url_for('book', user_name=user_name, book_title=book_title, book=book, reviews=reviews,
                                avg=avg, average_rating=average_rating, work_ratings_count=work_ratings_count))

@app.route("/api/book/<isbn>")
def book_review_api(isbn):

    # Make sure book exists.
    book = db.execute("SELECT * FROM books WHERE isbn=:isbn", {"isbn" :isbn}).fetchone()
    if book is None:
        return jsonify({"error": "Invalid flight_id"}), 422
    #fetch all the reviews about this particular book
    reviews = db.execute("SELECT * FROM reviews WHERE book_id=:book_id", {"book_id" :book.book_id}).fetchall()
    #get the total number of reviews and their average rating
    review_count = db.execute("SELECT * from reviews").rowcount
    avg = db.execute("SELECT AVG(rating) FROM reviews WHERE book_id = :book_id", {"book_id": book.book_id}).fetchone()
    #Problem with jsonify: it can not use decimals so in order to pass the average_score I made it
    #a sting. Not optimum. There is simplejson that can handle decimals and could resolve this issue.
    return jsonify({
            "title": book.title,
            "author": book.author,
            "year": book.year,
            "isbn": book.isbn,
            "review_count": review_count,
            "average_score": str(avg.avg)
        })

if __name__ == "__main__":
	main()
