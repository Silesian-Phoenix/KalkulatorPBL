function showPopupBlock() {
    document.getElementById('popup-block').style.display = 'block';
    document.getElementById('popupBlockOverlay').style.display = 'block';
}

function closePopupBlock() {
    document.getElementById('popup-block').style.display = 'none';
    document.getElementById('popupBlockOverlay').style.display = 'none';
}

function checkLesson(lessonId) {
    fetch(`/lessons/${lessonId}`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
    })
        .then(response => response.json())
        .then(data => {
            if (data.result === 'not') {
                showPopupBlock();
            } else if (data.result === 'redirect') {
                window.location.href = data.url;
            }
        })
        .catch(error => console.error('Error:', error));
}