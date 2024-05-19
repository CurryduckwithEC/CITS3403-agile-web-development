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
                                <img class="like-icon heart-icon" src="${post.liked ? '/static/images/aixin-2.png' : '/static/images/aixin.png'}" alt="Like" data-post-id="${post.id}">
                            </button>
                        </div>
                    `;
                    postsContainer.appendChild(postCard);
                });
                if (data.has_next) {
                    const loader = document.createElement('div');
                    loader.className = 'scroll-loader';
                    loader.innerHTML = 'Loading more posts...';
                    postsContainer.appendChild(loader);

                    postsContainer.addEventListener('scroll', function() {
                        if (postsContainer.scrollTop + postsContainer.clientHeight >= postsContainer.scrollHeight) {
                            postsContainer.removeChild(loader);
                            page++;
                            loadPosts(page);
                        }
                    }, { once: true });
                }
                bindLikeEventListeners();
            });
    }

    loadPosts(page);

    function bindLikeEventListeners() {
        const likeIcons = document.querySelectorAll('.like-icon');

        likeIcons.forEach(icon => {
            icon.removeEventListener('click', handleLikeClick); 
            icon.addEventListener('click', handleLikeClick);  
        });
    }

    function handleLikeClick() {
        const postId = this.getAttribute('data-post-id');
        const likesCount = document.getElementById(`likes-count-${postId}`);
        const currentIcon = this;

        fetch(`/like/${postId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                likesCount.textContent = data.likes;
                currentIcon.src = data.liked ? '/static/images/aixin-2.png' : '/static/images/aixin.png';
            } else if (data.status === 'fail' && data.message === 'Already liked') {
                alert('You have already liked this post.');
            } else {
                alert('You must be logged in to like a post.');
            }
        });
    }

    bindLikeEventListeners(); 
});
