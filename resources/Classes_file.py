from dataclasses import dataclass
from resources.dictionaries_file import fields_dictionary, append_list, remove_list


class GeneralClass:
    def update_field(self, field, value):
        if field in fields_dictionary:
            field = fields_dictionary[field]
            if getattr(self, field) is None:
                setattr(self, field, value)

    def filter_all(self, key):
        for field in self.__dict__:
            if self.filter_field(field, key):
                return True
        return False

    def filter_field(self, field, key):
        '''
        filtra in natural language - se parola è dentro
        :param field:
        :param key:
        :return:
        '''
        return key in getattr(self, field)

    def update_all_fields(self, child):
        tag = child.tag
        text = child.text
        self.update_field(tag, text)
        if len(child) > 0:
            for lower_level_child in child:
                self.update_all_fields(lower_level_child)


    # for lower_level_child in child: #todo se nuova soluzione sopra funziona, cancella questa parte
        #     tag = lower_level_child.tag
        #     text = lower_level_child.text.strip()
        #     self.update_field(tag, text)

class FieldFactory:
    @staticmethod
    def create_appropriate_class(child):
        if child.tag in fields_dictionary:
            tag = fields_dictionary[child.tag]
            if tag == 'iconography':
                return tag, Iconography(child)
            if tag == 'artist':
                return tag, Artist(child)
            if tag == 'other_artist_attribution':
                return tag, AlternativeArtist(child)
            if tag == 'date':
                return tag, Date(child)
            if tag == 'dimension_type':
                return tag, Dimensions(child)
            if tag == 'object_administrator':
                return tag, Institution(child)
            if tag == 'hosting_building':
                return tag, HostingBuilding(child)
            if tag == 'ref_relationship':
                return tag, RelationWithOtherObject(child)
            if tag == 'literature_short_title':
                return tag, ReferenceLiterature(child)
            if tag == 'location_obj_architecture':
                return tag, ObjArchitectureLocation(child)
            if tag == 'obj_architecture_detail':
                return tag, ObjArchitectureDetail(child)
            if tag == 'text_in_artwork':
                return tag, TextInArtwork(child)
            return tag, child.text #.strip(child)



class Iconography(GeneralClass):
    def __init__(self, child):
        self.iconclass_code = None
        self.iconography = None
        self.primary_iconography = None
        self.update_all_fields(child)

    def __repr__(self):
        return f'{self.iconography.strip()}'

    def filter_by(self, value):
        '''
        returns True if there is a match
        :param key:
        :param value:
        :return:
        '''
        attribute_list = [self.iconclass_code, self.iconography, self.primary_iconography]
        for attribute in attribute_list:
            if attribute is not None and value in str(attribute).lower():
                return True
        return False

class Artist(GeneralClass):
    def __init__(self, child):
        self.artist = None
        self.artist_name = None
        self.artist_name_khi = None
        self.artist_alt_names = None
        self.artist_authenticity = None
        self.artist_activity = None
        self.update_all_fields(child)

    def __repr__(self):
        return f'{self.artist_name}'

    def filter_by(self, value):
        '''
        returns True if there is a match
        :param key:
        :param value:
        :return:
        '''
        attribute_list = [self.artist, self.artist_name, self.artist_name_khi, self.artist_alt_names, self.artist_authenticity, self.artist_activity]
        for attribute in attribute_list:
            if attribute is not None and value in str(attribute).lower():
                return True
        return False


class AlternativeArtist(GeneralClass):
    def __init__(self, child):
        self.other_artist_attribution = None
        self.other_artist_attribution_name = None
        self.other_artist_attribution_detail = None
        self.artist = None
        self.artist_name = None
        self.artist_name_khi = None
        self.artist_alt_names = None
        self.artist_authenticity = None
        self.artist_activity = None
        self.update_all_fields(child)

    def __repr__(self):
        out = f'{self.other_artist_attribution}: {self.other_artist_attribution_name}'
        return out

    def filter_by(self, value):
        '''
        returns True if there is a match
        :param key:
        :param value:
        :return:
        '''
        attribute_list = [self.artist, self.artist_name, self.artist_name_khi, self.artist_alt_names,
                          self.artist_authenticity, self.artist_activity, self.other_artist_attribution,
                          self.other_artist_attribution_name, self.other_artist_attribution_detail]
        for attribute in attribute_list:
            if attribute is not None and value in str(attribute).lower():
                return True
        return False


