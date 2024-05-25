import pathlib
import xml.etree.ElementTree as ET
from resources.dictionaries_file import *
import pandas as pd
import re

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
    '''

    :param filepath:
    :return:
    '''
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

    # Iterate over elements to find art objects and photos on all levels
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

def get_dataframe(filepath):
    '''

    :param filepath:
    :return:
    '''
    from Thesis_project_main import CollectionOfPhotos
    data = parse_xml(filepath)
    photos_dataframe = pd.DataFrame([photo_obj.get_series() for photo_obj in data])
    photos_dataframe = photos_dataframe.drop(columns=[column_name for column_name in remove_list]).dropna(how='all',
                                                                                                          axis='columns')
    photos_dataframe['Photo_Archival_Date'] = photos_dataframe['Photo_Archival_Date'].apply(
        lambda date_str: pd.to_datetime(date_str, errors='coerce')).dt.strftime("%Y-%m-%d")
    photos_dataframe['Photo_Date'] = photos_dataframe['Photo_Date'].apply(
        lambda date_ph: pd.to_datetime(re.sub(r'[^0-9\-]+', '', str(date_ph)), errors='coerce')).dt.strftime("%Y")
    return CollectionOfPhotos(photos_dataframe)


