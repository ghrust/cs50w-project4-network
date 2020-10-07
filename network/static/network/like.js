document.addEventListener('DOMContentLoaded', function() {

    const likeLinks = document.querySelectorAll('.like-link');
    const csrftoken = document.cookie.match(/csrftoken=([\w-]+)/)[1];

    likeLinks.forEach(link => {
        link.onclick = (event) => {
            const cardBody = event.target.parentElement;
            try {
                var like_author = document.querySelector('#username').innerHTML;
            } catch (TypeError) {
                alert("Please log in.");
                return false;
            }

            const data = {
                like_author: like_author,
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
                .then(data => {
                    event.target.innerHTML = data.likes;
                })
                .catch(error => console.error(error));
        };
    });
});
