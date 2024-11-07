
export function get_post_element(post)
{
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

export function get_CRSF_input()
{
    return `<input type="hidden" name="csrfmiddlewaretoken" value="${CRSF_TOKEN}">`
}

export function get_createpost_element()
{
    let element = document.createElement('div');
    element.innerHTML =  `<form method="POST" class=" mt-4">
    ${get_CRSF_input()}
    <textarea id="content" name="content" class="form-control" placeholder="How are you feeling?"></textarea>
    <button id="submit_btn" value="submit" type="submit" class="btn btn-primary mt-2"> Create post </button>
    </form>`;
    return element;
}

export async function fetch_new_posts()
{
    const response = await fetch('/get_posts');
    return await response.json();
}

export async function fetch_user_posts(id)
{
    const response = await fetch(`/get_posts/user/${id}`);
    return await response.json();
}

export function show_posts(posts,selector,add_createpost=false)
{
    if (add_createpost)
        document.querySelector(selector).append(get_createpost_element());
    posts.forEach(post => {
        document.querySelector(selector).append(get_post_element(post));
    })
}

