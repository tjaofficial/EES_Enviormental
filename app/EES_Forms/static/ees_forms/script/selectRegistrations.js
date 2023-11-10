adjustPrice = (elem) => {
    const quantity = elem.value;
    console.log(quantity)
    const amount = document.getElementById('adjustedAmount');
    const planPrice = document.getElementById('planPrice');
    const totalPrice = document.getElementById('totalPrice');
    const additionalPrice =  quantity * 75;
    console.log(additionalPrice)
    console.log(planPrice.innerText.slice(1,4))
    amount.innerText = "$" + String(additionalPrice) + ".00";
    totalPrice.innerText = "$" + String(parseInt(additionalPrice) + parseInt(planPrice.innerText.slice(1,4))) + ".00"
}
