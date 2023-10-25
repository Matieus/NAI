import requests


GIOS_ENDPOINTS = {
	"all": "https://api.gios.gov.pl/pjp-api/rest/station/findAll",
	"index": "https://api.gios.gov.pl/pjp-api/rest/station/sensors",
	"air_particles": 'https://api.gios.gov.pl/pjp-api/rest/data/getData'
}


def create_dict_for_city(
	name: str,
	pm10: float,
	pm25: float,
	o3: float,
	no2: float,
	so2: float
) -> dict:
	"""
	Parameters
	----------
	name: str - name of the city
	pm10, pm25, o3, no2, so2: float - air particles mixture, cannot be set to 0 because the algorithm has set errors

	Returns
	-------
	city_dict: dict - ready dict to create custom city
	"""
	return {
		"name": name,
		"pm10": pm10,
		"pm25": pm25,
		"o3": o3,
		"no2": no2,
		"so2": so2
	}


class City:
	"""
	Parameters
	----------
	get_data_from_api: bool - should get data from api or not
	city_index: int - index of the city in the array, needed only if get_data_from_api is true
	name: str - name of the city
	pm10, pm25, o3, no2, so2: float - air particles mixture, cannot be set to 0.0 because the algorithm has set errors
																						of 0 or empty value
	"""
	def __init__(self, get_data_from_api: bool = False, city_index: int = 1):
		self.__get_data_from_api = get_data_from_api
		self.__city_index = city_index
		self.name = 'Test'
		self.pm10 = 0.1
		self.pm25 = 0.1
		self.o3 = 0.1
		self.no2 = 0.1
		self.so2 = 0.1

	def _set_city_value(
		self,
		key: str,
		value: [float, str]
	):
		"""
		Sets new values for the city

		Parameters
		----------
		key: str - attribute name
		value: float, str - attribute value
		"""
		setattr(self, key, value)

	def _get_all_cities(self):
		"""
		Gets all cities from api and select one from passed city_index
		"""
		try:
			r = requests.get(GIOS_ENDPOINTS['all'])
			data = r.json()

			index = None

			# This is only
			# for test to find and test each air quality

			# print("CITIES\n", data)
			# for i, item in enumerate(data):
			# 	if item['id'] == 740:
			# 		index = i
			# 		break
			#
			# print(f"INDEX {index}")

			if not index:
				index = self.__city_index
			city = data[index]
			self._set_city_value('name', city['city']['name'])
			print(f"Testing for {self.name}")

			self._get_city_data(city['id'])

		except Exception as e:
			print(f"Something went wrong: {str(e)}")

	def _get_city_data(self, id: int):
		"""
		Gets air particles mixture for selected city

		Parameters
		----------
		id: int - id of the selected city
		"""
		try:
			r = requests.get(
				f"{GIOS_ENDPOINTS['index']}/{id}"
			)
			data = r.json()

			for obj in data:
				self._get_air_particles(obj['id'])
		except Exception as e:
			print(f"Something went wrong: {str(e)}")

	def _get_air_particles(self, id: int):
		"""
		Gets the latest value of particle

		Parameters
		----------
		id: int - id of the selected city
		"""
		try:
			r = requests.get(
				f"{GIOS_ENDPOINTS['air_particles']}/{id}"
			)
			data = r.json()
			print('data', data)
			latest_value = data['values'][0]['value']
			if latest_value is None:
				index = 1
				while latest_value is None:
					latest_value = data['values'][index]['value']
					index += 1

			key = data['key'].lower()
			if key == 'pm2.5':
				key = 'pm25'

			self._set_city_value(
				key=key,
				value=latest_value
			)
		except Exception as e:
			print(f"Something went wrong: {str(e)}")

	def _get_data_from_api(self):
		self._get_all_cities()

	def _create_custom_city(self, dict_of_values: dict):
		"""
		Sets values for the city from passed dict

		Parameters
		----------
		dict_of_values: dict - dict of the city keys and values
		"""
		city_keys = ["name", "pm10", "pm25", "o3", "no2", "so2"]
		for city_key in city_keys:
			if city_key in dict_of_values.keys():
				if city_key == 'name':
					self.name = dict_of_values['name']
				else:
					self._set_city_value(
						key=city_key, value=float(dict_of_values[city_key])
					)

	def initialise(self, dict_of_values: dict = None):
		"""
		Initialise gets data from api for create city from dict
		Parameters
		----------
		dict_of_values: dict - dict of the city keys and values
		"""

		if self.__get_data_from_api:
			self._get_data_from_api()
		elif not self.__get_data_from_api and dict_of_values is not None:
			self._create_custom_city(dict_of_values)
		else:
			print("Nothing happened")

	def to_dict(self) -> dict:

		"""
		Returns city as a dict

		Returns
		----------
		returns city as dict
		"""
		return {
			"name": self.name,
			"pm10": self.pm10,
			"pm25": self.pm25,
			"o3": self.o3,
			"no2": self.no2,
			"so2": self.so2
		}

	def show(self):
		"""
		Shows city values
		"""
		print(self.to_dict())
