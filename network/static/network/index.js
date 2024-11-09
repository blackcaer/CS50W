import * as base from './base.js';

document.addEventListener('DOMContentLoaded', function () {
    base.fetch_new_posts()
        .then(posts => {
            base.show_posts(posts, '#main_container', true);
        });


    document.addEventListener('submit', async function (event) {
        if (event.target.getAttribute('data-role') === 'create-post') {
            event.preventDefault();
            
            const form = event.target
            const formData = new FormData(form);
            const content = formData.get('content');
            
            const response = await fetch('/add_post', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': base.get_CRSF_token(),
                },
                body: JSON.stringify({ content: content })

            });

            if (response.ok) {
                const newPost = await response.json();
                document.querySelector('[data-role="posts-container"]').prepend(base.get_post_element(newPost));
                form.querySelector('[name="content"]').value='';

            } else {
                console.error('Failed to create post:', response.statusText);
            }
        }
    });
});


