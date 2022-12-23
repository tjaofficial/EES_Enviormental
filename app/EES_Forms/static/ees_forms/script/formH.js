function weatherStoplight() {
    const weatherJson = JSON.parse(document.getElementById('weather').value);
    const wind_speed_start = document.getElementById('id_wind_speed_start').value;
    const wind_speed_stop = document.getElementById('id_wind_speed_stop').value;
    const ambient_temp_start = document.getElementById('id_ambient_temp_start').value;
    const ambient_temp_stop = document.getElementById('id_ambient_temp_stop').value;
    const sky_conditions = document.getElementById('id_sky_conditions').value;
    const wind_direction = document.getElementById('id_wind_direction').value;
    const humidity = document.getElementById('id_humidity').value;

    if (!sky_conditions){
        document.getElementById('id_sky_conditions').placeholder = weatherJson.description;
        document.getElementById('id_sky_conditions').style.backgroundColor = '#FFFA8B';
    } else {
        document.getElementById('id_sky_conditions').style.backgroundColor = '#3c983c85';
    }

    if (!wind_direction){
        document.getElementById('id_wind_direction').placeholder = weatherJson.wind_direction;
        document.getElementById('id_wind_direction').style.backgroundColor = '#FFFA8B';
    } else {
        document.getElementById('id_wind_direction').style.backgroundColor = '#3c983c85';
    }

    if (!humidity){
        document.getElementById('id_humidity').placeholder = weatherJson.humidity;
        document.getElementById('id_humidity').style.backgroundColor = '#FFFA8B';
    } else {
        document.getElementById('id_humidity').style.backgroundColor = '#3c983c85';
    }

    if (!wind_speed_start) {
        document.getElementById('id_wind_speed_start').placeholder = weatherJson.wind_speed;
        document.getElementById('id_wind_speed_start').style.backgroundColor = '#FFFA8B';
    } else {
        document.getElementById('id_wind_speed_start').style.backgroundColor = '#3c983c85';
    }
    if (!ambient_temp_start) {
        document.getElementById('id_ambient_temp_start').placeholder = weatherJson.temperature;
        document.getElementById('id_ambient_temp_start').style.backgroundColor = '#FFFA8B';
    } else {
        document.getElementById('id_ambient_temp_start').style.backgroundColor = '#3c983c85';
    }
}
weatherStoplight();