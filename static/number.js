number = "0922334455\n0912456789\n02-26223333";
document.getElementById("number").value = number;

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

function minusDays(date, days) {
  var result = new Date(date);
  result.setDate(result.getDate() - days);
  return result;
}


function getresult() {
  
  var number = document.getElementById("number").value;
  var numbers = number.split('\n');

  results = []

  var today = Date();

  end = minusDays(today, 1)
  from = minusDays(today, 7)

  from_formatted = from.getFullYear()+("0"+(from.getMonth()+1)).slice(-2)+("0" + from.getDate()).slice(-2)+("0" + from.getHours()).slice(-2)+("0" + from.getMinutes()).slice(-2)+("0" + from.getSeconds()).slice(-2)
  end_formatted = end.getFullYear()+("0"+(end.getMonth()+1)).slice(-2)+("0" + end.getDate()).slice(-2)+("0" + end.getHours()).slice(-2)+("0" + end.getMinutes()).slice(-2)+("0" + end.getSeconds()).slice(-2)
  


  var i;
  for (i = 0; i < numbers.length; i++) {
    if (numbers[i].includes("-")) {
      results.push(["市內電話", "-", numbers[i], from_formatted, end_formatted, "使用者資料"])
    }
    else {
      results.push(["行動電話", "-", "886"+numbers[i].substr(1), from_formatted, end_formatted, "使用者資料"])
    }

  }
  console.log(results)
  
  

  result_string = ""

  for (i = 0; i < results.length; i++) { 
  	result_string = result_string + results[i] + "\n"
  }

  //delete \n
  result_string = result_string.slice(0, -1)

  document.getElementById("result").value = result_string;

  document.getElementById("number").onclick = null;
  
  
}


function clickdownload() {
  
  var result = document.getElementById("result").value
  var results = result.split('\n');

  console.log(results)

  let csvContent = "data:text/csv;charset=utf-8,";


  results.forEach(function(result) {
    
    csvContent += result + "\r\n";
  });


  var encodedUri = encodeURI(csvContent);
  var link = document.createElement("a");
  link.setAttribute("href", encodedUri);
  link.setAttribute("download", "phones.csv");
  document.body.appendChild(link); // Required for FF

  link.click();
}



