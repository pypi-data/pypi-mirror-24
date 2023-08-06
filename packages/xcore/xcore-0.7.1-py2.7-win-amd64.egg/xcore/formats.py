#!/usr/bin/env python

import os

import pandas as pd
import unitcell
import numpy as np
from multiplicity import calc_multiplicity

import shlex

def parse_float(x):
    """Split numerical part from error"""
    if isinstance(x, (str, unicode)):
        return float(x.split("(")[0])
    else:
        return x

def line_iterator(f):
    for line in f:
        line = line.strip()
        if line.startswith("#"):
            continue
        inp = shlex.split(line)
        if not inp:
            continue
        yield inp
    # stopiteration indicates end of file
    # return None to cleanly excit loop
    yield None

def extract_symbol(s):
    """Extract element symbol from atom label"""
    symbol = ""
    for letter in s:
        if not letter.isdigit():
            symbol += letter
        else:
            break
    return symbol

def read_cif(f, verbose=False):
    if isinstance(f, str):
        f = open(f, "r")
    d = {}
    incols = False
    inrows = False
    inblock = False
    fiter = line_iterator(f)
    for inp in fiter:
        if not inp:
            continue
        if inp[0] == "loop_":
            inblock = True
            while inblock == True:
                incols = True
                cols = []
                rows = []
                while incols == True:
                    try:
                        inp = fiter.next()
                    except StopIteration:
                        incols = False
                        inrows = False
                        inblock = False
                        break
                    if not inp:
                        continue
                    if inp[0].startswith("_"):
                        cols.append(inp[0])
                        continue
                    else:
                        inrows = True
                        incols = False
                while inrows == True:
                    if not inp:
                        break
                    if inp[0].startswith("_"):
                        inrows = False
                        inblock = False
                        break
                    elif inp[0] == "loop_":
                        incols == True
                        break
                    assert len(inp) == len(cols), str(cols) + " : " + str(inp)
                    rows.append(inp)
                    
                    try:
                        inp = fiter.next()
                    except StopIteration:
                        incols = False
                        inrows = False
                        inblock = False
                        break
                for i, key in enumerate(cols):
                    vals = [row[i] for row in rows]
                    d[key] = vals


        if not inp:
            continue
        elif inp[0].startswith("data_"):
            d["data_"] = inp[0][5:]
        elif len(inp) == 2:
            key, value = inp
            d[key] = value
        else:
            raise IOError("{} -> Could not read line: {}".format(f.name, inp))
    
    cif2simple = {
    '_atom_site_label': "label",
    '_atom_site_type_symbol': "symbol",
    '_atom_site_symmetry_multiplicity': 'm',
    '_atom_site_fract_x': "x",
    '_atom_site_fract_y': "y",
    '_atom_site_fract_z': "z",
    '_atom_site_occupancy': "occ",
    "_atom_site_adp_type": "adp_type",
    '_atom_site_U_iso_or_equiv': "uiso",
    '_atom_site_B_iso_or_equiv': "biso" }

    a = parse_float( d.pop("_cell_length_a") )
    b = parse_float( d.pop("_cell_length_b") )
    c = parse_float( d.pop("_cell_length_c") )
    al = parse_float( d.pop("_cell_angle_alpha") )
    be = parse_float( d.pop("_cell_angle_beta") )
    ga = parse_float( d.pop("_cell_angle_gamma") )
    sg = d.pop("_symmetry_space_group_name_H-M").replace(" ", "")
    name = d.pop("data_")
    
    cell = unitcell.UnitCell((a,b,c,al,be,ga), sg, name=name)

    cols = [key for key in d.keys() if key.startswith("_atom")]
    vals = [d[key] for key in cols]
    
    # adps
    # adp_type = d["_atom_site_adp_type"] # "Biso", "Uiso", Uani"
    # Uiso: _atom_site_U_iso_or_equiv
    # Biso: _atom_site_B_iso_or_equiv
    # Uani: 
        # "_atom_site_aniso_label"
        # "_atom_site_aniso_U_11"
        # "_atom_site_aniso_U_22"
        # "_atom_site_aniso_U_33"
        # "_atom_site_aniso_U_23"
        # "_atom_site_aniso_U_13"
        # "_atom_site_aniso_U_12"
    
    atoms = pd.DataFrame([list(row) for row in zip(*vals)], columns=[cif2simple[key] for key in cols])

    for col in ["x", "y", "z", "occ", "biso", "uiso"]:
        if col in atoms:
            atoms[col] = atoms[col].apply(parse_float)

    if "uiso" in atoms:
        atoms["biso"] = 8*np.pi**2*atoms["uiso"]
    if not "m" in atoms:
        atoms["m"] = atoms.apply(calc_multiplicity, args=(cell,), axis=1)
    else:
        atoms["m"] = atoms["m"].astype(int)
        if not all(atoms["m"] == atoms.apply(calc_multiplicity, args=(cell,), axis=1)):
            mults = atoms.apply(calc_multiplicity, args=(cell,), axis=1)
            sel = atoms["m"] != mults
            print "From cif:",
            print atoms[sel]
            print 
            print "Calculated\n"
            print mults[sel]
            raise AssertionError("{} -> multiplicities from cif and calculated are different".format(f.name))
    
    if "occ" not in atoms:
        atoms["occ"] = 1.0
    if "biso" not in atoms:
        atoms["biso"] = 1.5
    if "symbol" not in atoms:
        atoms["symbol"] = atoms["label"].apply(extract_symbol)

    atoms = atoms[["label", "symbol", "m", "x", "y", "z", "occ", "biso"]]
  
    cell.info()

    if verbose:
        print atoms
    else:
        print "Read {} atom positions from file {} ({}: {})".format(len(atoms), f.name, name, cell.hermann_mauguin)
    
    return cell, atoms


