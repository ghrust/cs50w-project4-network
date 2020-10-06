document.addEventListener('DOMContentLoaded', function() {

    const likeLinks = document.querySelectorAll('.like-link');
    const csrftoken = document.cookie.match(/csrftoken=([\w-]+)/)[1];

    likeLinks.forEach(link => {
        link.onclick = (event) => {
            const cardBody = event.target.parentElement;

            const data = {
                like_author: document.querySelector('#username').innerHTML,
                liked_post: cardBody.dataset.post_id,
            };

            fetch('/like', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrftoken,
                },
                body: JSON.stringify(data),
            })
                .then(response => response.json())
                .then(data => console.log(data))
                .catch(error => console.error(error));
        };
    });
});
