import pathlib
import xml.etree.ElementTree as ET
import re
from pprint import pprint
from resources.PhotoAttributes import PhotoAttributes
from resources.dictionaries_file import *
from Classes_file import *
import numpy
import matplotlib.pyplot as plt
import pandas as pd
from pandas.api.types import is_datetime64_any_dtype as is_datetime


class CollectionOfPhotos:  # contains dataframe with all photographs
    def __init__(self, dataframe):
        self.dataframe = dataframe
        self.dataframe_for_filter = self.dataframe.map(lambda s: str(s).lower())  # todo check if works
        # self.dataframe_lower = self.dataframe.map(lambda s: s.lower() if type(s) == str else s)

    def filter_by(self, key, value, value_2=None):  # todo key è per forza in dizionario
        if not isinstance(value, str):
            value = str(value)
        if not isinstance(value_2, str):
            value_2 = str(value_2)
        key = key.lower()
        value = value.lower()
        result_dataframe = self.dataframe.loc[~self.dataframe[key].isnull()].copy()
        result_dataframe.reset_index(inplace=True, drop=True)
        # todo sanitize inputs error handling
        if key in append_list:
            if isinstance(result_dataframe[key].iloc[0][0], GeneralClass) and not isinstance(result_dataframe[key].iloc[0][0], Date): #todo CHECK
                return result_dataframe.loc[
                    result_dataframe[key].apply(lambda x: any([i.filter_by(value) for i in x]))]
            elif isinstance(result_dataframe[key].iloc[0][0], Date):
                return result_dataframe.loc[
                    result_dataframe[key].apply(lambda x: any([i.filter_by(value, value_2) for i in x]))] # todo CHECK
            else:
                return result_dataframe.loc[
                    result_dataframe[key].apply(lambda x: any([value in i.lower() for i in x]))]

        if is_datetime(result_dataframe[key]):
            value_datetime = pd.to_datetime(value, errors='coerce')
            input_year = str(value_datetime.year) if value_datetime.year != pd.NaT else value
            return result_dataframe.loc[
            result_dataframe[key].apply(
                lambda x: (
                    (isinstance(x, pd.Timestamp) and value_datetime == x) or  # Exact match with datetime
                    (isinstance(x, pd.Timestamp) and input_year == str(x.year))  # Match year component
                ) if pd.notnull(x) else False
            )
        ]

        filtered_res = result_dataframe.loc[
             result_dataframe[key].apply(lambda x: any([value in x.lower()]))]
        return filtered_res

    # todo handle dates pd.Datetime

    def plot_values(self, key, mode=None):
        '''

        :param key:
        :param mode: available modes are:
        - line: ...
        - bar: ...

        :return:
        '''
        if mode is None:
            mode = 'line'
        if mode == 'line':
            plt.plot(self.dataframe[key].dropna().reset_index(drop=True))
            plt.show()
        if mode == 'bar':
            plt.bar(self.dataframe[key].dropna().reset_index(drop=True))
            plt.show()
        pass


class PhotoObject(PhotoAttributes):
    def update_field(self, child):
        if child.tag in fields_dictionary:
            # FieldFactory handles child and returns a string or an object depending on the received input
            field_name, attribute = FieldFactory.create_appropriate_class(child)

            # append_list contains field names of elements that can appear multiple times within the same document
            # both string and object attributes are stored in a list to allow extension with further elements of the same type
            if getattr(self, field_name) is None:
                if field_name in append_list:
                    setattr(self, field_name, [attribute])
                # handle simplest case: neither nested nor multiple
                else:
                    setattr(self, field_name, attribute)

            # handle case in which attribute already has content to add further info in case of multiple elements
            elif field_name in append_list:
                attrib_value = getattr(self, field_name)
                str_attrib_value = []
                for el in attrib_value:
                    str_el = str(el)
                    str_attrib_value.append(str_el)
                    if str(attribute) not in str_attrib_value:
                        setattr(self, field_name, attrib_value + [attribute])

    def get_series(self):
        return pd.Series(self.__dict__)


