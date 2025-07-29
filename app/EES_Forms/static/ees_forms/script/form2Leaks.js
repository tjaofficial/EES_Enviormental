function addLeakRow(elem, forcedIndex = null) {
    const side = elem.dataset.side
    const tableBody = document.getElementById(`${side}LeaksTableBody`);
    const newRow = document.createElement("tr");
    
    let indexToUse;
    
    if (forcedIndex !== null) {
        indexToUse = forcedIndex;
    } else {
        const elements = document.querySelectorAll(`[id^="${side}_zoneSelect_"]`);
        let count = 0;
        elements.forEach(el => {
            //console.log(el.id.replace('${side}_zoneSelect_', ''))
            const suffix = Number(el.id.replace(`${side}_zoneSelect_`, ''));
            if (suffix > count){
                count = suffix;
            }
        });
        indexToUse = count + 1;
    }
    
    newRow.id = `${side}_leakRow_${indexToUse}`
    newRow.innerHTML = `
        <td><input type="number" id="${side}_oven_${indexToUse}" name="${side}_oven_${indexToUse}" placeholder="Oven #" style="width:90px;" required></td>
        <td>
            <select id="${side}_zoneSelect_${indexToUse}" name="${side}_location_${indexToUse}" placeholder="Location" multiple required>
                <option value="D" >D</option>
                <option value="C" >C</option>
                <option value="M" >M</option>
            </select>
        </td>
        <td>
            <input type="text" id="${side}_zone_${indexToUse}" name="${side}_zone_${indexToUse}" placeholder="Select Zone" style="width: 175px;" onclick="zoneSelectors(${indexToUse}, '${side}'); document.getElementById('${side}_zoneModal_${indexToUse}').style.display='flex'" required>
            <input type="hidden" id="${side}_selectedZones_${indexToUse}" name="${side}_selected_zones_${indexToUse}" value="">
            <div id="${side}_zoneModal_${indexToUse}" style="display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.5); z-index: 9999; align-items: center; justify-content: center; min-height: 800px;">
                <div style="background: white; padding: 2rem; border-radius: 8px; position: relative; min-width: 300px;">
                    <h3 style="margin-top: 0;">Add Leak Zones</h3>
                    <div style="position: relative; width: 130px; height: 300px; margin: 50px; background: #e0e0e0; border: 1px solid #333;">
                        <!-- Chuck Door Label -->
                        <div style="padding: 8px 6px; background: white; font-size: 20px; width: 100%; border-bottom: black 1px solid; text-align: center;">
                            Chuck Door
                        </div>
                        
                        <!-- Zones -->
                        <div class="zone ${side}_zone_${indexToUse}" data-zone="1" style="top: -50px; left: 50%; transform: translateX(-50%);">1</div>
                        <div class="zone ${side}_zone_${indexToUse}" data-zone="2" style="top: 20px; left: -50px;">2</div>
                        <div class="zone ${side}_zone_${indexToUse}" data-zone="3" style="top: 125px; left: -50px;">3</div>
                        <div class="zone ${side}_zone_${indexToUse}" data-zone="4" style="bottom: 20px; left: -50px;">4</div>
                        <div class="zone ${side}_zone_${indexToUse}" data-zone="5" style="bottom: -50px; left: 50%; transform: translateX(-50%);">5</div>
                        <div class="zone ${side}_zone_${indexToUse}" data-zone="6" style="bottom: 20px; right: -50px;">6</div>
                        <div class="zone ${side}_zone_${indexToUse}" data-zone="7" style="top: 125px; right: -50px;">7</div>
                        <div class="zone ${side}_zone_${indexToUse}" data-zone="8" style="top: 20px; right: -50px;">8</div>
                    </div>

                    <!-- Buttons -->
                    <div style="text-align: center; margin-top: 1rem;">
                        <button type="button" onclick="saveZoneSelection(${indexToUse}, '${side}')">Save</button>
                        <button type="button" onclick="document.getElementById('${side}_zoneModal_${indexToUse}').style.display='none'">Cancel</button>
                    </div>
                </div>
            </div>
        </td>
        <td><span id="${side}_delete_${indexToUse}" class="remove-row-btn" onclick="removeLeakRow(this)" data-side="${side}">✖</span></td>
    `;
    tableBody.appendChild(newRow);
    const newSelect = document.getElementById(`${side}_zoneSelect_${indexToUse}`);
    const choicesInstance = new Choices(newSelect, {
        removeItemButton: true,
        placeholderValue: 'Location',
        searchEnabled: false,
        shouldSort: false,
        duplicateItemsAllowed: false,
        itemSelectText: '',
    });
    newSelect.choicesInstance = choicesInstance;
    total_leaking_doors();
}

function removeLeakRow(btn) {
    const formName = document.getElementById('formName').dataset.form;
    const tempSaveKey = formName+"_tempFormData";
    const formTempData = JSON.parse(localStorage.getItem(tempSaveKey));
    const side = btn.dataset.side
    const row = btn.closest("tr");
    const tableBody = document.getElementById(`${side}LeaksTableBody`);
    if (tableBody.rows.length > 1) {
        const rowNumb = btn.id.replace(`${side}_delete_`, "");
        delete formTempData.data[`${side}_oven_${rowNumb}`];
        delete formTempData.data[`${side}_zoneSelect_${rowNumb}`];
        delete formTempData.data[`${side}_zone_${rowNumb}`];
        localStorage.setItem(tempSaveKey, JSON.stringify(formTempData));
        row.remove();
        total_leaking_doors();
    } else {
        alert("You must have at least one row.");
    }
}
let zones;
function zoneSelectors(zoneIndex, sideLetter){
    //console.log('chienc')
    zones = document.querySelectorAll(`.${sideLetter}_zone_${zoneIndex}`);
    zones.forEach(zone => {
        zone.addEventListener('click', () => {
            zone.classList.toggle('selected');
        });
    });
}

