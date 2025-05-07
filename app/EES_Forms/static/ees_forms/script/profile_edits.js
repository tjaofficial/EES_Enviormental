function cert_date1() {
    const position = document.getElementById('id_position').value;
    if (position == 'observer') {
        document.getElementById('certDateDiv').style.display = 'block';
        document.getElementById('id_cert_date').required = true;
        document.getElementById('facilityNameDiv').style.display = 'none';
    } else if (position == 'client') {
        document.getElementById('certDateDiv').required = false;
        document.getElementById('certDateDiv').style.display = 'none';
        document.getElementById('facilityNameDiv').style.display = 'block';
        document.getElementById('facilityNameDiv').required = true;
    } else {
        document.getElementById('id_cert_date').required = false;
        document.getElementById('certDateDiv').style.display = 'none';
        document.getElementById('facilityNameDiv').style.display = 'none';
    }
}
cert_date1()