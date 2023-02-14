from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

memos = []

@app.route('/')
def index():
    return render_template('index.html', memos=memos)

@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        memo = request.form['memo']
        memos.append(memo)
        return redirect(url_for('index'))
    return render_template('index.html', memos=memos)

@app.route('/memo/<int:memo_id>')
def show(memo_id):
    memo = memos[memo_id - 1]
    return render_template('index.html', memo=memo, memo_id=memo_id)

@app.route('/update/<int:memo_id>', methods=['GET', 'POST'])
def update(memo_id):
    memo = memos[memo_id - 1]
    if request.method == 'POST':
        memo = request.form['memo']
        memos[memo_id - 1] = memo
        return redirect(url_for('index'))
    return render_template('index.html', memo=memo, memo_id=memo_id)

@app.route('/delete/<int:memo_id>')
def delete(memo_id):
    del memos[memo_id - 1]
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)