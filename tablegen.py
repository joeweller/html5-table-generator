from bs4 import BeautifulSoup
from copy import copy


class Html5TableGenerator:
    """
    create html5 table from 2d data list or csv/tsv file

    usage

    from tablegen import Html5TableGenerator

    html_table = Html4TableGenerator(

    data=[['heading1', 'heading2', ], ['data1', 'data2', ], ]  # 2d list of values

    file='PATH_TO_FILE.CSV'  # path to file

    file_type='csv' -OR- 'tsv'  # choose between csv or tsv

    bs=False  # bootstrap classes

    clean=True  # to clean data from csv/tsv file only

    footer=true  # include footer headings in html

    )

    data or file can be used only be used independently, and may not be used together
    """

    def __str__(self):
        """return html or current status of object"""
        return self.html_output

    def __init__(self, data=None, file=None, file_type=None, bs=False, clean=False, footer=False):
        """init check arguments and corner cases for failed tables"""

        self.return_string = '<Empty HTNL Table>'

        # test for either data or file. raise error on both or none
        if not data and not file or data and data:
            raise ValueError('specify one: either data list or file')

        # test for correct file_type if file is specified
        if file and file_type not in ['csv', 'tsv']:
            raise ValueError('specify file_type: csv, tsv')

        # test type of file
        if file and not type(file) == str:
            raise ValueError('file must be string location')

        # test type of data
        if data and not type(data) == list:
            raise ValueError('data must be nested list')

        self.data = data  # nested list of data
        self.file = file  # location of csv/tsv file
        self.file_type = file_type  # csv or tsv required
        self.bs = bs  # true to include bootsrap classes
        self.clean = clean  # true if data list needs stripping
        self.footer = footer  # true if footer required
        self.html_output = None  # default value for output

        if self.file:
            self.data = self.get_data_from_file()

        elif self.data and self.clean:
            self.data = self.clean_data(self.data)

        self.html_output = self.generate_table(self.data, bs=self.bs, footer=self.footer)

    def get_data_from_file(self):
        """Get data from specified file"""

        # check file_type and format accordingly
        if self.file_type == 'csv':
            separator = ','
        elif self.file_type == 'tsv':
            separator = '\t'
        else:
            raise ValueError('file_type unknown. use tsv/csv')

        data = []  # return list of data. 2d array

        # open file and create 2d data array
        with open(self.file, 'r') as file:
                for line in file:

                    # split line by file_type
                    _ = line.split(separator)

                    # clean data from file
                    for i in range(len(_)):
                        _[i] = _[i].strip()

                    # append clean data to data list
                    data.append(_)

        return data

    @staticmethod
    def clean_data(raw_data):
        """clean supplied 2d array as requested"""

        data = []  # return list of data. 2d array

        # loop raw data and clean
        for i in raw_data:
            _ = []
            for j in i:
                _.append(j.strip())

            data.append(_)

        return data

    @staticmethod
    def generate_table(data, bs=False, footer=False):
        """Generate HTML table from clean data. return in class str"""

        # return complete table
        table = BeautifulSoup('<table></table>', 'html.parser')

        # add bs class to table
        if bs:
            table.table['class'] = 'table'

        # utility object
        new = BeautifulSoup('', 'html.parser')

        # initial thead tree
        thead_tree = BeautifulSoup('<thead></thead>', 'html.parser')

        # initial tfoot tree
        tfoot_tree = BeautifulSoup('<tfoot></tfoot>', 'html.parser')

        # initial tbody tree
        tbody_tree = BeautifulSoup('<tbody></tbody>', 'html.parser')

        # counter to determine thead/tfoot vs tbody
        thead_counter = 0

        for cd in data:

            # switch case for th (thead/tfoot) or td (tbody) tags
            if not thead_counter:
                c_tag = 'th'  # child tag
            else:
                c_tag = 'td'  # child tag

            # tr tree to be appended to thead/tfoot/tbody
            tr_tree = BeautifulSoup('', 'html.parser').new_tag('tr')

            # unpick each element in lower list
            for c in cd:

                n = new.new_tag(c_tag)

                # add bootstrap scope to th
                if c_tag == 'th' and bs:
                    n['scope'] = 'col'

                n.string = c
                tr_tree.append(n)

            # case to add to either thead/tfoot or tbody trr
            if not thead_counter:
                thead_tree.thead.append(copy(tr_tree))
                tfoot_tree.tfoot.append(copy(tr_tree))
            else:
                tbody_tree.tbody.append(tr_tree)

            thead_counter = 1

        # append values to final table
        table.table.append(thead_tree)

        # if specified add footer table
        if footer:
            table.table.append(tfoot_tree)

        table.table.append(tbody_tree)

        # add indentation to html
        html_output = table.prettify()

        # return
        return html_output

    def output(self):
        """return complete table as string"""
        if self.html_output:
            return self.html_output
        else:
            return 'Html5TableGenerator - None'
