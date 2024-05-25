import ipywidgets as widgets

glossary_dropdown = widgets.Dropdown(
    options=[''],
    value='',
    description='Definition:',
    disabled=False,
)

upload = widgets.FileUpload(
    accept='.xml',
    multiple=False
)

filter_column_widget = widgets.Dropdown(
    options=[''],
    value='',
    description='Column:',
    disabled=False,
)
text_to_filter = widgets.Text(
    value='',
    placeholder='Type your text here',
    description='Search text:',
    disabled=False
)

filter_additional_column_widget = widgets.Dropdown(
    options=[''],
    value='',
    description='Column:',
    disabled=False,
)
filter_additional_column_txt = widgets.Text(
    value='',
    placeholder='Type your text here',
    description='Search text:',
    disabled=False
)


filter_date_column_widget = widgets.Dropdown(
    options=[''],
    value='',
    description='Column:',
    disabled=False,
)

info_input_id_obj = widgets.Text(
    value='',
    placeholder='Input artwork ID',
    description='Artwork ID:',
    disabled=False
)

info_input_id_ph = widgets.Text(
    value='',
    placeholder='Input photo ID',
    description='Photo ID:',
    disabled=False
)

bar_number_widget = widgets.Text(
    value='',
    placeholder='Type a number here',
    description='Nr. of bars:',
    disabled=False
)

donut_legend_widget = widgets.Dropdown(
    options=[('Choose an option', None), ('Show legend', True), ('Hide legend', False)],
    value=None,
    description='Legend:',
    disabled=False,
)

add_filter = widgets.Combobox(
    value='',
    placeholder='Paste the DataFrame name',
    description='Data to filter:',
    ensure_option=True,
    options=['filter_by_column', 'filter_year_range', 'filter_year_operator'],
    disabled=False
)

choose_output = widgets.Combobox(
    value='',
    placeholder='Paste the file name',
    description='Download:',
    ensure_option=True,
    options=['file_1', 'file_2', 'file_3'],
    disabled=False
)

text_date_to_filter = widgets.Text(
    value='',
    placeholder='Type a start year',
    description='Year:',
    disabled=False   
)
text_date_to_filter_2 = widgets.Text(
    value='',
    placeholder='Type a end year',
    description='Year 2:',
    disabled=False   
)
widgets.Dropdown(
    options=[('One', 1), ('Two', 2), ('Three', 3)],
    value=2,
    description='Number:',
)
year_operator = widgets.Dropdown(
    options=[('Choose an operator',''),('Match exact year', '='), ('Before', '<'), ('After', '>'), ('Exact match or before', '<='), ('Exact match or after', '>=')],
    value='',
    description='Operator:',
    disabled=False,
)

input_file_dropdown = widgets.Dropdown(
    options=[('Choose a dataset', ''), ('Kornél Fabriczy (Paintings)','metadata/Fabr_pitt.xml'), ('Hilde Lotz-Bauer', 'metadata/Lotz-Bauer-Hilde.xml'), ('Candido Verri', 'metadata/Verri_Fotos.xml')],
    value='',
    description='Collection:',
    disabled=False,
)

x_widget = widgets.Dropdown(
    options=[''],
    value='',
    description='Column:',
    disabled=False,
)

y_widget = widgets.Dropdown(
    options=['bar', 'line', 'pie', 'donut'], #, 'histogram'],
    value='bar',
    description='Plot type:',
    disabled=False,
)

viz_dropdown = widgets.Dropdown(
    options=[('DF0: Initial DataFrame', 'photos_dataframe_no_digital'), ('DF1: First filtered DataFrame - by any column', 'filter_by_column'),
             ('DF2: Filtered by year range', 'filter_year_range'), ('DF3: Filtered by year and operator', 'filter_year_operator'), ('DF4: Additional filter', 'additional_filter')],
    value='photos_dataframe_no_digital',
    description='DataFrame:',
    disabled=False,
)

#Button
html_buttons = '''<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
</head>
<body>
<a download="{filename}" href="data:text/csv;base64,{payload}" download>
<button class="p-Widget jupyter-widgets jupyter-button widget-button mod-warning">Download File</button>
</a>
</body>
</html>
'''