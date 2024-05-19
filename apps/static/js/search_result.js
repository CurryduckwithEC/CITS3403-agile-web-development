document.addEventListener('DOMContentLoaded', function() {
    const query = new URLSearchParams(window.location.search).get('query');

    fetch(`/search?query=${query}`)
        .then(response => response.json())
        .then(data => {
            const resultsContainer = document.getElementById('results-container');
            data.forEach(item => {
                const resultDiv = document.createElement('div');
                resultDiv.className = 'result-item';
                resultDiv.innerHTML = `
                    <h3>${item.title}</h3>
                    <p>${item.content}</p>
                    <a href="/post/${item.id}" class="btn btn-primary">Read More</a>
                `;
                resultsContainer.appendChild(resultDiv);
            });
        });
});
