
function htmlList(list) {
    list = list.replace('[','').replace(']','')
    list = list.split(',')
    let htmlCode = "<ul>"
    for (let i=0; i<list.length; i++){
        htmlCode += "<li style='list-style-type: disc; display: list-item;list-style-position: inside;margin: 0px;'>" + list[i].replace("'","").replace("'","") + "</li>"
    }
    htmlCode += '</ul>'
    return htmlCode
}

function getid(obj) {
    const facility = document.getElementById('facility').innerHTML;
    const name = document.getElementById("name" + obj.id).innerHTML;
    const email = document.getElementById("email" + obj.id).innerHTML;
    const phone = document.getElementById("phone" + obj.id).innerHTML;
    const cert_date = document.getElementById("cert_date" + obj.id).innerHTML;
    const certs = document.getElementById("certs" + obj.id).innerHTML;
    const userID = document.getElementById("userID" + obj.id).innerHTML;
    const image = document.getElementById("image" + obj.id).innerHTML;
    console.log(facility);
    console.log(obj);
    
    // for (i=1; i<certs.length; i++){

    // }
    document.getElementById("replaceContent").innerHTML = "<div class='cardHeader'>" + name + "</div><div class='contact_data_cont'><div class='contact_image' style='text-align: center;'>"+ image + "</div><div class='contact_data_cont_inner'><div class='contact_data'><p class='categoryStyle'>Phone: " + phoneHandler(phone) + "</p><p class='categoryStyle'>Email: " + email + "</p><p class='categoryStyle'>Smoke Certification: " + cert_date + "</p><p style=''>Certifications:<br> " + htmlList(certs) + "</p></div></div></div><a href='../../" + facility + "/Register/" + userID + "'><div id='edit'>Edit</div></a>";
}

function phoneHandler(fullNumber){
    console.log(fullNumber)
    if (fullNumber){
        // let number = fullNumber.substring(2);
        // let first = number.substring(0,3);
        // let middle = number.substring(3,6);
        // let end = number.substring(6)
        // let parseNumber = '(' + first +')'+middle+'-'+end
        return fullNumber
    } else {
        return '{ No contact number }'
    }
}


