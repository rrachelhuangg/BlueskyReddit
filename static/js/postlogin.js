const addComponentButton = document.getElementById('add-button');
const addComponentModal = document.getElementById('add-component-modal');
const closeComponentModal = document.getElementById('close-modal-button');
const closeComponentModal2 = document.getElementById('close-add-component-button');
const addButton = document.getElementById('apply-changes-button');

const addAccount = document.getElementById('add-account-button');
addAccount.addEventListener('click', function(){
    const addedAccount = addAccount.value;
    fetch('/',{
        method:'POST',
        headers:{
            'Content-Type': 'application/json'
        },
        body:JSON.stringify({account:addedAccount})
    }).then(response=>response.json()).then(data=>{console.log("SUCCESS: ", addedAccount);}).catch(error=>{console.error("ERROR: ", error);})
})

function openAddComponentModal(){
    addComponentModal.style.display='flex';
}

function closeModal(){
    addComponentModal.style.display='none';
}

addComponentButton.addEventListener('click', openAddComponentModal);
closeComponentModal.addEventListener('click', closeModal);
closeComponentModal2.addEventListener('click', closeModal);
addButton.addEventListener('click', closeModal);

addComponentModal.addEventListener('click', function(e){
    if(e.target===addComponentModal){
        closeModal();
    }
});