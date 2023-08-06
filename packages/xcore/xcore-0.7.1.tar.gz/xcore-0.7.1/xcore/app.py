#!/usr/bin/env python

from spacegroup import *
from unitcell import *

import numpy as np
import pandas as pd

import argparse

from __init__ import __version__


def load_hkl(fn):
    df = pd.read_table(fn, sep="\s+", header=None)
    df.columns = ("h", "k", "l", "F", "esd", "frame")[:df.columns.size]
    # try:
    #     df.frame = df.frame.astype(int) 
    # except:
    #     pass
    df = df.set_index(["h", "k", "l"])
    # df.h = df.h.astype(int) 
    # df.k = df.k.astype(int) 
    # df.l = df.l.astype(int)

    # df.index = pd.Index(df.index) # 08-09-2016 - Do not merge MultiIndex
    return df


def write_hkl(df, cols=None, out=None, no_hkl=False, pre=None, post=None, data_fmt=None, hkl_fmt=None):
    """Function for writing indices + selected columns to specified file/file object or terminal."""

    if isinstance(pre, list):
        if all('\n' in line for line in pre):
            pre = ''.join(pre)
        else:
            pre = '\n'.join(pre)
    elif isinstance(pre, str):
        pre = '\n'.join(pre.strip('\n'))

    if isinstance(post, list):
        post = ''.join(post)

    if not cols:
        cols = df.columns

    if isinstance(cols, str):
        cols = (cols,)

    if isinstance(out, str):
        out = open(out, 'w')

    cols = list(cols)

    if not hkl_fmt:
        if no_hkl:
            hkl_fmt = ''
        else:
            hkl_fmt = '{:4d}{:4d}{:4d}'

    if not data_fmt:
        ifmt = '{:4d}'
        dfmt = ' {:5d}'
        ffmt = ' {:7.2f}'
        bfmt = ' {:4}'

        data_fmt = ''

        for item in cols[:]:
            if item == '*':
                cols.remove('*')
                data_fmt += '  *  '
                continue

            #tp = repr(type(df[item][0]))
            tp = repr(df[item].dtype)
            if 'int' in tp:
                data_fmt += dfmt
            elif 'float' in tp:
                data_fmt += ffmt
            elif 'bool' in tp:
                data_fmt += bfmt
            else:
                raise TypeError, "No format associated with type {}".format(tp)
    elif data_fmt == 'shelx':
        data_fmt = '{:8.3f}{:8.3f}'

    if pre:
        print >> out, pre

    print ' >> Writing {} refs to file {}'.format(len(df), out.name if out else 'stdout')

    for row in df.reindex(columns=cols).itertuples():

        print >> out, hkl_fmt.format(*row[0])+data_fmt.format(*row[1:])

    if post:
        print >> out, post


def main():
    description = """"""

    epilog = 'Version: {}'.format(__version__)

    parser = argparse.ArgumentParser(description=description,
                                     epilog=epilog,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)

    parser = argparse.ArgumentParser()

    parser.add_argument("args",
                        type=str, metavar="spgr", nargs='*',
                        help="Filenames or space group")

    parser.add_argument("-l", "--hkllisting",
                        action="store_true", dest="hkllisting",
                        help="Print hkl listing to file out.hkl")

    parser.add_argument("-d", "--dmin",
                        action="store", type=float, dest="dmin",
                        help="Resolution to generate hkl indices with (default = 1.0)")

    parser.add_argument("-k", "--maxhkl",
                        action='store', type=int, dest="maxhkl",
                        help="Maximum hkl values to generate indices with")

    parser.add_argument("-c", "--cell",
                        action='store', type=float, nargs="+", dest="cell",
                        help="Unit cell")

    parser.add_argument("-s", "--spgr",
                        action="store", type=str, dest="spgr",
                        help="Space group to use. Tell the program to interpret args as filenames, and use one of the commands below.")

    parser.add_argument("-m", "--merge",
                        action="store_true", dest="merge",
                        help="Merge symmetry equivalent reflections in data files")

    parser.add_argument("-p", "--completeness",
                        action="store_true", dest="completeness",
                        help="Calculate completeness of given data files")

    parser.add_argument("-f", "--filter",
                        action="store_true", dest="filter",
                        help="Filter systematic absences from data files.")

    parser.set_defaults(hkllisting=False,
                        dmin=1.0,
                        maxhkl=10,
                        cell=None,
                        # file specific
                        spgr=None,
                        merge=False,
                        completeness=False,
                        filtersymequiv=False,
                        sysabs_selfcheck=False)

    options = parser.parse_args()
    args = options.args

    if options.sysabs_selfcheck:
        for s in range(1, 231):
            spgr = SpaceGroup(s)
            cell = get_random_cell(spgr)

            print spgr, cell

            cell = UnitCell(cell, spgr)
            indices = generate_hkl_listing(cell, dmin=options.dmin, as_type="np.array")
            d = cell.calc_dspacing(indices)
            i = d.argsort()[::-1]
            d = d[i].reshape(-1, 1)
            indices = indices[i]
            df = pd.DataFrame(np.hstack([indices, d]), columns=("h","k","l","inty"))
            df.h = df.h.astype(int)
            df.k = df.k.astype(int)
            df.l = df.l.astype(int)
            df = df.set_index(["h","k","l"])

            df["flag2"] = spgr.is_absent_pd(df.index)

            from cctbx import crystal
            cs = crystal.symmetry( unit_cell = cell.parameters, space_group_symbol = spgr.spgr_name)
            sg = cs.space_group()
            df["flag3"] = [sg.is_sys_absent(j) for j in df.index]
            
            if not np.all((df.flag2 == True) == (df.flag3 == True)):
                print " ** Systematic absences mismatch 32 ** "
            
            df = cell.merge(df, remove_sysabs=True, key="inty")

    if not options.spgr:

        for arg in args:
            spgr = SpaceGroup(arg)
            if not spgr:
                continue
            print "# {}\n".format(arg)
    
            if options.cell:
                cell = options.cell
                if cell[0] < 0:
                    cell = get_random_cell(spgr)
                cell = UnitCell(cell, spgr)
                cell.info()
    
            spgr.info()

            if options.hkllisting:
                if not options.cell and options.maxhkl:
                    # bit hacky, but works! :)
                    cell = (1, 1, 1, 90, 90, 90)
                    cell = UnitCell(cell, spgr)
                    options.dmin = 1/float(options.maxhkl)

                indices = np.array(generate_hkl_listing(cell, dmin=options.dmin, as_type="np.array"))
                d = np.array(cell.calc_dspacing(indices)).reshape(-1,1)

                if len(args) > 1:
                    out = 'out_{}.hkl'.format(cell.spgr)
                else:
                    out = 'out.hkl'
                np.savetxt(out, np.hstack([indices, d]), fmt="%4d%4d%4d %7.2f     1.0")

    if options.spgr:
        spgr = options.spgr
        cell = options.cell
        cell = UnitCell(cell, spgr)
        for arg in args:
            # print arg, spgr
            df = load_hkl(arg)

            if options.dmin:
                d =  cell.calc_dspacing(df.index)
                sel = d > options.dmin
                df = df[sel]

            # columns = df.columns.tolist()
            # print df, columns
            if options.merge:
                df = cell.merge(df, remove_sysabs=options.filter)
            if options.completeness:
                compl = cell.completeness(df)
                print "Completeness: {:.2%} up to {:.2f} Angstrom".format(compl, df["d"].min())

            root, ext = os.path.splitext(arg)
            out = root+"_out"+ext
            write_hkl(df, out=out, data_fmt="shelx")


if __name__ == '__main__':
    main()
