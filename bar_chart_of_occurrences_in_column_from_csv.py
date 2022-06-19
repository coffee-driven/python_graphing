#!/usr/bin/env python3

import numpy as np
import plotly.express as px
import pandas as pd
import pathlib
import argparse

class createGraphFromCsvColumn:
    def __init__(self, path, column_name, sep=','):
        _data_frame = pd.read_csv(path, sep=sep)
        _column = list(_data_frame.get(column_name))
        np.array(_column)

        _dict_values_counts = {}
        _values, _counts = np.unique(_column, return_counts=True)

        for key,value in zip(_values, _counts):
            _dict_values_counts[key] = value 
        
        self.sorted_dict_values_counts = sorted(_dict_values_counts.items(), key=lambda x: x[1])
    
    def get_repeated_occurrences(self, depth, graph_name, x_name, y_name, desc=False):
        _iteration=0
        _list_keys = []
        _list_values = []
        
        # Create dict of $depth records
        if desc:
            for key,value in reversed(self.sorted_dict_values_counts):
                if _iteration < depth:
                    _list_keys.append(key)
                    _list_values.append(value)
                    _iteration += 1
        else:
            for key,value in self.sorted_dict_values_counts:
                if _iteration < depth:
                    _list_keys.append(key)
                    _list_values.append(value)
                    _iteration += 1

        _list_tuples = list(zip(_list_keys,_list_values))
        
        df = pd.DataFrame(_list_tuples, columns=[x_name, y_name])
        
        fig = px.bar(
            data_frame=df,
            x=x_name,
            y=y_name,
            color=x_name,
            color_discrete_sequence=["red", "red", "red", "orange", "orange", "orange", "orange", "orange", "orange", "orange"],
            hover_name=x_name,
            hover_data={x_name: True, y_name: False},
            title=graph_name
        )
        
        return(fig)

def main():
    data = createGraphFromCsvColumn(args.csv_data, args.column)
    graph = data.get_repeated_occurrences(args.depth, args.graph_name, args.x_name, args.y_name, desc=True)
    
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
    parser.add_argument('-d',
                        '--depth',
                        type=int,
                        action='store',
                        default= 5,
                        dest='depth',
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
