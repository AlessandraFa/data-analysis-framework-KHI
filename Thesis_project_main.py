import pathlib
import xml.etree.ElementTree as ET
import re
from collections import Counter
from pprint import pprint
from resources.PhotoAttributes import PhotoAttributes
from resources.dictionaries_file import *
from resources.Classes_file import *
import numpy
import matplotlib.pyplot as plt
import pandas as pd
from pandas.api.types import is_datetime64_any_dtype as is_datetime


class CollectionOfPhotos:  # contains dataframe with all photographs
    def __init__(self, dataframe):
        self.dataframe = dataframe
        # self.dataframe_for_filter = self.dataframe.map(lambda s: str(s).lower())  # todo check if works
        self.dataframe_no_scan = self.dataframe.loc[~self.dataframe['photo_id'].str.contains('scan')]
        # self.dataframe_lower = self.dataframe.map(lambda s: s.lower() if type(s) == str else s)

    def filter_by(self, key, value, value_2=None, ext_df=None):  # todo key è per forza in dizionario
        if not isinstance(value, str):
            value = str(value)
        if value_2 is not None and not isinstance(value_2, str):
            value_2 = str(value_2)

        key = key.lower()
        value = value.lower()
        if ext_df is None:
            result_dataframe = self.dataframe_no_scan.loc[~self.dataframe_no_scan[key].isnull()].copy()
            result_dataframe.reset_index(inplace=True, drop=True)
        else:
            result_dataframe = ext_df.copy()

        if key in append_list:
            if isinstance(result_dataframe[key].iloc[0][0], GeneralClass) and not isinstance(
                    result_dataframe[key].iloc[0][0], Date):  #todo CHECK
                return result_dataframe.loc[
                    result_dataframe[key].apply(lambda x: any([i.filter_by(value) for i in x]))]
            elif isinstance(result_dataframe[key].iloc[0][0], Date):
                return result_dataframe.loc[
                    result_dataframe[key].apply(lambda x: any([i.filter_by(value, value_2) for i in x]))]  # todo CHECK
            else:
                return result_dataframe.loc[
                    result_dataframe[key].apply(lambda x: any([value in i.lower() for i in x]))]

        if is_datetime(result_dataframe[key]):  #todo! remove hours 00:00:00
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

    # def filter_by_multiple_values(self, key_1, value_1, key_2, value_2, key_3 = None, value_3 = None, key_4 = None, value_4 = None):
    #     value_1 = str(value_1).lower()
    #     value_2 = str(value_2).lower()
    #     key_1 = key_1.lower()
    #     key_2 = key_2.lower()
    #     if value_3 is not None and key_3 is not None:
    #         value_3 = str(value_3).lower()
    #         key_3 = str(value_3).lower()
    #         if value_4 is not None and key_4 is not None:
    #             value_4 = str(value_4).lower()
    #             key_4 = str(value_3).lower()

    def get_dataset_description(self):
        ph_nr = len(self.dataframe_no_scan)
        obj_nr = self.dataframe_no_scan['obj_id'].nunique()
        return f"About this dataset:\nNumber of photos: {ph_nr}\nNumber of objects: {obj_nr}"

    def get_artwork_info(self, obj_id):
        # d = [self.dataframe.loc[self.dataframe[key] == str(obj_id) if key in self.dataframe.columns else False for key in object_id_list]]
        actual_list_id = []
        for i in object_id_list:
            if i in self.dataframe_no_scan.columns:
                actual_list_id.append(i)
        actual_list_info = []
        for j in artwork_info:
            if j in self.dataframe_no_scan.columns:
                actual_list_info.append(j)
        object_info = self.dataframe_no_scan.loc[
            (self.dataframe_no_scan[actual_list_id] == str(obj_id)).any(axis=1), actual_list_info].dropna(how='all',
                                                                                                          axis=1)

        return object_info

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
            self._plot_line(key, mode)
        elif mode == 'pie':
            self._plot_pie(key, mode)
        elif mode == 'bar':
            self._plot_bar(key, mode)
        else:
            raise ValueError('Please input correct mode')

    def _plot_line(self, key, mode):
        value_counts = self._get_value_counts(key, mode)
        value_counts.plot(kind='line', title=f'Number of photos by {key}', figsize=(10, 6), legend=False, fontsize=10)
        plt.xticks(rotation=45, ha='right', fontsize=10)  # Rotate x-axis labels for better readability
        plt.yticks([])
        plt.xlabel('')
        plt.gca().spines['top'].set_visible(False)
        plt.gca().spines['right'].set_visible(False)

    def _plot_pie(self, key, mode):
        value_counts = self._get_value_counts(key, mode)
        value_labels = value_counts.index
        plt.figure(figsize=(8, 8))
        plt.pie(value_counts, labels=value_labels, autopct='%1.1f%%', startangle=140)
        plt.title(f'Fraction of Photos by {key}')

    def _plot_bar(self, key, mode):
        value_counts = self._get_value_counts(key, mode)
        top_value_counts = value_counts.head(25)
        num_bars = len(top_value_counts)
        top_value_counts.plot(kind='bar', title=f'Number of photos by {key}', figsize=(num_bars * 0.6, 6), legend=False,
                              fontsize=10)
        bars = plt.bar(top_value_counts.index, top_value_counts.values, color='skyblue')
        plt.xticks(rotation=45, ha='right', fontsize=10)  # Rotate x-axis labels for better readability
        plt.yticks([])
        plt.xlabel('')
        plt.gca().spines['top'].set_visible(False)
        plt.gca().spines['right'].set_visible(False)
        plt.gca().spines['left'].set_visible(False)
        plt.gca().spines['bottom'].set_visible(False)
        # Add value counts to each bar
        for bar in bars:
            yval = bar.get_height()  # Get the height of each bar
            plt.text(bar.get_x() + bar.get_width() / 2, yval + 0.5, str(int(yval)),
                     ha='center', va='bottom', fontsize=10, color='black')
        plt.tight_layout()

    def _get_value_counts(self, key, mode):
        # handle lists
        values_dict = {}
        if key in append_list:
            for val_list in self.dataframe_no_scan[key].values:
                if isinstance(val_list, list):
                    for element in val_list:
                        if str(element) in values_dict:
                            values_dict[str(element)] += 1
                        else:
                            values_dict[str(element)] = 1
            df_output = pd.Series(data=values_dict.values(), index=values_dict.keys())

            # then:
            if mode == 'bar':
                # sorted_value_counts = self.dataframe_no_scan[key].dropna().sort_values()
                return df_output.sort_values(ascending=False)
            else:
                return self.dataframe_no_scan[key].dropna().value_counts()

        else:
            if mode == 'bar':
                sorted_value_counts = self.dataframe_no_scan[key].dropna().sort_values()
                value_counts = sorted_value_counts.value_counts()
            else:
                value_counts = self.dataframe_no_scan[key].dropna().value_counts()
            return value_counts


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
        with open('temp_clean.xml', 'w', encoding="Windows-1252") as w:  # todo questo deve essere una variabile?
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

    # @staticmethod
    # def get_dataset_info(filepath):
    #     photos_dataframe = XmlReaderKHI.get_dataframe(filepath)
    #     ph_nr = len(photos_dataframe.dataframe)
    #     obj_nr = photos_dataframe.dataframe['obj_id'].nunique()
    #     return f"About this dataset:\nNumber of photos: {ph_nr}\nNumber of objects: {obj_nr}"

    @staticmethod
    def get_filtered_dataset_description(dataframe):
        ph_nr = len(dataframe)
        obj_nr = dataframe['obj_id'].nunique()
        return f"About this dataset:\nNumber of photos: {ph_nr}\nNumber of objects: {obj_nr}"

    @staticmethod
    def get_digital_photos(filepath):
        photos_dataframe = XmlReaderKHI.get_dataframe(filepath)
        filtered_res = photos_dataframe.dataframe.loc[photos_dataframe.dataframe['photo_file_format'] == 'tif']
        return filtered_res


