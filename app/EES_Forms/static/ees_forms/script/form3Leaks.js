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
        <td><input type="number" id="${side}_oven_${indexToUse}" name="${side}_oven_${indexToUse}" placeholder="Oven #" style="width:90px;" required oninput="check_dampered_inoperable('${side}')"></td>
        <td>
            <select id="${side}_zoneSelect_${indexToUse}" name="${side}_location_${indexToUse}" placeholder="Location" multiple required onchange="set_not_observed('${side}')">
                <option value="D">D</option>
                <option value="C">C</option>
                <option value="F">F</option>
                <option value="S">S</option>
                <option value="B">B</option>
                <option value="P">P</option>
                <option value="O">O</option>
                <option value="MS">MS</option>
            </select>
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
    total_leaking_doors(side);
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
        localStorage.setItem(tempSaveKey, JSON.stringify(formTempData));
        row.remove();
        total_leaking_doors(side);
        set_not_observed(side);
        check_dampered_inoperable(side);
    } else {
        alert("You must have at least one row.");
    }
}

function initial_leak_add_rows() {
    const formName = document.getElementById('formName')?.dataset.form;
    const tempSaveKey = `${formName}_tempFormData`;
    const raw = localStorage.getItem(tempSaveKey);
    if (!raw) return;

    const data = JSON.parse(raw)?.data || {};
    const rowPattern = /^(?<side>[a-z]+)_(zoneSelect|oven)_(?<index>\d+)$/;
    //console.log(rowPattern)
    // Group: { p: Set(0,2,3), c: Set(1,4), ... }
    const indexMap = {};

    for (const key of Object.keys(data)) {
        //console.log(key)
        const match = key.match(rowPattern);
        if (!match) continue;
        //console.log(match)
        const { side, index } = match.groups;
        const idx = parseInt(index);

        if (!indexMap[side]) indexMap[side] = new Set();
        indexMap[side].add(idx);
    }
    //console.log(indexMap)
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
        if (indexes.length === 0) {
            document.getElementById(`no${side}LeaksMsg`).style.display = 'block';
        }
    });
}

function initial_leak_add_rows_exisiting(side) {
    if (!document.getElementById(`${side}Side_json`)) {
        initial_leak_add_rows();
    } else {
        const side_json = JSON.parse(document.getElementById(`${side}Side_json`).textContent);
        console.log(side_json); // Now usable as a JS object

        //console.log(indexMap)
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

            oven.value = lineItem['oven'];
            const instance = zoneSelect.choicesInstance;
            if (instance && lineItem['location']) {
                instance.setChoiceByValue(lineItem['location']);
            }
        })
        if (side_json.length === 0) {
            document.getElementById(`no${side}LeaksMsg`).style.display = 'block';
        }
    }
    total_leaking_doors(side);
    set_not_observed(side);
}

const searchVar = document.getElementById('formID').dataset.search;
document.addEventListener('DOMContentLoaded', () => {
    intiate_TempSave(); // this runs fillForm from temp_save.js
    check_dampered_inoperable('om');
    check_dampered_inoperable('l');
    initial_leak_add_rows_exisiting('om');
    initial_leak_add_rows_exisiting('l');
});