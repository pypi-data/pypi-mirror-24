# -*- coding: utf-8 -*-

# Copyright (c) 2016-2017 by University of Kassel and Fraunhofer Institute for Wind Energy and
# Energy System Technology (IWES), Kassel. All rights reserved. Use of this source code is governed
# by a BSD-style license that can be found in the LICENSE file.

import json
import numbers
import os
import sys
import pickle
import pandas as pd

import numpy

from pandapower.auxiliary import pandapowerNet
from pandapower.create import create_empty_network
from pandapower.toolbox import convert_format
from pandapower.io_utils import to_dict_of_dfs, collect_all_dtypes_df, dicts_to_pandas, \
                                from_dict_of_dfs, restore_all_dtypes

def to_pickle(net, filename):
    """
    Saves a pandapower Network with the pickle library.

    INPUT:
        **net** (dict) - The pandapower format network

        **filename** (string) - The absolute or relative path to the output file or an writable file-like objectxs

    EXAMPLE:

        >>> pp.to_pickle(net, os.path.join("C:", "example_folder", "example1.p"))  # absolute path
        >>> pp.to_pickle(net, "example2.p")  # relative path

    """
    if hasattr(filename, 'write'):
        pickle.dump(dict(net), filename, protocol=2)
        return
    if not filename.endswith(".p"):
        raise Exception("Please use .p to save pandapower networks!")
    save_net = dict()
    for key, item in net.items():
        if key != "_is_elements":
            save_net[key] = {"DF": item.to_dict("split"), "dtypes": {col: dt
                            for col, dt in zip(item.columns, item.dtypes)}}  \
                            if isinstance(item, pd.DataFrame) else item
    with open(filename, "wb") as f:
        pickle.dump(save_net, f, protocol=2) #use protocol 2 for py2 / py3 compatibility


def to_excel(net, filename, include_empty_tables=False, include_results=True):
    """
    Saves a pandapower Network to an excel file.

    INPUT:
        **net** (dict) - The pandapower format network

        **filename** (string) - The absolute or relative path to the output file

    OPTIONAL:
        **include_empty_tables** (bool, False) - empty element tables are saved as excel sheet

        **include_results** (bool, True) - results are included in the excel sheet

    EXAMPLE:

        >>> pp.to_excel(net, os.path.join("C:", "example_folder", "example1.xlsx"))  # absolute path
        >>> pp.to_excel(net, "example2.xlsx")  # relative path

    """
    writer = pd.ExcelWriter(filename, engine='xlsxwriter')
    dict_net = to_dict_of_dfs(net, include_results=False, create_dtype_df=True)
    dict_net["dtypes"] = collect_all_dtypes_df(net)
    for item, table in dict_net.items():
        table.to_excel(writer, sheet_name=item)
    writer.save()


def to_json_string(net):
    """
        Returns a pandapower Network in JSON format. The index columns of all pandas DataFrames will
        be saved in ascending order. net elements which name begins with "_" (internal elements)
        will not be saved. Std types will also not be saved.

        INPUT:
            **net** (dict) - The pandapower format network

            **filename** (string) - The absolute or relative path to the input file.

        EXAMPLE:

             >>> json = pp.to_json_string(net)

    """
    json_string = "{"
    for k in sorted(net.keys()):
        if k[0] == "_":
            continue
        if isinstance(net[k], pd.DataFrame):
            json_string += '"%s":%s,' % (k, net[k].to_json(orient="columns"))
        elif isinstance(net[k], numpy.ndarray):
            json_string += k + ":" + json.dumps(net[k].tolist()) + ","
        elif isinstance(net[k], dict):
            json_string += '"%s":%s,' % (k, json.dumps(net[k]))
        elif isinstance(net[k], bool):
            json_string += '"%s":%s,' % (k, "true" if net[k] else "false")
        elif isinstance(net[k], str):
            json_string += '"%s":"%s",' % (k, net[k])
        elif isinstance(net[k], numbers.Number):
            json_string += '"%s":%s,' % (k, net[k])
        elif net[k] is None:
            json_string += '"%s":null,' % k
        else:
            raise UserWarning("could not detect type of %s" % k)
    json_string = json_string[:-1] + "}\n"
    return json_string


