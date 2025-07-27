const submitButton = document.getElementById('submit');
document.addEventListener('DOMContentLoaded', () => {
    const leakPushDoors = document.getElementById('noomLeaksCheckbox');
    const leakCokeDoors = document.getElementById('nolLeaksCheckbox');
    one_pass_func();
    toggleLeaksMode(leakPushDoors);
    toggleLeaksMode(leakCokeDoors);
    set_not_observed('om');
    set_not_observed('l');
    check_dampered_inoperable('om');
    check_dampered_inoperable('l');

    total_leaking_doors('om');
    total_leaking_doors('l');
    total_time('offtakes');
    total_time('lids');
    inoperable_ovens();
    allowed_time('om');
    allowed_time('l');
    equation('om');
    equation('l');
});

function toggleLeaksMode(elem) {
    if (!elem) return;
    const side = elem.dataset.side;
    const checked = document.getElementById(`no${side}LeaksCheckbox`).checked;
    const table = document.getElementById(`${side}LeaksTable`);
    const header = document.getElementById(`${side}LeaksSubHeader`);
    const noLeaksMsg = document.getElementById(`no${side}LeaksMsg`);

    if (checked) {
        table.style.display = "none";
        header.style.display = "none";
        noLeaksMsg.style.display = "block";
        const allAreaLeaks = table.querySelectorAll(`[id*="${side}_location_"], [id*="${side}_oven_"]`)
        allAreaLeaks.forEach((el) => {
            el.removeAttribute("required");
        })
    } else {
        table.style.display = "table";
        header.style.display = "table-header-group";
        noLeaksMsg.style.display = "none";
        const allAreaLeaks = table.querySelectorAll(`[id*="${side}_location_"], [id*="${side}_oven_"]`)
        allAreaLeaks.forEach((el) => {
            el.setAttribute("required", true);
        })
    }
}

function total_leaking_doors(side) {
    if (!document.getElementById(`no${side}LeaksCheckbox`)) return;
    let allLeakElements = document.querySelectorAll(`[id*="${side}_leakRow_"]`);
    //console.log(side)
    const checked = document.getElementById(`no${side}LeaksCheckbox`).checked;
    
    let dampered_count = 0;
    if (checked){
        allLeakElements = Array.from(allLeakElements).filter(el => !el.id.includes(`${side}_leakRow_`));
    } else {
        allLeakElements.forEach((el) => {
            //console.log(el)
            const rowID = el.id.replace(`${side}_leakRow_`, "");
            const selectInput = document.getElementById(`${side}_zoneSelect_${rowID}`)
            const optionList = [...selectInput.options];
            optionList.forEach(option => {
                if (option.value == "D" && option.selected) {
                    dampered_count++;
                }
            });
        })
    }

    const total_doors = allLeakElements.length;
    const final_total = total_doors-dampered_count;
    document.getElementById(`${side}_leaks`).value = final_total;
    document.getElementById(`${side}_leaks2`).value = final_total;
    allowed_time(side);
    equation(side);
}

function total_time(observed){
    if (!document.getElementById('id_om_traverse_time_min')) return;
    if(observed == "offtakes"){
        const om_traverse_time_min = document.getElementById('id_om_traverse_time_min').value;
        const om_traverse_time_sec = document.getElementById('id_om_traverse_time_sec').value;
        const om_total_sec = document.getElementById('id_om_total_sec');
        const om_total = minutesToSeconds(om_traverse_time_min)+parseInt(om_traverse_time_sec? om_traverse_time_sec: 0);
        om_total_sec.value = om_total;
    } else {
        const l_traverse_time_min = document.getElementById('id_l_traverse_time_min').value;
        const l_traverse_time_sec = document.getElementById('id_l_traverse_time_sec').value;
        const l_total_sec = document.getElementById('id_l_total_sec');
        const l_total = minutesToSeconds(l_traverse_time_min)+parseInt(l_traverse_time_sec? l_traverse_time_sec: 0);
        l_total_sec.value = l_total;
    }
}

function minutesToSeconds(minutes){
    let total_seconds = minutes*60
    return parseInt(total_seconds)
}

function equation(side) {
    if (!document.getElementById(`${side}_leaks2`)) return;
    const leaks = document.getElementById(`${side}_leaks2`).value,
          inops = document.getElementById('inop_ovens').value,
          not_obs = document.getElementById(`${side}_not_observed`).value;
    
    if (parseInt(leaks) != 0) {
        const equate = (parseInt(leaks) * 100)/(4*(85 - parseInt(inops)) - parseInt(not_obs));
        document.getElementById(`${side}_percent_leaking`).value = equate? parseFloat(equate).toFixed(3): "";
    } else {
        document.getElementById(`${side}_percent_leaking`).value = 0;
    }
}

