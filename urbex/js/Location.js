class Location {
    constructor(id, created_by, name, coordinates, address, visitDate, partofDay, factor, links, description, titleImage, images) {
        this.created_by = created_by;
        this.id = id;
        this.name = name;
        this.coordinates = coordinates;
        this.address = address;
        this.visitDate = visitDate;
        this.partofDay = partofDay;
        this.factor = factor;
        this.links = links;
        this.description = description;
        this.titleImage = titleImage;
        this.images = images;
    }
}

class LocationBuilder {
    constructor() {
        this.location = new Location(null, null, null, null, null, null, null, null, null, null, null);
    }

    setId(id) {
        this.location.id = id;
        return this;
    }

    setCreated_by(created_by) {
        this.location.created_by = created_by;
        return this;
    }

    setName(name) {
        this.location.name = name;
        return this;
    }

    setCoordinates(coordinates) {
        this.location.coordinates = coordinates;
        return this;
    }

    setAddress(address) {
        this.location.address = address;
        return this;
    }

    setVisitDate(visitDate) {
        this.location.visitDate = visitDate;
        return this;
    }

    setPartofDay(partofDay) {
        this.location.partofDay = partofDay;
        return this;
    }

    setFactor(factor) {
        this.location.factor = factor;
        return this;
    }

    setLinks(links) {
        this.location.links = links;
        return this;
    }

    setDescription(description) {
        this.location.description = description;
        return this;
    }

    setTitleImage(titleImage) {
        this.location.titleImage = titleImage;
        return this;
    }

    setImages(images) {
        this.location.images = images;
        return this;
    }

    build() {
        return this.location;
    }
}


