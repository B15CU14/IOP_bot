import requests
class database_connector:
    def __init__(self):
    # attritutes

    def get_data(self,api_endpoint, sn):
    #send API to IOP database
    response= requests.get(url= f'{api_endpoint}’, params ={“***”:f”{sn}”})
    response.raise_for_status()
    data = response.json()
    return data


    def get_target(self):
    # further get into json data to get the "target_line_ID" and "hospital_name"
    # return target_line_id, hospital name


