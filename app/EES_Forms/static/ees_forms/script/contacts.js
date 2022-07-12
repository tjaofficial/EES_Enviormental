function getid(obj) {
    const name = document.getElementById("name" + obj.id).innerHTML;
    const email = document.getElementById("email" + obj.id).innerHTML;
    const phone = document.getElementById("phone" + obj.id).innerHTML;
    const cert_date = document.getElementById("cert_date" + obj.id).innerHTML;
    const image = document.getElementById("image" + obj.id).innerHTML;
    document.getElementById("replaceContent").innerHTML = "<div class='contact_data_cont'><div class='contact_image'></div><div class='contact_data_cont_inner'><p>"+name+"</p><div class='contact_data'><p>Phone: "+phone+"</p><p>Email: "+email+"</p><p>Certification Date: "+cert_date+"</p></div></div></div>";
}




