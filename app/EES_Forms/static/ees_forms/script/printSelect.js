document.getElementById('type').addEventListener("change", selectItemLis);
selectItemLis();

function selectItemLis() {
    // formList = ['a1','a2','a3','a4','a5','b','c','d','e','g1','g2','h','i','l','m','o','p', 'spill_kits', 'quarterly_trucks']
    console.log('CHECK 1')
    const start = document.getElementById('type').value;
    if(start == 'single'){
        console.log('CHECK 2')
        document.getElementById('selForm').style.display = 'block';
        document.getElementById('selGroup').style.display = 'none';
        // document.getElementById('forms').addEventListener("change", selectFormLis);
        // document.getElementById('formGroups').value = '';
    } else if ( start == 'group'){
        console.log('CHECK 4')
        document.getElementById('selGroup').style.display = 'block';
        document.getElementById('selForm').style.display = 'none';
        // document.getElementById('formGroups').addEventListener("change", selectGroupLis);
        // document.getElementById('forms').value = '';
    } else {
        document.getElementById('selForm').style.display = 'none';
        document.getElementById('selGroup').style.display = 'none';
        // document.getElementById('formGroups').value = '';
        // document.getElementById('forms').value = '';
    }
}

function selectGroupLis() {
    const group = document.getElementById('formGroups').value;
        if(group != ''){
            document.getElementById('selDate').style.visibility = 'visible';
            document.getElementById('formDate').addEventListener("change", selectPrintLis);
        } else if (group == ''){
            document.getElementById('selDate').style.visibility = 'hidden';
            document.getElementById('printButton').style.visibility = 'hidden';
        }
}

function selectPrintLis() {
    document.getElementById('printButton').style.visibility = 'visible';
}