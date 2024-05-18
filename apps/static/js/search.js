document.getElementById('search-input').addEventListener('input', function() {
    const query = this.value;

    if (query.length < 3) {
        document.getElementById('search-results').innerHTML = '';
        return;
    }

    fetch(`/search?query=${query}`)
        .then(response => response.json())
        .then(data => {
            const resultsContainer = document.getElementById('search-results');
            resultsContainer.innerHTML = '';
            data.forEach(item => {
                const resultItem = document.createElement('a');
                resultItem.className = 'dropdown-item';
                resultItem.href = `/post/${item.id}`;
                resultItem.textContent = item.title;
                resultsContainer.appendChild(resultItem);
            });
            resultsContainer.classList.add('show');
        });
});
