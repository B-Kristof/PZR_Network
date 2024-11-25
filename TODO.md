# Main Page

### Todo
- [ ] Modify intext on Google index

### In Progress

### Done ✓

# ESPORT:

### Todo

- [ ] Profile for each member
    - [ ] Link social medias for each member (Instagram, Youtube, Twitch, etc.)
    - [ ] Achievements of each member
- [ ] Mobile background for Driver profiles
- [ ] Better font for Driver profiles
- [ ] Translate "Subscribe" to Hungarian (Media section)
- [ ] Redirecthandler -> write in apache log
    - [ ] Filter for valid records 

### In Progress

- [ ] Website deployer (Python script)
- [ ] Website Monitor (Python script)
    - [ ] Offline state alert system
    - [ ] GUI


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


# URBEX:

### Todo
- [ ] Rang System
    - [ ] user: level 1
        - [ ] add location
        - [ ] cannot generate invitation
    - [ ] member: level 2
        - [ ] a user become a member if he add 5 VISITED locations -> desc, links
        - [ ] can generate 2 invitation codes (? after all locations validated ?) 
    - [ ] explorer: level 3
        - [ ] a user become an explorer if he add 10 VISITED locations, and 10 TARGET locations -> desc, links
        - [ ] can generate any invitation codes (? after all locations validated ?) 
    - [ ] admin: level n
        - [ ] update, remove, add location
        - [ ] can update other user's location
        - [ ] ban, pardon user, member
    - [ ] DEV: level n + 1
        - [ ] all admin rights
        - [ ] ban / pardon / add admin, user, member

- [ ] My Profile improvemenets
    - [ ] username
    - [ ] rang
    - [ ] added visited location count
    - [ ] added target location count

- [ ] SSL Certificate
    
- [ ] ÁSZF / Terms and Conditions

- [ ] Basic informations and tips
    - [ ] Urbex in general
    - [ ] Safety
    - [ ] Equipment
    - [ ] Tips

- [ ] Restructure Locations menu
    - [ ] All locations (No visited locations)

 - [ ] User can mark location as "Visited"
     - [ ] Modify Location model
     - [ ] Modify database -> add "visited_by" column -> store the user ID of the users who visited
     - [ ] Fix map display (red and blue marker)
     - [ ] Delete visited_locations.json
     - [ ] Fix js code (do not load visited_locations.json)

- [ ] Store locations in a database

- [ ] Download archived (rar/zip) images of a location

- [ ] robots.txt -> Avoid indexing by Google

- [ ] Location "flags" -> CCTV, Guard, Guard dog(s), Alarm system, Risk of collapse, Still water, Active demolotion, Squatter(s), Active electricity / Risk of electric shock, black mold, Partly Occupied Building, hazardous materials, other (provide description)

- [ ] Improved Gallery view

- [ ] ? Location type ? -> Residential (House, Apartment etc.), Industrial (Factories, Warehouses etc.), Public Service (Hospitals, Offices, Aslyiums, Fire / Police stations, School etc), Recreational (Amusement parks, Sport Arenas, Cinemas), Military or Historical (Bunkers, Castles, Military bases etc)
      
### In Progress

### Done ✓

# Members Only

### Todo

- [ ] Disable page indexing

### In Progress

### Done ✓

# WebsiteDeployer

### Todo

- [ ] GUI

- [ ] DiscordBotConfig

- [ ] CLI based Monitor

### In Progress

### Done ✓