function set_not_observed(side) {
    if (!document.getElementById(`${side}_not_observed`)) return;
    const allLeakElements = document.querySelectorAll(`[id*="${side}_leakRow_"]`);
    let dampered_count = 0;
    allLeakElements.forEach((el) => {
        //console.log(el)
        const rowID = el.id.replace(`${side}_leakRow_`, "");
        const selectInput = document.getElementById(`${side}_zoneSelect_${rowID}`)
        //console.log(`${side}_zoneSelect_${rowID}`)
        //console.log(selectInput)
        const optionList = [...selectInput.options];
        optionList.forEach(option => {
            if (option.value == "D" && option.selected) {
                dampered_count++;
            }
        });
    })
    //console.log(dampered_count)
    const totalDampered = side == "om"? dampered_count * 2: dampered_count * 4;
    //console.log(totalDampered)
    document.getElementById(`${side}_not_observed`).value = totalDampered;
}

function check_dampered_inoperable(side) {
    if (!document.getElementById('inop_numbs')) return;
    const inop_numbers = document.getElementById('inop_numbs').value.replaceAll(' ','').split(',');
    //console.log(inop_numbers)
    const allLeakElements = document.querySelectorAll(`[id*="${side}_leakRow_"]`);
    allLeakElements.forEach((el) => {
        const rowID = el.id.replace(`${side}_leakRow_`, "");
        const ovenInput = String(document.getElementById(`${side}_oven_${rowID}`).value);

        document.getElementById(`${side}_damperPopup`).style.display = inop_numbers.includes(ovenInput)? 'block': 'none';
    })
}

function inoperable_ovens() {
    if (!document.getElementById('inop_ovens')) return;
    const inop = document.getElementById('inop_ovens').value;
    //console.log(inop)
    document.getElementById('l_inop_ovens').value = parseInt(inop);
    document.getElementById('om_inop_ovens').value = parseInt(inop);
    equation('l');
    equation('om');

    const inop_numbs_input = document.getElementById('inop_numbs');
    var length_of_inop_numbers = inop_numbs_input.value.replace(' ', '').split(',').length
    const inop_message = document.getElementById('inop_message');
    if (inop_numbs_input.value == "-" && +inop == 0){
        inop_message.style.display = "none";
    } else if (length_of_inop_numbers != inop){
        console.log('Error message')
        inop_message.style.display = "block";
        submitButton.disabled = true;
    } else {
        var blank = false;
        for(let x=0;x<length_of_inop_numbers;x++){
            const oven_number = inop_numbs_input.value.replace(' ', '').split(',')[x];
            if (!oven_number || +oven_number == 0 || isNaN(+oven_number)) {
                var blank = true;
                console.log("you got it")
            }
        }
        if (blank) {
            inop_message.style.display = "block";
            submitButton.disabled = true;
        } else {
            inop_message.style.display = "none";
            submitButton.disabled = false;
        }
    }
}

function allowed_time(side) {
    if (!document.getElementById(`${side}_leaks`)) return;
    const leaks = document.getElementById(`${side}_leaks`).value;
    
    const equate_time = 340 + (10 * parseInt(leaks));
    
    document.getElementById(`id_${side}_allowed_traverse_time`).value = equate_time; 
}

function one_pass_func() {
    if (!document.getElementById('id_one_pass')) return;
    const checked = document.getElementById('id_one_pass').checked;
    const om_start = document.getElementById('id_om_start').value;
    const om_stop = document.getElementById('id_om_stop').value;
    const om_traverse_time_min = document.getElementById('id_om_traverse_time_min').value;
    const om_traverse_time_sec = document.getElementById('id_om_traverse_time_sec').value;
    const om_total_sec = document.getElementById('id_om_total_sec').value;
    //console.log(checked);
    if (checked) {
        document.getElementById('id_l_start').value = om_start;
        document.getElementById('id_l_stop').value = om_stop;
        document.getElementById('id_l_traverse_time_min').value = om_traverse_time_min;
        document.getElementById('id_l_traverse_time_sec').value = om_traverse_time_sec;
        document.getElementById('id_l_total_sec').value = om_total_sec;
    }
}