database = [{'sn':'SN68-00001', 'hos':'Hospital A', 'dr':"Dr. Teddy", 'hosID': '1111', 'drID':'U1'},
            {'sn':'SN68-00002', 'hos':'Hospital B', 'dr':"Dr. Lulu",'hosID': '2222', 'drID':'U2'},
            {'sn':'SN68-00003', 'hos':'Hospital C', 'dr':"Dr. Jingles",'hosID': '3333', 'drID':'U3'},
            {'sn':'SN68-00004', 'hos':'Hospital D', 'dr':"Dr. Biscuit",'hosID': '4444', 'drID':'U4'},
            ]

import requests
class DATABASECONNECTOR:
    # def get_data(self,api_endpoint, sn):
    # #send API to IOP database
    # response= requests.get(url= f'{api_endpoint}’, params ={“***”:f”{sn}”})
    # response.raise_for_status()
    # data = response.json()
    # return data
    #
    #
    # def get_target(self):
    # # further get into json data to get the "target_line_ID" and "hospital_name"
    # # return target_line_id, hospital name

    def work(self,sn):
        # check if data format is correct?
        if len(sn) < 10:
            return "Error: SN not correct format"
        else:
            return self.get_data(sn)

    def get_data(self,sn):
        # get data from database
        entry = next((item for item in database if item['sn'] == sn), "NO record found")
        return {
            'hos': entry['hos'],
            'dr': entry['dr'],
            'hosID': entry['hosID'],
            'drID': entry['drID']
        }
        # Returns dictionary