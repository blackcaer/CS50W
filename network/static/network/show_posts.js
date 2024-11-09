import * as base from './base.js';

document.addEventListener('DOMContentLoaded', function () {
    const viewFollowing = window.location.pathname === '/following'
    const fetchPosts = (viewFollowing)
        ? base.fetch_posts_by_followed
        : base.fetch_new_posts;

    fetchPosts().then(posts => {
        base.show_posts(posts, '#main_container', isAuthenticated && !viewFollowing);
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
                form.querySelector('[name="content"]').value = '';

            } else {
                console.error('Failed to create post:', response.statusText);
            }
        }
    });
});


