document.addEventListener('DOMContentLoaded', function() {
    let page = 1;

    function loadPosts(page) {
        fetch(`/get_trending_posts?page=${page}`)
            .then(response => response.json())
            .then(data => {
                const postsContainer = document.getElementById('trending-posts');
                data.posts.forEach(post => {
                    const postCard = document.createElement('div');
                    postCard.className = 'post-card';
                    postCard.innerHTML = `
                        <h3 class="post-title">${post.title}</h3>
                        <p class="post-content">${post.content}</p>
                        <div class="d-flex justify-content-between align-items-center">
                            <a class="btn btn-primary btn-sm mr-2" href="/post/${post.id}">Read More</a>
                            <button class="btn btn-outline-secondary btn-sm">
                                <img class="like heart-icon" src="${post.liked ? '/static/images/aixin-2.png' : '/static/images/aixin.png'}" alt="Like">
                            </button>
                        </div>
                    `;
                    postsContainer.appendChild(postCard);
                });

                // If there are more posts to load
                if (data.has_more) {
                    const loader = document.createElement('div');
                    loader.className = 'scroll-loader';
                    loader.innerHTML = 'Loading more posts...';
                    postsContainer.appendChild(loader);

                    // Load more posts when scrolled to bottom
                    postsContainer.addEventListener('scroll', function() {
                        if (postsContainer.scrollTop + postsContainer.clientHeight >= postsContainer.scrollHeight) {
                            postsContainer.removeChild(loader);
                            page++;
                            loadPosts(page);
                        }
                    }, { once: true });
                }
            });
    }

    loadPosts(page);
});