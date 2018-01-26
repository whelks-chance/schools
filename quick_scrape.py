import json

import os
import requests


class QuickScrape():
    def __init__(self):
        self.school_data = None

    def prepare(self):

        # http://mylocalschool.wales.gov.uk/Data/schools.json?111111
        # http://mylocalschool.wales.gov.uk/schools.json?{}
        res = requests.get('http://mylocalschool.wales.gov.uk/Data/schools.json?111111')
        print('Retrieved school data')
        self.school_data = json.loads(res.text)
        print('Found {} schools ({} reported)'.format(len(self.school_data['schools']), len(self.school_data['schools'])))

    def get_school_data(self, limit=2, save_to_db=True):
        data = {}
        with open('temp.txt', 'a') as tmp_file:

            save_count = 0
            for school in self.school_data['schools'][:limit]:
                try:
                    school_code = school['schoolCode']
                    school_data_file = 'data/school_{}_data.json'.format(school_code)

                    if os.path.isfile(school_data_file):
                        print('found file ', school_data_file)
                        with open(school_data_file, 'r') as school_tmp_file:
                            school_detail = json.load(school_tmp_file)

                            print("read ", len(school_detail.keys()))
                    else:
                        res = requests.get(
                            'http://mylocalschool.wales.gov.uk/schools/{}.json?807022358'.format(school_code)
                        )
                        print('Retrieved school data for {}.'.format(school_code))
                        school_detail = json.loads(res.text)

                        with open(school_data_file, 'a') as school_tmp_file:
                            school_tmp_file.write(json.dumps(school_detail, indent=4))

                except Exception as e:
                    print('\n', 'err ***', '\n')
                    print(e, type(e), school)
                    print('\n', 'err ***', '\n')


if __name__ == "__main__":
    qs = QuickScrape()
    qs.prepare()
    qs.get_school_data(limit=2000)
