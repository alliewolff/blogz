from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://get-it-done:beproductive@localhost:8889/get-it-done'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    body = db.Column(db.String(800))
    #completed = db.Column(db.Boolean)

    def __init__(self, name):
        self.name = name
        self.completed = False


@app.route('/', methods=['POST', 'GET'])
def index():

    if request.method == 'POST':
        blog_name = request.form['task']
        new_blog = Blog(blog_name)
        db.session.add(new_blog)
        db.session.commit()

    blogs = Blog.query.filter_by(completed=False).all()
    completed_blogs = Blog.query.filter_by(completed=True).all()
    return render_template('todos.html',title="My Blog", 
        blogs=blogs, completed_blogs=completed_blogs)


@app.route('/delete-task', methods=['POST'])
def delete_task():

    blog_id = int(request.form['task-id'])
    blog = Blog.query.get(blog_id)
    blog.completed = True
    db.session.add(task)
    db.session.commit()

    return redirect('/')


if __name__ == '__main__':
    app.run()