def write_cif(cell, atoms):
	try:
		cell.write_cif_block()
		atoms.write_cif_block()
	except:
		raise NotImplementedError


def read_hkl(fn):
    df = pd.read_table(fn, sep="\s*", engine="python", index_col=[0,1,2], header=None, names="h k l inty esd".split())
    df.index = pd.Index(df.index)
    return df


def write_hkl(df, out=None):
    if isinstance(out, str):
        out = open(out, "w")
    if not "sigma" in df:
        df["sigma"] = 1.0
    for (h, k, l), row in df.iterrows():
        print >> out, "{:4d} {:4d} {:4d} {:12.4f} {:12.4f}".format(h, k, l, row["inty"], row["esd"])


def write_shelx_ins(cell, wavelength=1.0000, out='shelx.ins', composition={}, tr_mat=None):
    """Simple function that writes a basic shelx input file

    cell: UnitCell class
    tr_mat: Matrix to put in TRMX card"""
    if isinstance(out,str):
        out = open(out,'w')

    params = cell.parameters
    Z = cell.order

    print >> out, "TITL", cell.name
    print >> out, "CELL {} {} {} {} {} {} {}".format(wavelength,*params)
    print >> out, "ZERR {}  0  0  0  0  0  0".format(Z)
    C = cell.centering_symbol
    LATT = {"P": 1, "I": 2, "R": 3, "F": 4, "A": 5, "B": 6, "C": 7}[C]

    if not cell.isCentrosymmetric():
        LATT = -LATT

    print >> out, "LATT {}".format(LATT)
    from xcore.spacegroup import SymOp
    nSMx = cell.sg.get_nSMx()
    for k in xrange(1,nSMx):   # symmetry operators
        Mx = cell.sg.getLISMx(0, 0, k, +1)
        print >> out, "SYMM", repr(SymOp(Mx)).upper()

    print >> out
    if composition:
        for key in composition:
            print >> out, "SFAC {}".format(key)
        print >> out, "UNIT", " ".join([str(composition[key]) for key in composition])
        print >> out

    if tr_mat:
        print >> out, 'TRMX {} {} {} {} {} {} {} {} {} 0 0 0'.format(*tr_mat)
        print >> out

    print >> out, 'TREF 500'
    print >> out, 'HKLF 4'
    print >> out, 'END'


def write_sir2014_inp(cell, hklfile, wavelength=1.000, out="sir2014.sir", radiation=None, formula=None, hklfmt="(3i4,f8.0,f8.1)"):
    """Simple function that writes a basic sir2014 input file

    cell: UnitCell class
    hklfile: path to hkl file"""

    import time
    if isinstance(out,str):
        out = open(out,'w')
    
    params = cell.parameters

    print >> out, "%Structure", cell.name
    print >> out, "%Job", cell.name,  time.strftime("%d-%m-%Y")
    print >> out, "%Data"

    print >> out, "    Cell", " ".join(map(str, params))
    print >> out, "    Space", cell.hermann_mauguin
    if formula:
        print >> out, "    Formula", formula
    if radiation:
        print >> out, "    {}".format(radiation.capitalize())
    print >> out, "    Reflections", hklfile
    print >> out, "    Format", hklfmt
    print >> out, "    Fosq"
    print >> out, "%Phase"
    print >> out, "%%End"


