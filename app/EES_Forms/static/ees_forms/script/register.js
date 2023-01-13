
//document.getElementById('id_password1').autocomplete = false;
//document.getElementById('id_password2').required = false;

function cert_date1() {
    const position = document.getElementById('id_position').value;
    if (position == 'SGI Technician') {
        document.getElementById('certDateDiv').style.display = 'block';
        document.getElementById('certDateDiv').required = true;
        document.getElementById('facilityNameDiv').required = false;
        document.getElementById('facilityNameDiv').style.display = 'none';
    } else if (position == 'EES Coke Employees') {
        document.getElementById('facilityNameDiv').style.display = 'block';
        document.getElementById('facilityNameDiv').required = true;
        document.getElementById('certDateDiv').required = false;
        document.getElementById('certDateDiv').style.display = 'none';
    } else {
        document.getElementById('certDateDiv').required = false;
        document.getElementById('facilityNameDiv').required = false;
        document.getElementById('certDateDiv').style.display = 'none';
        document.getElementById('facilityNameDiv').style.display = 'none';
    }
}
cert_date1();
document.getElementById("tab1").addEventListener("click", changeTab1);
document.getElementById("tab2").addEventListener("click", changeTab2);

function changeTab1() {
    document.getElementById('login').style.display = 'block';
    document.getElementById('newClient').style.display = 'none';

    document.getElementById('tab1').style.backgroundColor = 'white';
    document.getElementById('tab1').style.color = 'black';

    document.getElementById('tab2').style.backgroundColor = '#6c7d88';
    document.getElementById('tab2').style.color = 'white';
}
function changeTab2() {
    document.getElementById('login').style.display = 'none';
    document.getElementById('newClient').style.display = 'block';

    document.getElementById('tab2').style.backgroundColor = 'white';
    document.getElementById('tab2').style.color = 'black';

    document.getElementById('tab1').style.backgroundColor = '#6c7d88';
    document.getElementById('tab1').style.color = 'white';
}