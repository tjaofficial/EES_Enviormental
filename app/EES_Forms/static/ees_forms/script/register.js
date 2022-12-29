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