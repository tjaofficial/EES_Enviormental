function changePaymentArea(){
    const button = document.getElementById('saveContinue'),
    cardCont = document.getElementById('cardCont'),
    paypalCont = document.getElementById('paypalCont'),
    optionsCont = document.getElementById('optionsCont'),
    addNewCard = document.getElementById('addNewCard'),
    orderSummary = document.getElementById('orderSummary'),
    review = document.getElementById('review');
    console.log(optionsCont.children);
    for (let i=0; i<optionsCont.children.length; i++){
        if (optionsCont.children[i].children[0].checked != true){
            optionsCont.children[i].style.display = 'none';
        } else {
            optionsCont.children[i].children[0].style.display = 'none';
        }
    }
    button.style.display = 'none';
    addNewCard.style.display = 'none';
    orderSummary.style.display = 'block';
    review.style.display = 'block';
}
reviewCheck = (elem) => {
    const submit = document.getElementById('submit');
    if (elem.checked) {
        submit.style.display = 'inline';
    } else {
        submit.style.display = 'none';
    }
}

