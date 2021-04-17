
document.getElementById("input1").value = "text1\ntext3\ntext5";
document.getElementById("input2").value = "text2\ntext4\ntext6";


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
  
  var input1 = document.getElementById("input1").value;
  var input1s = input1.split('\n');

  var input2 = document.getElementById("input2").value;
  var input2s = input2.split('\n');

  if(input1s.length !== input2s.length) {
    alert("數量不相等！");
    return;
  }
  
  result_string = ""

  for (i = 0; i < input1s.length; i++) { 
  	result_string = result_string + input1s[i] + "," + input2s[i] + "\n"
  }

  //delete \n
  result_string = result_string.slice(0, -1)

  document.getElementById("result").value = result_string;
}

function getresult_2() {
  
  var input1 = document.getElementById("input1").value;
  var input1s = input1.split('\n');

  var input2 = document.getElementById("input2").value;
  var input2s = input2.split('\n');

  if(input1s.length !== input2s.length) {
    alert("數量不相等！");
    return;
  }
  
  result_string = ""

  for (i = 0; i < input1s.length; i++) { 
    result_string = result_string + input1s[i] + "，" + input2s[i] + "\n"
  }

  //delete \n
  result_string = result_string.slice(0, -1)

  document.getElementById("result").value = result_string;
}

function getresult_3() {
  
  var input1 = document.getElementById("input1").value;
  var input1s = input1.split('\n');

  var input2 = document.getElementById("input2").value;
  var input2s = input2.split('\n');

  if(input1s.length !== input2s.length) {
    alert("數量不相等！");
    return;
  }
  
  result_string = ""

  for (i = 0; i < input1s.length; i++) { 
    result_string = result_string + input1s[i] + "(" + input2s[i] + ")\n"
  }

  //delete \n
  result_string = result_string.slice(0, -1)

  document.getElementById("result").value = result_string;
}

function getresult_4() {
  
  var input1 = document.getElementById("input1").value;
  var input1s = input1.split('\n');

  var input2 = document.getElementById("input2").value;
  var input2s = input2.split('\n');

  if(input1s.length !== input2s.length) {
    alert("數量不相等！");
    return;
  }
  
  result_string = ""

  for (i = 0; i < input1s.length; i++) { 
    result_string = result_string + input1s[i] + "（" + input2s[i] + "）\n"
  }

  //delete \n
  result_string = result_string.slice(0, -1)

  document.getElementById("result").value = result_string;
}


function copytoinput1() {
  
  document.getElementById("input1").value = document.getElementById("result").value

}