def write_superflip_inp(cell, wavelength, composition, datafile, dataformat, filename='sf.inflip'):
    if isinstance(composition, dict):
        composition = unitcell.dict2comp(composition)

    fout = open(filename, 'w')

    print >> fout, 'title', filename.split('.')[0]
    print >> fout
    print >> fout, 'dimension 3'
    print >> fout, 'voxel',
    for p in cell.parameters[0:3]:
        print >> fout, int(((p*4) // 6 + 1) * 6),
    print >> fout
    print >> fout, 'cell',
    for p in cell.parameters:
        print >> fout, p,
    print >> fout, '  # vol = {:.4f} A3 \n'.format(cell.volume)

    print >> fout, 'centers'
    for cvec in cell.centering_vectors:
        print >> fout, "    {} {} {}".format(*cvec)
    print >> fout, 'endcenters\n'

    print >> fout, 'symmetry #', cell.hermann_mauguin
    for symop in cell._symmetry_operations(verbose=True):
        print >> fout, symop

    print >> fout, 'endsymmetry\n'
    print >> fout, 'derivesymmetry yes'
    print >> fout, 'searchsymmetry average'
    print >> fout
    print >> fout, 'delta AUTO'
    print >> fout, 'weakratio 0.00'
    print >> fout, 'biso 2.0'
    print >> fout, 'randomseed AUTO'
    print >> fout
    if composition:
        print >> fout, 'composition {}'.format(composition)
        print >> fout, 'histogram composition'
        print >> fout, 'hmparameters 10 5'
    else:
        print >> fout, '#composition #composition goes here'
        print >> fout, '#histogram composition'
        print >> fout, '#hmparameters 10 5'
    print >> fout
    print >> fout, 'fwhmseparation 0.3'
    print >> fout, 'lambda {}'.format(wavelength)
    print >> fout
    print >> fout, 'maxcycles 200'
    print >> fout, 'bestdensities 10'
    print >> fout, 'repeatmode 100'
    print >> fout
    print >> fout, 'polish yes'
    print >> fout, 'convergencemode never'
    print >> fout
    print >> fout, '#referencefile filename.cif'
    print >> fout, '#modelfile filename.cif 0.2'
    print >> fout
    print >> fout, 'terminal yes'
    print >> fout, 'expandedlog yes'
    outputfile = "superflip"
    print >> fout, 'outputfile {}.xplor {}.ccp4'.format(outputfile, outputfile)
    print >> fout, 'outputformat xplor ccp4'
    print >> fout
    print >> fout, 'dataformat', dataformat
    print >> fout, 'fbegin {}\n'.format(datafile)

    print "\n >> Wrote superflip input file {}".format(filename)


def write_focus_inp(cell, df=None, out="foc.inp", key="amplitude"):
    if isinstance(out, str):
        out = open(out, "w")
    template = """
# Focus input generated by xcore.formats.write_focus_inp

Title {name}
SpaceGroup  {spgr}
UnitCell   {a} {b} {c} {al} {be} {ga}   # {volume}

# AtomType Use Class ScatFact #PerUnitCell OccDefault UisoDefault Radius
# AtomType  +  Node  Si  8
AtomType  +  Node        Si  {nSi}
AtomType  -  NodeBridge  O   {nO}

# Chemistry  MinDistance  Node  Si  Node  Si  2.6
Chemistry  MinDistance  Node        Si  Node        Si  2.6
Chemistry  MinDistance  Node        Si  NodeBridge  O   1.4
Chemistry  MinDistance  NodeBridge  O   NodeBridge  O   2.3

MaxPotentialAtoms  {mpa}
MaxRecycledAtoms   {mra}

FwSearchMethod  FwTracking
MaxPeaksFwSearch  {mpfs}
MaxPeaksFwFragmentSearch  {mpffs}
MinNodeDistance  2.6
MaxNodeDistance  3.7
MinSymNodes  0
MaxSymNodes  {mpa}
NodeType  4  *  -6 -3 -1 4 6
MinLoopSize  4
MaxLoopSize  24
EvenLoopSizesOnly  Off
Check3DimConnectivity  On
IdealT_NodeDistance  3.1
CheckTetrahedralGeometry  Normal

RandomInitialization  Time
FeedBackCycles  1 1 1 1 1 1 1 1 1 1
FeedBackBreakIf  PhaseDiff < 5.00 % and DeltaR < 1.00 %

Grid_xyz  {gridx} {gridy} {gridz}
PeakSearchLevel  3
eDensityCutOff  1 %
MinPfI  17
CatchDistance  0.5
eD_PeaksSortElement  Grid_eD

Lambda  {wl}
FobsMin_d  1
FobsScale  1 # Fabs = Fobs * FobsScale
SigmaCutOff  0
OverlapFactor  0.0
OverlapAction  NoAction
ReflectionUsage  200

# Site  Label  ScatFact  x  y  z  Occ  Uiso
# Site  Si4  Si4+   0.00000   0.00000   0.00000    1.00    0.035

#  h    k    l         Fobs      Sigma     FWHM
{data}
End
"""
    if cell.composition:
        nSi = cell.composition["Si"]
        nO  = cell.composition["O"]
    else:
        nSi = int(20 * cell.volume / 1000.0) / 2 * 2 # make divisible by 2
        nO  = 2*nSi
    
    mpa = int(nSi)
    mra = int(2*nSi)
    mpfs = int(1.5*(nSi + nO))
    mpffs = int(1.5*nSi)
    
    gridx = int(((cell.a*3) // 6 + 1) * 6)
    gridy = int(((cell.b*3) // 6 + 1) * 6)
    gridz = int(((cell.c*3) // 6 + 1) * 6)
    
    data = "# Data goes here\n# ...\n# ...\n# ..."
    if df is not None:
        if key == "amplitude" and key not in df and "inty" in df:
            df[key] = df["inty"] ** 0.5
        if key in df:
            data = "\n".join(["{:4d} {:4d} {:4d} {:12.4f}".format(h, k, l, row["amplitude"]) for (h, k, l), row in df.iterrows()])
        else:
            print " >> Data format not understood, provide a df with amplitude/inty"
                             
    print >> out, template.format(
        name=cell.name,
        spgr=cell.spgr_name,
        a=cell.a,
        b=cell.b,
        c=cell.c,
        al=cell.al,
        be=cell.be,
        ga=cell.ga,
        volume=cell.volume,
        gridx=gridx,
        gridy=gridy,
        gridz=gridz,
        nSi=nSi,
        nO=nO,
        mpa=mpa,
        mra=mra,
        mpfs=mpfs,
        mpffs=mpffs,
        wl=1.0,
        data=data
    )
    print "\n >> Wrote focus input file {}".format(out.name)


def make_superflip_entry(filename='sf.inflip'):
    """Creates a basic superflip input file for structure solution by asking a few simple questions"""

    for x in xrange(3):
        cell = raw_input("Enter cell parameters:\n >> ")

        cell = cell.split()
        if len(cell) != 6:
            print 'Expecting 6 parameters: a b c alpha beta gamma'
            continue
        else:
            try:
                cell = tuple(map(float, cell))
            except ValueError, e:
                print 'ValueError:', e
                continue
            else:
                break

    for x in xrange(3):
        spgr = raw_input('Enter space group:\n >> ')

        if not spgr.split():
            continue
        else:
            break

    wavelength = raw_input('Enter wavelength\n >> [1.54056] ') or '1.54056'
    composition = raw_input('Enter composition:\n >> [skip] ') or ''
    datafile = raw_input('Enter datafile:\n >> [fobs.out] ') or 'fobs.out'

    for x in xrange(3):
        dataformat = raw_input(
            'Enter dataformat:\n >> [intensity fwhm] ') or 'intensity fwhm'
        if not all(i in ('intensity', 'amplitude', 'amplitude difference', 'a', 'b', 'phase', 'group', 'dummy', 'fwhm', 'm91', 'm90', 'shelx')
                   for i in dataformat.split()):
            print 'Unknown dataformat, please enter any of\n intensity/amplitude/amplitude difference/a/b/phase/group/dummy/fwhm/m91/m90/shelx\n'
            continue
        else:
            break

    make_superflip(
        cell, spgr, wavelength, composition, datafile, dataformat, filename=filename)


def make_focus_entry():
    params = raw_input("Enter cell parameters:\n [10 10 10 90 90 90] >> ") or "10 10 10 90 90 90"
    params = [float(val) for val in params.split()]
    spgr = raw_input("Enter spacegroup:\n [P1] >> ") or "P1"

    cell = unitcell.UnitCell(params, spgr)
    
    print
    cell.info()

    fn = raw_input("Enter hkl file (h k l Fobs sigma):\n [optional] >> ") or None

    if fn:
        df = read_hkl(fn)
    else:
        df = None

    write_focus_inp(cell, df=df)


def cif2hkl_entry():
    import sys
    from diffraction import calc_structure_factors
    for arg in sys.argv[1:]:
        cell, atoms = read_cif(arg)
        cell.info()
        print atoms

        df = calc_structure_factors(cell, atoms, table="xray")

        root, ext = os.path.splitext(arg)
        outfile = root + ".hkl"
        np.savetxt(outfile, df.as_matrix(), fmt="%4d%4d%4d %12.4f %12.4f")

if __name__ == '__main__':
    cif2hkl_entry()
    # make_focus_entry()
