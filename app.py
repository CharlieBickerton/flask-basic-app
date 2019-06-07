from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistrationForm, LoginForm
app = Flask(__name__)

app.config['SECRET_KEY'] = 'b182309d4ff36f9a272cc3495da8475b'

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
    return render_template('about.html', title='About')


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash(f'Welcome {form.email.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('login.html', title="Login", form=form)


# this will allow us to run the app with python
if __name__ == '__main__':
    app.run(debug=True)
