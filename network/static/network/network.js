document.addEventListener('DOMContentLoaded', function() {

    // Edit post.
    let editPostLinks = document.querySelectorAll('.edit-post-link');

    editPostLinks.forEach(link => {
        link.onclick = (event) => {

            // Hide post.
            const cardBody = event.target.parentElement;
            cardBody.style.display = 'none';

            // Render bond form.
            const form = document.createElement('form');
            form.onsubmit = function(event) {
                event.preventDefault();
                const request = new XMLHttpRequest();
                request.open('POST', '/edit_post', true);
                const csrftoken = getCookie('csrftoken');
                request.setRequestHeader('X-CSRFToken', csrftoken);

                request.onload = function() {
                    console.log(this.response);
                    form.style.display = 'none';
                    cardBody.querySelector('.card-text').innerText = textarea.value;
                    cardBody.style.display = 'block';
                };

                request.send();
            };

            const textarea = document.createElement('textarea');
            textarea.classList.add('w-100');
            textarea.value = cardBody.querySelector('.card-text').innerText;

            const inputSubmit = document.createElement('input');
            inputSubmit.type = 'submit';
            inputSubmit.value = 'Save';
            inputSubmit.classList.add('btn', 'btn-primary', 'w-100');

            form.appendChild(textarea);
            form.appendChild(inputSubmit);
            cardBody.parentNode.appendChild(form);

            event.preventDefault();
        };
    });
});


function getCookie(name) {
    // Get cooke with <name> name.
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
