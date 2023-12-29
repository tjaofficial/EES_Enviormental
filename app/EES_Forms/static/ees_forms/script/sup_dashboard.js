displayGroupOfOvens = (elem) => {
    console.log(elem);
    const dataDiv = document.getElementById('data_'+ elem)
    dataDiv.style.display = 'block';
    let groups = ['5Day', '10Day', '30Day']
    var filteredArray = groups.filter(function(e) { return e !== elem })
    for (let i=0; i<filteredArray.length; i++){
        document.getElementById('data_'+ filteredArray[i]).style.display = 'none';
    }
}