from resources.dictionaries_file import fields_dictionary, append_list, remove_list


class GeneralClass:
    def update_attributes(self, field, value):
        '''

        :param field:
        :param value:
        :return:
        '''
        if field in fields_dictionary:
            field = fields_dictionary[field]
            if getattr(self, field) is None:
                setattr(self, field, value)


    def update_all_fields(self, child):
        tag = child.tag
        text = child.text
        self.update_attributes(tag, text)
        if len(child) > 0:
            for lower_level_child in child:
                self.update_all_fields(lower_level_child)

class FieldFactory:
    @staticmethod
    def create_appropriate_class(child):
        '''

        :param child:
        :return:
        '''
        if child.tag in fields_dictionary:
            tag = fields_dictionary[child.tag]
            if tag == 'Artwork_Iconography':
                return tag, Iconography(child)
            if tag == 'Artist':
                return tag, Artist(child)
            if tag == 'Other_Artist_Attribution':
                return tag, AlternativeArtist(child)
            if tag == 'Artwork_Date':
                return tag, Date(child)
            if tag == 'Artwork_Dimension_Type':
                return tag, Dimensions(child)
            if tag == 'Cultural_Institution':
                return tag, Institution(child)
            if tag == 'Artwork_LocBuilding':
                return tag, HostingBuilding(child)
            if tag == 'Relation_Type_with_Other_Artwork':
                return tag, RelationWithOtherObject(child)
            if tag == 'Literature_Ref_Short_Title':
                return tag, ReferenceLiterature(child)
            if tag == 'ArchitectureObj_City':
                return tag, ObjArchitectureLocation(child)
            if tag == 'ArchitectureObj_Detail':
                return tag, ObjArchitectureDetail(child)
            if tag == 'Text_in_Artwork':
                return tag, TextInArtwork(child)
            return tag, child.text #.strip(child)



class Iconography(GeneralClass):
    def __init__(self, child):
        self.Artwork_Iconclass_Code = None
        self.Artwork_Iconography = None
        self.Artwork_Iconography_Description = None
        self.update_all_fields(child)

    def __repr__(self):
        return f'{self.Artwork_Iconography.strip()}'

    def filter_by(self, value):
        '''
        returns True if there is a match
        :param key:
        :param value:
        :return:
        '''
        attribute_list = [self.Artwork_Iconclass_Code, self.Artwork_Iconography, self.Artwork_Iconography_Description]
        for attribute in attribute_list:
            if attribute is not None and value in str(attribute).lower():
                return True
        return False


class Artist(GeneralClass):
    def __init__(self, child):
        self.Artist = None
        self.Artist_Name = None
        self.Artist_Name_KHI = None
        self.Artist_Alternative_Name = None
        self.Artist_Authenticity_Attribution = None
        self.Artist_Activity = None
        self.update_all_fields(child)

    def __repr__(self):
        return f'{self.Artist_Name}'

    def filter_by(self, value):
        '''
        returns True if there is a match
        :param key:
        :param value:
        :return:
        '''
        attribute_list = [self.Artist, self.Artist_Name, self.Artist_Name_KHI, self.Artist_Alternative_Name, self.Artist_Authenticity_Attribution, self.Artist_Activity]
        for attribute in attribute_list:
            if attribute is not None and value in str(attribute).lower():
                return True
        return False


class AlternativeArtist(GeneralClass):
    def __init__(self, child):
        self.Other_Artist_Attribution = None
        self.Other_Artist_Attribution_Name = None
        self.Other_Artist_Attribution_Detail = None
        self.Artist = None
        self.Artist_Name = None
        self.Artist_Name_KHI = None
        self.Artist_Alternative_Name = None
        self.Artist_Authenticity_Attribution = None
        self.Artist_Activity = None
        self.update_all_fields(child)

    def __repr__(self):
        out = f'{self.Other_Artist_Attribution}: {self.Other_Artist_Attribution_Name}'
        return out

    def filter_by(self, value):
        '''
        returns True if there is a match
        :param key:
        :param value:
        :return:
        '''
        attribute_list = [self.Artist, self.Artist_Name, self.Artist_Name_KHI, self.Artist_Alternative_Name,
                          self.Artist_Authenticity_Attribution, self.Artist_Activity, self.Other_Artist_Attribution,
                          self.Other_Artist_Attribution_Name, self.Other_Artist_Attribution_Detail]
        for attribute in attribute_list:
            if attribute is not None and value in str(attribute).lower():
                return True
        return False


