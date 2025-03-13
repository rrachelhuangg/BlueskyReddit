const modal = document.getElementById('login-modal');
const closeModalButton = document.getElementById('close-modal-button');
const loginButton = document.getElementById('submit-button');

function openModal(){
    modal.style.display='flex';
}

function closeModal(){
    modal.style.display='none';
}

closeModalButton.addEventListener('click', closeModal);
loginButton.addEventListener('click', closeModal);

modal.addEventListener('click', function(e){
    if(e.target===modal){
        closeModal();
    }
});