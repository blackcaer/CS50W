import * as base from './base.js';

document.addEventListener('DOMContentLoaded', function () {
    base.fetch_user_posts(user_id)
        .then(posts => {
            base.show_posts(posts, '#user_posts_container'); 
        });
});


