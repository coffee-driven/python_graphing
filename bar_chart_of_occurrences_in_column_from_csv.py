#!/usr/bin/env python3

import numpy as np
import plotly.express as px
import pandas as pd
import pathlib
import argparse

class barChartFromCsvColumn:
    def __init__(self, path, column_name, sep=','):
        
        self.column = []

        _data_frame = pd.read_csv(path, sep=sep)
        self.column = list(_data_frame.get(column_name))
        np.array(self.column)

    def graph_uniq_values(self,count=True, desc=False, graph_name='Uniq values', limit=10, x_name='values', y_name='no.'):

        if count:
            _dict_column_name_number_of_occurrences = {}
            _list_keys = []
            _list_values = []
            
            _column_name, _number_of_occurrences = np.unique(self.column, return_counts=True)

            for _key,_value in zip(_column_name, _number_of_occurrences):
                _dict_column_name_number_of_occurrences[_key] = _value 
            
            self.sorted_list_of_tuples = sorted(_dict_column_name_number_of_occurrences.items(), key=lambda x: x[1])
            
            # Create dict of $limit records
            _iteration=0
            if desc:
                for _key,_value in reversed(self.sorted_list_of_tuples):
                    if _iteration < limit:
                        _list_keys.append(_key)
                        _list_values.append(_value)
                        _iteration += 1
            else:
                for _key,_value in self.sorted_dict_column_name_number_of_occurrences:
                    if _iteration < limit:
                        _list_keys.append(_key)
                        _list_values.append(_value)
                        _iteration += 1
      
            _list_tuples = list(zip(_list_keys,_list_values))
            
            self.data_frame = pd.DataFrame(_list_tuples, columns=[x_name, y_name])
            
            fig = px.bar(
                data_frame=self.data_frame,
                x=x_name,
                y=y_name,
                color=x_name,
                color_discrete_sequence=["red", "red", "red", "orange", "orange", "orange", "orange", "orange", "orange", "orange"],
                hover_name=x_name,
                hover_data={x_name: True, y_name: True},
                title=graph_name
            )
            return(fig)
        else:
            _column_name = np.unique(self.column)

def main():
    bar_chart = barChartFromCsvColumn(args.csv_data, args.column)

    graph = bar_chart.graph_uniq_values(
        graph_name=args.graph_name, 
        limit=args.limit, 
        x_name=args.x_name, 
        y_name=args.y_name, desc=True)
    
    if args.create_html:
      graph.write_html(str(args.graph_name) + '.html')  
    else:
      graph.show()


if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument('-c',
                        '--column_name',
                        required=True,
                        type=str,
                        action='store',
                        dest='column',
                        help='''Column name''')
    parser.add_argument('--create_html',
                        action='store_true',
                        help='''Create interactive HTML representation''')
    parser.add_argument('-csv', 
                        '--csv_file',
                        required=True, 
                        type=pathlib.Path,
                        action='store',
                        dest='csv_data',
                        help='''Path to CSV data file''')
    parser.add_argument('-l',
                        '--limit',
                        type=int,
                        action='store',
                        default= 5,
                        dest='limit',
                        help='''Number of records to graph (number of bars in graph)''')
    parser.add_argument('-name',
                        '--name_of_graph',
                        type=str,
                        action='store',
                        dest='graph_name',
                        help='''The name of this graph''')
    parser.add_argument('--x_axe',
                        type=str,
                        action='store',
                        dest='x_name',
                        default='X AXE',
                        help='''The name of X axe''')
    parser.add_argument('--y_axe',
                        type=str,
                        action='store',
                        dest='y_name',
                        default='Y AXE',
                        help='''The name of Y axe''')

    args = parser.parse_args()

    main()
