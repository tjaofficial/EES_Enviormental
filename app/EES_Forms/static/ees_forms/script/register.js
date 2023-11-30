window.addEventListener('load', setInitialTab())
document.getElementById("tab1").addEventListener("click", changeTab1);
document.getElementById("tab2").addEventListener("click", changeTab2);
document.getElementById("tab3").addEventListener("click", changeTab3);

function setInitialTab() {
    const access_page = document.getElementById('access_page').value;
    if (access_page == 'form' || access_page == 'observer'){
        changeTab1();
        cert_date1();
    } else if (access_page == 'facility'){
        changeTab2();
    } else if (access_page == 'client'){
        changeTab3();
    }
}

function changeTab1() {
    document.getElementById('login').style.display = 'block';
    document.getElementById('newFacility').style.display = 'none';
    document.getElementById('newClient').style.display = 'none';
    
    document.getElementById('tab1').style.backgroundColor = 'white';
    document.getElementById('tab1').style.color = 'black';
    
    document.getElementById('tab2').style.backgroundColor = '#253544';
    document.getElementById('tab2').style.color = 'white';
    
    document.getElementById('tab3').style.backgroundColor = '#253544';
    document.getElementById('tab3').style.color = 'white';
}
function changeTab2() {
    document.getElementById('login').style.display = 'none';
    document.getElementById('newClient').style.display = 'none';
    document.getElementById('newFacility').style.display = 'block';
    
    document.getElementById('tab2').style.backgroundColor = 'white';
    document.getElementById('tab2').style.color = 'black';
    
    document.getElementById('tab1').style.backgroundColor = '#253544';
    document.getElementById('tab1').style.color = 'white';
    
    document.getElementById('tab3').style.backgroundColor = '#253544';
    document.getElementById('tab3').style.color = 'white';
}
function changeTab3() {
    document.getElementById('login').style.display = 'none';
    document.getElementById('newClient').style.display = 'block';
    document.getElementById('newFacility').style.display = 'none';
    
    document.getElementById('tab2').style.backgroundColor = '#253544';
    document.getElementById('tab2').style.color = 'white';
    
    document.getElementById('tab1').style.backgroundColor = '#253544';
    document.getElementById('tab1').style.color = 'white';
    
    document.getElementById('tab3').style.backgroundColor = 'white';
    document.getElementById('tab3').style.color = 'black';
}

function cert_date1() {
    const position = document.getElementById('id_position').value;
    if (position == 'observer') {
        document.getElementById('certDateDiv').style.display = 'block';
        document.getElementById('id_cert_date').required = true;
        document.getElementById('id_facilityChoice').required = false;
        document.getElementById('facilityNameDiv').style.display = 'none';
    } else if (position == 'client') {
        document.getElementById('facilityNameDiv').style.display = 'block';
        document.getElementById('facilityNameDiv').required = true;
        document.getElementById('certDateDiv').required = false;
        document.getElementById('certDateDiv').style.display = 'none';
    } else {
        document.getElementById('id_cert_date').required = false;
        document.getElementById('id_facilityChoice').required = false;
        document.getElementById('certDateDiv').style.display = 'none';
        document.getElementById('facilityNameDiv').style.display = 'none';
    }
}
