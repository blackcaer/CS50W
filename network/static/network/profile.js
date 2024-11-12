import * as base from './base.js';

document.addEventListener('DOMContentLoaded', function () {
    const followButton = document.querySelector("#follow-btn");

    display_posts_on_site()

    if (followButton !== null)
        handle_follow_btn(followButton)

    document.addEventListener('click', async function (event) {
        if (event.target.matches('.page-link')) {
            await handle_pagination_btns(event);
        }
    });
});

function display_posts_on_site() {
    base.fetch_user_posts(user_id, base.get_page_num())
        .then(resp => {
            document.querySelector('#user_posts_container').innerHTML = '';
            const avalibe_pages_num = resp['page_count']
            base.show_posts(resp['posts'], '#user_posts_container', avalibe_pages_num, false);
        });
}

async function handle_pagination_btns(event) {
    event.preventDefault();

    const pageNum = base.get_clicked_pagination_btn(event)

    const url = new URL(window.location.href);
    url.searchParams.set('page', pageNum);
    history.pushState(null, '', url);

    display_posts_on_site()
}

function handle_follow_btn(followButton) {
    fetch(`/profile/${user_id}/is_followed`)
        .then(response => response.json())
        .then(data => {
            followButton.innerHTML = data.is_followed ? "Unfollow" : "Follow";
            followButton.style.visibility = "visible";
        });

    followButton.addEventListener("click", () => {
        fetch(`/profile/${user_id}/toggle_follow`, {
            method: "PUT",
            headers: {
                "X-CSRFToken": base.get_CRSF_token()
            }
        })
            .then(response => response.json())
            .then(data => {
                followButton.innerHTML = data.is_followed ? "Unfollow" : "Follow";
            });
    });
}

