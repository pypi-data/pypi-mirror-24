#! /usr/bin/python3
import logging
import json
import sys
import googlemaps
from functools import singledispatch

# Package imports from local PIP
from magen_logger.logger_config import LogDefaults

__author__ = "repennor@cisco.com"
__copyright__ = "Copyright(c) 2016, Cisco Systems, Inc."
__version__ = "0.1"
__status__ = "alpha"


class GeocodeApis(object):
    gmaps = googlemaps.Client(key='AIzaSyAgeBEokKn7MT8CDc3u_e36dR0Y-fZnsTk')

    logger = logging.getLogger(LogDefaults.default_log_name)

    @singledispatch
    def create_geofence_configuration(e):
        """

        """
        GeocodeApis.logger.error('Unexpected Error. Error: %s', sys.exc_info()[0])
        return None

    @create_geofence_configuration.register(str)
    def _(geofence_address):
        geocode_result = GeocodeApis.gmaps.geocode(geofence_address)
        applied_config = GeocodeApis.process_geocode_info(geocode_result)
        return applied_config, geocode_result

    @create_geofence_configuration.register(tuple)
    def _(latlng):
        reverse_geocode_result = GeocodeApis.gmaps.reverse_geocode(latlng)
        applied_config = GeocodeApis.process_reverse_geocode_info(reverse_geocode_result)
        return applied_config, reverse_geocode_result

    # @staticmethod
    # def create_geofence_configuration(geofence_address):
    #     geocode_result = GeocodeApis.gmaps.geocode(geofence_address)
    #     applied_config = GeocodeApis.process_geocode_info(geocode_result)
    #     return applied_config, geocode_result
    #
    # @staticmethod
    # def create_geofence_configuration(lat, lng):
    #     reverse_geocode_result = GeocodeApis.gmaps.reverse_geocode((lat, lng))
    #     applied_config = GeocodeApis.process_reverse_geocode_info(reverse_geocode_result)
    #     return applied_config, reverse_geocode_result

    @staticmethod
    def process_geocode_info(geocode_result):
        try:
            applied_config = dict()
            applied_config["address"] = geocode_result[0]["formatted_address"]
            applied_config["lat"] = geocode_result[0]['geometry']['location']['lat']
            applied_config["lng"] = geocode_result[0]['geometry']['location']['lng']
            applied_config["location_type"] = geocode_result[0]['geometry']["location_type"]
            applied_config["types"] = geocode_result[0]['address_components'][0]['types']
            applied_config["long_name"] = geocode_result[0]['address_components'][0]['long_name']
            applied_config["short_name"] = geocode_result[0]['address_components'][0]['short_name']
            applied_config["place_id"] = geocode_result[0]["place_id"]
            return applied_config
        except KeyError as e:
            GeocodeApis.logger.error("Geocode Error: %s", str(e))
            return None

    @staticmethod
    def process_reverse_geocode_info(reverse_geocode_result):
        try:
            applied_config = dict()
            applied_config["address"] = reverse_geocode_result[0]["formatted_address"]
            applied_config["lat"] = reverse_geocode_result[0]['geometry']['location']['lat']
            applied_config["lng"] = reverse_geocode_result[0]['geometry']['location']['lng']
            applied_config["location_type"] = reverse_geocode_result[0]['geometry']["location_type"]
            applied_config["types"] = reverse_geocode_result[0]['address_components'][0]['types']
            applied_config["long_name"] = reverse_geocode_result[0]['address_components'][0]['long_name']
            applied_config["short_name"] = reverse_geocode_result[0]['address_components'][0]['short_name']
            applied_config["place_id"] = reverse_geocode_result[0]["place_id"]
            return applied_config
        except KeyError as e:
            GeocodeApis.logger.error("Reverse Geocode Error: %s", str(e))
            return None

    @staticmethod
    def find_gmaps_api_key():
        try:
            with open('google_maps_apis/gmaps_api_key.json') as f:
                config = json.load(f)
                key = config['key']
                if key:
                    return key
                else:
                    GeocodeApis.logger.error("No Gmaps API key found")
                    return None
        except KeyError as e:
            GeocodeApis.logger.error("find_gmaps_api_key Error: %s", str(e))
            return None


if __name__ == '__main__':
    a_game = GeocodeApis()
    a_game.run()
