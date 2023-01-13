function getid(obj) {
    const name = document.getElementById("name" + obj.id).innerHTML;
    const email = document.getElementById("email" + obj.id).innerHTML;
    const phone = document.getElementById("phone" + obj.id).innerHTML;
    const cert_date = document.getElementById("cert_date" + obj.id).innerHTML;
    const image = document.getElementById("image" + obj.id).innerHTML;
    phoneHandler(phone)
    
    document.getElementById("replaceContent").innerHTML = "<div class='contact_data_cont'><div class='contact_image' style='text-align: center;'>"+ image + "</div><div class='contact_data_cont_inner'><p>"+name+"</p><div class='contact_data'><p>Phone: "+phoneHandler(phone)+"</p><p>Email: "+email+"</p><p>Certification Date: "+cert_date+"</p></div></div></div><a href='../../ees_forms/admin/Register/"+email+"'><div id='edit'>Edit</div></a>";
}

function phoneHandler(fullNumber){
    if (fullNumber){
        let number = fullNumber.substring(2);
        let first = number.substring(0,3);
        let middle = number.substring(3,6);
        let end = number.substring(6)
        let parseNumber = '(' + first +') '+middle+'-'+end
        return parseNumber
    } else {
        return '{ No contact number }'
    }
}