class Date(GeneralClass):
    def __init__(self, child):
        self.date = None
        self.date_span = None
        self.date_start = None
        self.date_end = None
        self.update_all_fields(child)

    def __repr__(self):
        if self.date is not None:
            out = f'{self.date}: {self.date_span}'
        else:
            out = f'{self.date_span}'
        return out

    def filter_by(self, value_1, value_2_or_operator=None):
        '''
        Returns True if there is a match based on specified conditions.
        :param value_1: First value to compare.
        :param value_2_or_operator: Second value to compare (optional).
        :param value_2_or_operator: Comparison operator (<, >, =, <=, >=) (optional).
        :return: True if the conditions are met, otherwise False.
        '''
        if (value_1 is None or not all(char.isdigit() or char == '-' for char in str(value_1))) or (value_2_or_operator is not None and not all(char.isdigit() or char == '-' or char in '<>=' for char in str(value_2_or_operator))):# or (value_2_or_operator is not None and operator is not None):
            # Invalid input configuration
            print('Invalid input configuration. Please provide either a single value, a value with a valid comparison operator (=, <, >, <=, >=), or two values. If year before Christ, use a minus "-" before the year (e.g., -300 for 300 BC)')
            raise ValueError('Invalid input configuration. Please provide either a single value, a value with a valid comparison operator (=, <, >, <=, >=), or two values. If year before Christ, use a minus "-" before the year (e.g., -300 for 300 BC)')

        # Clean dates from self.date_start and self.date_end (check if all numbers)
        clean_date_start = ''.join([char for char in str(self.date_start) if char in '-0123456789'])
        clean_date_end = ''.join([char for char in str(self.date_end) if char in '-0123456789'])

        value_1 = int(value_1)
        clean_date_start = int(clean_date_start) if clean_date_start else None
        clean_date_end = int(clean_date_end) if clean_date_end else None

        if value_2_or_operator is None:
            # if operator is None:
                # Check if value_1 matches cleaned dates
            if clean_date_start is not None and clean_date_end is not None:
                if value_1 == clean_date_start or value_1 == clean_date_end or (
                        clean_date_start <= value_1 <= clean_date_end):
                    return True
            elif clean_date_start is not None or clean_date_end is not None:
                if value_1 == clean_date_start or value_1 == clean_date_end:
                    return True
            return False

        value_2_or_operator = str(value_2_or_operator)
        # Handle comparison with operator and optional value_2
        if value_2_or_operator == '=':
            return value_1 == clean_date_start or value_1 == clean_date_end
        elif value_2_or_operator == '<':
            return clean_date_end < value_1
        elif value_2_or_operator == '>':
            return clean_date_start > value_1
        elif value_2_or_operator == '<=':
            return clean_date_end <= value_1
        elif value_2_or_operator == '>=':
            return clean_date_start >= value_1

        # If value_2 is provided, perform range comparison
        elif all(char.isdigit() or char == '-' for char in str(value_2_or_operator)):
            value_2_or_operator = int(value_2_or_operator)
            if clean_date_start is not None and clean_date_end is not None:
                return value_1 <= clean_date_start <= clean_date_end <= value_2_or_operator
            elif clean_date_start is not None or clean_date_end is not None: # todo CHECK
                temp = clean_date_start if clean_date_start is not None else clean_date_end
                return value_1 <= temp <= value_2_or_operator

        return False  #if no match found


class Dimensions(GeneralClass):
    def __init__(self, child):
        self.dimension_type = None
        self.dimension_value = None
        self.update_all_fields(child)

    def __repr__(self):
        out = f'{self.dimension_type}: {self.dimension_value}'
        return out

    def filter_by(self, value):
        '''
        returns True if there is a match
        :param key:
        :param value:
        :return:
        '''
        attribute_list = [self.dimension_type, self.dimension_value, self.dimension_value]
        for attribute in attribute_list:
            if attribute is not None and value in str(attribute).lower():
                return True
        return False


class Institution(GeneralClass):
    def __init__(self, child):
        self.object_administrator = None
        self.institution_location = None
        self.institution_locality = None
        self.administrator_type = None
        self.institution_name = None
        self.institution_department = None
        self.institution_inventory_number = None
        self.institution_timespan = None
        self.holding_person = None
        self.update_all_fields(child)

    def __repr__(self):
        out = f'{self.object_administrator}: {self.institution_name}, {self.institution_location}'
        return out

    def filter_by(self, value):
        '''
        returns True if there is a match
        :param key:
        :param value:
        :return:
        '''
        attribute_list = [self.object_administrator, self.institution_location, self.institution_locality,
                          self.administrator_type, self.institution_name, self.institution_department,
                          self.institution_inventory_number, self.institution_timespan, self.holding_person]
        for attribute in attribute_list:
            if attribute is not None and value in str(attribute).lower():
                return True
        return False