def to_json(net, filename=None):
    """
        Saves a pandapower Network in JSON format. The index columns of all pandas DataFrames will
        be saved in ascending order. net elements which name begins with "_" (internal elements)
        will not be saved. Std types will also not be saved.

        INPUT:
            **net** (dict) - The pandapower format network

            **filename** (string or file) - The absolute or relative path to the output file or file-like object

        EXAMPLE:

             >>> pp.to_json(net, "example.json")

    """
    dict_net = to_dict_of_dfs(net, include_results=False, create_dtype_df=True)
    dict_net["dtypes"] = collect_all_dtypes_df(net)
    json_string = to_json_string(dict_net)
    if hasattr(filename, 'write'):
        filename.write(json_string)
        return
    with open(filename, "w") as text_file:
        text_file.write(json_string)


def to_sql(net, con, include_empty_tables=False, include_results=True):
    dodfs = to_dict_of_dfs(net, include_results=include_results)
    dodfs["dtypes"] = collect_all_dtypes_df(net)
    for name, data in dodfs.items():
        data.to_sql(name, con, if_exists="replace")


def to_sqlite(net, filename):
    import sqlite3
    conn = sqlite3.connect(filename)
    to_sql(net, conn)
    conn.close()


def from_pickle(filename, convert=True):
    """
    Load a pandapower format Network from pickle file

    INPUT:
        **filename** (string or file) - The absolute or relative path to the input file or file-like object

    OUTPUT:
        **net** (dict) - The pandapower format network

    EXAMPLE:

        >>> net1 = pp.from_pickle(os.path.join("C:", "example_folder", "example1.p")) #absolute path
        >>> net2 = pp.from_pickle("example2.p") #relative path

    """
    def read(f):
        if sys.version_info >= (3,0):
            return pickle.load(f, encoding='latin1')
        else:
            return pickle.load(f)
    if hasattr(filename, 'read'):
        net = read(filename)
    elif not os.path.isfile(filename):
        raise UserWarning("File %s does not exist!!" % filename)
    else:
        with open(filename, "rb") as f:
            net = read(f)
    net = pandapowerNet(net)
    for key, item in net.items():
        if isinstance(item, dict) and "DF" in item:
            df_dict = item["DF"]
            if "columns" in item["DF"]:
                net[key] = pd.DataFrame(columns=df_dict["columns"],
                                                  index=df_dict["index"],
                                                  data=df_dict["data"])
            else:
                net[key] = pd.DataFrame.from_dict(item["DF"])
                if "columns" in item:
                    net[key] = net[key].reindex_axis(item["columns"], axis=1)
            if "dtypes" in item:
                try:
                    #only works with pandas 0.19 or newer
                    net[key] = net[key].astype(item["dtypes"])
                except:
                    #works with pandas <0.19
                    for column in net[key].columns:
                        net[key][column] = net[key][column].astype(item["dtypes"][column])
    if convert:
        convert_format(net)
    return net


def from_excel(filename, convert=True):
    """
    Load a pandapower network from an excel file

    INPUT:
        **filename** (string) - The absolute or relative path to the input file.

    OUTPUT:
        **convert** (bool) - use the convert format function to

        **net** (dict) - The pandapower format network

    EXAMPLE:

        >>> net1 = pp.from_excel(os.path.join("C:", "example_folder", "example1.xlsx")) #absolute path
        >>> net2 = pp.from_excel("example2.xlsx") #relative path

    """

    if not os.path.isfile(filename):
        raise UserWarning("File %s does not exist!" % filename)
    xls = pd.ExcelFile(filename).parse(sheetname=None)
    try:
        net = from_dict_of_dfs(xls)
        restore_all_dtypes(net, xls["dtypes"])
    except:
        net = _from_excel_old(xls)
    if convert:
        convert_format(net)
    return net


