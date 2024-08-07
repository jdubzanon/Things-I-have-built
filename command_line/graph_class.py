import matplotlib.pyplot as plt
import csv

class MakeGraph:
    def __init__(self, location_dict, dates_dict, split_input, category_dict):
        self.location_dict = location_dict
        self.dates_dict = dates_dict
        self.split_input = split_input
        self.category_dict = category_dict
        self.graph_map = dict()
        self.years = []




    def _graph_val_mapper(self):
        self.years.clear()
        self._make_graph_map()
        file = '/media/jdubzanon/SmallStorage/csv_files/state_crime.csv'

        with open(file) as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:

                for year in range(int(self.dates_dict[self.split_input[-1]][0]),
                                  int(self.dates_dict[self.split_input[-1]][1]) + 1):
                    if not year in self.years:
                        self.years.append(year)

                    for location in self.location_dict.values():

                        if location.title() in row.values() and str(year) in row['Year']:
                            for cats in self.category_dict.values():
                                self.graph_map[location].append(float(row[cats]))



    def _make_graph_map(self):
        self.graph_map.clear()
        for location in self.location_dict.values():
            self.graph_map[location] = list()

    def create_da_graph(self):
        for key in self.graph_map.keys():
            plt.plot(self.years, self.graph_map[key], label=key)
        for key in self.category_dict.keys():
            plt.title(f'{key.title()}')
        plt.legend()

        plt.show()
