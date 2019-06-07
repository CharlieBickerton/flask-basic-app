from flask import Flask, render_template
app = Flask(__name__)

# dummy data
posts = [
    {
        'author': 'Charlie Bickerton',
        'title': 'Blog post 1',
        'content': 'First post content',
        'date_posted': 'Janurary 7, 2019'
    },
    {
        'author': 'Jane Doe',
        'title': 'Blog post 2',
        'content': 'Second post content',
        'date_posted': 'February 7, 2019'
    },
]


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', posts=posts)


@app.route("/about")
def about():
    return render_template('about.html')


# this will allow us to run the app with python
if __name__ == '__main__':
    app.run(debug=True)
