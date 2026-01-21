database = [{'sn':'SN68-00001', 'hos':'Hospital A', 'dr':"Dr. Teddy"},
            {'sn':'SN68-00002', 'hos':'Hospital B', 'dr':"Dr. Lulu"},
            {'sn':'SN68-00003', 'hos':'Hospital C', 'dr':"Dr. Jingles"},
            {'sn':'SN68-00004', 'hos':'Hospital D', 'dr':"Dr. Biscuit"},
            ]

input = input("Input: ")
for_search = input[0:11]
request = input[11:]

target_hos = [entry['hos'] for entry in database if entry['sn'] == for_search]
print(f'{request}')


if target_hos:
    print(f'from {target_hos}')
else:
    print('Wrong input style')