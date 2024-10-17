URBEX:
--- RANG SYSTEM ---

user: level 1
    - add location
    - cannot generate invitation

member: level 2
    - a user become a member if he add 5 VISITED locations -> desc, links
    - can generate 2 invitation codes (? after all locations validated ?) 

explorer: level 3
    - a user become an explorer if he add 10 VISITED locations, and 10 TARGET locations -> desc, links
    - can generate any invitation codes (? after all locations validated ?) 

implement:
admin: level n
    - update, remove, add location
    - can update other user's location
    - ban, pardon user, member

DEV: level n + 1
    - all admin rights
    - ban / pardon / add admin, user, member

--- MY PROFILE ---
- username
- rang
- added visited location count
- added target location count

ESPORT:
### Todo

- [ ] Profile for each member
    - [ ] Link social medias for each member (Instagram, Youtube, Twitch, etc.)
    - [ ] Achievements of each member

### In Progress

- [ ] Website deployer (Python script)


### Done ✓
- [x] State UML diagram
- [x] About (vertical second)
- [x] SSL certificate
- [x]  Sponsors (vertical sixth)
    - [x] add Sponsors to top menu
    - [x] Link sponsor's website to logo
- [x] Media.html (vertical fifth)
    - [x] gallery with ingame images
    - [x] embedded Youtube and Twitch links
    - [x] move footer to vertical_seventh
- [x] mobile optimized CSS for home.html
- [x] fix iframe video on mobile
- [x] Language switch (HU/EN)
- [x] RedirectionHandler.js
    - [x] Count visits on social medias and Partner websites
    - [x] Test for vulnerabilities (DDOS/XSS/Open Redirect)
- [x] fix background size for desktop
- [x] members transparent images
- [x] Home background for mobile
- [x] member descriptions
