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

#@app.route('/blog', methods=['POST', 'GET'])
#def index():
    #blogs = Blog.query.all()
    #return render_template('blog.html', title="My Blog", blogs=blogs)

@app.route('/blog')
def blog_display(): 

    blogs = Blog.query.all()
    blog_id = request.args.get('id')

    if blog_id:
        individual_blog = Blog.query.filter_by(id=blog_id).first()
        return render_template('individual.html', title="A blog", individual_blog=individual_blog)

    return render_template('blog.html', title="My Blog", blogs=blogs)

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
            post_id = str(new_blog.id)
            return redirect('/blog?id='+ post_id)

    return render_template('newpost.html')        

  
if __name__ == '__main__':
    app.run()