class Date(GeneralClass):
    def __init__(self, child):
        self.Artwork_Date = None
        self.Artwork_Date_Range = None
        self.Artwork_Date_Start = None
        self.Artwork_Date_End = None
        self.update_all_fields(child)

    def __repr__(self):
        if self.Artwork_Date is not None:
            out = f'{self.Artwork_Date}: {self.Artwork_Date_Range}'
        else:
            out = f'{self.Artwork_Date_Range}'
        return out

    def filter_by(self, value_1, value_2_or_operator=None):
        '''
        Returns True if there is a match based on specified conditions.
        :param value_1: First value to compare.
        :param value_2_or_operator: Second value to compare (optional).
        :param value_2_or_operator: Comparison operator (<, >, =, <=, >=) (optional).
        :return: True if the conditions are met, otherwise False.
        '''
        if ((value_1 is None or not all(char.isdigit() or char == '-' for char in str(value_1))) or
                (value_2_or_operator is not None and not all(char.isdigit() or char == '-' or char in '<>=' for char in str(value_2_or_operator)))):# or (value_2_or_operator is not None and operator is not None):
            # Invalid input configuration
            print('Invalid input configuration. Please provide either a single value, a value with a valid comparison operator (=, <, >, <=, >=), or two values. If year before Christ, use a minus "-" before the year (e.g., -300 for 300 BC)')
            raise ValueError('Invalid input configuration. Please provide either a single value, a value with a valid comparison operator (=, <, >, <=, >=), or two values. If year before Christ, use a minus "-" before the year (e.g., -300 for 300 BC)')

        # Clean dates from self.date_start and self.date_end (check if all numbers)
        clean_date_start = ''.join([char for char in str(self.Artwork_Date) if char in '-0123456789'])
        clean_date_end = ''.join([char for char in str(self.Artwork_Date_End) if char in '-0123456789'])

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


        #TODO HANDLE COMPARISON WITH NONE OPERATOR (LINE 201-202) also handle:
        '''
                elif value_2_or_operator == '<' and clean_date_end is None:
            return clean_date_start < value_1--> also with start date!!!
            '''
        value_2_or_operator = str(value_2_or_operator)
        # Handle comparison with operator and optional value_2
        if value_2_or_operator == '=':
            if clean_date_start is not None or clean_date_end is not None:
                return value_1 == clean_date_start or value_1 == clean_date_end
        elif value_2_or_operator == '<':
            if clean_date_end is not None:
                return clean_date_end < value_1
            elif clean_date_start is not None:
                return clean_date_start < value_1
        elif value_2_or_operator == '>':
            if clean_date_start is not None:
                return clean_date_start > value_1
        elif value_2_or_operator == '<=':
            if clean_date_end is not None:
                return clean_date_end <= value_1
            elif clean_date_start is not None:
                return clean_date_start <= value_1
        elif value_2_or_operator == '<=' and clean_date_start is not None and clean_date_end is None:
            return clean_date_start <= value_1
        elif value_2_or_operator == '>=':
            if clean_date_start is not None:
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
        self.Artwork_Dimension_Type = None
        self.Artwork_Dimension_Value = None
        self.update_all_fields(child)

    def __repr__(self):
        out = f'{self.Artwork_Dimension_Type}: {self.Artwork_Dimension_Value}'
        return out

    def filter_by(self, value):
        '''
        returns True if there is a match
        :param key:
        :param value:
        :return:
        '''
        attribute_list = [self.Artwork_Dimension_Type, self.Artwork_Dimension_Value, self.Artwork_Dimension_Value]
        for attribute in attribute_list:
            if attribute is not None and value in str(attribute).lower():
                return True
        return False


class Institution(GeneralClass):
    def __init__(self, child):
        self.Cultural_Institution = None
        self.Cultural_Institution_City = None
        self.Cultural_Institution_PreciseLoc = None
        self.Artwork_Administrator_Details = None
        self.Cultural_Institution_Name = None
        self.Cultural_Institution_Section = None
        self.Artwork_Inventory_Number = None
        self.Cultural_Institution_Date_Range = None
        self.Artwork_Private_Owner = None
        self.update_all_fields(child)

    def __repr__(self):
        out = f'{self.Cultural_Institution}: {self.Cultural_Institution_Name}, {self.Cultural_Institution_City}'
        return out

    def filter_by(self, value):
        '''
        returns True if there is a match
        :param key:
        :param value:
        :return:
        '''
        attribute_list = [self.Cultural_Institution, self.Cultural_Institution_City, self.Cultural_Institution_PreciseLoc,
                          self.Artwork_Administrator_Details, self.Cultural_Institution_Name, self.Cultural_Institution_Section,
                          self.Artwork_Inventory_Number, self.Cultural_Institution_Date_Range, self.Artwork_Private_Owner]
        for attribute in attribute_list:
            if attribute is not None and value in str(attribute).lower():
                return True
        return False

