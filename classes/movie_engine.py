import os
import json
import numpy as np


class MovieEngine:
    def __init__(
        self,
        user_fullname: str,
        movie_rec_number: int,
        neighbors_number: int,
        metric_method: str = "pearson",
    ):
        """
        Parameters
        ----------
        user_fullname: str - Fullname of user
        movie_rec_number: int - Number of shows recommended and not recommended movies
        neighbors_number: int - To takes the best passed number neighbors
        metric_method: str - Chosen metric method
        """
        self.__user_fullname = user_fullname
        self.__movie_rec_number = movie_rec_number
        self.__metric_method = metric_method
        self.__neighbors_number = neighbors_number
        self.__data = self._read_json() or []
        self.__functions = {
            "pearson": self._pearson_score,
            "euclidean": self._euclidean_distance,
        }

    def _read_json(self):
        """
        Reads json data and returns them

        Returns
        -------
        data: dict - Dict of data
        """
        here = os.getcwd()
        json_data = os.path.join(here, "data", "movie_data.json")

        if not os.path.exists(json_data):
            raise Exception("The json data not exists")

        with open(json_data, "r") as json_file:
            data = json.loads(json_file.read())

        return data

    def _pearson_score(self, neighbor):
        """
        Calculates distance using Pearson

        Parameters
        ----------
        neighbor: string - Name of the neighbor

        Returns
        -------
        score: float - Distance score
        """
        if neighbor not in self.__data.keys():
            raise Exception(f"Cannot find {neighbor} in the data")

        common_movies = {
            item: 1
            for item in self.__data[self.__user_fullname].keys()
            if item in self.__data[neighbor].keys()
        }

        num_ratings = len(common_movies)
        if num_ratings == 0:
            return 0

        selected_user_sum = np.sum(
            [self.__data[self.__user_fullname][item] for item in common_movies.keys()]
        )
        neighbor_sum = np.sum(
            [self.__data[neighbor][item] for item in common_movies.keys()]
        )

        selected_user_sqr_sum = np.sum(
            [
                np.square(self.__data[self.__user_fullname][item])
                for item in common_movies.keys()
            ]
        )
        neighbor_sqr_sum = np.sum(
            [np.square(self.__data[neighbor][item]) for item in common_movies.keys()]
        )

        sum_of_products = np.sum(
            [
                self.__data[self.__user_fullname][item]
                * self.__data[self.__user_fullname][item]
                for item in common_movies.keys()
            ]
        )

        Sxy = sum_of_products - (selected_user_sum * neighbor_sum / num_ratings)
        Sxx = selected_user_sqr_sum - np.square(selected_user_sum) / num_ratings
        Syy = neighbor_sqr_sum - np.square(neighbor_sum) / num_ratings

        # If there is no deviation, then the score is 0:
        if Sxx * Syy == 0:
            return 0

        return Sxy / np.sqrt(Sxx * Syy)

    def _euclidean_distance(self, neighbor):
        """
        Calculates distance using Euclidean

        Parameters
        ----------
        neighbor: string - Name of the neighbor

        Returns
        -------
        score: float - Distance score
        """
        if neighbor not in self.__data.keys():
            raise Exception(f"Cannot find {neighbor} in the data")

        common_movies = {
            item: 1
            for item in self.__data[self.__user_fullname].keys()
            if item in self.__data[neighbor].keys()
        }

        if not common_movies:
            return 0

        distances = np.array(
            [
                np.square(
                    self.__data[self.__user_fullname][item]
                    - self.__data[neighbor][item]
                )
                for item in common_movies.keys()
            ]
        )

        euclidean_distance = np.sqrt(np.sum(distances))
        return 1 / (1 + euclidean_distance)

    def _find_similar_users(self):
        """
        Finds best neighbors to selected user
        """
        num_users = len(self.__data.keys())
        if self.__user_fullname not in self.__data.keys():
            raise Exception(f"Cannot find {self.__user_fullname} in the data")
        scores = np.array(
            [
                [user, self.__functions[self.__metric_method](user)]
                for user in self.__data.keys()
                if user != self.__user_fullname
            ]
        )
        scores_sorted = np.argsort(scores[:, 1])[::-1]
        top_users = scores_sorted[:num_users]

        similar_users = [scores[n] for n in top_users]
        self.__cor_users = [u[0] for u in similar_users]
        print("\nCorr result\n", similar_users)
        self.__cor_users = self.__cor_users[: self.__neighbors_number]
        print("\nChosen best 5 neighbors", self.__cor_users)

    def _get_recommendations(self):
        """
        Returns recommendations for selected user

        Returns
        -------
        movie_recommendations: list - List of recommended movie
        not_recommended_movies: list - List of not recommended movie
        """
        if self.__user_fullname not in self.__data.keys():
            raise Exception(f"Cannot find {self.__user_fullname} in the data")

        overall_scores = {}
        similarity_scores = {}

        for user in self.__cor_users:
            similarity_score = self.__functions[self.__metric_method](user)

            filtered_list = [
                x
                for x in self.__data[user].keys()
                if x not in self.__data[self.__user_fullname].keys()
                or self.__data[self.__user_fullname][x] == 0
            ]

            for item in filtered_list:
                overall_scores[item] = (
                    overall_scores.get(item, 0)
                    + self.__data[user][item] * similarity_score
                )
                similarity_scores[item] = (
                    similarity_scores.get(item, 0) + similarity_score
                )

        if not overall_scores:
            return [], []

        movie_scores = np.array(
            [
                [
                    overall_score / similarity_scores[item]
                    if similarity_scores[item] != 0
                    else 0,
                    item,
                ]
                for item, overall_score in overall_scores.items()
            ]
        )

        movie_scores = movie_scores[np.argsort(movie_scores[:, 0].astype(float))[::-1]]
        movie_recommendations = [movie for _, movie in movie_scores]

        movie_scores = movie_scores[np.argsort(movie_scores[:, 0].astype(float))]
        not_recommended_movies = [movie for _, movie in movie_scores]

        return (
            movie_recommendations[: self.__movie_rec_number],
            not_recommended_movies[: self.__movie_rec_number],
        )

    def recommendations(self):
        """
        Inits finds similar users and get recommendations
        """
        if self.__user_fullname not in self.__data.keys():
            raise Exception(f"Cannot find {self.__user_fullname} in the data")

        self._find_similar_users()
        recommended_movies, not_recommended_movies = self._get_recommendations()

        print(f"\nMovie recommended for {self.__user_fullname}:")
        for i, movie in enumerate(recommended_movies):
            print(f"{str(i + 1)}. {movie}")

        print(f"\nMovies not recommended for {self.__user_fullname}:")
        for i, movie in enumerate(not_recommended_movies):
            print(f"{str(i + 1)}. {movie}")
