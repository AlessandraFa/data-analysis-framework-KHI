from dictionaries_file import fields_dictionary


output = ['from dataclasses import dataclass\n',
          'from typing import Union\n',
          '\n',
          '\n',
          '@dataclass\n',
          'class PhotoAttributes:\n']
for key, value in fields_dictionary.items():
    if f'\t{value}: str = None\n' not in output:
        output.append(f'\t{value}: Union[str, list] = None\n')
with open('PhotoAttributes.py', 'w') as w:
    w.writelines(output)