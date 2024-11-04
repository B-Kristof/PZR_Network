let martinBefore = window.getComputedStyle(document.getElementById("martin_profile"), "::before");
let martinBg = martinBefore.getPropertyValue("background-image");

let markBefore = window.getComputedStyle(document.getElementById("mark_profile"), "::before");
let markBg = markBefore.getPropertyValue("background-image");

// Define the expanded HTML content for each profile
const expandedContent = {
    martin: `
      <div class="profile-picture">
        <img src="images/members/martin_alt.png">
      </div>
      <div class="description">
        <p>" Bővebb információ: A versenyzés iránti szenvedélyemet a Forulma 1 játék inspirálta. Azóta számos versenyen vettem részt. "</p>
        <p>Achievements: 2017 - First sim-racing win, hundreds of races completed since.</p>
      </div>
    `,
    mark: `
      <div class="profile-picture">
        <img src="images/members/mark_alt.png">
      </div>
      <div class="description">
        <p>" Kiskorom óta érdekel a szimulátoros versenyzés. Azóta több száz versenyt teljesítettem, és ez már több, mint hobbi számomra. "</p>
        <p>Achievements: 2018 - Entered online racing, hundreds of races since then.</p>
      </div>
    `
  };

  // Toggle between initial and expanded content
  function toggleProfile(profile, id) {
    profile.classList.toggle('expanded');
    profile.classList.toggle('collapsed');
    
    if (profile.classList.contains('expanded')) {
      // Load expanded content
      profile.innerHTML = expandedContent[id];
    } else {
      // Load initial content (replace with original HTML or simpler version)
      if (id === 'martin') {
        profile.innerHTML = `
          <div class="profile-picture">
            <img src="images/members/martin_alt.png">
          </div>
          <div class="description">
            <p>" Mózes Martin vagyok, és a szenvedélyem a versenyzés iránt már gyerekkoromban elkezdődött a 2005-ös Forulma 1 játékkal. 2014-ben a billentyűzetet sikeresen egy kormányra tudtam cserélni, ami az első mérföldkő volt a karrieremben. Először 2017-ben vettem részt szimulátoros versenyen amit sikerült is megnyerni. Innentől ez a hobbimmé vált és szerelem lett belőle. Azóta több száz versenyen résztvettem, mint egyénileg, mint csapatban, amik sikerrel zárultak. Mára ez szenvedéllyé forrta ki magát és nem tudok a pódium első foka alá adni. "</p>
          </div>
        `;
      } else if (id === 'mark') {
        profile.innerHTML = `
          <div class="profile-picture">
            <img src="images/members/mark_alt.png">
          </div>
          <div class="description">
            <p>" Nagy Márknak hívnak, és a PZR Esport Team szimulátoros csapatát erősítem. Már kiskoromban lehetőségem volt otthon számítógépes kormánnyal játszani. Már ekkor éreztem, hogy ez a világnekem való. Bár csak 2018-ban értem el arra a szintre, hogy online komolyabb versenyeken is részt vehessek. Akár egyénileg, akár csapatban. Mára már több, mint hobbiként kezelem ezt a tevékenységet és azóta már több száz versenyt teljesítettem! "</p>
          </div>
        `;
      }
    }
  }