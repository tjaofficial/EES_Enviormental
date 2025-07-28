document.addEventListener('DOMContentLoaded', () => {
    const blockPushDoors = document.getElementById('nopBlockedCheckbox');
    const blockCokeDoors = document.getElementById('nocBlockedCheckbox');
    const leakPushDoors = document.getElementById('nopLeaksCheckbox');
    const leakCokeDoors = document.getElementById('nocLeaksCheckbox');
    toggleBlockedInputs(blockPushDoors);
    toggleBlockedInputs(blockCokeDoors);
    toggleLeaksMode(leakPushDoors);
    toggleLeaksMode(leakCokeDoors);
    total_doors_not_obs();
    inoperable_ovens();
    total_leaking_doors();
    total_traverse();
    allowed_time();
    equation();
});

function toggleBlockedInputs(elem) {
    if (!elem) return;
    const side = elem.dataset.side;
    const checkbox = document.getElementById(`no${side}BlockedCheckbox`);
    const start = document.getElementById(`${side}_temp_block_from`);
    const end = document.getElementById(`${side}_temp_block_to`);

    if (checkbox.checked) {
        start.disabled = true;
        end.disabled = true;
        start.removeAttribute("required");
        end.removeAttribute("required");
        start.style.backgroundColor = "gray";
        end.style.backgroundColor = "gray";
    } else {
        start.disabled = false;
        end.disabled = false;
        start.setAttribute("required", true);
        end.setAttribute("required", true);
        start.style.backgroundColor = "white";
        end.style.backgroundColor = "white";
    }
}

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
        const allAreaLeaks = table.querySelectorAll(`[id*="${side}_zone_"], [id*="${side}_location_"], [id*="${side}_oven_"], [id*="${side}_zoneSelect_"]`)
        allAreaLeaks.forEach((el) => {
            el.removeAttribute("required");
        })
    } else {
        table.style.display = "table";
        header.style.display = "table-header-group";
        noLeaksMsg.style.display = "none";
        const allAreaLeaks = table.querySelectorAll(`[id*="${side}_zone_"], [id*="${side}_location_"], [id*="${side}_oven_"], [id*="${side}_zoneSelect_"]`)
        allAreaLeaks.forEach((el) => {
            el.setAttribute("required", true);
        })
    }
}
//Get total of doors not observed
function pc_doors_not_observed(side) {
    if (!document.getElementById(`${side}_temp_block_from`)) return;
    //console.log(side);
    const doors_from = document.getElementById(`${side}_temp_block_from`).value,
          doors_to = document.getElementById(`${side}_temp_block_to`).value,
          noBlock = document.getElementById(`no${side}BlockedCheckbox`).checked;

    const coke_from = document.getElementById('c_temp_block_from').value,
          coke_to = document.getElementById('c_temp_block_to').value,
          inop_numbs = document.getElementById('inop_numbs').value;
    
    //Gets an array of all inoperable doors
    let remove_spaces = inop_numbs.split(' ').join(""),
    select_numbers = remove_spaces.split(',');
   
    if (!noBlock) {
        let blocked_doors = Math.abs(parseInt(doors_from) - parseInt(doors_to)) +1,
        x = 0;
        if(parseInt(doors_from) < parseInt(doors_to)){
            for(o=parseInt(doors_from); o<=parseInt(doors_to); o++){
                for(i=0; i<select_numbers.length; i++){
                    if(parseInt(o) === parseInt(select_numbers[i])){
                        x += 1;
                    }
                }
            }
        }
        else {
            for(o=parseInt(doors_to); o<=parseInt(doors_from); o++){
                for(i=0; i<select_numbers.length; i++){
                    if(parseInt(o) === parseInt(select_numbers[i])){
                        x += 1;
                    }
                }
            }
        }
        var block_total = parseInt(blocked_doors) - parseInt(x);
    }
    else {
        var block_total = 0;
    }
    return block_total;
}

