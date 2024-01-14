const planContainer = document.getElementById('planHolder');
const planID = document.getElementById('planID').dataset.planid;
for (let i=0; i<planContainer.children.length; i++){
    let planElem = planContainer.children[i];
    if (planElem.id == planID){
        planElem.classList.add("currentPlanBorder");
    } else {
        planElem.classList.remove("currentPlanBorder");
    }
}

changeSelected = (elem) => {
    const plan = elem.parentElement.parentElement;
    const plan_id = plan.id
    const allPlansList = plan.parentElement.children;
    for(let x=0; x<allPlansList.length; x++){
        let listPlan = allPlansList[x];
        let currentPlan = false;
        console.log(listPlan.classList)
        for(let z=0; z<listPlan.classList.length; z++){
            const classSelect = listPlan.classList[z];
            if (classSelect == "currentPlanBorder"){
                currentPlan = true
            }
        }
        if (!currentPlan){
            if (listPlan.id == plan_id){
                listPlan.style.border = "#177b19 dotted 4px";
            } else {
                listPlan.style.border = "none";
            }
        }
    }
}
