document.addEventListener('DOMContentLoaded', function () {
    show_posts();
});


function get_post_element(post)
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

function show_posts()
{
    fetch('/get_posts',)
    .then(response=>response.json())
    .then(posts=>{
            posts.forEach(post => {
                document.querySelector('#posts_wall').append(get_post_element(post));
            })
        })
}

