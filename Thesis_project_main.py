import pprint
import numpy as np
from resources.PhotoAttributes import PhotoAttributes
from resources.dictionaries_file import *
from resources.Classes_file import *
import functions_for_KHI_data_extraction
import matplotlib.pyplot as plt
import datetime
import pandas as pd
import seaborn as sns
from pandas.api.types import is_datetime64_any_dtype as is_datetime

PHOTO_FORMAT = 'photo_file_format'
PHOTO_FORMAT_VALUE = 'tif'
DATE_KEY_LIST = ['photo_entry_archival_date', 'photo_date']

class CollectionOfPhotos:  # contains dataframe with all photographs
    def __init__(self, dataframe):
        self.dataframe = dataframe
        # self.dataframe_for_filter = self.dataframe.map(lambda s: str(s).lower())  # todo check if works
        self.dataframe_no_scan = self.dataframe.loc[~self.dataframe['photo_id'].str.contains('scan')]
        # self.dataframe_lower = self.dataframe.map(lambda s: s.lower() if type(s) == str else s)

    def filter_by(self, key, value, value_2=None, ext_df=None):  # todo key è per forza in dizionario
        '''

        :param key:
        :param value:
        :param value_2:
        :param ext_df:
        :return:
        '''
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

        if key in DATE_KEY_LIST:
            return result_dataframe.loc[
                result_dataframe[key].apply(lambda x: any([self.filter_date_noclass(value, value_2, x)]))]


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


    def filter_date_noclass(self, value_1, value_2_or_operator = None, df_data = None):
        if (value_1 is None or not all(char.isdigit() or char == '-' for char in str(value_1))) or (
                value_2_or_operator is not None and not all(char.isdigit() or char == '-' or char in '<>=' for char in
                                                            str(value_2_or_operator))):  # or (value_2_or_operator is not None and operator is not None):
            # Invalid input configuration
            print(
                'Invalid input configuration. Please provide either a single value, a value with a valid comparison operator (=, <, >, <=, >=), or two values. If year before Christ, use a minus "-" before the year (e.g., -300 for 300 BC)')
            raise ValueError(
                'Invalid input configuration. Please provide either a single value, a value with a valid comparison operator (=, <, >, <=, >=), or two values. If year before Christ, use a minus "-" before the year (e.g., -300 for 300 BC)')

        # Clean date (check if all digits)
        if df_data is not None and isinstance(df_data, str):
            clean_date = ''.join([char for char in df_data if char.isdigit() or char == '-'])
        else:
            clean_date = None

        value_1 = value_1+'-01-01'
        value_1 = datetime.datetime.strptime(value_1, '%Y-%m-%d')
        if len(clean_date) == 4:
            clean_date = clean_date+'-01-01'
        clean_date = datetime.datetime.strptime(clean_date, '%Y-%m-%d') if clean_date else None

        if value_2_or_operator is None:
            # if no operator provided as input:
            # Check if value_1 matches cleaned dates
            if clean_date is not None:# and clean_date_end is not None:
                if value_1 == clean_date:
                    return True
            return False

        comparison_operator = str(value_2_or_operator)
        # Handle comparison with operator and optional value_2
        if comparison_operator == '=':
            return clean_date == value_1 if clean_date else False
        elif comparison_operator == '<':
            return clean_date < value_1 if clean_date else False
        elif comparison_operator == '>':
            return clean_date > value_1 if clean_date else False
        elif comparison_operator == '<=':
            return clean_date <= value_1 if clean_date else False
        elif comparison_operator == '>=':
            return clean_date >= value_1 if clean_date else False

        # If value_2 is provided, perform range comparison
        elif all(char.isdigit() for char in str(value_2_or_operator)) and len(str(value_2_or_operator))==4:
            value_2_or_operator = value_2_or_operator + '-01-01'
            end_year_range = datetime.datetime.strptime(value_2_or_operator, '%Y-%m-%d')
            return value_1 <= clean_date <= end_year_range if clean_date else False

        return False  # if no match found

    def get_dataset_description(self, dataframe = None):
        '''

        :param dataframe:
        :return:
        '''
        if dataframe is None:
            ph_nr = len(self.dataframe_no_scan)
            obj_nr = self.dataframe_no_scan['obj_id'].nunique()
            return f"About this dataset:\nNumber of photos: {ph_nr}\nNumber of objects: {obj_nr}"
        else:
            ph_nr = len(dataframe)
            obj_nr = dataframe['obj_id'].nunique()
            return f"About this dataset:\nNumber of photos: {ph_nr}\nNumber of objects: {obj_nr}"

    def get_artwork_info(self, obj_id):
        # d = [self.dataframe.loc[self.dataframe[key] == str(obj_id) if key in self.dataframe.columns else False for key in object_id_list]]
        actual_list_id = [i for i in object_id_list if i in self.dataframe_no_scan.columns]
        actual_list_info = [j for j in artwork_info if j in self.dataframe_no_scan.columns]

        filtered_df = self.dataframe_no_scan.loc[
            (self.dataframe_no_scan[actual_list_id] == str(obj_id)).any(axis=1), actual_list_info].dropna(how='all',
                                                                                                          axis=1)
        object_info = filtered_df.transpose()

        transformed_obj_info = pd.DataFrame(index=object_info.index, columns=[f'Artwork {obj_id}'])

        # Iterate over each row to merge values into a list if needed
        for index, row in object_info.iterrows():
            merged_values = []
            for column in object_info.columns:
                value = row[column]
                if not isinstance(row[column], list) and value not in merged_values and not pd.isna(value):
                    merged_values.append(str(value))
                elif isinstance(row[column], list):
                    for el in row[column]:
                        if str(el) not in merged_values:
                            merged_values.append(str(el))

            # Convert list of one element back to string if applicable
            if len(merged_values) == 1:
                merged_values = merged_values[0]  # Convert single-element list to string

            transformed_obj_info.loc[index, f'Artwork {obj_id}'] = merged_values

        return transformed_obj_info



    def get_photo_info(self, photo_id):
        photo_list_info = []
        for j in photo_info:
            if j in self.dataframe_no_scan.columns:
                photo_list_info.append(j)
        photo_data = self.dataframe_no_scan.loc[
            self.dataframe_no_scan['photo_id'] == str(photo_id), photo_list_info].dropna(how='all',
                                                                                                          axis=1)
        photo_data = photo_data.set_index("photo_id")
        photo_data = photo_data.transpose()

        return photo_data


    def get_digital_photos(self, dataframe = None):
        '''

        '''
        return self.filter_by(key=PHOTO_FORMAT, value=PHOTO_FORMAT_VALUE, ext_df=dataframe)

    def sort_columns_by(self, column_name, dataframe = None):
        '''

        '''
        column_name = str(column_name)

        if dataframe is None:
            dataframe = self.dataframe_no_scan

        filtered_df = dataframe[dataframe[column_name].notna()].reset_index(drop=True)

        if column_name == 'date' and 'date_start' not in filtered_df.columns:
            dates_min = filtered_df.date.apply(lambda x: x[0].date_start)
            order = dates_min.sort_values().index
            return filtered_df.iloc[order].reset_index(drop = True)

        #test for int values
        try:
            filtered_df[column_name] = filtered_df[column_name].astype(int)
        except:
            filtered_df = filtered_df.astype(str)

        sorted_df = filtered_df.sort_values(by=[column_name], na_position='last')

        return sorted_df


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
        elif mode == 'donut':
            self._plot_donut(key, mode)
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
        plt.pie(value_counts, labels=value_labels, autopct='%1.1f%%', startangle=140, colors = sns.color_palette('Set2')
)
        plt.title(f'Fraction of Photos by {key}')

    def _plot_donut(self, key, mode):
        value_counts = self._get_value_counts(key, mode)
        value_labels = value_counts.index
        plt.figure(figsize=(8, 8))
        plt.pie(value_counts, labels=value_labels, autopct='%1.1f%%', startangle=140,
                colors=sns.color_palette('Set2')
                )
        plt.title(f'Fraction of Photos by {key}')
        hole = plt.Circle((0, 0), 0.65, facecolor='white')
        plt.gcf().gca().add_artist(hole)

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


