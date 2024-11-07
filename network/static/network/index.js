import * as base from './base.js';

document.addEventListener('DOMContentLoaded', function () {
    base.fetch_new_posts()
        .then(posts => {
            base.show_posts(posts, '#main_container', true);
        });
});


