let addedComponents = [];
document.addEventListener("DOMContentLoaded", function(){
    const addComponentButton = document.getElementById('add-button');
    const addComponentModal = document.getElementById('add-component-modal');
    const closeComponentModal = document.getElementById('close-modal-button');
    const addButton = document.getElementById('apply-changes-button');

    function openAddComponentModal(){
        addComponentModal.style.display='flex';
    }

    function closeModal(){
        addComponentModal.style.display='none';
    }

    addComponentButton.addEventListener('click', openAddComponentModal);
    closeComponentModal.addEventListener('click', closeModal);

    const addAccountButton = document.getElementById('add-account-button');
    const componentTagsContainer = document.getElementById('added-components-container');
    const applyChangesButton = document.getElementById('apply-changes-button');
    const accountInput = document.getElementById('account');
    addAccountButton.addEventListener('click', function(event){
        event.preventDefault();
        const accountHandle = accountInput.value;
        addedComponents.push(accountHandle);
        let componentTag = document.createElement('div');
        componentTag.classList.add('added-component-tag');
        componentTag.innerHTML = `${accountHandle} <span class="remove-component-tag" data-handle="${accountHandle}">x</span>`;
        componentTagsContainer.appendChild(componentTag);
        accountInput.value='';
    });

    componentTagsContainer.addEventListener('click', function(event){
        if(event.target.classList.contains('remove-component-tag')){
            const handleToRemove = event.target.getAttribute('data-handle');
            addedComponents = addedComponents.filter(handle=>handle!==handleToRemove);
            event.target.parentElement.remove();
        }
    });

    const postsContainer = document.getElementById('posts-container');
    let posts;

    async function fetchPosts(){
        try{
            const response = await fetch('/get_posts',{
                method: 'POST',
                headers:{
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({handles:addedComponents})
            });
            posts = await response.json();
            renderPosts(posts);
        } catch (error){
            console.log("Error fetching posts: ", error);
        }
    }

    function renderPosts(posts){
        postsContainer.innerHTML='';
        posts.forEach(post=>{
            const postElement = document.createElement('div');
            postElement.classList.add('skeet-card');
            postElement.innerHTML = `<div class="username">${post.name}<span class="handle">@${post.handle}</span><span class="handle">• 7h</span></div>
            <div class = "content">
                ${post.text_content}
            </div>
            <div class = "status">
                <span class="status-chunk"><img src="../static/images/comment_icon.png" class="status-icon"/><span>${post.reply_count}</span></span><span class="filler"></span>
                <span class="status-chunk"><img src="../static/images/repost_icon.png" class="status-icon"/><span>${post.repost_count}</span></span><span class="filler"></span>
                <span class="status-chunk"><img src="../static/images/like_icon.png" class="status-icon"/><span>${post.like_count}</span></span><span class="filler"></span>
                <span class="status-chunk"><img src="../static/images/hamburger_icon.png" class="status-icon"/></span>
            </div>
            `;
            postsContainer.appendChild(postElement);
        });
    }

    applyChangesButton.addEventListener('click', async function(event){
        event.preventDefault();
        fetchPosts();
    });

    addButton.addEventListener('click', closeModal);

    addComponentModal.addEventListener('click', function(e){
        if(e.target===addComponentModal){
            closeModal();
        }
    });

});