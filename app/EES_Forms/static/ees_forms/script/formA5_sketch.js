
window.addEventListener("load", ()=>{
  //get the containers
  const sketchContainer = document.getElementById('sketchBox');
  const sketchInput = document.getElementById('canvas');
  const spinner = document.getElementById('imgspinner')

  //create 2 images the defualt image and the stored image
  const blankImageUrl = sketchContainer.dataset.base_img
  const existingImgUrl = sketchContainer.dataset.filledsketch
  const selector = sketchContainer.dataset.selector
  let urlToRender = sketchContainer.dataset.base_img
  const blankImage= newImageObject(blankImageUrl)
  
  //check if existing image
  if(existingImgUrl != "") urlToRender = existingImgUrl

  if(selector == 'form'){
    //if moreUptodateone is saved locally
    const localSavedLink = loadLocalStorage()
    if(localSavedLink) urlToRender = localSavedLink;
  }
  //Create render Image
  const renderedImage = newImageObject(urlToRender)

  //hide loader add Image
  sketchContainer.removeChild(spinner);
  sketchContainer.appendChild(renderedImage);

  sketchContainer.addEventListener('click', (elem)=>{sketchPopup(elem.currentTarget, blankImage, renderedImage)});
  
})


function sketchPopup(elemClicked, blankImage, renderedImage){
  const sketchContainer = document.getElementById('sketchBox');
  const selector = sketchContainer.dataset.selector
  const canvas = document.getElementById('sketchpad');
  elemEffected = elemClicked.dataset.controls;
  elem = document.getElementById(elemEffected);
  canvisInitiated = elem.dataset.canvis_intiated;
  if(selector == 'form'){
    if(canvisInitiated == 'False'){
      let sketchpad = initiateSketch(canvas, renderedImage);
      elem.dataset.canvis_intiated = 'True'
      document.getElementById('clearCanvis').addEventListener('click', ()=>{sketchpad.clear();  drawImgToCanvas(canvas, blankImage);});
      document.getElementById('canvas_save').addEventListener('click', (elem)=>{save_canvas(elem.currentTarget, canvas, renderedImage, elemClicked)});
    }
    console.log('test');
    toggleDisplayed(elemClicked);
  }
}
  
  
  function initiateSketch(canvas, imageElem){
  
    // Use the intrinsic size of image in CSS pixels for the canvas element
    canvas.width = 650;
    canvas.height = 500;
  
      
    console.log(canvas);
    const sketchpad = new Atrament(canvas, {
        color: 'black',

        
    });
    sketchpad.smoothing = 0.2;
  
    drawImgToCanvas(canvas, imageElem);
    
    return sketchpad;
    //sketchpad.addEventListener('strokeend', () => console.info('strokeend'));
  
  }
  
  function save_canvas(elem, canvas, renderedImage, elemClicked){
      let pngLink = canvas.toDataURL();
      //document.querySelector("#sketchPng").value = pngLink;
      renderedImage.src = pngLink;
      document.getElementById('canvas').value = pngLink;
      saveToLocalStorage(pngLink)

      
     //if(elemClicked.contains(renderedImage)){
       //elemClicked.removeChild(renderedImage);
       // elemClicked.appendChild(savedImage);
      //}



      toggleDisplayed(elem);
  }
  
  function drawImgToCanvas(canvas, imageElem){
    const ctx = canvas.getContext('2d');
      ctx.drawImage(imageElem, 0, 0, imageElem.width, imageElem.height,
                          0, 0, canvas.width, canvas.height);
  }

  function newImageObject(imageURL)
  {
    image = new Image()
    image.src = imageURL;
    image.crossOrigin = "ananymous";
    return image;
  }

  function saveToLocalStorage(link){
    const tempSaveKey = document.getElementById('formName').dataset.form + "_tempFormData";
    const formTempData = localStorage.getItem(tempSaveKey)?JSON.parse(localStorage.getItem(tempSaveKey)): {"Experation":currentDate, data:{}};
    formTempData.data.canvas = link;
    localStorage.setItem(tempSaveKey, JSON.stringify(formTempData))

  }

  function loadLocalStorage(){
    const tempSaveKey = document.getElementById('formName').dataset.form + "_tempFormData";
    if( !JSON.parse(localStorage.getItem(tempSaveKey))) return undefined
    
    
    let  localSavedLink = JSON.parse(localStorage.getItem(tempSaveKey)).data.canvas;

    if(!localSavedLink) return undefined

    return localSavedLink

  }


