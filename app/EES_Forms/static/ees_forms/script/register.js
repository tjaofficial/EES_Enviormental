function cert_date1() {
    const position = document.getElementById('id_position').value;
    if (position == 'SGI Technician') {
        document.getElementById('certDateDiv').style.display = 'block';
        document.getElementById('certDateDiv').required = true;
    } else {
        document.getElementById('certDateDiv').required = false;
        document.getElementById('certDateDiv').style.display = 'none';
    }
}