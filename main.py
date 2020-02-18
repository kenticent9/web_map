"""Creates a map of at most 10 nearest to given coordinates movie locations
in html format. More details at

P.S. Please, treat the module with respect and do not enter invalid data (e.g.,
300 years BC, international waters)."""
import folium
import pycountry
from haversine import haversine
from opencage.geocoder import OpenCageGeocode

key = '952ba00d94cd46a588b58f0c664a940e'
geocoder = OpenCageGeocode(key)


def get_country(latitude: float, longitude: float) -> str:
    """Returns the country within which the coordinates are specified.

    >>> get_country(49.83826, 24.02324)
    'Ukraine'
    >>> get_country(-19.468857, 29.797749)
    'Zimbabwe'
    """
    country = geocoder.reverse_geocode(latitude, longitude)[0]['components'][
        'country']
    return country


def read_file(file_name: str, given_year: str, country: str) -> list:
    """Returns a list of tuples extracted from file in the (title, year,
    latitude, longitude) format after applying year and country filters.

    P.S. This function is only configured to work with locations.list file.
    """
    locations = []
    passed_titles = set()
    passed_locations = set()
    with open(file_name) as f:
        lines = f.readlines()
        for line in lines[14:-1]:

            # Deletes episode name if present
            if '{' in line:
                line = line[:line.find('{') - 1] + line[line.find('}') + 1:]

            line = line.strip().split(' (')

            title = line[0]
            if title.startswith('"') and title.endswith('"'):
                title = title[1:-1]

            line = line[1].split('\t')

            year = line[0][:-1]

            location = ' '.join(i for i in line[1:] if i != '')

            # Applies year and country filters
            if country == "United States of America":
                country = "USA"
            if country == "United Kingdom":
                country = "UK"
            try:
                if title not in passed_titles and location not in \
                        passed_locations and year == given_year and country \
                        in location:
                    results = geocoder.geocode(location)[0]['geometry']

                    locations.append(
                        (title, year, results['lat'], results['lng']))
                    passed_titles.add(title)
                    passed_locations.add(location)
                    if len(locations) > 42:
                        break  # Limits the number of coordinates to work
                        # with for better performance
            except:
                pass

        return locations


def create_map(movies: list, country: str, year: str,
               given_location: tuple) -> None:
    """Creates a map of at most 10 nearest to given coordinates movie
    locations in html format."""
    my_map = folium.Map(location=given_location, zoom_start=7)

    # Creates markers of nearest to the given location movies
    fg_nr = folium.FeatureGroup(name="Nearest Movies")
    fg_nr.add_child(folium.Marker(location=given_location,
                                  popup=given_location,
                                  icon=folium.Icon(color='red')))
    for title, year, lt, ln in movies:
        fg_nr.add_child(folium.Marker(location=(lt, ln),
                                      popup=title + f" ({year})"))
        fg_nr.add_child(folium.PolyLine(locations=[given_location, (lt, ln)],
                                        color='blue',
                                        tooltip=haversine(given_location,
                                                          (lt, ln))))

    # Outlines given country
    fg_gc = folium.FeatureGroup(name="Given Country")
    fg_gc.add_child(folium.GeoJson(
        data=open('world.json', 'r', encoding='utf-8-sig').read(),
        style_function=lambda x: {
            'fillColor': 'blue' if x['properties']['ISO2'] ==
                                   pycountry.countries.search_fuzzy(country)[
                                       0].alpha_2 else 'None',
            'color': 'blue' if x['properties']['ISO2'] ==
                               pycountry.countries.search_fuzzy(country)[
                                   0].alpha_2 else 'None'}))

    # Adds layers and interface element to hide and show them
    my_map.add_child(fg_gc)
    my_map.add_child(fg_nr)
    my_map.add_child(folium.LayerControl())

    # Saves map
    my_map.save(f'{year}_movies_map.html')


if __name__ == '__main__':
    given_year = input(
        "Please enter a year you would like to have a map for: ")
    given_location = tuple(map(float, input(
        "Please enter your location (format: lat, long): ").split(', ')))
    print("Initializing map creation process. Estimated time to complete is "
          "2-3 minutes.")

    given_latitude, given_longitude = given_location
    given_country = get_country(given_latitude, given_longitude)

    print("Reading file...")
    suitable_locations = read_file('locations.list', given_year, given_country)

    suitable_locations.sort(
        key=lambda x: haversine((x[2], x[3]), given_location))

    print("Creating map...")
    create_map(suitable_locations[:10], given_country, given_year,
               given_location)
    print("Your map is ready.")