class XmlReaderKHI:

    @staticmethod
    def read_clean_doc(path_to_file):  # todo Da sistemare: funziona con xml con un solo obj?
        '''
        The XML file referenced as input is returned as a list of its lines as strings
        with correct encoding provided in the converter dictionary
        :param path_to_file: path of the xml document
        :return: list of lines
        '''
        # TODO: verifica text encoding dei dati nuovi - modo di standardizzare encoding?
        clean_doc = []
        with open(path_to_file, encoding="Windows-1252") as xmlfile:
            for i in xmlfile.readlines():
                if not i.strip() == "":
                    for k in converter:
                        i = i.replace(k, converter[k])
                    clean_doc.append(i)
        with open('../temp_clean.xml', 'w', encoding="Windows-1252") as w:  # todo questo deve essere una variabile?
            w.writelines(clean_doc)

    @staticmethod
    def parse_xml(filepath: pathlib.Path):
        photo_objects_list = []
        XmlReaderKHI.read_clean_doc(filepath)

        # Parse XML and retrieve its root element
        tree = ET.parse('temp_clean.xml')
        root = tree.getroot()

        # Mapping each child element to its parent in a dict with children as key and parents as values
        parent_map = {}
        for parent in tree.iter():
            for child in parent:
                parent_map[child] = parent

        # Iterate over elements to find art objects on all levels
        # for i in ['a5000', 'a5001', 'a5002', 'a5003', 'a5004']:
        for i in ['a84fl']:
            for k in tree.findall(f'.//{i}'):
                f = PhotoObject()
                current = k

                # Iterate over current, the parent object, until reaching root level
                while current != tree.getroot():
                    current = parent_map[current]
                    for child in current:
                        if child.tag in nested_elements_list:
                            if child.text != '':
                                f.update_field(child)
                            # if len(child) > 0:  # just in case of elements that are supposed to have children don't
                            #     for field, content in XmlReaderKHI.handle_nested_data(child).items(): # todo da modificare?
                            #         f.update_field(child)
                        else:
                            f.update_field(child)

                photo_objects_list.append(f)
        return photo_objects_list


    # @staticmethod
    # def handle_nested_data(child):
    #     temp_dict = {}
    #     for lower_level_child in child:
    #         temp_dict[lower_level_child.tag] = lower_level_child.text
    #         if len(lower_level_child) > 0:
    #             temp_dict.update(XmlReaderKHI.handle_nested_data(lower_level_child))
    #     return temp_dict

    @staticmethod
    def get_dataframe(filepath):
        data = XmlReaderKHI.parse_xml(filepath)
        # for photo in data:
        #     for attribute in vars(photo):
        #         if attribute not in remove_list:
        photos_dataframe = pd.DataFrame([photo_obj.get_series() for photo_obj in data])
        photos_dataframe = photos_dataframe.drop(columns=[column_name for column_name in remove_list]).dropna(how='all',
                                                                                                              axis='columns')
        photos_dataframe['photo_entry_archival_date'] = photos_dataframe['photo_entry_archival_date'].apply(
            lambda date_str: pd.to_datetime(date_str, errors='coerce'))
        return CollectionOfPhotos(photos_dataframe)

    # @staticmethod
    # def filter_by(filepath, field, entry): # TODO: idea è di far selezionare da una lista di attributi predefinita
    #     photos_dataframe = XmlReaderKHI.get_dataframe(filepath)
    #     photos_dataframe = photos_dataframe.map(lambda s: s.lower() if type(s) == str else s)
    #     entry = entry.lower()
    #     field = field.lower()
    #     filtered_res = photos_dataframe[photos_dataframe[field].str.contains(fr'\b{entry}\b')==True]
    #     return filtered_res

    @staticmethod
    def get_dataset_info(filepath):
        photos_dataframe = XmlReaderKHI.get_dataframe(filepath)
        ph_nr = len(photos_dataframe.dataframe)
        obj_nr = photos_dataframe.dataframe['obj_id'].nunique()
        return f"About this dataset:\nNumber of photos: {ph_nr}\nNumber of objects: {obj_nr}"

    @staticmethod
    def get_digital_photos(filepath):
        photos_dataframe = XmlReaderKHI.get_dataframe(filepath)
        filtered_res = photos_dataframe.dataframe.loc[photos_dataframe.dataframe['photo_file_format'] == 'tif']
        return filtered_res


class JsonReaderDifferent:
    pass


filepath_test_case = r'../data/test_case.xml'
filepath_buerkelens = r'../data/cleaned_string.xml'

ppo = XmlReaderKHI.parse_xml(filepath_buerkelens)
# print(XmlReaderKHI.get_dataframe(r'data/test_case.xml'))

dataframe_photos = XmlReaderKHI.get_dataframe(filepath_buerkelens)
dataframe_filter = dataframe_photos.dataframe_for_filter
# for i in dataframe_photos.dataframe.columns:
#     if dataframe_photos.dataframe[i].count() == 0:
#         print(f'column {i} has all None')
print('arrivati')
filter_by_artist_name = dataframe_photos.filter_by('artist', 'Sebastiano')
filter_by_title= dataframe_photos.filter_by('title', 'Madonna')
filter_by_material= dataframe_photos.filter_by('material', 'Putz')
filter_by_iconography= dataframe_photos.filter_by('iconography', 'kreuz')
filter_by_date= dataframe_photos.filter_by('date', '-1000', '>=')
filter_by_photo_date= dataframe_photos.filter_by('photo_entry_archival_date', 2022)
print(filter_by_photo_date)
# filter_by_artist_name1 = dataframe_photos.filter_by('artist_name', 'leonardo')
# filter_by_material = dataframe_photos.filter_by('material', 'putz')
# digital_ph_df = XmlReaderKHI.get_digital_photos(filepath_buerkelens)
# df_df = dataframe_photos.dataframe
#
# # print(XmlReaderKHI.get_dataset_info(r'data/cleaned_string.xml'))
# # print(filter_by_artist_name1)
# print(digital_ph_df)
