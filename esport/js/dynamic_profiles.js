const mark_desc_original = document.getElementById("mark_profile").querySelector('.description p').textContent;
let mark_profile_picture_div = document.getElementById("mark_profile_picture");
const mark_desc_style = document.getElementById("mark_profile").querySelector('.description p').style;
const mark_profile_picture_div_b = document.getElementById("mark_profile_picture").innerHTML;

const martin_desc_original = document.getElementById("martin_profile").querySelector('.description p').textContent;
let martin_profile_picture_div = document.getElementById("martin_profile_picture");
const martin_desc_style = document.getElementById("martin_profile").querySelector('.description p').style;
const martin_profile_picture_div_b = document.getElementById("martin_profile_picture").innerHTML;

document.getElementById('mark_profile').addEventListener('mouseenter', function() {
  this.querySelector('.description p').textContent = "Nagy Márk vagyok, és a versenyzés a szenvedélyem.";
  this.querySelector('.description p').style.textAlign = "left";
  this.querySelector('.description p').style.marginLeft = "30px";
  if (mark_profile_picture_div.innerHTML == mark_profile_picture_div_b){
    mark_profile_picture_div.style.display = "flex";
    mark_profile_picture_div.innerHTML += `
      <div style="margin-left: 20px; font-size: 50px; display: flex; width: 100%;">Nagy Márk</div>
    `;
  }
});

document.getElementById('mark_profile').addEventListener('mouseleave', function() {
  this.querySelector('.description p').textContent = mark_desc_original;
  mark_profile_picture_div.innerHTML = mark_profile_picture_div_b;
  this.querySelector('.description p').style = mark_desc_style
});

document.getElementById('martin_profile').addEventListener('mouseenter', function() {
  this.querySelector('.description p').textContent = "Mózes Martin vagyok, és a versenyzés a szenvedélyem.";
  this.querySelector('.description p').style.textAlign = "left";
  this.querySelector('.description p').style.marginLeft = "30px";
  if (martin_profile_picture_div.innerHTML == martin_profile_picture_div_b){
    martin_profile_picture_div.style.display = "flex";
    martin_profile_picture_div.innerHTML += `
      <div style="margin-left: 20px; font-size: 50px; display: flex; width: 100%;">Mózes Martin</div>
    `;
  }
});
document.getElementById('martin_profile').addEventListener('mouseleave', function() {
  this.querySelector('.description p').textContent = martin_desc_original;
  martin_profile_picture_div.innerHTML = martin_profile_picture_div_b;
  this.querySelector('.description p').style = martin_desc_style
});
