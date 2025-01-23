const profiles = document.querySelectorAll('.vertical_fourth .profile-container .martin_profile, .vertical_fourth .profile-container .mark_profile, .vertical_fourth .profile-container .csonor_profile');

function toggle_profile(){
    profiles.forEach(profile => {
    profile.addEventListener('click', () => {
        const profileName = profile.classList[0]; // Get the profile name (e.g., "martin_profile")
        const driver_name = profileName.split('_')[0];
        divs_to_hide = [`${driver_name}_profile_picture`, `${driver_name}_desc`]
        const achievementsId = `${profileName.replace('_profile', '_achievements')}`; 
        const achievementsDiv = document.getElementById(achievementsId);
        const computedStyle = window.getComputedStyle(achievementsDiv);
        if (computedStyle.display === 'none') {
        achievementsDiv.style.display = 'grid';
        divs_to_hide.forEach(element => {
            divchild = document.getElementById(element);
            console.log(divchild);
            divchild.style.display = 'none';
        });
        } else {
        achievementsDiv.style.display = 'none';
        divs_to_hide.forEach(element => {
            divchild = document.getElementById(element);
            divchild.style.display = 'grid';
        });
        }
    });
    });
}


toggle_profile();