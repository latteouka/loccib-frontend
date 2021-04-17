
document.getElementById("input").value = "text1\ntext2\ntext3";


function clickcopy() {
  /* Get the text field */
  var copyText = document.getElementById("result");

  /* Select the text field */
  copyText.select(); 
  copyText.setSelectionRange(0, 99999); /* For mobile devices */

  /* Copy the text inside the text field */
  document.execCommand("copy");

  /* Alert the copied text */
  alert("Copied!!");
}

function getresult_1() {
  
  var input = document.getElementById("input").value;
  var inputs = input.split('\n');
  
  result_string = ""

  for (i = 0; i < inputs.length; i++) { 
  	result_string = result_string + inputs[i] + ","
  }

  //delete \n
  result_string = result_string.slice(0, -1)

  document.getElementById("result").value = result_string;
}

function getresult_2() {
  
  var input = document.getElementById("input").value;
  var inputs = input.split('\n');
  
  result_string = ""

  for (i = 0; i < inputs.length; i++) { 
    result_string = result_string + inputs[i] + "，"
  }

  //delete \n
  result_string = result_string.slice(0, -1)

  document.getElementById("result").value = result_string;
}

function getresult_3() {
  
  var input = document.getElementById("input").value;
  var inputs = input.split('\n');
  
  result_string = ""

  for (i = 0; i < inputs.length; i++) { 
    result_string = result_string + inputs[i] + "、"
  }

  //delete \n
  result_string = result_string.slice(0, -1)

  document.getElementById("result").value = result_string;
}