"""
Authors:
    Jakub Żurawski: https://github.com/s23047-jz/NAI/tree/air-pollution
    Mateusz Olstowski: https://github.com/Matieus/NAI/tree/air-pollution

used api: https://powietrze.gios.gov.pl/pjp/current#

Conclusions:
(Jakub)
    The first problem I encountered was that air molecules cannot have a value of 0.0.
    Must be at least 0.1, otherwise the algorithm sets errors.

    Unfortunately the API was not conducive to the topic of fuzzy logic.
    You need to make a result for each air particle and then check the air quality.

    The worst idea, but still accepted, was to create rules for every possible scheme.
    But I decided to do it in another way
"""

from classes.air_pollution import CityAirQuality
from classes.city import City, create_dict_for_city


def main():
    city = City(get_data_from_api=True, city_index=0)
    city.initialise()
    # city = City()
    # city.initialise(create_dict_for_city(
    #     name="Test",
    #     pm10=1.0,
    #     pm25=1.0,
    #     o3=1.0,
    #     no2=1.0,
    #     so2=1.0
    # ))
    city.show()
    city_air_pollution = CityAirQuality(city=city)
    city_air_pollution.show()


if __name__ == "__main__":
    main()
