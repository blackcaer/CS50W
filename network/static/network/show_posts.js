import * as base from './base.js';


const viewFollowing = window.location.pathname === '/following'
    const fetchPosts = (viewFollowing)
        ? base.fetch_posts_by_followed
        : base.fetch_new_posts;

document.addEventListener('DOMContentLoaded', function () {
    display_posts_on_site();
    
    window.addEventListener('popstate', async function(){await display_posts_on_site()});
    
    document.addEventListener('click', async function (event) {
        if (event.target.matches('.page-link')) {
            await handle_pagination_btns(event);
        }
    });

    document.addEventListener('submit', async function (event) {
        if (event.target.getAttribute('data-role') === 'create-post') {
            await createpost_handler(event);
        }
    });
});

async function handle_pagination_btns(event) {
    event.preventDefault();
    
    const pageNum = base.get_clicked_pagination_btn(event)

    const url = new URL(window.location.href);
    url.searchParams.set('page', pageNum);
    history.pushState(null, '', url);
    
    display_posts_on_site()
}

async function display_posts_on_site()
{
    fetchPosts(base.get_page_num())
    .then(resp => {
        document.querySelector('#main_container').innerHTML='';
        const avalibe_pages_num = resp['page_count']
        base.show_posts(resp['posts'], '#main_container', avalibe_pages_num, isAuthenticated && !viewFollowing);
    });

}

async function createpost_handler(event)
{
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
        document.querySelector('[data-role="posts-container"]').prepend(base.get_post_element(newPost,true));
        form.querySelector('[name="content"]').value = '';

    } else {
        console.error('Failed to create post:', response.statusText);
    }
}