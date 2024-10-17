class LocationRepo {
    constructor() {
        this.locations = [];
    }

    // CRUD FUNCTIONS //

    // Method to add a location to the repository
    addLocation(location) {
        this.locations.push(location);
    }

    // Method to retrieve all locations from the repository
    getAllLocations() {
        return this.locations;
    }

    // Method to remove a location by its ID
    removeLocationById(id) {
        this.locations = this.locations.filter(location => location.id !== id);
    }

    // Method to update a location by its ID
    updateLocationById(id, updatedLocation) {
        const index = this.locations.findIndex(location => location.id === id);
        if (index !== -1) {
            this.locations[index] = updatedLocation;
            return true; // Location updated successfully
        }
        return false; // Location not found
    }



    // NON CRUD FUNCTIONS //

    // Method to find a location by its ID
    findLocationById(id) {
        return this.locations.find(location => location.id === id);
    }
    // Method to find locations by name
    searchByName(name) {
        return this.locations.filter(location => location.name.toLowerCase().includes(name.toLowerCase()));
    }

    // Method to find locations by address
    searchByAddress(address) {
        return this.locations.filter(location => location.address.toLowerCase().includes(address.toLowerCase()));
    }

    // Method to load locations from a JSON file
    async loadFromJson(filePath) {
        try {
            const response = await fetch(filePath);
            const locationsData = await response.json();
    
            const locations = locationsData.map(locationData => {
                return new LocationBuilder()
                    .setId(locationData.id)
                    .setCreated_by(created_by)
                    .setName(locationData.name)
                    .setCoordinates(locationData.coordinates)
                    .setAddress(locationData.address)
                    .setVisitDate(locationData.visitDate)
                    .setPartofDay(locationData.partofDay)
                    .setFactor(locationData.factor)
                    .setDescription(locationData.description)
                    .setTitleImage(locationData.titleImage)
                    .setImages(locationData.images)
                    .build();
            });
    
            return locations;
        } catch (error) {
            console.error('Error fetching locations:', error);
            return [];
        }
    }


    // Method to save locations to a JSON string
    saveToJson() {
        try {
            return JSON.stringify(this.locations);
        } catch (error) {
            console.error('Error saving locations to JSON:', error.message);
            return null;
        }
    }
}