function inoperable_ovens() {
    if (!document.getElementById('inop_ovens')) return;
    const inop = document.getElementById('inop_ovens').value;
    
    document.getElementById('inop_doors_eq').value = parseInt(inop) * 2;
    equation();

    const inop_numbs_input = document.getElementById('inop_numbs');
    var length_of_inop_numbers = inop_numbs_input.value.replace(' ', '').split(',').length
    const inop_message = document.getElementById('inop_message');
    if (inop_numbs_input.value == "-" && +inop == 0){
        inop_message.style.display = "none";
    } else if (length_of_inop_numbers != inop ){
        console.log('Error message')
        inop_message.style.display = "block";
    } else {
        var blank = false;
        for(let x=0;x<length_of_inop_numbers;x++){
            const oven_number = inop_numbs_input.value.replace(' ', '').split(',')[x];
            if (!oven_number || +oven_number == 0 || isNaN(+oven_number)){
                var blank = true;
            }
        }
        if (blank) {
            inop_message.style.display = "block";
        } else {
            inop_message.style.display = "none";
        }
    }
}

function total_leaking_doors() {
    if (!document.getElementById(`nopLeaksCheckbox`)) return;
    let allLeakElements = document.querySelectorAll('[id*="_leakRow_"]');
    
    const checkedPush = document.getElementById(`nopLeaksCheckbox`).checked;
    const checkedCoke = document.getElementById(`nocLeaksCheckbox`).checked;
    if (checkedPush){
        allLeakElements = Array.from(allLeakElements).filter(el => !el.id.includes('p_leakRow_'));
    }
    if (checkedCoke){
        allLeakElements = Array.from(allLeakElements).filter(el => !el.id.includes('c_leakRow_'));
    }
    //---------------------------------------------------------------
    //-------Attempt to remove duplicates but might need to just add a popup---------
    //---------------------------------------------------------------

    const total_doors = allLeakElements.length
    //console.log(total_doors);
    document.getElementById('leaking_doors').value = total_doors;
    allowed_time();
    equation();
}

function total_traverse() {
    if (!document.getElementById('id_p_traverse_time_min')) return;
    const push_traverse_min = document.getElementById('id_p_traverse_time_min').value,
          push_traverse_sec = document.getElementById('id_p_traverse_time_sec').value,
          coke_traverse_min = document.getElementById('id_c_traverse_time_min').value,
          coke_traverse_sec = document.getElementById('id_c_traverse_time_sec').value;
    
    
    console.log(push_traverse_sec);
    if (push_traverse_min == '') {
        console.log('push minutes are empty');
        if(push_traverse_sec == '') {
            var push_secs = 0;
            console.log('push seconds are empty');
        }
    }
    else {
        var push_secs = (parseInt(push_traverse_min) * 60) + parseInt(push_traverse_sec);
    }
    
    if (coke_traverse_min == '') {
        console.log('coke minutes are empty');
        if(coke_traverse_sec == '') {
            var coke_secs = 0;
            console.log('coke seconds are empty');
        }
    }
    else {
        var coke_secs = (parseInt(coke_traverse_min) * 60) + parseInt(coke_traverse_sec);
    }
    
  //  const push_secs = (parseInt(push_traverse_min) * 60) + parseInt(push_traverse_sec);
          
    
    let total_secs = parseInt(push_secs) + parseInt(coke_secs);

    if (total_secs == 0) {
        document.getElementById('total_traverse_time').value = total_secs;
    } else {
        document.getElementById('total_traverse_time').value = total_secs;
    }
}

function equation() {
    if (!document.getElementById('leaking_doors')) return;
    const leaks = document.getElementById('leaking_doors').value,
          inops = document.getElementById('inop_doors_eq').value,
          not_obs = document.getElementById('doors_not_observed').value;
    
    const equate = (parseInt(leaks) * 100)/(170 - parseInt(inops) - parseInt(not_obs));
    if (isNaN(equate)) {
        document.getElementById('id_percent_leaking').value = '';
    } else {
        document.getElementById('id_percent_leaking').value = parseFloat(equate).toFixed(3);
    }
}

function allowed_time() {
    if (!document.getElementById('leaking_doors')) return;
    const leaks = document.getElementById('leaking_doors').value;
    
    const equate_time = 680 + (10 * parseInt(leaks));
    
    document.getElementById('allowed_traverse_time').value = equate_time; 
}

function total_doors_not_obs(){
    if (!document.getElementById('doors_not_observed')) return;
    const total_not_obs = pc_doors_not_observed('p') + pc_doors_not_observed('c');
    document.getElementById('doors_not_observed').value = total_not_obs;
    equation();
}
