
window.addEventListener("load", ()=>{
  const sketchContainer = document.getElementById('sketchBox');
  const sketchInput = document.getElementById('canvas');
  const blankImageURL = sketchContainer.dataset.base_img;
  const blankImage = new Image()
  blankImage.src = blankImageURL;
  blankImage.crossOrigin = "ananymous";

  let fetchedImage = blankImage;

  if(sketchInput.value){
    const storedImage = new Image()
    storedImage.src = sketchContainer.dataset.filledsketch;
    storedImage.crossOrigin = "ananymous";
    fetchedImage = storedImage
  }
  
  const savedImage = new Image();

  sketchContainer.appendChild(fetchedImage);

  sketchContainer.addEventListener('click', (elem)=>{sketchPopup(elem.currentTarget, blankImage, fetchedImage, savedImage)});
})


function sketchPopup(elemClicked, blankImage, fetchedImage, savedImage){
    const canvas = document.getElementById('sketchpad');
    elemEffected = elemClicked.dataset.controls;
    elem = document.getElementById(elemEffected);
    canvisInitiated = elem.dataset.canvis_intiated;
    if(canvisInitiated == 'False'){
      let sketchpad = initiateSketch(canvas, fetchedImage);
      elem.dataset.canvis_intiated = 'True'
      document.getElementById('clearCanvis').addEventListener('click', ()=>{sketchpad.clear();  drawImgToCanvas(canvas, blankImage);});
      document.getElementById('canvas_save').addEventListener('click', (elem)=>{save_canvas(elem.currentTarget, canvas, fetchedImage, savedImage, elemClicked)});
    }
      console.log('test');
      toggleDisplayed(elemClicked);
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

  
  function save_canvas(elem, canvas, fetchedImage, savedImage, elemClicked){
      let pngLink = canvas.toDataURL();
      //document.querySelector("#sketchPng").value = pngLink;
      savedImage.src = pngLink;
      console.log(elemClicked);
      let val = pngLink;
      let response = val.substring(val.indexOf(",") + 1);
      document.getElementById('canvas').value = response;
      
      if(elemClicked.contains(fetchedImage)){
        elemClicked.removeChild(fetchedImage);
        elemClicked.appendChild(savedImage);
      }



      toggleDisplayed(elem);
  }
  
  function drawImgToCanvas(canvas, imageElem){
    const ctx = canvas.getContext('2d');
  

      ctx.drawImage(imageElem, 0, 0, imageElem.width, imageElem.height,
                          0, 0, canvas.width, canvas.height);
    
  }



