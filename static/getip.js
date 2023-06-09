

function copyToClipboard(elementId) {

  // Create an auxiliary hidden input
  var aux = document.createElement("input");

  // Get the text from the element passed into the input
  aux.setAttribute("value", document.getElementById(elementId).innerHTML);

  // Append the aux input to the body
  document.body.appendChild(aux);

  // Highlight the content
  aux.select();

  // Execute the copy command
  document.execCommand("copy");

  // Remove the input from the body
  document.body.removeChild(aux);

  /* Alert the copied text 
  alert("Copied!!");
  */

}


function show() {
  var x = document.getElementById("formContent");
  if (x.style.display === "none") {
    x.style.display = "block";
  } else {
    x.style.display = "none";
  }
}