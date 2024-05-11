import ipywidgets as widgets

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