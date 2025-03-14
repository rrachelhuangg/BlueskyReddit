const modal = document.getElementById('welcome-modal');
const closeModalButton = document.getElementById('close-modal-button');
const loginButton = document.getElementById('submit-button');

const loginModal = document.getElementById('login-modal');
const closeLoginButton = document.getElementById('close-login-button');
const pressButton = document.getElementById('press-button');

function openModal(){
    modal.style.display='flex';
    loginModal.style.display='none';
}

function closeModal(){
    modal.style.display='none';
    loginModal.style.display='flex';
}

function closeLoginModal(){
    modal.style.display='none';
    loginModal.style.display='none';
}

closeModalButton.addEventListener('click', closeModal);
loginButton.addEventListener('click', closeModal);

closeLoginButton.addEventListener('click', closeLoginModal);
pressButton.addEventListener('click', closeLoginModal);