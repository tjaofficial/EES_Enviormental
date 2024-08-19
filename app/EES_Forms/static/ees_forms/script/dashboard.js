packetChange = (elem) => {
    const packetID = String(elem.value);
    const packetList = JSON.parse(elem.dataset.allpackets);
    for(let x=0; x<packetList.length; x++){
        let packIdFromList = packetList[x];
        document.getElementById("i"+packIdFromList).style.display = 'none';
        document.getElementById('i0').style.display = 'none';
        document.getElementById("c"+packIdFromList).style.display = 'none';
        document.getElementById('c0').style.display = 'none';
    }
    document.getElementById("i"+packetID).style.display = 'block';
    document.getElementById("c"+packetID).style.display = 'block';
}

// function sort() {
//     const sortSelect = document.getElementById('cardDropdown').value;
//     if (sortSelect == 'all') {
//         document.getElementById('allIncomplete').hidden = false;
//         document.getElementById('dailyIncomplete').hidden = true;
//         document.getElementById('weeklyIncomplete').hidden = true;
//         document.getElementById('monthlyIncomplete').hidden = true;
//         document.getElementById('quarterlyIncomplete').hidden = true;
//         document.getElementById('sannualIncomplete').hidden = true;
//         document.getElementById('annualIncomplete').hidden = true;

//         document.getElementById('allComplete').hidden = false;
//         document.getElementById('dailyComplete').hidden = true;
//         document.getElementById('weeklyComplete').hidden = true;
//         document.getElementById('monthlyComplete').hidden = true;
//         document.getElementById('quarterlyComplete').hidden = true;
//         document.getElementById('sannualComplete').hidden = true;
//         document.getElementById('annualComplete').hidden = true;
//     } else if (sortSelect == 'daily') {
//         document.getElementById('allIncomplete').hidden = true;
//         document.getElementById('dailyIncomplete').hidden = false;
//         document.getElementById('weeklyIncomplete').hidden = true;
//         document.getElementById('monthlyIncomplete').hidden = true;
//         document.getElementById('quarterlyIncomplete').hidden = true;
//         document.getElementById('sannualIncomplete').hidden = true;
//         document.getElementById('annualIncomplete').hidden = true;

//         document.getElementById('allComplete').hidden = true;
//         document.getElementById('dailyComplete').hidden = false;
//         document.getElementById('weeklyComplete').hidden = true;
//         document.getElementById('monthlyComplete').hidden = true;
//         document.getElementById('quarterlyComplete').hidden = true;
//         document.getElementById('sannualComplete').hidden = true;
//         document.getElementById('annualComplete').hidden = true;
//     } else if (sortSelect == 'weekly') {
//         document.getElementById('allIncomplete').hidden = true;
//         document.getElementById('dailyIncomplete').hidden = true;
//         document.getElementById('weeklyIncomplete').hidden = false;
//         document.getElementById('monthlyIncomplete').hidden = true;
//         document.getElementById('quarterlyIncomplete').hidden = true;
//         document.getElementById('sannualIncomplete').hidden = true;
//         document.getElementById('annualIncomplete').hidden = true;

//         document.getElementById('allComplete').hidden = true;
//         document.getElementById('dailyComplete').hidden = true;
//         document.getElementById('weeklyComplete').hidden = false;
//         document.getElementById('monthlyComplete').hidden = true;
//         document.getElementById('quarterlyComplete').hidden = true;
//         document.getElementById('sannualComplete').hidden = true;
//         document.getElementById('annualComplete').hidden = true;
//     } else if (sortSelect == 'monthly') {
//         document.getElementById('allIncomplete').hidden = true;
//         document.getElementById('dailyIncomplete').hidden = true;
//         document.getElementById('weeklyIncomplete').hidden = true;
//         document.getElementById('monthlyIncomplete').hidden = false;
//         document.getElementById('quarterlyIncomplete').hidden = true;
//         document.getElementById('sannualIncomplete').hidden = true;
//         document.getElementById('annualIncomplete').hidden = true;

//         document.getElementById('allComplete').hidden = true;
//         document.getElementById('dailyComplete').hidden = true;
//         document.getElementById('weeklyComplete').hidden = true;
//         document.getElementById('monthlyComplete').hidden = false;
//         document.getElementById('quarterlyComplete').hidden = true;
//         document.getElementById('sannualComplete').hidden = true;
//         document.getElementById('annualComplete').hidden = true;
//     } else if (sortSelect == 'quarterly') {
//         document.getElementById('allIncomplete').hidden = true;
//         document.getElementById('dailyIncomplete').hidden = true;
//         document.getElementById('weeklyIncomplete').hidden = true;
//         document.getElementById('monthlyIncomplete').hidden = true;
//         document.getElementById('quarterlyIncomplete').hidden = false;
//         document.getElementById('sannualIncomplete').hidden = true;
//         document.getElementById('annualIncomplete').hidden = true;

//         document.getElementById('allComplete').hidden = true;
//         document.getElementById('dailyComplete').hidden = true;
//         document.getElementById('weeklyComplete').hidden = true;
//         document.getElementById('monthlyComplete').hidden = true;
//         document.getElementById('quarterlyComplete').hidden = false;
//         document.getElementById('sannualComplete').hidden = true;
//         document.getElementById('annualComplete').hidden = true;
//     } else if (sortSelect == 'sAnnual') {
//         document.getElementById('allIncomplete').hidden = true;
//         document.getElementById('dailyIncomplete').hidden = true;
//         document.getElementById('weeklyIncomplete').hidden = true;
//         document.getElementById('monthlyIncomplete').hidden = true;
//         document.getElementById('quarterlyIncomplete').hidden = true;
//         document.getElementById('sannualIncomplete').hidden = false;
//         document.getElementById('annualIncomplete').hidden = true;

//         document.getElementById('allComplete').hidden = true;
//         document.getElementById('dailyComplete').hidden = true;
//         document.getElementById('weeklyComplete').hidden = true;
//         document.getElementById('monthlyComplete').hidden = true;
//         document.getElementById('quarterlyComplete').hidden = true;
//         document.getElementById('sannualComplete').hidden = false;
//         document.getElementById('annualComplete').hidden = true;
//     } else if (sortSelect == 'annual') {
//         document.getElementById('allIncomplete').hidden = true;
//         document.getElementById('dailyIncomplete').hidden = true;
//         document.getElementById('weeklyIncomplete').hidden = true;
//         document.getElementById('monthlyIncomplete').hidden = true;
//         document.getElementById('quarterlyIncomplete').hidden = true;
//         document.getElementById('sannualIncomplete').hidden = true;
//         document.getElementById('annualIncomplete').hidden = false;

//         document.getElementById('allComplete').hidden = true;
//         document.getElementById('dailyComplete').hidden = true;
//         document.getElementById('weeklyComplete').hidden = true;
//         document.getElementById('monthlyComplete').hidden = true;
//         document.getElementById('quarterlyComplete').hidden = true;
//         document.getElementById('sannualComplete').hidden = true;
//         document.getElementById('annualComplete').hidden = false;
//     }
// }
// sort()