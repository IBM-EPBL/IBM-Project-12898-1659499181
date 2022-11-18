let url = window.location.href;
let xhr = new XMLHttpRequest();
xhr.open("GET", "http://127.0.0.1:5000/extension?url="+url, true);
xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
xhr.send();

xhr.onreadystatechange = function () {
  if (xhr.readyState === 4 && xhr.status === 200)
  {
    let pred = JSON.parse(this.responseText);
    console.log(pred['prediction']);
    if(pred['prediction']=='-1')
    {
      alert("This website looks like a Phishing site. Proceed with caution.");
    }
	else if(pred['prediction']=='1'){
		alert("This website looks good. Enjoy the web!");
}
  }
};
