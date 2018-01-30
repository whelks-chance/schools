import os

import requests
from geojson import Point, Feature, FeatureCollection, dumps
import json
import csv
# import imp
# geojson = imp.load_source('geojson', '/home/ianh/venv/local/lib/python2.7/site-packages/geojson/__init__.py')
# foo.MyClass()


class SchoolGeo:
    def __init__(self, filepath='./data', slash = '/'):
        self.filepath = filepath
        self.slash = slash
        self.all_points = []
        self.filelist = []

        for root, dir, files in os.walk(self.filepath):
            for file in files:
                self.filelist.append(file)
        print(self.filelist)

    def geotag_school_to_geojson(self):
        # from school_meals.py import FreeSchoolMeals

        # school_data= FreeSchoolMeals.get_school_data()

        school_data= []
        res = requests.get('http://mylocalschool.wales.gov.uk/Data/schools.json?111111')
        print('Retrieved school data')
        all_school_data = json.loads(res.text)

        with open('Pioneer schools data - NN Jan 2017.csv') as csvfile:
            dialect = csv.Sniffer().sniff(csvfile.read(1024))
            csvfile.seek(0)
            print(dialect.__dict__)
            reader = csv.DictReader(csvfile, dialect=dialect)
            print(reader.fieldnames)
            for row in reader:
                print('\n', row['School name'], '#', row['Ref Number'])

                for school in all_school_data['schools']:
                    if int(school['schoolCode']) == int(row['Ref Number']):
                        print(school['lat'], school['lng'])

                        properties = {}
                        for field in reader.fieldnames:
                            properties[field] = row[field]
                        self.all_points.append(
                            Feature(
                                geometry=Point((school['lng'], school['lat'])),
                                properties=properties
                            )
                        )

        print(self.all_points)
        fc = FeatureCollection(self.all_points)
        print(dumps(fc))

        with open('schools_geo.json', 'w') as geo1:
            geo1.write(dumps(fc, indent=4))


# properties = {}
# properties['School name']
# properties['Postcode - space']
# properties['School Type Name']
# properties['School Type']
# properties['Became a Pioneer school']
# properties['Medium']
# properties['Percentage of students eligible for FSM ']
# properties['Number of students']
# properties['Support Category']
# properties['Expected outcome in the Foundation Phase areas of learning']
# properties['Expected level - Core subject indicator Key Stage 2']
# properties['% expected level - Core subject indicator (Key Stage 3)']
# properties['% Pupils achieving the level 2 threshold (Key Stage 4)']
# properties['Ref Number']
# properties['Region']

    def mylocalschool(self):

        for file in self.filelist:
            try:
                properties = {}

                fullfilepath = self.filepath + self.slash + file
                # with open(filepath+slash+file) as jsonfile:
                print (fullfilepath)
                with open(fullfilepath) as data:
                    json_data = json.loads(data.read())

                print('lat', json_data['lat'])
                print('lng', json_data['lon'])

                # print json.load(filepath+slash+file)
                json_lat = float(json_data['lat'])
                json_lng = float(json_data['lon'])
                json_schoolname = json_data['schName']
                json_schoolcode = json_data ['schoolCode']
                json_type = json_data ['schTypeEnglish']
                json_medium = json_data ['schLanguageEnglish']
                indicatorlist= json_data ['lstSubjectsIndicators']
                for i in indicatorlist:
                    if 'lstCharts' in i and len(i['lstCharts']):
                        print('\n\n', i, '\n\n')
                        lstseries = i['lstCharts'][0]['lstSeries']
                        for j in lstseries:
                            if j['subjectCode'] == 'FSM3' and j['nameEnglish'] == 'School':
                                json_fsmyear = j['years']
                                json_fsmdata = j['data']
                                print (json_fsmdata)
                                json_fsmdata = json_fsmdata[-1]
                                print (json_fsmdata)

                                properties['json_fsmyear'] = json_fsmyear
                                properties['json_fsmdata'] = json_fsmdata
                                properties['json_fsmdata'] = json_fsmdata
                                properties['json_schoolname'] = json_schoolname
                                properties['json_type'] = json_type
                                properties['json_medium'] = json_medium

                self.all_points.append(
                    Feature(
                        geometry=Point((json_lng, json_lat)),
                        properties=properties
                    )
                )
            except Exception as ex1:
                print(ex1)

        print(self.all_points)

        fc = FeatureCollection(self.all_points)
        print(dumps(fc))

        with open('schools_geo.json', 'w') as geo1:
            geo1.write(dumps(fc, indent=4))


if __name__ == "__main__":
    school_geo = SchoolGeo()
    school_geo.mylocalschool()
