const keyword = document.getElementById("keyword");
keyword.addEventListener("keyup", liveSearching);

function liveSearching() {
  const query = keyword.value;
  const xhr = new XMLHttpRequest();
  xhr.open("POST", "/search", true);
  xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
  xhr.onload = function () {
    if (this.status === 200) {
      document.getElementById("dataItems").innerHTML = this.responseText;
    }
  };
  xhr.send("keyword=" + encodeURIComponent(query));
}