def _from_excel_old(xls):
    par = xls["parameters"]["parameters"]
    name = None if pd.isnull(par.at["name"]) else par.at["name"]
    net = create_empty_network(name=name, f_hz=par.at["f_hz"])

    for item, table in xls.items():
        if item == "parameters":
            continue
        elif item.endswith("std_types"):
            item = item.split("_")[0]
            for std_type, tab in table.iterrows():
                net.std_types[item][std_type] = dict(tab)
        elif item == "line_geodata":
            points = int(len(table.columns) / 2)
            for i, coords in table.iterrows():
                coord = [(coords["x%u" % nr], coords["y%u" % nr]) for nr in range(points)
                         if pd.notnull(coords["x%u" % nr])]
                net.line_geodata.loc[i, "coords"] = coord
        else:
            net[item] = table
    return net

def from_json(filename, convert=True):
    """
    Load a pandapower network from a JSON file.
    The index of the returned network is not necessarily in the same order as the original network.
    Index columns of all pandas DataFrames are sorted in ascending order.

    INPUT:
        **filename** (string or file) - The absolute or relative path to the input file or file-like object

    OUTPUT:
        **convert** (bool) - use the convert format function to

        **net** (dict) - The pandapower format network

    EXAMPLE:

        >>> net = pp.from_json("example.json")

    """
    if hasattr(filename, 'read'):
        data = json.load(filename)
    elif not os.path.isfile(filename):
        raise UserWarning("File %s does not exist!!" % filename)
    else:
        with open(filename) as data_file:
            data = json.load(data_file)
    try:
        pd_dicts = dicts_to_pandas(data)
        net = from_dict_of_dfs(pd_dicts)
        restore_all_dtypes(net, pd_dicts["dtypes"])
        if convert:
            convert_format(net)
        return net
    except UserWarning:
        # Can be deleted in the future, maybe now
        return from_json_dict(data, convert=convert)


def from_json_string(json_string, convert=True):
    """
    Load a pandapower network from a JSON string.
    The index of the returned network is not necessarily in the same order as the original network.
    Index columns of all pandas DataFrames are sorted in ascending order.

    INPUT:
        **json_string** (string) - The json string representation of the network

    OUTPUT:
        **convert** (bool) - use the convert format function to

        **net** (dict) - The pandapower format network

    EXAMPLE:

        >>> net = pp.from_json_string(json_str)

    """
    data = json.loads(json_string)
    return from_json_dict(data, convert=convert)


def from_json_dict(json_dict, convert=True):
    """
    Load a pandapower network from a JSON string.
    The index of the returned network is not necessarily in the same order as the original network.
    Index columns of all pandas DataFrames are sorted in ascending order.

    INPUT:
        **json_dict** (json) - The json object representation of the network

    OUTPUT:
        **convert** (bool) - use the convert format function to

        **net** (dict) - The pandapower format network

    EXAMPLE:

        >>> net = pp.pp.from_json_dict(json.loads(json_str))

    """
    net = create_empty_network(name=json_dict["name"], f_hz=json_dict["f_hz"])

    # checks if field exists in empty network and if yes, matches data type
    def check_equal_type(name):
        if name in net:
            if isinstance(net[name], type(json_dict[name])):
                return True
            elif isinstance(net[name], pd.DataFrame) and isinstance(json_dict[name], dict):
                return True
            else:
                return False
        return True

    for k in sorted(json_dict.keys()):
        if not check_equal_type(k):
            raise UserWarning("Different data type for existing pandapower field")
        if isinstance(json_dict[k], dict):
            if isinstance(net[k], pd.DataFrame):
                columns = net[k].columns
                net[k] = pd.DataFrame.from_dict(json_dict[k], orient="columns")
                net[k].set_index(net[k].index.astype(numpy.int64), inplace=True)
                net[k] = net[k][columns]
            else:
                net[k] = json_dict[k]
        else:
            net[k] = json_dict[k]
    if convert:
        convert_format(net)
    return net


def from_sql(con):
    cursor = con.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    dodfs = dict()
    for t, in cursor.fetchall():
        table = pd.read_sql_query("SELECT * FROM %s" % t, con, index_col="index")
        table.index.name = None
        dodfs[t] = table
    net = from_dict_of_dfs(dodfs)
    restore_all_dtypes(net, dodfs["dtypes"])
    return net


def from_sqlite(filename, netname=""):
    import sqlite3
    con = sqlite3.connect(filename)
    net = from_sql(con)
    con.close()
    return net
