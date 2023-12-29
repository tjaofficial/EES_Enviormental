//document.getElementById('adminLabel').addEventListener('click', collapse1)
//document.getElementById('reportsLabel').addEventListener('click', collapse2)
//document.getElementById('sbClient').addEventListener('click', collapse3)
//document.getElementById('calendarLabel').addEventListener('click', collapse4)

function collapse1(){
    const adminDisplay = document.getElementById('adminGroup').style.display;
    if(adminDisplay == 'block'){
        document.getElementById('adminGroup').style.display = 'none';
    } else {
        document.getElementById('adminGroup').style.display = 'block';
    }
}
function collapse2(){
    const reportsDisplay = document.getElementById('reportsGroup').style.display;
    if(reportsDisplay == 'block'){
        document.getElementById('reportsGroup').style.display = 'none';
    } else {
        document.getElementById('reportsGroup').style.display = 'block';
    }
}
function collapse3(){
    const clientDisplay = document.getElementById('sbClientGroup').style.display;
    if(clientDisplay == 'block'){
        document.getElementById('sbClientGroup').style.display = 'none';
    } else {
        document.getElementById('sbClientGroup').style.display = 'block';
    }
}
function collapse4(){
    const calendarDisplay = document.getElementById('calendarGroup').style.display;
    if(calendarDisplay == 'block'){
        document.getElementById('calendarGroup').style.display = 'none';
    } else {
        document.getElementById('calendarGroup').style.display = 'block';
    }
}