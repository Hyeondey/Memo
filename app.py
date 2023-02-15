from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

memos = []
users = {'hyeondey':'iscool'}
authors = {}


@app.route('/')
def index():
    is_logged_in = 'username' in request.cookies
    return render_template('index.html', memos=memos, is_logged_in=is_logged_in)


@app.route('/create', methods=['GET', 'POST'])
def create():
    is_logged_in = 'username' in request.cookies

    if request.method == 'POST':
        memo = request.form['memo']
        author = request.cookies.get('username')
        memos.append(memo)
        authors[len(memos)] = author
        return redirect(url_for('index'))

    return render_template('index.html', is_logged_in=is_logged_in)


@app.route('/memo/<int:memo_id>')
def show(memo_id):
    is_logged_in = 'username' in request.cookies

    memo = memos[memo_id - 1]
    author = authors.get(memo_id)

    return render_template('index.html', memo=memo, memo_id=memo_id, author=author, is_logged_in=is_logged_in)


@app.route('/update/<int:memo_id>', methods=['GET', 'POST'])
def update(memo_id):
    is_logged_in = 'username' in request.cookies
    author = authors.get(memo_id)
    if not is_logged_in or author != request.cookies.get('username'):
        return redirect(url_for('index'))

    memo = memos[memo_id - 1]

    if request.method == 'POST':
        memo = request.form['memo']
        memos[memo_id - 1] = memo
        return redirect(url_for('index'))

    return render_template('index.html', memo=memo, memo_id=memo_id, is_logged_in=is_logged_in)


@app.route('/delete/<int:memo_id>')
def delete(memo_id):
    is_logged_in = 'username' in request.cookies
    author = authors.get(memo_id)
    if not is_logged_in or author != request.cookies.get('username'):
        return redirect(url_for('index'))

    del memos[memo_id - 1]
    del authors[memo_id]

    return redirect(url_for('index'))

@app.route('/signup')
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users:
            return render_template('signup.html', error='Username already exists')
        else:
            users[username] = password
            return redirect(url_for('index'))
    return render_template('index.html')

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username] == password:
            users[username] = True
            return redirect(url_for('index'))
        else:
            return render_template('index.html', error='Incorrect username or password')
    return render_template('index.html')

@app.route('/signout', methods=['GET', 'POST'])
def signout():
    for username in users:
        users[username] = False
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)