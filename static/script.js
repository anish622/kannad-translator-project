function translateText() {
    const englishText = document.getElementById('englishText').value;
    fetch('/translate', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ text: englishText })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('output').innerText = data.translatedText;
        // Append a unique query parameter (timestamp) to the audio URL
        const audio = new Audio(`/static/${data.audioFile}?t=${new Date().getTime()}`);
        audio.play();
    })
    .catch(error => console.error('Error:', error));
}
