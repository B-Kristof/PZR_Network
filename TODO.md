# 🛠️ PZR Websites TODO List

---

## 🌐 **Main Page**

### 📝 Todo
- [ ] Modify intext on Google index

### 🔄 In Progress

### ✅ Done

---

## 🎮 **ESPORT**

### 📝 Todo
- [ ] Mobile background for Driver profiles
- [ ] Redirect handler -> Write logs in Apache
    - [ ] Filter for valid records
- [ ] Database integration for RedirectHandler

### 🔄 In Progress

- [ ] Gallery page

### ✅ Done
- [x] State UML diagram
- [x] About section (vertical second)
- [x] SSL certificate
- [x] Sponsors (vertical sixth)
    - [x] Added sponsors to the top menu
    - [x] Linked sponsor logos to their websites
- [x] Media.html (vertical fifth)
    - [x] Gallery with in-game images
    - [x] Embedded YouTube and Twitch links
    - [x] Footer moved to vertical seventh
- [x] Mobile-optimized CSS for home.html
- [x] Fixed iframe video on mobile
- [x] Language switch (HU/EN)
- [x] RedirectionHandler.js
    - [x] Counted visits to social media and partner websites
    - [x] Tested for vulnerabilities (DDOS/XSS/Open Redirect)
- [x] Desktop background fixes
- [x] Transparent member images
- [x] Mobile-friendly home background
- [x] Member descriptions
- [x] Profile for each member
    - [x] Link social media accounts (Instagram, YouTube, Twitch, etc.)
    - [x] Achievements of each member
- [x] Better font for Driver profiles
- [x] Translate "Subscribe" to Hungarian (Media section)
- [x] Add Simhome partner

---

## 🏚️ **URBEX**

### 📝 Todo
- [ ] **Rank System**
    - [ ] **Level 1 - User**: Add locations but cannot generate invitations.
    - [ ] **Level 2 - Member**: Add 5 visited locations to level up and generate 2 invitations.
    - [ ] **Level 3 - Explorer**: Add 10 visited and 10 target locations to level up; unlimited invitations after validation.
    - [ ] **Admin**: Manage locations, ban/pardon users, update other users' locations.
    - [ ] **DEV**: All admin rights, plus manage admins.
- [ ] **My Profile Improvements**
    - [ ] Show username, rank, visited location count, and target location count.
- [ ] Add SSL certificate
- [ ] **Terms and Conditions** (ÁSZF)
- [ ] Add basic information and tips:
    - [ ] General Urbex overview
    - [ ] Safety
    - [ ] Equipment
    - [ ] Tips
- [ ] Restructure Locations menu
    - [ ] Add "All locations" (excluding visited locations).
- [ ] Enable marking locations as "Visited"
    - [ ] Update location model and database (add `visited_by` column).
    - [ ] Replace `visited_locations.json` with database integration.
    - [ ] Update JS for map markers (red for unvisited, blue for visited).
- [ ] Store locations in a database
- [ ] Add the ability to download archived images (RAR/ZIP) of locations
- [ ] Add `robots.txt` to block Google indexing
- [ ] Location "Flags" (e.g., CCTV, Guard dogs, Alarms, Collapsing structures, etc.)
- [ ] Improved gallery view
- [ ] Add location types (Residential, Industrial, Public Service, Recreational, Military, Historical)

### 🔄 In Progress

### ✅ Done

---

## 🔒 **Members Only**

### 📝 Todo
- [ ] Disable page indexing for search engines

### 🔄 In Progress

- [ ] Database integration

### ✅ Done

---

## 📦 **WebsiteDeployer**

### 📝 Todo
- [ ] Add a GUI interface
- [ ] Discord Bot configuration
- [ ] CLI-based monitor tool

### 🔄 In Progress

### ✅ Done

---

### Legend:
- **📝 Todo**: Planned tasks to work on
- **🔄 In Progress**: Actively being developed
- **✅ Done**: Completed features and fixes
