var tDate = new Date
const today = (`${tDate.getYear()+1900}-${tDate.getMonth()+1}-${tDate.getDate()}`)
const form = document.querySelector("#form_container")
form.addEventListener("submit",(e)=>preSubmit(e))
const canvas = document.querySelector("#signature_canvas");

const formDate = document.querySelector("#form_date");
formDate.value = today
const canvasHeight = canvas.clientHeight
const canvasWidth = canvas.clientWidth
canvas.width = canvasWidth;
canvas.height = canvasHeight;



const sketchpad = new Atrament(canvas, {
    color: 'black',
});
sketchpad.smoothing = 0.2;
var ctx = canvas.getContext("2d");
ctx.lineWidth=3;
ctx.beginPath();
ctx.moveTo(20, canvasHeight-100);
ctx.lineTo(canvasWidth-20, canvasHeight-100);
ctx.stroke();
ctx.font = "16px Arial";
ctx.fillText(today, canvasWidth-100, canvasHeight-50);


function preSubmit(event){
    const canvas = document.querySelector("#signature_canvas");
    const form_canvas = document.querySelector("#form_canvas")
    const pngLink = canvas.toDataURL();

    form_canvas.value = pngLink
}