function saveZoneSelection(zoneIndex, sideLetter) {
    const hiddenInput = document.getElementById(`${sideLetter}_selectedZones_${zoneIndex}`);
    const shownInput = document.getElementById(`${sideLetter}_zone_${zoneIndex}`)
    //console.log(shownInput)
    //console.log(zoneIndex)
    //console.log(zones)
    const selected = [...zones]
        .filter(z => z.classList.contains('selected'))
        .map(z => z.dataset.zone);
    //console.log(selected)
    const joined = selected.join(',');
    hiddenInput.value = joined;
    shownInput.value = joined;
    shownInput.dispatchEvent(new Event('input', { bubbles: true }));
    document.getElementById(`${sideLetter}_zoneModal_${zoneIndex}`).style.display = 'none';
    //console.log('Selected zones:', hiddenInput.value);
}

function initial_leak_add_rows() {
    const formName = document.getElementById('formName')?.dataset.form;
    const tempSaveKey = `${formName}_tempFormData`;
    const raw = localStorage.getItem(tempSaveKey);
    if (!raw) return;

    const data = JSON.parse(raw)?.data || {};
    const rowPattern = /^(?<side>[a-z])_(zone|zoneSelect|oven)_(?<index>\d+)$/;

    // Group: { p: Set(0,2,3), c: Set(1,4), ... }
    const indexMap = {};

    for (const key of Object.keys(data)) {
        const match = key.match(rowPattern);
        if (!match) continue;

        const { side, index } = match.groups;
        const idx = parseInt(index);

        if (!indexMap[side]) indexMap[side] = new Set();
        indexMap[side].add(idx);
    }

    Object.entries(indexMap).forEach(([side, indexes]) => {
        const addBtn = document.querySelector(`.add-row-btn[data-side="${side}"]`);
        if (!addBtn) return;

        const existingIndexes = Array.from(document.querySelectorAll(`[id^="${side}_oven_"]`))
            .map(el => parseInt(el.id.replace(`${side}_oven_`, '')))
            .filter(i => !isNaN(i));

        indexes.forEach(idx => {
            if (!existingIndexes.includes(idx)) {
                // Keep calling addLeakRow until this index is created
                while (!document.getElementById(`${side}_oven_${idx}`)) {
                    addLeakRow(addBtn, idx);
                }
            }
        });
    });
    //console.log(`sd;lgks;dglsdflk=-----------------${Object.keys(indexMap).length}`)
    if (Object.keys(indexMap).length === 0) {
        document.getElementById('nopLeaksMsg').style.display = 'block';
        document.getElementById('nocLeaksMsg').style.display = 'block';
    }
}

function initial_leak_add_rows_exisiting(side) {
    if (!document.getElementById(`${side}Side_json`)) {
        initial_leak_add_rows();
    } else {
        const side_json = JSON.parse(document.getElementById(`${side}Side_json`).textContent);
        console.log(side_json); // Now usable as a JS object

        side_json.forEach((leakLine, index) => {
            const addBtn = document.querySelector(`.add-row-btn[data-side="${side}"]`);
            if (!addBtn) return;

            const existingIndexes = Array.from(document.querySelectorAll(`[id^="${side}_oven_"]`))
                .map(el => parseInt(el.id.replace(`${side}_oven_`, '')))
                .filter(i => !isNaN(i));
            console.log(existingIndexes);

            if (!existingIndexes.includes(index)) {
                // Keep calling addLeakRow until this index is created
                while (!document.getElementById(`${side}_oven_${index}`)) {
                    addLeakRow(addBtn, index);
                }
            }
        });
        side_json.forEach((lineItem, idx) => {
            const oven = document.getElementById(`${side}_oven_${idx}`);
            const zoneSelect = document.getElementById(`${side}_zoneSelect_${idx}`);
            const zone = document.getElementById(`${side}_zoneSelect_${idx}`);

            oven.value = lineItem['oven'];
            zone.value = lineItem['zone'];
            const instance = zoneSelect.choicesInstance;
            if (instance && lineItem['location']) {
                instance.setChoiceByValue(lineItem['location']);
            }
        })
        if (side_json.length === 0) {
            document.getElementById(`no${side}LeaksMsg`).style.display = 'block';
            document.getElementById(`no${side}LeaksCheckbox`).checked = true;
        }
    }
    total_leaking_doors(side);
    toggleLeaksMode(document.getElementById(`no${side}LeaksCheckbox`));
}

const searchVar = document.getElementById('formID').dataset.search;
document.addEventListener('DOMContentLoaded', () => {
    // if (searchVar == "False") {
    //     initial_leak_add_rows();
    // }
    intiate_TempSave(); // this runs fillForm from temp_save.js
    initial_leak_add_rows_exisiting('p');
    initial_leak_add_rows_exisiting('c');
});