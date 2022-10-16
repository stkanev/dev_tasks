from flask import Flask, render_template, request, url_for, flash, redirect
import psycopg2
from psycopg2 import Error
from config import config

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret key"


#     cursor.execute(
#         "CREATE TABLE posts (post_id SERIAL PRIMARY KEY, title TEXT, content TEXT, date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP)")
#     connection.commit()


@app.route('/create', methods=["GET", "POST"])  # Allowing Post requests
def create_post():
    if request.method.upper() == "POST":
        title = request.form.get("title")
        content = request.form.get("content")
        print(f'values for: {title} and {content}')
        if title == None or content == None or title.strip() == "" or content.strip() == "":
            # flashes a message to tell the user to fill all the fields
            flash("Please fill all the fields")
            return render_template("create.html")

        insert_title_content_into_db(title, content)

        return redirect(url_for("display_posts"))  # redirect user
    return render_template("create.html")


def insert_title_content_into_db(title: str, content: str):
    # Connect to an existing database
    connection = None
    try:
        params = config()
        connection = psycopg2.connect(**params)

        # Create a cursor to perform database operations
        cursor = connection.cursor()
        # Adding the post to the database
        insert_query = "INSERT INTO posts(title, content) VALUES(%s, %s); "
        cursor.execute(insert_query, (title, content))
        connection.commit()
        count = cursor.rowcount
        print(count, "Record inserted successfully into posts table")
    except (Exception, Error) as error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        if (connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")


@app.route("/")
def main():
    return render_template("index.html")


@app.route("/posts")
def display_posts():

    return render_template("posts.html", posts=read_posts_from_db())


def read_posts_from_db():
    connection = None
    try:
        params = config()
        connection = psycopg2.connect(**params)

        # Create a cursor to perform database operations
        cursor = connection.cursor()
        # Adding the post to the database
        cursor.execute('SELECT * FROM posts')
        posts = cursor.fetchall()
        return posts
    except (Exception, Error) as error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        if (connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")


if __name__ == "__main__":
    app.run(debug=True)
