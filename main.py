from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:blogz@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'Sp1VuEMalpPu'

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    body = db.Column(db.String(800))
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    def __init__(self, name, body, author):
        self.name = name
        self.body = body
        self.author = author

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    blogs = db.relationship('Blog', backref='author')

    def __init__(self, username, password):
        self.username = username
        self.password = password

@app.before_request
def require_login():
    allowed_routes = ['login', 'blog_display', 'index', 'signup']
    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect('/login')

@app.route('/', methods=['POST', 'GET'])
def index():
    users = User.query.all()
    return render_template('index.html', users=users)

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            user = existing_user
            if password != user.password:
                flash('Incorrect password', 'error')
                return redirect('/login')
            elif password == user.password:
                session['username'] = user.username
                return redirect('/newpost')
        else:
            flash('Username does not exist', 'error')
    return render_template('login.html')

@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        verify = request.form['verify']
        existing_user = User.query.filter_by(username=username).first()   
    
        if username == '':
            flash('Please enter a username.', 'error')
            return redirect('/signup')
        if len(username) < 3 or len(username) > 20:
            flash('Please enter a valid username.', 'error')
            return redirect('/signup')
        if password == '':
            flash('Please enter a password.', 'error')   
            return redirect('/signup')     
        if len(password) < 3 or len(password) > 20:
            flash('Please enter a valid password.', 'error')
            return redirect('/signup')
        if verify != password:
            flash('Those passwords do not match.', 'error')
            return redirect('/signup')
        if existing_user:
            flash('Username already exists.', 'error')
            return redirect('/signup')
        else:
            new_user = User(username=username, password=password)
            db.session.add(new_user)
            db.session.commit()
            session['username'] = username
        return redirect('/newpost')
    else:
        return render_template('signup.html')

@app.route('/blog', methods=['GET', 'POST'])
def blog_display(): 
 
    if request.args.get('id'):
        id = request.args.get('id')
        blog = Blog.query.get(id)
        name = blog.name
        body = blog.body
        author = blog.author
        return render_template('individual.html', name=name, body=body, author=author)
    if request.args.get('user'):
        user_id = request.args.get('user')
        blogs = Blog.query.filter_by(author_id=user_id)
        return render_template('singleUser.html', blogs=blogs)
   # if request.method == 'POST':
    #    blog_name = request.form['name']
     #   blog = request.form['blog']
      #  author = User.query.filter_by(username=session['username']).first()
       # new_blog = Blog(blog_name, blog, author)
        #db.session.add(new_blog)
        #db.session.commit()
        #return redirect('/blog?id={0}'.format(new_blog.id))

    blogs = Blog.query.all()
    users = User.query.all()

    return render_template('blog.html', blogs=blogs, users=users)
#@app.route('/individual')
#def individual():
   # id = request.args.get('id')
   # blog = Blog.query.filter_by(id=id).first()
   # return render_template('individual.html', blog=blog)
#@app.route('/blog', methods=['POST', 'GET'])
#def user_display():
 #   if request.args.get('id'):
  #      id = request.args.get('id')
   #     blogs = Blog.query.filter_by(author_id=id).all()
    #    return render_template('singleUser.html', blogs=blogs)
 

@app.route('/newpost',methods=['POST', 'GET'])
def add_post():
    if request.method== 'GET':
        return render_template('newpost.html')
    if request.method == 'POST':
        name = request.form['name']
        body = request.form['body']
        author = User.query.filter_by(username=session['username']).first()
        #if not session['username']:
            #return redirect('/login')
        if len(name) == 0:
            flash('Please enter a title.', 'error')
            return render_template('login.html')
        if len(body) == 0:
            flash('Please fill in the body.', 'error')
            return render_template('login.html')  
        else:
            new_blog = Blog(name, body, author)
            db.session.add(new_blog)
            db.session.commit()
            post_id = str(new_blog.id)
            return redirect("/blog?id=" + post_id) 
        return render_template('newpost.html')     

@app.route('/logout')
def logout():
    del session['username']
    return redirect('/')

if __name__ == '__main__':
    app.run()