function getElement(id) {
  const element = document.getElementById(id);
  if (!element) throw new Error(`Element with ID '${id}' not found.`);
  return element;
}

function getQuerySelector(parent, selector) {
  if (!parent) return null;
  const element = parent.querySelector(selector);
  if (!element) throw new Error(`Selector '${selector}' not found in '${parent.id}'.`);
  return element;
}

// Profile elements
const profiles = ["mark", "martin", "csonor"];
const profileData = {};

profiles.forEach(name => {
  profileData[name] = {
      profile: getElement(`${name}_profile`),
      desc_original: getQuerySelector(getElement(`${name}_profile`), ".description p")?.textContent || "",
      profile_picture_div: getElement(`${name}_profile_picture`),
      desc_style: getQuerySelector(getElement(`${name}_profile`), ".description p")?.style || {},
      desc: getElement(`${name}_desc`),
      profile_picture_div_b: getElement(`${name}_profile_picture`)?.innerHTML || "",
      achievements: getElement(`${name}_achievements`)
  };
});

// Function to handle hover effect
function setupProfileHover(name, displayName, fontSize) {
  const data = profileData[name];
  if (!data.profile) return;

  data.profile.addEventListener('mouseenter', function () {
      const descEl = getQuerySelector(data.profile, ".description p");
      if (descEl) {
          descEl.textContent = `${displayName} vagyok, és a versenyzés a szenvedélyem.`;
          descEl.style.textAlign = "left";
          descEl.style.marginLeft = "30px";
      }

      if (data.profile_picture_div?.innerHTML === data.profile_picture_div_b) {
          if (data.desc) data.desc.style.display = "none";
          if (data.achievements) data.achievements.style.display = "block";
          if (data.profile_picture_div) {
              data.profile_picture_div.style.display = "flex";
              data.profile_picture_div.innerHTML += `
                  <div style="margin-left: 20px; font-size: ${fontSize}px; display: flex; width: 100%;">${displayName}</div>
              `;
          }
      }
  });

  data.profile.addEventListener('mouseleave', function () {
      if (data.desc) data.desc.style.display = "block";
      if (data.achievements) data.achievements.style.display = "none";
      if (data.profile_picture_div) data.profile_picture_div.innerHTML = data.profile_picture_div_b;

      const descEl = getQuerySelector(data.profile, ".description p");
      if (descEl) {
          descEl.textContent = data.desc_original;
          Object.assign(descEl.style, data.desc_style); // Restore original styles
      }
  });
}

// Apply hover effects to profiles
setupProfileHover("mark", "Márk Nagy", 50);
setupProfileHover("martin", "Martin Mózes", 45);
setupProfileHover("csonor", "Csongor Dobák", 45);

// Add staggered animation delays
profiles.forEach(name => {
  document.querySelectorAll(`#${name}_achievements li`).forEach((item, index) => {
      item.style.animationDelay = `${index * 0.1}s`;
  });
});
