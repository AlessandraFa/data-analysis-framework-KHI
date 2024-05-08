import pathlib
import xml.etree.ElementTree as ET
from resources.dictionaries_file import *
import pandas as pd

def read_clean_doc(path_to_file, path_output = "temp_clean.xml"):  # todo Da sistemare: funziona con xml con un solo obj?
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
    with open(path_output, 'w', encoding="Windows-1252") as w:
        w.writelines(clean_doc)
    return path_output


def parse_xml(filepath: pathlib.Path):
    from Thesis_project_main import PhotoObject
    photo_objects_list = []
    pth_output = read_clean_doc(filepath)

    # Parse XML and retrieve its root element
    tree = ET.parse(pth_output)
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

def get_dataframe(filepath):
    from Thesis_project_main import CollectionOfPhotos
    data = parse_xml(filepath)
    # for photo in data:
    #     for attribute in vars(photo):
    #         if attribute not in remove_list:
    photos_dataframe = pd.DataFrame([photo_obj.get_series() for photo_obj in data])
    photos_dataframe = photos_dataframe.drop(columns=[column_name for column_name in remove_list]).dropna(how='all',
                                                                                                          axis='columns')
    photos_dataframe['photo_entry_archival_date'] = photos_dataframe['photo_entry_archival_date'].apply(
        lambda date_str: pd.to_datetime(date_str, errors='coerce'))
    return CollectionOfPhotos(photos_dataframe)