
export function get_post_element(post, with_edit = false) {
    const postDiv = document.createElement('div');
    postDiv.classList.add('col', 'border', 'rounded', 'border-secondary', 'p-1', 'mt-2', 'shadow');
    postDiv.id = `post-${post.id}`;
    postDiv.setAttribute('data-role', 'post-container');

    const postHeader = `<div class="row mt-2">
            <h4 class="col text-left font-weight-bold">
                <a href="/profile/${post.author.id}">
                    ${post.author.username} 
                </a>
            </h4>
            <div class="col text-right">${new Date(post.date_created).toLocaleString()} </div>
        </div>`;

    const postEdit = (with_edit) ? `<div class="row mt-2">
            <div class="col">
                <a href="#" class="m-0" data-role="edit-link">Edit</a>
            </div>
        </div>` : '';

    const postContent = `<div class="row mt-2">
        <div class="col" data-role="post-content">
            ${post.content}
        </div>
    </div>`;

    const postFooter = `<div class="row my-2">
            <div class="col">Likes: ${post.users_liking.length} </div>
        </div>`;

    postDiv.innerHTML = postHeader + postEdit + postContent + postFooter;
    return postDiv;
}


export function handleEditClick(postId) {
    const postContentDiv = document.querySelector(`#post-${postId} [data-role="post-content"]`);
    const currentContent = postContentDiv.textContent.trim();

    postContentDiv.innerHTML = `
<textarea id="edit-content-${postId}" class="form-control">${currentContent}</textarea>
<button data-role="save-post" class="btn btn-primary mt-2">Save</button>
    `;
}
export async function handleSaveClick(postId) {
    const newContent = document.getElementById(`edit-content-${postId}`).value;
    console.log("postid: ",postId)
    console.log("newContent: ",newContent)

    try {
        const response = await fetch(`/update_post/${postId}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': get_CRSF_token(),
            },
            body: JSON.stringify({ content: newContent })
        });
        console.log("resp: ",response)
        if (response.ok) {
            const postContentDiv = document.querySelector(`#post-${postId} [data-role="post-content"]`);
            postContentDiv.innerHTML = newContent;
        } else {
            console.error('Failed to update post:', response.statusText);
        }
    } catch (error) {
        console.error('Error:', error);
    }
}


export function get_CRSF_token() {
    return document.querySelector("input[name=csrfmiddlewaretoken]").value;
}

export function get_createpost_element() {
    let element = document.createElement('div');
    element.innerHTML = `<form data-role="create-post" class=" mt-4">
    <textarea name="content" class="form-control" placeholder="How are you feeling?"></textarea>
    <button type="submit" class="btn btn-primary mt-2">Create post</button>
    </form>`;
    return element;
}

async function fetch_posts(endpoint, params = {}) {
    try {
        const url = new URL(endpoint, window.location.origin);
        Object.keys(params).forEach(key => url.searchParams.append(key, params[key]));

        const response = await fetch(url);
        if (!response.ok) {
            throw new Error(`Error: ${response.statusText}`);
        }
        return await response.json();
    } catch (error) {
        console.error(`Failed to fetch posts from ${endpoint}:`, error);
    }
}

export async function fetch_new_posts(pageNum = 1) {
    return await fetch_posts('/get_posts', { page: pageNum });
}

export async function fetch_posts_by_followed(pageNum = 1) {
    return await fetch_posts('/get_posts', { followed: 'true', page: pageNum });
}

export async function fetch_user_posts(id, pageNum = 1) {
    return await fetch_posts('/get_posts', { user_id: id, page: pageNum });
}

export function get_page_num() {
    const url = new URL(window.location.href);
    const params = new URLSearchParams(url.search);
    const pageNum = parseInt(params.get('page'));

    if (isNaN(pageNum) || pageNum==undefined)
        return 1;
    return pageNum;
}

function get_pagination(max_pages) {
    const pageNum = get_page_num();
    const div = document.createElement('div');
    div.classList.add('mt-2');

    if (max_pages === 1)
        return document.createElement('div'); 

    let element = `<nav aria-label="Page navigation" data-maxpage="${max_pages}">
        <ul class="pagination">`

    if (pageNum > 1)
        element += `<li class="page-item"><a class="page-link" href="#" data-page="prev">Previous</a></li>`;

    for (let i = 1; i <= max_pages; i++){
        const activeClass = i === pageNum ? 'active' : '';
        element += `<li class="page-item ${activeClass}"><a class="page-link" href="#" data-page="${i}">${i}</a></li>`;
    }
    if (pageNum < max_pages)
        element += `<li class="page-item"><a class="page-link" href="#" data-page="next">Next</a></li>`;
    element += `</ul></nav>`;

    div.innerHTML = element;

    return div;
}


export function show_posts(posts, selector, avalibe_pages_num,add_createpost = false) {
    if (add_createpost)
        document.querySelector(selector).append(get_createpost_element());

    const posts_div = document.createElement('div');
    posts_div.setAttribute('data-role', 'posts-container');
    document.querySelector(selector).append(posts_div);

    posts.forEach(post => {
        const with_edit = (post.author.id===logged_user_id);

        const new_post_el = get_post_element(post,with_edit);

        new_post_el.addEventListener('click', function(event) {
            const target = event.target;
            
            if (target.matches('[data-role="edit-link"]')) {
                event.preventDefault();
                const postId = target.closest('[data-role="post-container"]').id.split('-')[1];
                handleEditClick(postId);
            }
    
            if (target.matches('[data-role="save-post"]')) {
                event.preventDefault();
                const postId = target.closest('[data-role="post-container"]').id.split('-')[1];
                handleSaveClick(postId);
            }
        });
        posts_div.append(new_post_el);
    })

    posts_div.append(get_pagination(avalibe_pages_num));
}

export function get_clicked_pagination_btn(event) {
    const clicked_page = event.target.getAttribute('data-page');
    const max_pages = event.target.parentNode.parentNode.parentNode.getAttribute('data-maxpage');

    let pageNum;
    if (clicked_page === 'prev') {
        pageNum = Math.min(Math.max(1, get_page_num() - 1),max_pages);
    } else if (clicked_page === 'next') {
        pageNum = Math.max(Math.min(get_page_num() + 1,max_pages),1);
    } else {
        pageNum = parseInt(clicked_page);
    }
    return pageNum;
}