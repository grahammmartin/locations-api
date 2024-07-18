# LocationRequest API
The LocationRequest API allows users to fetch and store location data based on addresses and coordinates using the Google Maps API.

## Table of Contents
- [Installation & Usage](#installation)
- [Example Data](#example-data)
- [Feature Documentation](#feature-documentation)
  - [Get Geo Code](#get-geo-code)
  - [Reverse Geo Code](#reverse-geo-code)
  - [Calculate Distance](#calculate-distance)


## Installation
### 1. **Clone the repository**:
```sh
   git clone https://github.com/grahammmartin/locations-api.git
   cd locations-api
```

### Set up your environment variables:

Add your Google Maps API key to .env.local file in the project root

```
GOOGLE_MAPS_API_KEY=<PASTE_YOUR_API_KEY_HERE>
```

### 2. **Use Docker to run the project**
```sh
   docker-compose up -d
```

That's all you will be able to access the application at `localhost:8000`

## Example Data
You can use the following example addresses to interact with the application:

### Address 1:
- **Address:** Amphitheatre Parkway
- **Coordinates:** 37.4224764, -122.0842499

### Address 2:
- **Address:** Cupertino
- **Coordinates:** 37.33182, -122.03118

### Address 3:

- **Address:** 350 5th Ave
- **Coordinates:** 40.748817, -73.985428

### Address 4:
- **Address:** Downing Street
- **Coordinates:** 51.5033635, -0.127625

## Feature Documentation

### Get Geo Code
**Endpoint:** `POST /api/locations/get_geocode/`

#### Implementation:
#### Serializer: AddressLocationRequest
- The create method of the serializer fetches data from the Google Maps API and creates a LocationRequest object if it doesn't exist.
- Validates and stores the address and its corresponding latitude, longitude, and formatted address.

#### Example Request:
```json
{
    "user_address": "Amphitheatre Parkway"
}
```
#### Example Response:

```json
{
    "id": 1,
    "address": "1600 Amphitheatre Parkway, Mountain View, CA",
    "formatted_address": "1600 Amphitheatre Parkway, Mountain View, CA 94043, USA",
    "latitude": 37.4224764,
    "longitude": -122.0842499
}
```

### Reverse Geo Code
**Endpoint:** `POST /api/locations/reverse_geocode/`

#### Implementation:
#### Serializer: CoorsLocationRequest
- The create method of the serializer fetches data from the Google Maps API and creates a LocationRequest object if it doesn't exist.
- Validates and stores the coordinates and their corresponding address, and formatted address.

#### Example Request:
```json
{
    "latitude_input": 37.422476,
    "longitude_input": -122.084249
}
```
#### Example Response:

```json
{
    "id": 1,
    "address": "1600 Amphitheatre Parkway, Mountain View, CA",
    "formatted_address": "1600 Amphitheatre Parkway, Mountain View, CA 94043, USA",
    "latitude": 37.422476,
    "longitude": -122.084249
}
```

### Calculate Distance
**Endpoint:** `POST /api/locations/calculate_distance/`

#### Implementation:
#### Serializer: DistanceLocationRequestSerializer
- The create method fetches source and destination locations, calculates the distance using the haversine function, and returns the distance in kilometers.

#### Example Request:
```json
{
    "from_address": "1600 Amphitheatre Parkway, Mountain View, CA",
    "to_address": "1 Infinite Loop, Cupertino, CA"
}
```

#### Example Response:
```json
{
    "from_address": "Amphitheatre Parkway",
    "to_address": "Cupertino",
    "distance": "12.04 KM"
}
```
