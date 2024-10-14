document.getElementById('search-form').addEventListener('submit', function (event) {
    event.preventDefault();

    let query = document.getElementById('query').value;
    let resultsDiv = document.getElementById('results');
    resultsDiv.innerHTML = '';

    fetch('/search', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: new URLSearchParams({
            'query': query
        })
    })
        .then(response => response.json())
        .then(data => {
            console.log(data);
            displayResults(data);
            displayChart(data);
        });
});

function displayResults(data) {
    let resultsDiv = document.getElementById('results');
    resultsDiv.innerHTML = '<h2>Results</h2>';
    for (let i = 0; i < data.documents.length; i++) {
        let docDiv = document.createElement('div');
        docDiv.innerHTML = `<strong>Document ${data.indices[i]}</strong><p>${data.documents[i]}</p><br><strong>Similarity: ${data.similarities[i]}</strong>`;
        resultsDiv.appendChild(docDiv);
    }
}

function displayChart(data) {
    const ctx = document.getElementById('similarity-chart').getContext('2d');

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: data.indices, // x-axis: document indices
            datasets: [{
                label: 'Cosine Similarities',
                data: data.similarities, // y-axis: similarity values
                backgroundColor: 'rgba(75, 192, 192, 0.2)', // Bar colors
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true, // Ensure y-axis starts at 0
                    title: {
                        display: true,
                        text: 'Similarity'
                    }
                },
                x: {
                    title: {
                        display: true,
                        text: 'Document Index'
                    }
                }
            }
        }
    });
}
