autoFillZeros = (divID) => {
    console.log(divID)
    const inputValue = document.getElementById(divID).value;
    console.log(inputValue)
    if (inputValue == 'fil'){
        let parseID = divID.slice(0,-1)
        console.log(parseID)
        for (i=1;i<13;i+=1){
            document.getElementById(parseID+i).value = 0;
        }
    } 
}