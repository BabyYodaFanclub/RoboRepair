import io
import json
from typing import List, Tuple


class Location:
    name: str
    available_items: List[str]
    connected_to: List[Tuple['Location', int]]

    def __init__(self, name, available_items, connected_to):
        self.name = name
        self.available_items = available_items
        self.connected_to = connected_to


class LocationStore:
    current: Location
    held_items: List[str]
    available_locations: List[Location]

    def __init__(self, start_location: Location, available_locations: List[Location]) -> None:
        self.current = start_location
        self.held_items = []
        self.available_locations = available_locations

    def move_to_location(self, location: Location):
        self.available_locations.remove(location)
        self.available_locations.append(self.current)
        self.current = location

    @staticmethod
    def from_location_file(file: str) -> 'LocationStore':
        location_file = io.open(file)
        loc_json = json.load(location_file)

        locations = [Location(location['name'],
                              location['available_items'],
                              location['connected_to'])
                     for location in loc_json]

        locations = [LocationStore.reference_correct_location(loc, locations) for loc in locations]

        return LocationStore(locations[0], locations[1:])

    @staticmethod
    def reference_correct_location(loc, locations) -> Location:
        for i in range(0, len(loc.connected_to)):
            connected_to_name = loc.connected_to[i][0]
            connection = [loc for loc in locations if loc.name == connected_to_name][0]
            loc.connected_to[i] = (connection, loc.connected_to[i][1])
        return loc

# store = LocationStore.from_location_file('./level2locations.json')
# print(store.current.name)
# store.move_to_location(store.current.connected_to[0][0])
# print(store.current.name)
