from apps import db
from apps.models import User, Post, Tag

# Create a test user
test_user = User(username='testuser', email='testuser@example.com')
test_user.set_password('password')
db.session.add(test_user)
db.session.commit()

# Create some tags
tag1 = Tag(name='tag1')
tag2 = Tag(name='tag2')
tag3 = Tag(name='tag3')

db.session.add(tag1)
db.session.add(tag2)
db.session.add(tag3)
db.session.commit()

# Create some test posts
post1 = Post(title='First Post', content='This is the first test post content.', user_id=test_user.id)
post2 = Post(title='Second Post', content='This is the second test post content with more details.', user_id=test_user.id)
post3 = Post(title='Third Post', content='This post contains the keyword search.', user_id=test_user.id)

# Associate tags with posts
post1.tags.append(tag1)
post2.tags.append(tag2)
post3.tags.append(tag3)
post3.tags.append(tag1)  # Example of a post with multiple tags

db.session.add(post1)
db.session.add(post2)
db.session.add(post3)
db.session.commit()

print("Test data added successfully.")
