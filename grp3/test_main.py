import unittest
from unittest.mock import MagicMock, patch

from main import backend_selection


class TestMain(unittest.TestCase):  # Erbt von unittest.TestCase
    """
    Unit tests for the backend selection functionality in the main module.
    Test Cases:
        - test_backend_selection_local: Tests the backend selection for local data retrieval.
        - test_backend_selection_webapp: Tests the backend selection for webapp data retrieval.
        - test_backend_selection_webservice_http: Tests the backend selection for webservice HTTP data retrieval.
        - test_backend_selection_mqtt: Tests the backend selection for MQTT data retrieval.
    Each test case uses the unittest.mock.patch to mock the respective functions and verifies that they are called with the expected arguments.

    --- The further comments in this class are in German for better understanding ---
    """

    def test_backend_selection_local(self):
        with (  # Sicherstellen, dass die Funktionen get_local_data und show_routes nur temporär gepatcht gehalten werden
            patch(
                "main.local.get_local_data"
            ) as mock_get_local_data,  # Mocken (Platzhalter) der Funktion get_local_data
            patch(
                "main.routes.show_routes"
            ) as mock_show_routes,  # Mocken (Platzhalter) der Funktion show_routes
        ):
            mock_get_local_data.return_value = [
                "data1",
                "data2",
            ]  # Rückgabewert der Funktion get_local_data festlegen
            backend_selection(
                1, path="dummy_path"
            )  # Funktion backend_selection mit Backend 1 und Pfad "dummy_path" aufrufen
            mock_get_local_data.assert_called_once_with(
                "dummy_path"
            )  # Sicherstellen, dass die Funktion get_local_data 1x mit dem Pfad "dummy_path" aufgerufen wurde
            mock_show_routes.assert_called_once_with(
                ["data1", "data2"]
            )  # Sicherstellen, dass die Funktion show_routes 1x mit den Daten ["data1", "data2"] aufgerufen wurde

    def test_backend_selection_webapp(self):
        with (
            patch("main.webapp.fetch_webapp") as mock_fetch_webapp,
            patch("main.routes.show_routes") as mock_show_routes,
        ):
            mock_fetch_webapp.return_value = ["data1", "data2"]
            backend_selection(2)
            mock_fetch_webapp.assert_called_once()
            mock_show_routes.assert_called_once_with(["data1", "data2"])

    def test_backend_selection_webservice_http(self):
        with (
            patch(
                "main.webservice_http.fetch_webservice_http"
            ) as mock_fetch_webservice_http,
            patch("main.routes.show_routes") as mock_show_routes,
        ):
            mock_fetch_webservice_http.return_value = ["data1", "data2"]
            backend_selection(3, container_id="container1", route_id="route1")
            mock_fetch_webservice_http.assert_called_once_with("container1", "route1")
            mock_show_routes.assert_called_once_with(["data1", "data2"])

    def test_backend_selection_mqtt(self):
        with (
            patch("main.mqtt.mqtt_func") as mock_mqtt_func,
            patch("main.mqtt.stop_event") as mock_stop_event,
        ):
            mock_stop_event.set = MagicMock()
            backend_selection(4)
            mock_mqtt_func.assert_called_once()

    def test_backend_selection_invalid_backend(self):
        with (
            self.assertRaises(ValueError) as context
        ):  # Überprüft, ob eine ValueError-Ausnahme mit der richtigen Nachricht ausgelöst wird
            backend_selection(5)  # Ungültiger Backend-Typ

        self.assertEqual(
            str(context.exception), "Invalid backend type. Please select 1, 2, 3, or 4."
        )  # Überprüfen, ob die richtige Fehlermeldung ausgelöst wurde


if __name__ == "__main__":
    unittest.main()
