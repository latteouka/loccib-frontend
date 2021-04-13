

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

function time_format() {
  
  var time = document.getElementById("time").value;

  var lines = time.split('\n');

  var i;
  for (i = 0; i < lines.length; i++) { 
  	lines[i] = lines[i].substring(0, 4)+lines[i].substring(5, 7)+lines[i].substring(8, 10)+lines[i].substring(11, 13)+lines[i].substring(14, 16)
    //console.log(lines[i].substring(0, 4)+lines[i].substring(5, 7)+lines[i].substring(8, 10)+lines[i].substring(11, 13)+lines[i].substring(14, 16))
  }


  time_formatted = ""

  for (i = 0; i < lines.length; i++) { 
  	time_formatted = time_formatted + lines[i] + "\n"
  }

  //delete \n
  time_formatted = time_formatted.slice(0, -1)

  document.getElementById("time").value = time_formatted;

  document.getElementById("format").onclick = null;
  
}


function getresult() {
  
  var time = document.getElementById("time").value;
  var lines = time.split('\n');

  var ip = document.getElementById("ip").value;
  var ips = ip.split('\n');

  result = []


  if(lines.length !== ips.length) {
  	alert("時間跟IP數量不相等！");
  	return;
  }


  var i;
  for (i = 0; i < lines.length; i++) { 
  	result.push(ips[i]+","+lines[i])
  }


  result_string = ""

  for (i = 0; i < result.length; i++) { 
  	result_string = result_string + result[i] + "\n"
  }

  //delete \n
  result_string = result_string.slice(0, -1)

  document.getElementById("result").value = result_string;

  document.getElementById("result_button").onclick = null;
  
}

function getresultport() {
  
  var time = document.getElementById("time").value;
  var lines = time.split('\n');

  var ip = document.getElementById("ip").value;
  var ips = ip.split('\n');

  var port = document.getElementById("port").value;
  var ports = port.split('\n');

  result = []

  if(lines.length !== ips.length) {
    alert("時間跟IP數量不相等！");
    return;
  } else if (lines.length !== ports.length) {
    alert("時間跟Port數量不相等！");
    return;
  } else if (ips.length !== ports.length) {
    alert("IP跟Port數量不相等！");
    return;
  }


  var i;
  for (i = 0; i < lines.length; i++) { 
    result.push(ips[i]+","+lines[i]+","+ports[i])
  }


  result_string = ""

  for (i = 0; i < result.length; i++) { 
    result_string = result_string + result[i] + "\n"
  }

  //delete \n
  result_string = result_string.slice(0, -1)

  document.getElementById("result").value = result_string;

  document.getElementById("result_button").onclick = null;
  
}


function clickdownload() {
  
  text = document.getElementById("result").value

  var link = document.createElement('a');
  link.href = 'data:text/plain;charset=UTF-8,' + encodeURIComponent(text);
  
  //set default action on link to force download, and set default filename:
  link.download = 'ips.txt';     

  //now put the link somewhere in the html document:
  document.body.appendChild(link);
  link.click();
}


