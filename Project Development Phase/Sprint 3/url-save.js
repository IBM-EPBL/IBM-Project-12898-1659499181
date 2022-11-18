/*url = window.location.href

const xhr = new XMLHttpRequest();
xhr.open("POST", "http://127.0.0.1:5000/extension", true);

//triggered when the response is completed

xhr.onload = function() {
  if (xhr.status === 200) {
    data = JSON.parse(xhr.responseText)
    if(data==0){
      alert("This website looks like a phishing website. Proceed with caution!!!")
    }
    console.log(data)
  } 
  else if (xhr.status === 404) {
    console.log("No records found")
  }
}

xhr.onerror = function() {
  console.log("Network error occurred")
}

xhr.onprogress = function(e) {
  if (e.lengthComputable) {
    console.log(`${e.loaded} B of ${e.total} B loaded!`)
  } else {
    console.log(`${e.loaded} B loaded!`)
  }
}


xhr.send({'url':url});
*/

function sendURL(){

  let url = window.location.href;
  let xhr = new XMLHttpRequest();

  xhr.open("POST", "http://127.0.0.1:5000/extension", true);
  xhr.setRequestHeader("Content-Type", "application/json");

  xhr.onload = function () {
    if (xhr.readyState === 4 && xhr.status === 200) {
      console.log(this.responseText);
    }
  };

  var data = JSON.stringify({"url":url});
  xhr.send(data);
}