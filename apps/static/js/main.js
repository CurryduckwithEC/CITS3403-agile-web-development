document.addEventListener('DOMContentLoaded', function() {
    function bindLikeEventListeners() {
        const likeIcons = document.querySelectorAll('.like-icon');

        likeIcons.forEach(icon => {
            icon.addEventListener('click', handleLikeClick);  
        });
    }

    function handleLikeClick() {
        const postId = this.getAttribute('data-post-id');
        const likesCount = document.getElementById(`likes-count-${postId}`);
        const currentIcon = this;

        console.log(`Liking post with ID: ${postId}`);

        fetch(`/like/${postId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            if (data.status === 'success') {
                likesCount.textContent = data.likes;
                currentIcon.src = data.liked ? '/static/images/aixin-2.png' : '/static/images/aixin.png';
                console.log(`Post ${postId} liked: ${data.liked}`);
            } else {
                alert(data.message);
            }
        })
        .catch(error => {
            console.error('There was a problem with the fetch operation:', error);
        });
    }

    bindLikeEventListeners();
});
