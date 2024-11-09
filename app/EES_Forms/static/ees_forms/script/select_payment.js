function changePaymentArea(){
    const button = document.getElementById('saveContinue'),
    cardCont = document.getElementById('cardCont'),
    paypalCont = document.getElementById('paypalCont'),
    optionsCont = document.getElementById('optionsCont'),
    changePayment = document.getElementById('changePayment'),
    orderSummary = document.getElementById('orderSummary'),
    review = document.getElementById('review');
    if (button.style.display == 'block'){
        var set1 = "none",
        set2 = "block";
    } else {
        var set1 = "block",
        set2 = "none";
    }
    for (let i=0; i<optionsCont.children.length-2; i++){
        if (optionsCont.children[i].children[0].checked != true){
            optionsCont.children[i].style.display = set1;
        } else {
            optionsCont.children[i].children[0].style.display = set1;
        }
    }
    button.style.display = set1;
    changePayment.style.display = set2;
    orderSummary.style.display = set2;
    review.style.display = set2;
}
function setReviewInput(){
    document.getElementById("reviewed").checked = false;
    document.getElementById("submit").style.display = 'none';
}
reviewCheck = (elem) => {
    const submit = document.getElementById('submit');
    if (elem.checked) {
        submit.style.display = 'inline';
    } else {
        submit.style.display = 'none';
    }
}
document.getElementById('dataGather').addEventListener('change', paymentSelect)
window.addEventListener('load', checkPaymentOnLoad);

function paymentSelect(event){
    if (event.target.name !== "paymentSelected") {
        return;
    }
    const selectedPayment = document.querySelector('input[name="paymentSelected"]:checked');
    if (selectedPayment && selectedPayment.value === 'new-payment') {
        document.getElementById('newPaymentOptions').style.display = 'block';
        document.getElementById('saveContinue').style.display = 'none';
        let token = selectedPayment.value.slice(5)
        let cardInfoDivList = document.getElementsByClassName('cardInformationDiv');
        for (let x=0; x < cardInfoDivList.length; x++){
            console.log(cardInfoDivList[x])
            let theDiv = cardInfoDivList[x];
            theDiv.style.display = 'none';
            document.getElementById('break-' + theDiv.id).style.display = "none";
        }
    } else {
        document.getElementById('newPaymentOptions').style.display = 'none';
        document.getElementById('saveContinue').style.display = 'block';
        let token = selectedPayment.value.slice(5)
        let cardInfoDivList = document.getElementsByClassName('cardInformationDiv');
        for (let x=0; x < cardInfoDivList.length; x++){
            console.log(cardInfoDivList[x])
            let theDiv = cardInfoDivList[x];
            if (theDiv.id == token) {
                theDiv.style.display = 'block';
                document.getElementById('break-' + theDiv.id).style.display = "block";
                document.getElementById('selectedPaymentToken').value = theDiv.id;
            } else {
                theDiv.style.display = 'none';
                document.getElementById('break-' + theDiv.id).style.display = "none";
            }
        }
    }
}

function checkPaymentOnLoad() {
    const selectedPayment = document.querySelector('input[name="paymentSelected"]:checked');
    if (selectedPayment && selectedPayment.value === 'new-payment') {
        document.getElementById('newPaymentOptions').style.display = 'block';
        document.getElementById('saveContinue').style.display = 'none';
    } else {
        document.getElementById('newPaymentOptions').style.display = 'none';
        document.getElementById('saveContinue').style.display = 'block';
        let token = selectedPayment.value.slice(5)
        let cardInfoDivList = document.getElementsByClassName('cardInformationDiv');
        for (let x=0; x < cardInfoDivList.length; x++){
            console.log(cardInfoDivList[x])
            let theDiv = cardInfoDivList[x];
            if (theDiv.id == token) {
                theDiv.style.display = 'block';
                document.getElementById('break-' + theDiv.id).style.display = "block";
                document.getElementById('selectedPaymentToken').value = theDiv.id;
            } else {
                theDiv.style.display = 'none';
                document.getElementById('break-' + theDiv.id).style.display = "none";
            }
        }
    }
  }
