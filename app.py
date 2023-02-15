from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(80))
    memos = db.relationship('Memo', backref='author', lazy='dynamic')

    def __repr__(self):
        return '<User %r>' % self.username

class Memo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(120))
    deleted = db.Column(db.Boolean, default=False)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    comments = db.relationship('Comment', backref='memo', lazy='dynamic')

    def __repr__(self):
        return '<Memo %r>' % self.content

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(120))
    memo_id = db.Column(db.Integer, db.ForeignKey('memo.id'))

    def __repr__(self):
        return '<Comment %r>' % self.content

@app.route('/')
def index():
    memos = Memo.query.filter_by(deleted=False).all()
    return render_template('index.html', memos=memos)

@app.route('/memo/<int:memo_id>')
def show(memo_id):
    memo = Memo.query.get(memo_id)
    comments = memo.comments.all()
    return render_template('index.html', memo=memo, comments=comments)

@app.route('/create', methods=['POST'])
def create():
    if 'username' not in session:
        return redirect(url_for('login'))
    memo = Memo(content=request.form['memo'], author_id=session['user_id'])
    db.session.add(memo)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete/<int:memo_id>')
def delete(memo_id):
    memo = Memo.query.get(memo_id)
    if memo.author_id != session['user_id']:
        return redirect(url_for('index'))
    memo.deleted = True
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/recover/<int:memo_id>')
def recover(memo_id):
    memo = Memo.query.get(memo_id)
    if memo.author_id != session['user_id']:
        return redirect(url_for('index'))
    memo.deleted = False
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/memo/<int:memo_id>/comment', methods=['POST'])
def add_comment(memo_id):
    comment = Comment(content=request.form['comment'], memo_id=memo_id)
    db.session.add(comment)
    db.session.commit()
    return redirect(url_for('show', memo_id=memo_id))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user:
            return redirect(url_for('signup'))
        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('signup.html')
    
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            session['username'] = username
            session['user_id'] = user.id
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error='Incorrect username or password')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('user_id', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
