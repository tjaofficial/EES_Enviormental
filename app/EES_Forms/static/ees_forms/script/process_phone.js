// document.getElementById('id_phone').addEventListener('input', function (e) {
//     let input = e.target.value.replace(/\D/g, ''); // Remove all non-digit characters
//     let formattedNumber = '';
  
//     if (input.length > 0) {
//       formattedNumber += '(' + input.substring(0, 3); // First 3 digits, add "("
//     }
//     if (input.length >= 4) {
//       formattedNumber += ') ' + input.substring(3, 6); // Next 3 digits, add ") "
//     }
//     if (input.length >= 7) {
//       formattedNumber += '-' + input.substring(6, 10); // Final 4 digits, add "-"
//     }
  
//     e.target.value = formattedNumber; // Assign formatted number back to input
// });
function processPhone(e){
    let input = e.target.value.replace(/\D/g, ''); // Remove all non-digit characters
    let formattedNumber = '';
  
    if (input.length > 0) {
      formattedNumber += '(' + input.substring(0, 3); // First 3 digits, add "("
    }
    if (input.length >= 4) {
      formattedNumber += ') ' + input.substring(3, 6); // Next 3 digits, add ") "
    }
    if (input.length >= 7) {
      formattedNumber += '-' + input.substring(6, 10); // Final 4 digits, add "-"
    }
  
    e.target.value = formattedNumber; // Assign formatted number back to input
}