function openNav() {
  document.getElementById("mySidenav").style.width = "250px";
}

function closeNav() {
  document.getElementById("mySidenav").style.width = "0";
}



var ms = document.getElementById("mssg");

setTimeout(function () {
  ms.style.display = "none";
}, 4000);


function openModal(url) {
  var modal = document.getElementById('myModal');
  var modalImg = document.getElementById("img01");
  modal.style.display = "block";
  modalImg.src = url;
}

function closeModal() {
  document.getElementById('myModal').style.display = "none";
}

