import * as base from './base.js';

document.addEventListener('DOMContentLoaded', function () {
    const followButton = document.querySelector("#follow-btn");

    base.fetch_user_posts(user_id)
        .then(posts => {
            base.show_posts(posts, '#user_posts_container');
        });

    if (followButton !== null)
        handle_follow_btn(followButton)

});

function handle_follow_btn(followButton) {
    fetch(`/profile/${user_id}/is_followed`)
        .then(response => response.json())
        .then(data => {
            followButton.innerHTML = data.is_followed ? "Unfollow" : "Follow";
            followButton.style.visibility = "visible";
        });

    followButton.addEventListener("click", () => {
        fetch(`/profile/${user_id}/toggle_follow`, {
            method: "POST",
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

