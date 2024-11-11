
export function get_post_element(post) {
    const postDiv = document.createElement('div');
    postDiv.classList.add('col', 'border', 'rounded', 'border-secondary', 'p-1', 'mt-2', 'shadow');

    const postHeader = `<div class="row mt-2">
            <h4 class="col text-left font-weight-bold">
                <a href="/profile/${post.author.id}">
                    ${post.author.username} 
                </a>
            </h4>
            <div class="col text-right">${new Date(post.date_created).toLocaleString()} </div>
        </div>`;

    const postContent = `<div class="row mt-2">
            <div class="col text-capitalize">
                ${post.content}
            </div>
        </div>`;

    const postFooter = `<div class="row my-2">
            <div class="col">Likes: ${post.users_liking.length} </div>
        </div>`;

    postDiv.innerHTML = postHeader + postContent + postFooter;
    return postDiv;
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
    return parseInt(params.get('page'));
}

function get_pagination(num_pages) {
    let element = `<nav aria-label="Page navigation example">
        <ul class="pagination">
        <li class="page-item"><a class="page-link" href="#">Previous</a></li>`;

    for (let i = 1; i <= num_pages; i++) {
        element += `<li class="page-item"><a class="page-link" href="#">${i}</a></li>`;
    }

    element += `<li class="page-item"><a class="page-link" href="#">Next</a></li>
        </ul>
      </nav>`;

    const div = document.createElement('div')
    div.classList.add('mt-2')
    div.innerHTML = element;
    return div
}

export function show_posts(posts, selector, add_createpost = false, avalibe_pages_num) {
    if (add_createpost)
        document.querySelector(selector).append(get_createpost_element());

    const posts_div = document.createElement('div');
    posts_div.setAttribute('data-role', 'posts-container');
    document.querySelector(selector).append(posts_div);

    posts.forEach(post => {
        posts_div.append(get_post_element(post));
    })

    posts_div.append(get_pagination(avalibe_pages_num));
}

