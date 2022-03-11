document.getElementById('formA5sketch').addEventListener('click', (elem)=>{sketchPopup(elem.currentTarget)});

function sketchPopup(elemClicked){
    const canvas = document.getElementById('sketchpad');
    elemEffected = elemClicked.dataset.controls;
    elem = document.getElementById(elemEffected);
    console.log(elem);
    canvisInitiated = elem.dataset.canvis_intiated;
    console.log(canvisInitiated);
    if(canvisInitiated == 'False'){
      initiateSketch(elemClicked);
      elem.dataset.canvis_intiated = 'True'
    }
      console.log('test');
      toggleDisplayed(elemClicked);
  }
  
  
  function initiateSketch(imgElem){
    const canvas = document.getElementById('sketchpad');
  
    // Use the intrinsic size of image in CSS pixels for the canvas element
    canvas.width = 650;
    canvas.height = 500;
  
      
    console.log(canvas);
    const sketchpad = new Atrament(canvas, {
        color: 'black',
        
    });
    sketchpad.smoothing = 0.2;
  
    drawImgToCanvas(canvas, imgElem);
    
    document.getElementById('clearCanvis').addEventListener('click', ()=>{sketchpad.clear() });
    document.getElementById('canvas_save').addEventListener('click', (elem)=>{save_canvas(elem.currentTarget, canvas, imgElem)});
  
  
  }
  
  
  function save_canvas(elem, canvas, imgElem){
      
      imgElem.src = canvas.toDataURL();
      toggleDisplayed(elem);
    
  }
  
  function drawImgToCanvas(canvas, imgElem){
    const ctx = canvas.getContext('2d');
  
    const image = new Image(); // Using optional size for image
    image.onload = drawPhotograph; // Draw when image has loaded
  
    // Load an image of intrinsic size 300x227 in CSS pixels
    image.src = imgElem.dataset.base_img;
  
    function drawPhotograph() {
      // Use the intrinsic size of image in CSS pixels for the canvas element
      //canvas.width = 650;
      //canvas.height = 500;
    
      // Will draw the image as 300x227, ignoring the custom size of 60x45
      // given in the constructor
      //ctx.drawImage(this, 0, 0);
    
      // To use the custom size we'll have to specify the scale parameters
      // using the element's width and height properties - lets draw one
      // on top in the corner:
      ctx.drawImage(this, 0, 0, this.width, this.height,
                          0, 0, canvas.width, canvas.height);
    };
  }
  