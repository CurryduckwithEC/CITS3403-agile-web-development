from flask import Flask, render_template, url_for

app = Flask(__name__)

@app.route('/')
def main():
    return render_template('main.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/post')
def post():
    return render_template('post.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/submit_post', methods=['POST'])
def submit_post():
    title = request.form['title']
    tags = request.form['tags']
    content = request.form['content']
    return redirect(url_for('main')) 

if __name__ == '__main__':
    app.run(debug=True)

