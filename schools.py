# coding=utf-8
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
        self.all_points2 = []
        self.filelist = []
        self.pioneer_school_codes = {}

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

                        self.pioneer_school_codes[int(row['Ref Number'])] = properties

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

                    if int(json_data['schoolCode']) in self.pioneer_school_codes:
                        print('This is a pioneer school.')
                        # properties['pioneer_̣school'] = 'True'
                        # properties['display_icon'] = 'fa graduation-cap'

                        print('lat', json_data['lat'])
                        print('lng', json_data['lon'])

                        # print json.load(filepath+slash+file)
                        json_lat = float(json_data['lat'])
                        json_lng = float(json_data['lon'])
                        json_schoolname = json_data['schName']
                        json_schoolcode = json_data['schoolCode']
                        json_type = json_data['schTypeEnglish']
                        json_medium = json_data['schLanguageEnglish']
                        indicatorlist = json_data['lstSubjectsIndicators']
                        for i in indicatorlist:
                            if 'lstCharts' in i and len(i['lstCharts']):
                                print('\n\n', i, '\n\n')
                                lstseries = i['lstCharts'][0]['lstSeries']
                                for j in lstseries:
                                    if j['subjectCode'] == 'FSM3' and j['nameEnglish'] == 'School':
                                        json_fsmyear = j['years']
                                        json_fsmdata = j['data']
                                        # print (json_fsmdata)
                                        json_fsmdata = json_fsmdata[-1]
                                        # print (json_fsmdata)

                                        properties['json_fsmyear'] = json_fsmyear
                                        properties['json_fsmdata'] = json_fsmdata
                                        properties['json_fsmdata'] = json_fsmdata
                                        properties['json_schoolname'] = json_schoolname
                                        properties['json_type'] = json_type
                                        properties['json_medium'] = json_medium

                        if json_data['schTypeEnglish'] == 'Nursery, Infants & Juniors':
                            properties['point_icon'] = 'fa-users'
                        elif json_data['schTypeEnglish'] == 'Infants & Juniors':
                            properties['point_icon'] = 'fa-child'
                        elif json_data['schTypeEnglish'] == 'Secondary (ages 11-16)':
                            properties['point_icon'] = 'fa-bank'
                        elif json_data['schTypeEnglish'] == 'Juniors':
                            properties['point_icon'] = 'fa-user'
                        elif json_data['schTypeEnglish'] == 'Nursery & Infants':
                            properties['point_icon'] = 'fa-graduation-cap'
                        elif json_data['schTypeEnglish'] == 'Middle (ages 3-16)':
                            properties['point_icon'] = 'fa-mortar-board'
                        elif json_data['schTypeEnglish'] == 'Middle (ages 3-19)':
                            properties['point_icon'] = 'fa-institution'
                        elif json_data['schTypeEnglish'] == 'Secondary (ages 11-19)':
                            properties['point_icon'] = 'fa-male'
                        elif json_data['schTypeEnglish'] == 'Special (with post-16 provision)':
                            properties['point_icon'] = 'fa-building'
                        elif json_data['schTypeEnglish'] == 'Special (without post-16 provision)':
                            properties['point_icon'] = 'fa-building-o'

                        if json_data['schLanguageEnglish'] == 'Welsh medium':
                            properties['point_icon_colour'] = 'black'
                            properties['point_icon_bgcolour'] = 'green'
                        elif json_data['schLanguageEnglish'] == 'English medium':
                            properties['point_icon_colour'] = 'white'
                            properties['point_icon_bgcolour'] = 'red'
                        elif json_data['schLanguageEnglish'] == 'Bilingual (Type A)':
                            properties['point_icon_colour'] = 'purple'
                            properties['point_icon_bgcolour'] = 'yellow'
                        elif json_data['schLanguageEnglish'] == 'Bilingual (Type B)':
                            properties['point_icon_colour'] = 'orange'
                            properties['point_icon_bgcolour'] = 'darkblue'
                        elif json_data['schLanguageEnglish'] == 'English with significant Welsh':
                            properties['point_icon_colour'] = 'black'
                            properties['point_icon_bgcolour'] = 'red'

                        properties.update(self.pioneer_school_codes[int(json_data['schoolCode'])])

                        self.all_points2.append(
                            Feature(
                                geometry=Point((json_lng, json_lat)),
                                properties=properties
                            )
                        )

                    else:
                        print('Ignore this school')
                        properties['pioneer_school'] = 'False'
                        properties['display_icon'] = 'fa map-pin'


            except Exception as ex1:
                print(ex1)

        print(self.all_points2)

        fc = FeatureCollection(self.all_points2)
        print(dumps(fc))

        with open('schools_geo1.json', 'w') as geo1:
            geo1.write(dumps(fc, indent=4))


if __name__ == "__main__":
    school_geo = SchoolGeo()
    school_geo.geotag_school_to_geojson()
    school_geo.mylocalschool()
