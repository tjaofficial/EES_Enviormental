document.getElementById('button_hamburger').addEventListener('click', (elem)=>{toggleDisplayed(elem.currentTarget)});
document.getElementById('button_profile').addEventListener('click', (elem)=>{toggleDisplayed(elem.currentTarget)});
document.getElementById('drop_down').addEventListener('click', (elem)=>{toggleDisplayed(elem.currentTarget)});
document.getElementById('exitModal').addEventListener('click', (elem)=>{toggleDisplayed(elem.currentTarget)});

//document.getElementsByTagName('body').addEventListener('click', hideMenus)


function toggleDisplayed(elemClicked){
  if (!document.getElementById('hide_menu').value) {
    elemEffected = elemClicked.dataset.controls;
    elem = document.getElementById(elemEffected);
    const hiddenClassName = elem.id+"_hidden";
    const shownClassName = elem.id+"_shown";
    if(elementDisplayed(elem)){
      elem.classList.remove(shownClassName);
      elem.classList.add(hiddenClassName);
      elem.dataset.displayed = 'False';
    }
    else{
      elem.classList.remove(hiddenClassName);
      elem.classList.add(shownClassName); 
      elem.dataset.displayed = 'True';
    }
  }
}

// Takes the element and checks if data-displayed is true or false and returns the bool
function elementDisplayed(elem){
  //console.log(elem.id);
  isDisplayedValue = elem.dataset.displayed;
  //console.log(isDisplayedValue);
  if(isDisplayedValue){
    isDisplayed = false;
    if(isDisplayedValue == 'True'){
      isDisplayed = true;
      
    }
    return isDisplayed;
  }
  
}





//function showProfileDropDown(){};

// function clickOutsideContainer(event, container){
//     let clickedOutside = False;
//     if (container !== event.target && !container.contains(event.target)) {    
//         clickedOutside = True;
//       }

//       console.log(clickedOutside);
// }