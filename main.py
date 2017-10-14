from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:build-a-blog@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'Sp1VuEMalpPu'

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    body = db.Column(db.String(800))

    def __init__(self, name, body):
        self.name = name
        self.body = body

@app.route('/', methods=['POST', 'GET'])
def index():
    return render_template('newpost.html')

@app.route('/newpost',methods=['POST', 'GET'])
def add_post():
    if request.method == 'POST':
        blog_name = request.form['name']
        blog_body = request.form['body']
        if len(blog_name) == 0:
            flash('Please enter a title.', 'error')
        if len(blog_body) == 0:
            flash('Please fill in the body.', 'error')
        else:
            new_blog = Blog(blog_name, blog_body)
            db.session.add(new_blog)
            db.session.commit()
            blogs = Blog.query.all()
            return redirect('/blog')

    return render_template('newpost.html')        

@app.route('/blog', methods=['POST', 'GET'])
def blog_display():

    #blog_post = Blog.query.filter_by(id=session['id']).first()

    #if request.method == 'POST':
        #blog_id = int(request.form['blog-id'])
        #blog = Blog.query.get(blog_id)
    blogs = Blog.query.all()
    return render_template('blog.html', title="My Blog", blogs=blogs)

if __name__ == '__main__':
    app.run()