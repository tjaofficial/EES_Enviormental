window.addEventListener("load", ()=>{
    //get the containers
    const sketchContainer = document.querySelector('#signitureBox');
    const sketchInput = document.getElementById('canvas');
    //check if existing signiture
    
    //add event listener for Popuop
    sketchContainer.addEventListener('click', (elem)=>{sketchPopup(elem.currentTarget)});
  })

  function sketchPopup(elemClicked){

    const canvas = document.getElementById('sketchpad');
    elemEffected = elemClicked.dataset.controls;
    elem = document.getElementById(elemEffected);
    canvisInitiated = elem.dataset.canvis_intiated;
    if(canvisInitiated == 'False'){
      let sketchpad = initiateSketch(canvas/*, renderedImage*/);
      elem.dataset.canvis_intiated = 'True'
      document.getElementById('clearCanvis').addEventListener('click', ()=>{sketchpad.clear();  /*drawImgToCanvas(canvas, blankImage);*/});
      //document.getElementById('canvas_save').addEventListener('click', (elem)=>{save_canvas(elem.currentTarget, canvas, renderedImage, elemClicked)});
    }
      //console.log('test');
      toggleDisplayed(elemClicked);
  }

  function initiateSketch(canvas, /*imageElem*/){
  
    // Use the intrinsic size of image in CSS pixels for the canvas element
    const width = canvas.width = 650;
    const height = canvas.height = 250;
    const padding = 25;

      
    console.log(canvas);
    const sketchpad = new Atrament(canvas, {
        color: 'black',


    });
    sketchpad.smoothing = 0.2;

    const ctx = canvas.getContext('2d');
    ctx.lineWidth = 3;
    ctx.beginPath();
    ctx.moveTo(padding, height - padding);
    ctx.lineTo(width - padding, height - padding);
    ctx.stroke();

    ctx.font = "12px Arial";
    ctx.fillText("12/13/2022", width - 90, height - 10);
  
    //drawImgToCanvas(canvas, imageElem);
    
    return sketchpad;
    //sketchpad.addEventListener('strokeend', () => console.info('strokeend'));
  
  }
  
  function save_canvas(elem, canvas, renderedImage, elemClicked){
      let pngLink = canvas.toDataURL();
      //document.querySelector("#sketchPng").value = pngLink;
      renderedImage.src = pngLink;
      document.getElementById('canvas').value = pngLink;
      //saveToLocalStorage(pngLink)

      
     //if(elemClicked.contains(renderedImage)){
       //elemClicked.removeChild(renderedImage);
       // elemClicked.appendChild(savedImage);
      //}



      toggleDisplayed(elem);
  }
  
  function drawImgToCanvas(canvas, imageElem){
    
      ctx.drawImage(imageElem, 0, 0, imageElem.width, imageElem.height,
                          0, 0, canvas.width, canvas.height);
  }