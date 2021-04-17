function getresult_1() {
  
  var input = document.getElementById("number").value;
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
  
  var input = document.getElementById("number").value;
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
  
  var input = document.getElementById("number").value;
  var inputs = input.split('\n');
  
  result_string = ""

  for (i = 0; i < inputs.length; i++) { 
    result_string = result_string + inputs[i] + "、"
  }

  //delete \n
  result_string = result_string.slice(0, -1)

  document.getElementById("result").value = result_string;
}