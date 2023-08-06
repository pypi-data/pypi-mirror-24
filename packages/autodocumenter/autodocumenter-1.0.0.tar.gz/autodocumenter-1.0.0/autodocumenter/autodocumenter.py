""" Python package for generating documentation templates for codebooks of csv files.

Example:
    First, build a csv codebook with codes using generate_template. Edit this file (which
    is updated with new variable names every time generate_template is run) to produce
    documentation of variabless. Then, run generate_documentation_formats to output to
    pdf, html, and doc formats.

        $ # if pandoc not installed, install it
        $ autodocumenter.install_pandoc()
        $ autodocumenter.generate_template('name_of_file.csv', 'name_of_destination_codebook.csv')
        $ autodocumenter.generate_documentation_formats('name_of_destination_codebook.csv')
"""
import datetime
import os
import pandas
import pypandoc
from pypandoc.pandoc_download import download_pandoc
import tabulate
import pkg_resources
from shutil import copyfile
import autodocumenter

def install_pandoc():
    """ Installs pandoc, if not already installed on this computer.
    """
    download_pandoc()

def generate_template(file_location, dest_location=None):
    """ Generates and validates the template documentation codebook for this file.

    Args:
        file_location (string): Location of the data (in csv format!) to generate a template
        for.
    """
    # validate inputsexit
    if not os.path.isfile(file_location):
        raise IOError("Could not find the file " + file_location)
    filename, extension = os.path.splitext(file_location)
    basename = os.path.basename(file_location)
    if extension != '.csv':
        raise ValueError('File must be in csv format')
    # load the file
    dataset = pandas.read_csv(
        file_location,
        header=0,
        nrows=1
    )
    # destination if none is source
    if (dest_location is None):
        dest_location = filename[0:-4] + '_codebook.csv'
    # get the column names
    column_names = {
        'variable': list(dataset.columns.values),
        'codes': ['']*len(list(dataset.columns.values)),
        'description': ['']*len(list(dataset.columns.values)),
        'universe': ['']*len(list(dataset.columns.values)),
        'detailed_description': ['']*len(list(dataset.columns.values))
    }
    del dataset
    # look for existing documentation
    if not os.path.isfile(dest_location):
        codebook_values = pandas.DataFrame.from_dict(column_names)
    else:
        # look for missing variables, extraneous variables, add and delete them
        codebook_values = pandas.read_csv(dest_location)
        existing_variables = set(codebook_values.ix[:, 'variable'].tolist())
        required_variables = set(column_names['variable'])
        variables_to_delete = list(existing_variables - required_variables)
        variables_to_add = list(required_variables - existing_variables)
        if len(variables_to_delete) > 0:
            if input(
                    'Warning: Variables '
                    + ', '.join(variables_to_delete)
                    + ' are no longer in the dataset but are in '
                    + basename + '_codebook.csv. Delete them? (y/N)'
            ).lower() == 'y':
                for variable_to_delete in variables_to_delete:
                    codebook_values = codebook_values[
                        ~(codebook_values['variable'] == variable_to_delete)
                    ]
        for variable in variables_to_add:
            codebook_values = codebook_values.append(
                pandas.DataFrame(
                    {
                        'variable': variable,
                        'codes': 'CODE = 0\n CODE = 1',
                        'description': '',
                        'universe': '',
                        'detailed_description': ''
                    },
                    index=range(1)
                )
            )
    codebook_values = codebook_values.sort_values('variable')
    # write to file
    codebook_values.to_csv(
        dest_location,
        columns=['variable', 'codes', 'description', 'universe', 'detailed_description'],
        index=False
    )

def generate_documentation_formats(file_location, author):
    """ Reads the csv codebook file, uses pandoc to print to human-readable formats.

    Args:
        file_location (string): Location of the data (in csv format!) to generate
        documentation for. There already must be a codebook (generated with
        generate_template(file_location) for this to be successful.)
    """
    # validate inputs
    if not os.path.isfile(file_location):
        raise IOError(
            "Failed to find "
            + file_location[0:-4]
            + '_codebook.csv. Did you run generate_template('
            + file_location
            + ')?'
        )
    basename = os.path.basename(file_location)
    dirname = os.path.dirname(file_location)
    # load documentation file
    codebook_values = pandas.read_csv(
        file_location
    )
    codebook_values = codebook_values.fillna('')
    # pretty-print
    if not os.path.exists(os.path.join(dirname, 'codebook_readable')):
        os.makedirs(os.path.join(dirname, 'codebook_readable'))
    markdown_file = os.path.join(dirname, 'codebook_readable', basename[0:-4] + '.md')
    with open(markdown_file, "w+") as text_file:
        text_file.write(
            "---" + "\n"
            "author: " + author + "\n"
            "date: \\today\n" +
            "title: CODEBOOK FOR " + basename + '\n' +
            "---\n\n"
        )
        text_file.write('# List of variables\n\n')
        for index, row in codebook_values.iterrows():
            text_file.write('### `' + row['variable'] + '`\n')
            text_file.write('> &nbsp;\n>\n')
            text_file.write('> **Definition:** ' + row['description'] + '\n>\n')
            text_file.write('> **Codes:** ' + row['codes'] + '\n>\n')
            text_file.write('> **Universe:** ' + row['universe'] + '\n>\n')
            text_file.write('> **Notes:** ' + row['detailed_description'] + '\n>\n')
            text_file.write('> &nbsp;\n>\n\n')
        text_file.write('\n\n# Table of variable names\n\n')
        text_file.write(
            tabulate.tabulate(
                codebook_values,
                headers=[
                    'Variable:',
                    'Codes:',
                    'Description:',
                    'Universe:',
                    'Notes:'
                ],
                tablefmt='grid',
                showindex=False
            )
        )
    # copy template in
    template_path = pkg_resources.resource_filename('autodocumenter', 'templates/template.html')
    css_path = pkg_resources.resource_filename('autodocumenter', 'templates/template.css')
    copyfile(css_path, os.path.join(dirname, 'codebook_readable', 'template.css'))
    pypandoc.convert(
        markdown_file,
        outputfile=os.path.join(dirname, 'codebook_readable', basename[0:-4] + '.html'),
        format='md',
        to='html',
        extra_args=['--template', template_path, '--css', 'template.css', '--toc', '--toc-depth', '2'])
    pypandoc.convert(
        markdown_file,
        outputfile=os.path.join(dirname, 'codebook_readable', basename[0:-4] + '.pdf'),
        format='md',
        to='pdf')
    pypandoc.convert(
        markdown_file,
        outputfile=os.path.join(dirname, 'codebook_readable', basename[0:-4] + '.docx'),
        format='md',
        to='docx'
    )
