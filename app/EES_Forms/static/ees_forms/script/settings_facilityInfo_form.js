function batteryInformation(){
    const batteryInfo = document.getElementById('batteryInfo');
    const cokeBattery = document.getElementById('cokeBattery');

    if (cokeBattery) {
        if (cokeBattery.value == "Yes"){
            batteryInfo.style.display = 'block';
        } else {
            batteryInfo.style.display = 'none';
        }
    }
}
batteryInformation();