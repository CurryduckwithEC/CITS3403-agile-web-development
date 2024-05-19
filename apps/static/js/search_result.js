document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.querySelector('input[name="query"]');
    const resultsContainer = document.getElementById('results-container');

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
                        if (data.posts.length) {
                            data.posts.forEach(post => {
                                resultsContainer.innerHTML += `<div class="result-item">
                                    <h3>${post.title}</h3>
                                    <p>${post.content}</p>
                                    <small>Author: ${post.author}</small>
                                </div>`;
                            });
                        }
                        if (data.comments.length) {
                            data.comments.forEach(comment => {
                                resultsContainer.innerHTML += `<div class="result-item">
                                    <p>${comment.content}</p>
                                    <small>Author: ${comment.author}</small>
                                </div>`;
                            });
                        }
                        if (data.users.length) {
                            data.users.forEach(user => {
                                resultsContainer.innerHTML += `<div class="result-item">
                                    <p>Username: ${user.username}</p>
                                </div>`;
                            });
                        }
                    });
            } else {
                resultsContainer.innerHTML = '';
            }
        }, 200); // delay in milliseconds
    });
});