class HostingBuilding(GeneralClass):
    def __init__(self, child):
        self.Artwork_LocBuilding = None
        self.Artwork_LocBuilding_ID = None
        self.Artwork_LocBuilding_City = None
        self.Artwork_LocBuilding_PreciseLoc = None
        self.Artwork_LocBuilding_Type = None
        self.Artwork_LocBuilding_ReligiousOrder = None
        self.Artwork_LocBuilding_Name = None
        self.Artwork_LocBuilding_Room = None
        self.Artwork_LocBuilding_SectionName = None
        self.Artwork_LocBuilding_SectionType = None
        self.Artwork_LocBuilding_SectionRoom = None
        self.update_all_fields(child)

    def __repr__(self):
        out = f'{self.Artwork_LocBuilding}: {self.Artwork_LocBuilding_Name}, {self.Artwork_LocBuilding_City}'
        return out

    def filter_by(self, value):
        '''
        returns True if there is a match
        :param key:
        :param value:
        :return:
        '''
        attribute_list = [self.Artwork_LocBuilding, self.Artwork_LocBuilding_ID, self.Artwork_LocBuilding_City,
                          self.Artwork_LocBuilding_PreciseLoc, self.Artwork_LocBuilding_Type, self.Artwork_LocBuilding_ReligiousOrder,
                          self.Artwork_LocBuilding_Name, self.Artwork_LocBuilding_Room, self.Artwork_LocBuilding_SectionName,
                          self.Artwork_LocBuilding_SectionType, self.Artwork_LocBuilding_SectionRoom]
        for attribute in attribute_list:
            if attribute is not None and value in str(attribute).lower():
                return True
        return False


class RelationWithOtherObject(GeneralClass):
    def __init__(self, child):
        self.Relation_Type_with_Other_Artwork = None
        self.Related_Artwork_ID = None
        self.Related_Artwork_Artist = None
        self.Related_Artwork_Type = None
        self.update_all_fields(child)

    def __repr__(self):
        out = f'{self.Relation_Type_with_Other_Artwork}: {self.Related_Artwork_ID}'
        return out

    def filter_by(self, value):
        '''
        returns True if there is a match
        :param key:
        :param value:
        :return:
        '''
        attribute_list = [self.Relation_Type_with_Other_Artwork, self.Related_Artwork_ID, self.Related_Artwork_Artist, self.Related_Artwork_Type]
        for attribute in attribute_list:
            if attribute is not None and value in str(attribute).lower():
                return True
        return False


class ReferenceLiterature(GeneralClass):
    def __init__(self, child):
        self.Literature_Ref_Short_Title = None
        self.Literature_Ref_Page = None
        self.update_all_fields(child)

    def __repr__(self):
        return f'{self.Literature_Ref_Short_Title}'

    def filter_by(self, value):
        '''
        returns True if there is a match
        :param key:
        :param value:
        :return:
        '''
        attribute_list = [self.Literature_Ref_Short_Title, self.Literature_Ref_Page]
        for attribute in attribute_list:
            if attribute is not None and value in str(attribute).lower():
                return True
        return False


class ObjArchitectureLocation(GeneralClass):
    def __init__(self, child):
        self.ArchitectureObj_City = None
        self.ArchitectureObj_PreciseLoc = None
        self.ArchitectureObj_AddressStreet = None
        self.ArchitectureObj_AddressNr = None
        self.update_all_fields(child)

    def __repr__(self):
        return f'{self.ArchitectureObj_City}'

    def filter_by(self, value):
        '''
        returns True if there is a match
        :param key:
        :param value:
        :return:
        '''
        attribute_list = [self.ArchitectureObj_City, self.ArchitectureObj_PreciseLoc,
                          self.ArchitectureObj_AddressStreet, self.ArchitectureObj_AddressStreet]
        for attribute in attribute_list:
            if attribute is not None and value in str(attribute).lower():
                return True
        return False

class ObjArchitectureDetail(GeneralClass):
    def __init__(self, child):
        self.ArchitectureObj_Detail = None
        self.ArchitectureObj_Detail_Location = None
        self.ArchitectureObj_Detail_Description = None
        self.update_all_fields(child)

    def __repr__(self):
        return f'{self.ArchitectureObj_Detail}'

    def filter_by(self, value):
        '''
        returns True if there is a match
        :param key:
        :param value:
        :return:
        '''
        attribute_list = [self.ArchitectureObj_Detail, self.ArchitectureObj_Detail_Location, self.ArchitectureObj_Detail_Description]
        for attribute in attribute_list:
            if attribute is not None and value in str(attribute).lower():
                return True
        return False


class TextInArtwork(GeneralClass):
    def __init__(self, child):
        self.Text_in_Artwork = None
        self.Text_in_Artwork_Content = None
        self.Text_Location_in_Artwork = None
        self.update_all_fields(child)

    def __repr__(self):
        out = f'{self.Text_in_Artwork}: {self.Text_in_Artwork_Content}'
        return out

    def filter_by(self, value):
        '''
        returns True if there is a match
        :param key:
        :param value:
        :return:
        '''
        attribute_list = [self.Text_in_Artwork, self.Text_in_Artwork_Content, self.Text_Location_in_Artwork]
        for attribute in attribute_list:
            if attribute is not None and value in str(attribute).lower():
                return True
        return False