const mark_desc_original = document.getElementById("mark_profile").querySelector('.description p').textContent;
let mark_profile_picture_div = document.getElementById("mark_profile_picture");
const mark_desc_style = document.getElementById("mark_profile").querySelector('.description p').style;
let mark_desc = document.getElementById("mark_desc");
const mark_profile_picture_div_b = document.getElementById("mark_profile_picture").innerHTML;
let mark_achievements = document.getElementById("mark_achievements");

const martin_desc_original = document.getElementById("martin_profile").querySelector('.description p').textContent;
let martin_profile_picture_div = document.getElementById("martin_profile_picture");
const martin_desc_style = document.getElementById("martin_profile").querySelector('.description p').style;
let martin_desc = document.getElementById("martin_desc");
const martin_profile_picture_div_b = document.getElementById("martin_profile_picture").innerHTML;
let martin_achievements = document.getElementById("martin_achievements");

const csonor_desc_original = document.getElementById("csonor_profile").querySelector('.description p').textContent;
let csonor_profile_picture_div = document.getElementById("csonor_profile_picture");
const csonor_desc_style = document.getElementById("csonor_profile").querySelector('.description p').style;
let csonor_desc = document.getElementById("csonor_desc");
const csonor_profile_picture_div_b = document.getElementById("csonor_profile_picture").innerHTML;
let csonor_achievements = document.getElementById("csonor_achievements");

document.getElementById('mark_profile').addEventListener('mouseenter', function() {
  this.querySelector('.description p').textContent = `Nagy Márk vagyok, és a versenyzés a szenvedélyem.`;
  this.querySelector('.description p').style.textAlign = "left";
  this.querySelector('.description p').style.marginLeft = "30px";
  if (mark_profile_picture_div.innerHTML == mark_profile_picture_div_b){
    mark_desc.style.display = "none";
    mark_achievements.style.display = "block";
    mark_profile_picture_div.style.display = "flex";
    mark_profile_picture_div.innerHTML += `
      <div style="margin-left: 20px; font-size: 50px; display: flex; width: 100%;">Nagy Márk</div>
    `;
  }
});

document.getElementById('mark_profile').addEventListener('mouseleave', function() {
  mark_desc.style.display = "block";
  mark_achievements.style.display = "none";
  this.querySelector('.description p').textContent = mark_desc_original;
  mark_profile_picture_div.innerHTML = mark_profile_picture_div_b;
  this.querySelector('.description p').style = mark_desc_style
});



document.getElementById('martin_profile').addEventListener('mouseenter', function() {
  if (martin_profile_picture_div.innerHTML == martin_profile_picture_div_b){
    martin_desc.style.display = "none";
    martin_achievements.style.display = "block";
    this.querySelector('.description p').display = "none";
    martin_profile_picture_div.style.display = "flex";
    martin_profile_picture_div.innerHTML += `
      <div style="margin-left: 20px; font-size: 45px; display: flex; width: 80%;">Mózes Martin</div>
    `;
  }
});
document.getElementById('martin_profile').addEventListener('mouseleave', function() {
  martin_desc.style.display = "block";
  martin_achievements.style.display = "none";
  this.querySelector('.description p').textContent = martin_desc_original;
  martin_profile_picture_div.innerHTML = martin_profile_picture_div_b;
  this.querySelector('.description p').style = martin_desc_style
});

document.getElementById('csonor_profile').addEventListener('mouseenter', function() {
  if (csonor_profile_picture_div.innerHTML == csonor_profile_picture_div_b){
    csonor_desc.style.display = "none";
    csonor_achievements.style.display = "block";
    this.querySelector('.description p').display = "none";
    csonor_profile_picture_div.style.display = "flex";
    csonor_profile_picture_div.innerHTML += `
      <div style="margin-left: 20px; font-size: 45px; display: flex; width: 80%;">Dobák Csongor</div>
    `;
  }
});
document.getElementById('csonor_profile').addEventListener('mouseleave', function() {
  csonor_desc.style.display = "block";
  csonor_achievements.style.display = "none";
  this.querySelector('.description p').textContent = csonor_desc_original;
  csonor_profile_picture_div.innerHTML = csonor_profile_picture_div_b;
  this.querySelector('.description p').style = csonor_desc_style
});

// JavaScript to add staggered delay dynamically
document.querySelectorAll("#martin_achievements li").forEach((item, index) => {
  item.style.animationDelay = `${index * 0.1}s`;
});

// JavaScript to add staggered delay dynamically
document.querySelectorAll("#mark_achievements li").forEach((item, index) => {
  item.style.animationDelay = `${index * 0.1}s`;
});

// JavaScript to add staggered delay dynamically
document.querySelectorAll("#csonor_achievements li").forEach((item, index) => {
  item.style.animationDelay = `${index * 0.1}s`;
});