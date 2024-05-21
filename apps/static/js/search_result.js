document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.querySelector('input[name="query"]');
    const resultsContainer = document.getElementById('results-container');

    resultsContainer.style.display = 'none';

    let timeout = null;
    searchInput.addEventListener('keyup', function() {
        clearTimeout(timeout);
        timeout = setTimeout(function() {
            const query = searchInput.value;
            if (query.length > 2) {
                fetch(`/search?query=${query}`)
                    .then(response => response.json())
                    .then(data => {
                        resultsContainer.innerHTML = '';
                        if (data.posts.length || data.comments.length || data.users.length || data.tags.length) {
                            resultsContainer.style.display = 'block';
                            if (data.posts.length) {
                                resultsContainer.innerHTML += `<h3>Posts</h3>`;
                                data.posts.forEach(post => {
                                    resultsContainer.innerHTML += `<div class="result-item">
                                        <h4><a href="/post/${post.id}">${post.title}</a></h4>
                                        <p>${post.content}</p>
                                        <small>Author: ${post.author}</small>
                                        <p>Tags: ${post.tags.join(', ')}</p>
                                    </div>`;
                                });
                            }
                            if (data.comments.length) {
                                resultsContainer.innerHTML += `<h3>Comments</h3>`;
                                data.comments.forEach(comment => {
                                    resultsContainer.innerHTML += `<div class="result-item">
                                        <p>${comment.content}</p>
                                        <small>Author: ${comment.author}</small>
                                    </div>`;
                                });
                            }
                            if (data.users.length) {
                                resultsContainer.innerHTML += `<h3>Users</h3>`;
                                data.users.forEach(user => {
                                    resultsContainer.innerHTML += `<div class="result-item">
                                        <p><a href="/profile/${user.username}">${user.username}</a></p>
                                    </div>`;
                                });
                            }
                            if (data.tags.length) {
                                resultsContainer.innerHTML += `<h3>Tags</h3>`;
                                data.tags.forEach(tag => {
                                    resultsContainer.innerHTML += `<div class="result-item">
                                        <p>Tag: ${tag.name}</p>
                                    </div>`;
                                });
                            }
                        } else {
                            resultsContainer.style.display = 'none';
                        }
                    });
            } else {
                resultsContainer.innerHTML = '';
                resultsContainer.style.display = 'none';
            }
        }, 200);
    });
});
