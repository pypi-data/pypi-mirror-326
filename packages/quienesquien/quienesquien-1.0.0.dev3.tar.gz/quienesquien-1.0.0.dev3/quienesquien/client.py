from dataclasses import dataclass
from typing import TypedDict

import requests

from .person import PERSON_FIELDNAMES, Person


class SearchResult(TypedDict):
    resumen: dict[str, int | bool]
    persons: list[Person]


@dataclass
class Client:
    base_url: str
    username: str
    client_id: str
    secret_key: str
    percent: int = 80

    def _fetch_auth_token(self) -> str:
        """Retrieve authentication token from the API."""
        auth_url = f'{self.base_url}/api/token?client_id={self.client_id}'
        headers = {'Authorization': f'Bearer {self.secret_key}'}

        response = requests.get(auth_url, headers=headers)
        response.raise_for_status()

        return response.text

    def search(self, nombre: str, paterno: str, materno: str) -> SearchResult:
        """Perform a search request and return the results."""
        token = self._fetch_auth_token()

        search_url = (
            f'{self.base_url}/api/find?client_id={self.client_id}'
            f'&username={self.username}&percent={self.percent}'
            f'&name={nombre} {paterno} {materno}'
        )

        headers = {'Authorization': f'Bearer {token}'}
        response = requests.get(search_url, headers=headers)
        response.raise_for_status()

        response_data = response.json()
        matched_persons = []

        for person_data in response_data.get('data', []):
            person_attributes = {
                field: person_data.get(field.upper())
                for field in PERSON_FIELDNAMES
                if person_data.get(field.upper()) is not None
            }
            matched_persons.append(Person(person_attributes))

        result: SearchResult = {
            'resumen': {
                'success': response_data['success'],
                'num_registros': len(matched_persons),
            },
            'persons': matched_persons,
        }

        return result
