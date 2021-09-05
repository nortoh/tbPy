import requests
import json
import logging

class TwitchAPI(object):

    def __init__(self, client_id, client_secret):
        self.__client_id__ = client_id
        self.__client_secret__ = client_secret
        self.__client_authenticated__ = False
        self.call_count = 0

        self.logger = logging.getLogger('main')

        self.grant_client_credientials()        

    def grant_client_credientials(self):
        self.logger.info(f'Authenticating with <{self.__client_id__}:{self.__client_secret__}>')

        endpoint = f'https://id.twitch.tv/oauth2/token?client_id={self.__client_id__}&client_secret={self.__client_secret__}&grant_type=client_credentials'
        response = requests.post(endpoint)
        self.call_count += 1

        if response.status_code == 200:
            response_json = json.loads(response.text)
            self.__access_token__ = response_json['access_token']
            self.logger.info(f'Acquired Access Token: {self.__access_token__}')
            self.__client_authenticated__ = True

    def search_channel(self, channel, value):

        # If user is not authenticated
        if not self.client_authenticated(): return

        channel = str.lower(channel)

        endpoint = f'https://api.twitch.tv/helix/search/channels?query={channel}'
        response = requests.get(endpoint, headers={'client-id': self.__client_id__, 'Authorization': f'Bearer {self.__access_token__}'})
        self.call_count += 1

        # If 200 response
        if response.status_code == 200:            
        
            # Get response as json
            response_json = json.loads(response.text)
            
            index = 0

            # Loop through response until channel is found
            for data in response_json['data']:
                display_name = str.lower(data['display_name'])

                # If channel equals parameter
                if channel == display_name:
                    
                    # If a value is provided
                    if value is not None:
                        
                        # If we are requesting everything
                        if value == 'all':
                            return response_json['data'][index]

                        # We are requesting a specific value
                        result = response_json['data'][index][value]

                    return result
                
                index += 1
    
        # Return nothing if we found nothing
        return None

    def get_follower_count(self, channel_id):

        # If user is not authenticated
        if not self.client_authenticated(): return        

        endpoint = f'https://api.twitch.tv/helix/users/follows?from_id={channel_id}&first=1'
        response = requests.get(endpoint, headers={'client-id': self.__client_id__, 'Authorization': f'Bearer {self.__access_token__}'})
        self.call_count += 1

        # If 200 response
        if response.status_code == 200:
            # Get response as json
            response_json = json.loads(response.text)

            return response_json['total']

        return -1


    def search_game(self, game_id):
        
        # If user is not authenticated
        if not self.client_authenticated(): return
        
        endpoint = f'https://api.twitch.tv/helix/games?id={game_id}'
        response = requests.get(endpoint, headers={'client-id': self.__client_id__, 'Authorization': f'Bearer {self.__access_token__}'})
        self.call_count += 1

        # If 200 response
        if response.status_code == 200:
            # Get response as json
            response_json = json.loads(response.text)

            return response_json

    def client_id(self):
        return self.__client_id__
    
    def client_secret(self):
        return self.__client_secret__

    def client_authenticated(self):
        return self.__client_authenticated__

    