class HostingBuilding(GeneralClass):
    def __init__(self, child):
        self.hosting_building = None
        self.building_id = None
        self.building_location = None
        self.building_locality = None
        self.building_type_category = None
        self.building_holder = None
        self.building_name = None
        self.building_position = None
        self.building_section_name = None
        self.building_section_type = None
        self.building_section_position = None
        self.update_all_fields(child)

    def __repr__(self):
        out = f'{self.hosting_building}: {self.building_name}, {self.building_location}'
        return out

    def filter_by(self, value):
        '''
        returns True if there is a match
        :param key:
        :param value:
        :return:
        '''
        attribute_list = [self.hosting_building, self.building_id, self.building_location,
                          self.building_locality, self.building_type_category, self.building_holder,
                          self.building_name, self.building_position, self.building_section_name,
                          self.building_section_type, self.building_section_position]
        for attribute in attribute_list:
            if attribute is not None and value in str(attribute).lower():
                return True
        return False


class RelationWithOtherObject(GeneralClass):
    def __init__(self, child):
        self.ref_relationship = None
        self.ref_obj_id = None
        self.ref_creator = None
        self.ref_obj_type_category = None
        self.update_all_fields(child)

    def __repr__(self):
        out = f'{self.ref_relationship}: {self.ref_obj_id}'
        return out

    def filter_by(self, value):
        '''
        returns True if there is a match
        :param key:
        :param value:
        :return:
        '''
        attribute_list = [self.ref_relationship, self.ref_obj_id, self.ref_creator, self.ref_obj_type_category]
        for attribute in attribute_list:
            if attribute is not None and value in str(attribute).lower():
                return True
        return False


class ReferenceLiterature(GeneralClass):
    def __init__(self, child):
        self.literature_short_title = None
        self.literature_reference_section = None
        self.update_all_fields(child)

    def __repr__(self):
        return f'{self.literature_short_title}'

    def filter_by(self, value):
        '''
        returns True if there is a match
        :param key:
        :param value:
        :return:
        '''
        attribute_list = [self.literature_short_title, self.literature_reference_section]
        for attribute in attribute_list:
            if attribute is not None and value in str(attribute).lower():
                return True
        return False


class ObjArchitectureLocation(GeneralClass):
    def __init__(self, child):
        self.location_obj_architecture = None
        self.locality_obj_architecture = None
        self.street_place_obj_architecture = None
        self.house_number_obj_architecture = None
        self.update_all_fields(child)

    def __repr__(self):
        return f'{self.location_obj_architecture}'

    def filter_by(self, value):
        '''
        returns True if there is a match
        :param key:
        :param value:
        :return:
        '''
        attribute_list = [self.location_obj_architecture, self.locality_obj_architecture,
                          self.street_place_obj_architecture, self.street_place_obj_architecture]
        for attribute in attribute_list:
            if attribute is not None and value in str(attribute).lower():
                return True
        return False

class ObjArchitectureDetail(GeneralClass):
    def __init__(self, child):
        self.obj_architecture_detail = None
        self.obj_architecture_detail_localization = None
        self.obj_architecture_detail_description = None
        self.update_all_fields(child)

    def __repr__(self):
        return f'{self.obj_architecture_detail}'

    def filter_by(self, value):
        '''
        returns True if there is a match
        :param key:
        :param value:
        :return:
        '''
        attribute_list = [self.obj_architecture_detail, self.obj_architecture_detail_localization, self.obj_architecture_detail_description]
        for attribute in attribute_list:
            if attribute is not None and value in str(attribute).lower():
                return True
        return False


class TextInArtwork(GeneralClass):
    def __init__(self, child):
        self.text_in_artwork = None
        self.text_in_artwork_content = None
        self.text_position_in_artwork = None
        self.update_all_fields(child)

    def __repr__(self):
        out = f'{self.text_in_artwork}: {self.text_in_artwork_content}'
        return out

    def filter_by(self, value):
        '''
        returns True if there is a match
        :param key:
        :param value:
        :return:
        '''
        attribute_list = [self.text_in_artwork, self.text_in_artwork_content, self.text_position_in_artwork]
        for attribute in attribute_list:
            if attribute is not None and value in str(attribute).lower():
                return True
        return False