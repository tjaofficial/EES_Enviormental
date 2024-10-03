
function openClose_modal() {
    const printModal = document.getElementById('print_modal').style;
    //let value = document.getElementById('labelSelect').value;
    printModal.display = 'block';
}

function exit_modal(){
    const printModal = document.getElementById('print_modal').style;
    printModal.display = 'none';
}

window.addEventListener('click', function(e){   
    if (document.getElementById('cancelReg').contains(e.target)){
        console.log('within box')
    } else{
        const printModal = document.getElementById('print_modal').style;
        if (e.target.id != 'printButton'){
            printModal.display = 'none';
        }
    }
});


