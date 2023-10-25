import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt

from classes.city import City

air_pollution_dict = {
    "pm10": {
        "very good": [0, 10, 20],
        "good": [20, 35, 50],
        "moderate": [50, 65, 80],
        "sufficient": [80, 95, 110],
        "bad": [110, 130, 150],
        "very bad": [150, 150, 600],
    },
    "pm25": {
        "very good": [0, 6.5, 13],
        "good": [13, 24, 35],
        "moderate": [35, 45, 55],
        "sufficient": [55, 65, 75],
        "bad": [75, 92.5, 110],
        "very bad": [110, 110, 600],
    },
    "o3": {
        "very good": [0, 35, 70],
        "good": [70, 95, 120],
        "moderate": [120, 135, 150],
        "sufficient": [150, 165, 180],
        "bad": [180, 210, 240],
        "very bad": [240, 240, 600],
        "index": 0,
    },
    "no2": {
        "very good": [0, 20, 40],
        "good": [40, 70, 100],
        "moderate": [100, 125, 150],
        "sufficient": [150, 190, 230],
        "bad": [230, 315, 400],
        "very bad": [400, 400, 600],
        "index": 1,
    },
    "so2": {
        "very good": [0, 25, 50],
        "good": [50, 75, 100],
        "moderate": [100, 150, 200],
        "sufficient": [200, 275, 350],
        "bad": [350, 425, 500],
        "very bad": [500, 500, 600],
    },
}


class CityAirQuality:
    """
    Parameters
    ----------
    city: city - Created a city according to the City class

    Variables
    ---------
    antecedents: dict - Dict of antecedents for each air particle
    mixture_of_air_particles: dict - Dict of air particle compartments
    air_quality_levels: array - Array of air quality levels
    air_quality_levels_range: list - List of ranges for each air quality level
    air_quality: ctrl.Consequent - Consequent for air quality / (output/control) variable for a fuzzy control system
    """

    def __init__(self, city: City):
        self.__city = city
        self.__antecedents = {}
        self.__mixture_of_air_particles = {
            "pm10": [0, 250],
            "pm25": [0, 200],
            "o3": [0, 340],
            "no2": [0, 500],
            "so2": [0, 600],
        }
        self.__air_quality_levels_range = [
            [0, 50, 100],
            [100, 150, 200],
            [200, 250, 300],
            [300, 350, 400],
            [400, 450, 500],
            [500, 550, 600],
        ]
        self.__air_quality_levels = [
            "very good",
            "good",
            "moderate",
            "sufficient",
            "bad",
            "very bad",
        ]
        self.__air_quality = ctrl.Consequent(np.arange(0, 601, 1), "air_quality")
        self.initialise()

    def _create_antecedent(self, param_name: str, universe_range: np.arange):
        """
        Sets antecedent for air particle

        Parameters
        ----------
        param_name: str - name of variable / air particle
        universe_range: np.arange - compartments for air particle
        """
        self.__antecedents[param_name] = ctrl.Antecedent(universe_range, param_name)

    def _setup(self):
        """
        Creates whole setup for fuzzy logic, create antecedent and sets
                    compartments for each air particle
        """

        for param_name, range_values in self.__mixture_of_air_particles.items():
            self._create_antecedent(
                param_name, np.arange(range_values[0], range_values[1] + 1, 1)
            )

        for key in self.__mixture_of_air_particles.keys():
            for aql in self.__air_quality_levels:
                self.__antecedents[key][aql] = fuzz.trimf(
                    self.__antecedents[key].universe, air_pollution_dict[key][aql]
                )

    def _get_air_quality(self, result: float) -> str:
        """
        Returns air quality

        Parameters
        ----------
        result: float - End result of evaluate air quality

        Returns
        -------
        level: string - city air quality result
        """

        for (low, mid, high), level in zip(
            self.__air_quality_levels_range, self.__air_quality_levels
        ):
            if low < result and high >= result:
                return level

    def _create_a_range_for_air_quality(self):
        """
        Creates range for air quality for each air quality level
        """
        for param, level in zip(
            self.__air_quality_levels_range, self.__air_quality_levels
        ):
            self.__air_quality[level] = fuzz.trimf(self.__air_quality.universe, param)

    def _get_particles_from_quality_with_or(self, quality: str):
        return (
            self.__antecedents["pm10"][quality]
            | self.__antecedents["pm25"][quality]
            | self.__antecedents["o3"][quality]
            | self.__antecedents["no2"][quality]
            | self.__antecedents["so2"][quality]
        )

    def _get_particles_from_quality_with_and(self, quality: str):
        return (
            self.__antecedents["pm10"][quality]
            & self.__antecedents["pm25"][quality]
            & self.__antecedents["o3"][quality]
            & self.__antecedents["no2"][quality]
            & self.__antecedents["so2"][quality]
        )

    def _evaluate_air_quality(self):
        """
        Creates rules for each antecedent and compartments, and shows
                air quality for the city
        """
        self._create_a_range_for_air_quality()

        rules = []
        for aql in self.__air_quality_levels:
            if aql == "very good":
                rules.append(
                    ctrl.Rule(
                        self._get_particles_from_quality_with_and(aql),
                        self.__air_quality[aql],
                    )
                )
            else:
                rules.append(
                    ctrl.Rule(
                        self._get_particles_from_quality_with_or(aql),
                        self.__air_quality[aql],
                    )
                )

        result_ctrl = ctrl.ControlSystem(rules)
        result = ctrl.ControlSystemSimulation(result_ctrl)
        for k in self.__mixture_of_air_particles.keys():
            result.input[k] = self.__city.to_dict()[k]

        result.compute()
        self.__air_quality.view(sim=result)

        air_quality = self._get_air_quality(result.output["air_quality"])
        print(f"result: {result.output['air_quality']}")
        print(f"{self.__city.name} has '{air_quality}' air quality")

    def show(self):
        """
        Shows all antecedents
        """
        for param_name, antecedent in self.__antecedents.items():
            antecedent.view()

        plt.show()

    def initialise(self):
        """
        Initialise fuzzy logic and check air quality for the city
        """
        self._setup()
        self._evaluate_air_quality()