class JsonReaderDifferent:
    pass


# filepath_test_case = r'/Users/alessandrafailla/Desktop/thesis_project_KHI_data_analysis/data-analysis-framework-KHI/metadata/test_case.xml'
#filepath_buerkelens = r'/Users/alessandrafailla/Desktop/thesis_project_KHI_data_analysis/data-analysis-framework-KHI/metadata/cleaned_string.xml'
# ppo = XmlReaderKHI.parse_xml(filepath_buerkelens)
# # print(XmlReaderKHI.get_dataframe(r'metadata/test_case.xml'))
#
#dataframe_photos = XmlReaderKHI.get_dataframe(filepath_buerkelens)
# # dataframe_filter = dataframe_photos.dataframe_for_filter
# # for i in dataframe_photos.dataframe.columns:
# #     if dataframe_photos.dataframe[i].count() == 0:
# #         print(f'column {i} has all None')
# # print('arrivati')
# filter_by_artist_name = dataframe_photos.filter_by('artist', 'Sebastiano')
# filter_by_title = dataframe_photos.filter_by('title', 'Madonna')
# filter_by_material = dataframe_photos.filter_by('material', 'Putz')
# filter_by_iconography = dataframe_photos.filter_by('iconography', 'kreuz')
#filter_by_date = dataframe_photos.filter_by('date', '1400')
#filter_by_photo_date = dataframe_photos.filter_by('photo_entry_archival_date', 2022)
#
# #filter_by_dateartist = dataframe_photos.filter_by('date', 'sebastiano')
#
# # print(filter_by_photo_date)
# # print(dataframe_photos.get_dataset_description())
# pprint(dataframe_photos.get_artwork_info('07700713,T,001'))
# print(XmlReaderKHI.get_filtered_dataset_description(filter_by_photo_date))
# dataframe_photos.plot_values('iconography', 'bar')
# filter_by_artist_name1 = dataframe_photos.filter_by('artist_name', 'leonardo')
# filter_by_material = dataframe_photos.filter_by('material', 'putz')
# digital_ph_df = XmlReaderKHI.get_digital_photos(filepath_buerkelens)
# df_df = dataframe_photos.dataframe
#
# # print(XmlReaderKHI.get_dataset_info(r'metadata/cleaned_string.xml'))
# # print(filter_by_artist_name1)
# print(digital_ph_df)
