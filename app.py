from flask import Flask, render_template, url_for, redirect, request, jsonify
from dataclasses import dataclass

app = Flask(__name__)

# Mock database
@dataclass
class Post:
    id: int
    title: str
    content: str
    liked: bool

posts = [
    Post(id=1, title="First Post", content="Content of the first post", liked=False),
    Post(id=2, title="Second Post", content="Content of the second post", liked=True),
]

@app.route('/')
def main():
    posts = [
        {'id': 1, 'title': 'First Post', 'content': 'This is the content of the first post.'},
        {'id': 2, 'title': 'Second Post', 'content': 'This is the content of the second post.'}
    ]
    return render_template('main.html', posts=posts)
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
    new_post = Post(id=len(posts) + 1, title=title, content=content, liked=False)
    posts.append(new_post)
    return redirect(url_for('main'))

@app.route('/view_post/<int:post_id>')
def view_post(post_id):
    post = next((post for post in posts if post.id == post_id), None)
    if post:
        return render_template('view_post.html', post=post)
    return "Post not found", 404

@app.route('/toggle_like/<int:post_id>', methods=['POST'])
def toggle_like(post_id):
    post = next((post for post in posts if post.id == post_id), None)
    if post:
        post.liked = not post.liked
        return jsonify(success=True, liked=post.liked)
    return jsonify(success=False), 404

if __name__ == '__main__':
    app.run(debug=True)
