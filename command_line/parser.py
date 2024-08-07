

class Parser:
    '''Parse the text based arguments in the shell'''
    def __init__(self, inputs):
        self.locations = None
        self.split_input = inputs.split()
        self.location_dict = dict()
        self.category_dict = dict()
        self.dates_dict = dict()
        self.file = None
        self.func_dict = {
            'list': None,
            'connect': None,
            'peek': None,
            'graph': None
        }
        self.func_list = list(filter(lambda func : func in self.func_dict,
                                     self.split_input))
    def arg_organizer(self):
        if len(self.split_input) < 3:
            self.category_dict[self.split_input[-1]] = self.split_input[-1]
        elif len(self.split_input) > 2:
            self.dates_dict[self.split_input[-1]] = self.split_input[-1].split('-')
            if "&" in self.split_input[-2]:
                self.locations = self.split_input[-2].split('&')
                for loc in self.locations:
                    self.location_dict[loc] = self._internal_parse(loc)

            else:
                self.location_dict[self.split_input[-2]] = self._internal_parse(self.split_input[-2])
            self.category_dict[self.split_input[-3]] = self.split_input[-3]


    def _internal_parse(self, var):
            return var.replace('-', ' ') if '-' in var else var






