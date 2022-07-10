function sort() {
    const sortSelect = document.getElementById('cardDropdown').value;
    if (sortSelect == 'all') {
        document.getElementById('allIncomplete').hidden = false;
        document.getElementById('dailyIncomplete').hidden = true;
        document.getElementById('weeklyIncomplete').hidden = true;
        document.getElementById('monthlyIncomplete').hidden = true;
        document.getElementById('quarterlyIncomplete').hidden = true;
        document.getElementById('sannualIncomplete').hidden = true;
        document.getElementById('annualIncomplete').hidden = true;
    } else if (sortSelect == 'daily') {
        document.getElementById('allIncomplete').hidden = true;
        document.getElementById('dailyIncomplete').hidden = false;
        document.getElementById('weeklyIncomplete').hidden = true;
        document.getElementById('monthlyIncomplete').hidden = true;
        document.getElementById('quarterlyIncomplete').hidden = true;
        document.getElementById('sannualIncomplete').hidden = true;
        document.getElementById('annualIncomplete').hidden = true;
    } else if (sortSelect == 'weekly') {
        document.getElementById('allIncomplete').hidden = true;
        document.getElementById('dailyIncomplete').hidden = true;
        document.getElementById('weeklyIncomplete').hidden = false;
        document.getElementById('monthlyIncomplete').hidden = true;
        document.getElementById('quarterlyIncomplete').hidden = true;
        document.getElementById('sannualIncomplete').hidden = true;
        document.getElementById('annualIncomplete').hidden = true;
    } else if (sortSelect == 'monthly') {
        document.getElementById('allIncomplete').hidden = true;
        document.getElementById('dailyIncomplete').hidden = true;
        document.getElementById('weeklyIncomplete').hidden = true;
        document.getElementById('monthlyIncomplete').hidden = false;
        document.getElementById('quarterlyIncomplete').hidden = true;
        document.getElementById('sannualIncomplete').hidden = true;
        document.getElementById('annualIncomplete').hidden = true;
    } else if (sortSelect == 'quarterly') {
        document.getElementById('allIncomplete').hidden = true;
        document.getElementById('dailyIncomplete').hidden = true;
        document.getElementById('weeklyIncomplete').hidden = true;
        document.getElementById('monthlyIncomplete').hidden = true;
        document.getElementById('quarterlyIncomplete').hidden = false;
        document.getElementById('sannualIncomplete').hidden = true;
        document.getElementById('annualIncomplete').hidden = true;
    } else if (sortSelect == 'sAnnual') {
        document.getElementById('allIncomplete').hidden = true;
        document.getElementById('dailyIncomplete').hidden = true;
        document.getElementById('weeklyIncomplete').hidden = true;
        document.getElementById('monthlyIncomplete').hidden = true;
        document.getElementById('quarterlyIncomplete').hidden = true;
        document.getElementById('sannualIncomplete').hidden = false;
        document.getElementById('annualIncomplete').hidden = true;
    } else if (sortSelect == 'annual') {
        document.getElementById('allIncomplete').hidden = true;
        document.getElementById('dailyIncomplete').hidden = true;
        document.getElementById('weeklyIncomplete').hidden = true;
        document.getElementById('monthlyIncomplete').hidden = true;
        document.getElementById('quarterlyIncomplete').hidden = true;
        document.getElementById('sannualIncomplete').hidden = true;
        document.getElementById('annualIncomplete').hidden = false;
    }
}
sort()