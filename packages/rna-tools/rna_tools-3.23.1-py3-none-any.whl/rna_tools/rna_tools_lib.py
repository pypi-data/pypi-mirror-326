#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""rna_tools_lib.py - main lib file, many tools in this lib is using this file."""

import os
import sys
from collections import OrderedDict
import re
import string
import time
import gzip
import tempfile
import shutil
import subprocess

from rna_tools.tools.extra_functions.select_fragment import select_pdb_fragment_pymol_style, select_pdb_fragment

from icecream import ic
import sys
ic.configureOutput(outputFunction=lambda *a: print(*a, file=sys.stderr), includeContext=True)
ic.configureOutput(prefix='')

import logging
logger = logging.getLogger('rna-tools')
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

# Don't fix OP3, ignore it
ignore_op3 = False

# Settings: what is what in a PDB file
AMINOACID_CODES = ["ALA", "ARG", "ASN", "ASP", "CYS", "GLU", "GLN", "GLY",
                   "HIS", "ILE", "LEU", "LYS", "MET", "PHE", "PRO", "SER", "THR",
                   "TRP", "TYR", "VAL"]

def generate_conect_records(residue_type, shift=0, no_junction=True):
    """
    Generate CONECT records for an RNA residue (U, A, C, or G).
    
    Args:
        residue_type (str): Type of residue ('U', 'A', 'C', or 'G').
        shift (int): Value to shift all atom serial numbers by.
    
    Returns:
        list: List of CONECT records as strings.
    """
    # Define connections for each residue type
    if residue_type == "U":
        connections = [
            (1, 2),   # P -> OP1
            (1, 3),   # P -> OP2
            (1, 4),   # P -> O5'
            (4, 5),   # O5' -> C5'
            (5, 6),   # C5' -> C4'
            (6, 7),   # C4' -> O4'
            (6, 8),   # C4' -> C3'
            (8, 9),   # C3' -> O3'
            (8, 10),  # C3' -> C2'
            (10, 11), # C2' -> O2'
            (10, 12), # C2' -> C1'
            (12, 13), # C1' -> N1
            (13, 14), # N1 -> C2
            (14, 15), # C2 -> O2
            (14, 16), # C2 -> N3
            (16, 17), # N3 -> C4
            (17, 18), # C4 -> O4
            (17, 19), # C4 -> C5
            (19, 20), # C5 -> C6
            (20, 13), # C6 -> N1
            (7, 12),  # O4' -> C1'
        ]
        if not no_junction:
            connections.append((9, 21))
        print(connections)
    elif residue_type == "A":
        connections = [
            (1, 2),   # P -> OP1
            (1, 3),   # P -> OP2
            (1, 4),   # P -> O5'
            (4, 5),   # O5' -> C5'
            (5, 6),   # C5' -> C4'
            (6, 7),   # C4' -> O4'
            (6, 8),   # C4' -> C3'
            (8, 9),   # C3' -> O3'
            (8, 10),  # C3' -> C2'
            (10, 11), # C2' -> O2'
            (10, 12), # C2' -> C1'
            (12, 13), # C1' -> N9
            (13, 14), # N9 -> C8
            (14, 15), # C8 -> N7
            (15, 16), # N7 -> C5
            (16, 17), # C5 -> C6
            (17, 18), # C6 -> N6
            (17, 19), # C6 -> N1
            (19, 20), # N1 -> C2
            (20, 21), # C2 -> N3
            (21, 22), # N3 -> C4
            (22, 16), # C4 -> C5
            (22, 13), # C4 -> N9
            (7, 12),  # O4' -> C1'
        ]
        if not no_junction:
            connections.append((9, 23))
    elif residue_type == "C":
        connections = [
            (1, 2),   # P -> OP1
            (1, 3),   # P -> OP2
            (1, 4),   # P -> O5'
            (4, 5),   # O5' -> C5'
            (5, 6),   # C5' -> C4'
            (6, 7),   # C4' -> O4'
            (6, 8),   # C4' -> C3'
            (8, 9),   # C3' -> O3'
            (8, 10),  # C3' -> C2'
            (10, 11), # C2' -> O2'
            (10, 12), # C2' -> C1'
            (12, 13), # C1' -> N1
            (13, 14), # N1 -> C2
            (14, 15), # C2 -> O2
            (14, 16), # C2 -> N3
            (16, 17), # N3 -> C4
            (17, 18), # C4 -> N4
            (17, 19), # C4 -> C5
            (19, 20), # C5 -> C6
            (20, 13), # C6 -> N1
            (7, 12),  # O4' -> C1' (additional connection)
        ]
        if not no_junction:
            connections.append((9, 21))
    elif residue_type == "G":
        connections = [
            (1, 2),   # P -> OP1
            (1, 3),   # P -> OP2
            (1, 4),   # P -> O5'
            (4, 5),   # O5' -> C5'
            (5, 6),   # C5' -> C4'
            (6, 7),   # C4' -> O4'
            (6, 8),   # C4' -> C3'
            (8, 9),   # C3' -> O3'
            (8, 10),  # C3' -> C2'
            (10, 11), # C2' -> O2'
            (10, 12), # C2' -> C1'
            (12, 13), # C1' -> N9
            (13, 14), # N9 -> C8
            (14, 15), # C8 -> N7
            (15, 16), # N7 -> C5
            (16, 17), # C5 -> C6
            (17, 18), # C6 -> O6
            (17, 19), # C6 -> N1
            (19, 20), # N1 -> C2
            (20, 21), # C2 -> N2
            (20, 22), # C2 -> N3
            (22, 23), # N3 -> C4
            (23, 16), # C4 -> C5
            (23, 13), # C4 -> N9
            (7, 12),  # O4' -> C1' (additional connection)
        ]
        if not no_junction:
            connections.append((9, 24))
    else:
        raise ValueError("Invalid residue type. Choose 'U', 'A', 'C', or 'G'.")

    # Generate CONECT records with shifted serial numbers
    conect_records = []
    for conn in connections:
        atom1_serial, atom2_serial = conn
        # Shift the serial numbers
        atom1_serial += shift
        atom2_serial += shift
        conect_records.append(f"CONECT{atom1_serial:>5}{atom2_serial:>5}")
    return conect_records

    
def aa3to1(aaa):
    """based on https://pymolwiki.org/index.php/Aa_codes"""
    if len(aaa) != 3:  # aaa is 'G', like for RNA ;-)
        return '' # dont do it for rna test aaa
    one_letter ={'VAL':'V', 'ILE':'I', 'LEU':'L', 'GLU':'E', 'GLN':'Q', \
                 'ASP':'D', 'ASN':'N', 'HIS':'H', 'TRP':'W', 'PHE':'F', 'TYR':'Y',    \
                 'ARG':'R', 'LYS':'K', 'SER':'S', 'THR':'T', 'MET':'M', 'ALA':'A',    \
                 'GLY':'G', 'PRO':'P', 'CYS':'C'}
    return one_letter[aaa]


RES = ['DA', 'DG', 'DT', 'DC']
RES += ['A', 'G', 'U', 'C']

RESS = ['A', 'C', 'G', 'U', 'ADE', 'CYT', 'GUA', 'URY', 'URI', 'U34', 'U31', 'C31', '4SU', 'H2U', 'QUO', 'G7M', '5MU',
        '5MC', 'PSU', '2MG', '1MG', '1MA', 'M2G', '5BU', 'FHU', 'FMU', 'IU', 'OMG', 'OMC', 'OMU', 'A2M', 'A23', 'CCC',
        'I'] + ['RC', 'RU', 'RA', 'RG', 'RT']
DNA = ['DA', 'DG', 'DT', 'DC']
RNA = ['A', 'G', 'U', 'C']
IONS = ['NA', 'MG', 'MN', 'JOS'] # and ligands JOS
HYDROGEN_NAMES = ["H", "H5'", "H5''", "H4'", "H3'", "H2'", "HO2'", "H1'", "H3", "H5", "H6", "H5T", "H41", "1H5'",
                  "2H5'", "HO2'", "1H4", "2H4", "1H2", "2H2", "H1", "H8", "H2", "1H6", "2H6", "HO5'", "H21", "H22",
                  "H61", "H62", "H42", "HO3'", "1H2'", "2HO'", "HO'2", "H2'1", "HO'2", "HO'2", "H2", "H2'1", "H1", "H2",
                  "1H5*", "2H5*", "H4*", "H3*", "H1*", "1H2*", "2HO*", "1H2", "2H2", "1H4", "2H4", "1H6", "2H6", "H1",
                  "H2", "H3", "H5", "H6", "H8", "H5'1", "H5'2", "H3T"]


class PDBFetchError(Exception):
    pass

class MethodUnknown(Exception):
    pass


try:
    from Bio.PDB import *
except ImportError:
    print("Biopython is not detected. It is required for some functions.")

import warnings
warnings.filterwarnings('ignore', '.*Invalid or missing.*',)
warnings.filterwarnings('ignore', '.*with given element *',)
warnings.filterwarnings('ignore', '.*is discontinuous*',)
warnings.filterwarnings('ignore', '.*Some atoms or residues may be missing in the data structure.*',)
warnings.filterwarnings('ignore', '.*Ignoring unrecognized record.*',)


import subprocess
def exe(cmd):
    o = subprocess.Popen(
        cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out = o.stdout.read().strip().decode()
    err = o.stderr.read().strip().decode()
    return out, err


def get_rna_tools_path():
    """Return path to the rt."""
    import inspect
    import rna_tools
    return os.path.dirname(inspect.getfile(rna_tools))

def get_version(currfn='', verbose=False):
    import rna_tools
    return rna_tools.__version__


def sort_strings(l):
    """ Sort the given list in the way that humans expect.
    http://blog.codinghorror.com/sorting-for-humans-natural-sort-order/
    """
    def convert(text): return int(text) if text.isdigit() else text

    def alphanum_key(key): return [convert(c) for c in re.split('([0-9]+)', key)]
    l.sort(key=alphanum_key)
    return l


class RNAStructure:
    """RNAStructure - handles an RNA pdb file.

    Attributes:

        fn (string)  : path to the structural file, e.g., "../rna_tools/input/4ts2.pdb"
        name(string) : filename of the structural file, "4ts2.pdb"
        lines (list) : the PDB file is loaded and ATOM/HETATM/TER/END go to self.lines

    """

    def __init__(self, fn=''):
        if not fn: # if empty
            tf = tempfile.NamedTemporaryFile(delete=False)
            fn = tf.name

        self.fn = os.path.abspath(fn) # ../rna_tools/input/4ts2.pdb
        # add name attribute with filename 4ts2.pdb
        self.name = self.fn.split(os.sep)[-1] # OS.path.splitext(self.fn)[0]

        self.report = []
        self.report.append('The RNARNAStructure report: %s ' % self.fn)

        self.mol2_format = False

        self.lines = []

        try:
            # lines = open(fn).read().strip().split('\n') # don't strip?, good or bed?
            lines = open(fn).read().split('\n')
        except UnicodeDecodeError:
            print("Can't open a binary file")
            self.lines = ''
            return

        self.has_many_models = False

        for l in lines:
            # multi-models pdb files
            if l.startswith('MODEL'):
                self.has_many_models = True
            if l.startswith('ENDMDL'):
                break

            if l.startswith('ATOM') or l.startswith('HETATM') or l.startswith('TER') or l.startswith('END'):
                self.lines.append(l) # don't strip .strip())
            if l.startswith("@<TRIPOS>"):
                self.mol2_format = True
                self.report.append('This is mol2 format')

        self.res = self.get_resn_uniq()

    def reload(self):
        """Reload the object."""
        self.__init__(self.fn)
        
    def is_pdb(self):
        """Return True if the files is in PDB format.

        If self.lines is empty it means that nothing was parsed into the PDB format."""
        if len(self.lines):
            return True
        else:
            return False

    def is_nmr(self):
        """True if the file is an NMR-style multiple model pdb

        :returns: True or Fo
        :rtype: boolean
        """
        return self.has_many_models

    def un_nmr(self, startwith1=True, directory='', verbose=False):
        """Un NMR - Split NMR-style multiple model pdb files into individual models.

        Take self.fn and create new files in the way::

            input/1a9l_NMR_1_2_models.pdb
               input/1a9l_NMR_1_2_models_0.pdb
               input/1a9l_NMR_1_2_models_1.pdb

        .. warning:: This function requires biopython.

        rna_pdb_tools.py --un-nmr AF-Q5TCX8-F1-model_v1_core_Ctrim_mdr_MD.pdb
36
        cat *MD_* > md.pdb
        """
        #
        npdb = ''
        c = 0

        nmodels = 0
        for l in open(self.fn):
            if l.startswith('MODEL'):
                nmodels += 1
        print(nmodels)

        for l in open(self.fn):
            if 1:
                if not l.startswith('HETATM'):
                    npdb += l
            if l.startswith('MODEL'):
                c += 1
            if l.startswith('ENDMDL'):
                id = str(c).zfill(len(str(nmodels)))
                nf = self.fn.replace('.pdb', '_%s.pdb' % id)
                verbose = 1
                if verbose:
                    print(nf)
                with open(nf, 'w') as f:
                    f.write(npdb)
                npdb = ''
        biopython = 0
        
        if biopython:
            parser = PDBParser()
            structure = parser.get_structure('', self.fn)
            for c, m in enumerate(structure):
                if verbose:
                    print(m)
                io = PDBIO()
                io.set_structure(m)
                if startwith1:
                    c += 1
                if directory:
                    io.save(directory + os.sep + self.fn.replace('.pdb', '_%i.pdb' % c))
                else:
                    io.save(self.fn.replace('.pdb', '_%i.pdb' % c))                

    def is_mol2(self):
        """Return True if is_mol2 based on the presence of ```@<TRIPOS>```."""
        return self.mol2_format

    def decap_gtp(self):
        lines = []
        for l in self.lines:
            if l.startswith('ATOM') or l.startswith('HETATM'):
                if l[12:16].strip() in ['PG', 'O1G', 'O2G', 'O3G', 'O3B', 'PB', 'O1B', 'O2B', 'O3A']:
                    continue
                if l[12:16].strip() == 'PA':
                    l = l.replace('PA', 'P ')
                if l[12:16].strip() == 'O1A':
                    l = l.replace('O1A', 'O1P')
                if l[12:16].strip() == 'O2A':
                    l = l.replace('O2A', 'O2P')
                if l[17:20].strip() == 'GTP':
                    l = l[:17] + '  G' + l[20:]
                    l = l.replace('HETATM', 'ATOM  ')
                lines.append(l)
        self.lines = lines

    def is_amber_like(self):
        """Use self.lines and check if there is XX line
        """
        for l in self.lines:
            if l.startswith('ATOM') or l.startswith('HETATM'):
                rn = l[17:20]
                if rn in ['RU5', 'RC5', 'RA5', 'RT5', 'RG5']:
                    self.report.append('This is amber-like format')
                    return True
        return False

    def replace_hetatms(self):
        nlines = []
        for l in self.lines:
            l = l.replace('HETATM', 'ATOM  ')
            nlines.append(l)
        self.lines = nlines

    def fix_with_qrnas(self, outfn="", verbose=False):
        """Add missing heavy atom.

        A residue is recognized base on a residue names.

        Copy QRNAS folder to curr folder, run QRNAS and remove QRNAS.

        .. warning:: QRNAS required (http://genesilico.pl/QRNAS/QRNAS.tgz)
        """
        from rpt_config import QRNAS_PATH

        # prepare folder get ff folder
        to_go = os.path.abspath(os.path.dirname(self.fn))
        curr = os.getcwd()

        # set occupancy to 0
        s = RNAStructure(self.fn)
        s.set_occupancy_atoms(0.00)
        s.write(self.fn)

        os.chdir(to_go)
        try:
            shutil.copytree(QRNAS_PATH, to_go + os.sep + "QRNAS")
        except OSError:
            pass
        # prepare config file
        with open('qrna_config.txt', 'w') as f:
            f.write("WRITEFREQ   1\n")
            f.write("NSTEPS      1\n")
        # run qrnas
        print('QRNAS...')

        if not outfn:
            cmd = "QRNAS -c qrna_config.txt -i " + os.path.basename(self.fn)
        else:
            cmd = "QRNAS -c qrna_config.txt -i " + \
                os.path.basename(self.fn) + " -o " + curr + os.sep + outfn
        #o = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        os.system(cmd)
        if False:
            out = o.stdout.read().strip()
            err = o.stderr.read().strip()
            if verbose:
                print(out)
                print(err)
                shutil.rmtree(to_go + os.sep + "QRNAS")
        # post cleaning
        if outfn:
            print('Cleaning...')
            s = RNAStructure(curr + os.sep + outfn)
            s.remove_hydrogen()
            s.std_resn()
            s.write(curr + os.sep + outfn)
        os.chdir(curr)

    def mol2toPDB(self, outfn=""):
        try:
            import pybel
        except ImportError:
            print ('pybel is needed for mol2 to pdb convertion')
            # sys.exit(1)
            sys.exit(0)

        if not outfn:
            outfn = self.fn.replace('.mol2', '.pdb')

        for mol in pybel.readfile("mol2", self.fn):
            mol.write("pdb", outfn, overwrite=True)

        print('outfn: ', outfn)
        self.report.append('  Converted from mol2 to PDB')
        return outfn

    def get_no_lines(self):
        return len(self.lines)
        
    def check_geometry(self, verbose=False):
        """Check for correct "Polymer linkage, it should be around 1.6Å with a sigma around 0.01.
        
        Carrascoza, F., Antczak, M., Miao, Z., Westhof, E. & Szachniuk, M. Evaluation of the stereochemical quality of predicted RNA 3D models in the RNA-Puzzles submissions. Rna 28, 250–262 (2022).

        Values for 1xjr.pdb::

            op.mean(): 1.599316
            op.std(): 0.009274074

            po.mean(): 1.5984017
            po.std(): 0.0069191623
        
        requires biopython
        """
        if verbose:
            logger.setLevel(logging.DEBUG)

        try:
            from Bio import PDB
            from Bio.PDB import PDBIO
            import warnings
            warnings.filterwarnings('ignore', '.*Invalid or missing.*',)
            warnings.filterwarnings('ignore', '.*with given element *',)
        except:
            sys.exit('Error: Install biopython to use this function (pip biopython)')

        pdb = self.fn
        struc = PDB.PDBParser().get_structure('struc', pdb)
        resi_prev = {}
        op = []
        po = []
        angles = []
        angles2 = []

        p_ps = []
        sigma = 0.009274074
        mean =  1.599316
        po3p_p  = []
        import numpy as np

        dist_o3pp= []
        for s in struc:
            for c in s:
                # for new chain reset resi_prev
                resi_prev = None
                for r in c:
                    if resi_prev:
                        p_p = resi_prev["P"] - r['P']
                        p_ps.append(p_p)
                        
                        v = resi_prev["O3'"] - r['P']
                        po3p_p = resi_prev["O3'"] - r['P']
                        op.append(v)
                        import math
                        dist_o3pp.append(abs(1.6 - v))
                        x = mean - 6 * sigma
                        y = mean + 6 * sigma

                        v2 = r["P"] - r["O5'"]
                        #ic(v2)
                        po.append(v2)

                        if not (x <= v <= y):
                            #print(f' ! lack of connectivity between {r}, {resi_prev}, distance between residues: {v:.2f}')
                            pass

                        # angle o3' p o5'
                        pc3p = resi_prev["C3'"].get_vector()
                        po3p = resi_prev["O3'"].get_vector()
                        p = r['P'].get_vector()

                        v1 = po3p - p
                        v2 = po3p - pc3p
                        angle = np.rad2deg(v1.angle(v2))#o5p)) 
                        angles.append(angle)

                        # agnle o3'-p-o5' angle
                        o5p = r["O5'"].get_vector()
                        v1 = po3p - p
                        v2 = o5p - p
                        angle2 = np.rad2deg(v2.angle(v1))
                        angles2.append(angle2)

                    resi_prev = r
        #ic(dist_o3pp, len(dist_o3pp), np.mean(dist_o3pp))
        # Colors
        RED = "\033[31m"
        GREEN = "\033[32m"
        YELLOW = "\033[33m"
        BLUE = "\033[34m"
        RESET = "\033[0m"

        print(f'Connectivity Score; {GREEN} {sum(dist_o3pp) } {RESET}')
        print('Connectivity Score; ', sum(dist_o3pp) / len(dist_o3pp))
        p_ps = np.array(p_ps)

        plots = True

        ic(v)

        plots = False

        if plots:
            import matplotlib.pyplot as plt
            plt.hist(op, bins='auto')
            plt.xlim(-1, 10)
            plt.title("prev-o3' p")
            plt.show()

        #np.set_printoptions(threshold=np.inf)
        # ic.disable()
        ic(p_ps)
        ic(p_ps.mean(), p_ps.std())

        if plots:
            import matplotlib.pyplot as plt
            plt.hist(p_ps, bins='auto')
            plt.title("p-ps")
            plt.xlim(0, 10)
            plt.show()

            #plt.savefig("histogram.png")  # Save the figure as a PNG file
        
        op = np.array(op)
        ic(op.mean(), op.std())

        po = np.array(po)
        ic(po.mean(), po.std())

        print("c3'-o3'-p")
        angles = np.array(angles)
        ic(angles)
        ic(angles.mean(), angles.std())

        import math
        angle_degrees = angles.mean()
        angle_radians = math.radians(angle_degrees)  # Convert to radians
        cos_value = math.cos(angle_radians)  # Calculate cosine
        ic(cos_value)
        
        coss = []
        for a in angles:
            angle_radians = math.radians(a)
            cos_value = math.cos(angle_radians)  # Calculate cosine
            coss.append(cos_value)
        coss = np.array(coss)
        ic(coss.std())

        if plots:
            import matplotlib.pyplot as plt
            plt.hist(angles, bins='auto')
            plt.title("Histogram of angles o3'-p-o5'")
            plt.xlim(0, 360)
            plt.show()

        angles2 = np.array(angles2)
        print("o3'-p-o5'")
        ic(angles2)
        ic(angles2.mean(), angles2.std())

        angle_degrees = angles2.mean()
        angle_radians = math.radians(angle_degrees)  # Convert to radians
        cos_value = math.cos(angle_radians)  # Calculate cosine

        ic(cos_value)

        coss = []
        for a in angles2:
            angle_radians = math.radians(a)
            cos_value = math.cos(angle_radians)  # Calculate cosine
            coss.append(cos_value)
        coss = np.array(coss)
        ic(coss.std())

        if plots:
            import matplotlib.pyplot as plt
            plt.hist(angles2, bins='auto')
            plt.title("Histogram of angles c3'-o3'-p")
            plt.xlim(0, 360)
            plt.show()
        #ic.enable()
        
    def get_text(self, add_end=True):
        """works on self.lines."""
        txt = ''
        for l in self.lines:
            if l.startswith('END'):
                continue  # skip end
            txt += l + '\n' # .strip()
        if add_end:
            if not l.startswith('END'):
                txt += 'END'
        return txt.strip()

    def get_chain(self, chain_id='A'):
        txt = ''
        for l in self.lines:
            if l.startswith('ATOM') or l.startswith('HETATM'):
                if l[21] == chain_id:
                    txt += l.strip() + '\n'
            if l.startswith('TER'):
                if len(l) < 21: # this is only TER
                    #                     ter = 'TER   ' +  str(self.get_atom_num(txt) + 1).rjust(5) + '\n'
                    raise Exception('TER line has no chain id')
                else:     
                    if l[21] == chain_id:
                          txt += l.strip() + '\n'
        ## ll = txt.strip().split('\n')[-1] # last line = ll
        ## print(ll)
        ## #if ll.startswith('TER'):  # if the last line does not start with ter
        ## ter = self.set_res_code(ter, self.get_res_code(ll)) # + self.get_chain_id(l).rjust(11)
        ## print(ter)
        return txt.strip()

    def rename_chain(self, chain_id_old, chain_id_new, debug=False):
        """Rename chains

        Args:
            chain_id_old (str): e.g., A
            chain_id_new (str): e.g., B
            debug (bool): show some diagnostics

        Returns:
            pdb content (txt)
            self.lines is updated with new lines
        """
        txt = ''
        lines = []
        for l in self.lines:
            if l.startswith('ATOM') or l.startswith('HETATM') or l.startswith('TER'):
                # TER
                try:
                    l[21]
                except IndexError:
                    continue
                if l[21] == chain_id_old:
                    l = l[:21] + chain_id_new + l[22:]
            if debug: print(l)
            txt += l.strip() + '\n'  # ok, actually keep all lines as it was
            lines.append(l)
        self.lines = lines
        return txt


    def get_resn_uniq(self):
        res = set()
        for l in self.lines:
            r = l[17:20].strip().upper()
            res.add(r)
        return res

    def check_res_if_std_na(self):
        wrong = []

        for r in self.res:
            if r not in RES:
                wrong.append(r)
        return wrong

    def get_seq(self, compact=False, chainfirst=False, fasta=False, addfn='', color=False):
        """Get seq (v2) gets segments of chains with correct numbering

        Run::

            python rna_pdb_seq.py input/1ykq_clx.pdb
            > 1ykq_clx A:101-111
            GGAGCUCGCCC
            > 1ykq_clx B:201-238
            GGGCGAGGCCGUGCCAGCUCUUCGGAGCAAUACUCGGC

            > 6_solution_0 A:1-19 26-113 117-172
            GGCGGCAGGUGCUCCCGACGUCGGGAGUUAAAAGGGAAG

        Chains is ``{'A': {'header': 'A:1-19 26-113 117-172', 'resi': [1, 2, 3, ..., \
        19, 26, 27, ..., 172], 'seq': ['G', 'G', 'C', 'G', ... C', 'G', 'U', 'C']}}``

        Chains are in other as the appear in the file.

        .. warning :: take only ATOM and HETATM lines.
        """
        if addfn:
            addfn += ' ' # add space to file name
        seq = self.lines[0][19]
        chains = OrderedDict()
        resi_prev = None
        chain_prev = None

        for l in self.lines:
            if l.startswith('ATOM') or l.startswith('HETATM'):
                resi = int(l[22:26])
                if resi_prev != resi:
                    resname = l[17:20].strip()
                    chain_curr = l[21]
                    if resname in AMINOACID_CODES:
                        resname = aa3to1(resname)
                    if len(resname) == 'GTP':  # DG -> g GTP
                        resname = 'g'
                    if len(resname) > 1:  # DG -> g GTP
                        resname = resname[-1].lower()
                    try:
                        chains[chain_curr]['resi'].append(resi)
                        chains[chain_curr]['seq'].append(resname)
                    except KeyError:
                        chains[chain_curr] = {}
                        chains[chain_curr]['resi'] = []
                        chains[chain_curr]['resi'].append(resi)
                        chains[chain_curr]['seq'] = []
                        chains[chain_curr]['seq'].append(resname)

                    resi_prev = resi
                    chain_prev = chain_curr
                    
        def color_seq(seq, color):
            if not color:
                return seq
            else:
                from termcolor import colored
                seqc = ''
                for s in seq:
                    if s in ['G']:
                        seqc += colored(s, 'green')
                    if s in ['G']:
                        seqc += colored(s, 'red')
                    if s in ['T', 'U']:
                        seqc += colored(s, 'blue')                        
                    if s in ['C']:
                        seqc += colored(s, 'yellow')                        
                return seqc
            

        for c in list(chains.keys()):
            header = c + ':' + str(chains[c]['resi'][0]) + '-'  # add A:1-
            for i in range(1, len(chains[c]['resi'])):  # start from second element
                if chains[c]['resi'][i] - chains[c]['resi'][i - 1] > 1:
                    header += '' + str(chains[c]['resi'][i - 1]) + ' '
                    header += '' + str(chains[c]['resi'][i]) + '-'
            header += '' + str(chains[c]['resi'][-1])
            chains[c]['header'] = header  # add -163 (last element)

        if compact:
            txt = ''
            for c in list(chains.keys()):
                if chainfirst:
                    txt += '' + chains[c]['header'].ljust(15) + color_seq(''.join(chains[c]['seq']), color) + ' '
                elif fasta:
                    txt += color_seq(''.join(chains[c]['seq']), color) + ' '
                else:
                    txt += color_seq(''.join(chains[c]['seq']), color) + ' # ' + chains[c]['header'] + ' '
            return txt.strip()
        else:
            txt = ''
            for c in list(chains.keys()):
                txt += '>' + addfn + chains[c]['header'] + '\n'
                txt += color_seq(''.join(chains[c]['seq']), color) + '\n' # color ;-)
            return txt.strip()

    def __get_seq(self):
        """get_seq DEPRECATED

        You get `chains` such as:
        OrderedDict([('A', {'header': 'A:1-47', 'seq': 'CGUGGUUAGGGCCACGUUAAAUAGUUGCUUAAGCCCUAAGCGUUGAU'}), ('B', {'header': 'B:48-58', 'seq': 'AUCAGGUGCAA'})])

        .. warning:: take only ATOM and HETATM lines.
        """
        seq = ''
        curri = int(self.lines[0][22:26])
        seq = self.lines[0][19]
        chains = OrderedDict()
        curri = -100000000000000000000000000000000  # ugly
        chain_prev = None

        for l in self.lines:
            if l.startswith('ATOM') or l.startswith('HETATM'):
                resi = int(l[22:26])
                if curri != resi:
                    print(l)
                    resname = l[17:20].strip()
                    if len(resname) == 'GTP':  # DG -> g GTP
                        resname = 'g'
                    if len(resname) > 1:  # DG -> g GTP
                        resname = resname[-1].lower()

                    seq += resname
                    chain_curr = l[21]

                    # if distances between curr res and previevs is bigger than 1, then show it as a fragment
                    if resi - curri > 1 and resi - curri < 100000000000000000000000000000000:  # ugly hack
                        print(resi - curri)
                        chains[chain_prev]['header'] += '-' + str(resi_prev)
                    if chain_prev != chain_curr and chain_prev:
                        chains[chain_prev]['header'] += '-' + str(resi_prev)
                    if chaoin_curr in chains:
                        chains[chain_curr]['seq'] += resname
                    else:
                        chains[chain_curr] = dict()
                        chains[chain_curr]['header'] = chain_curr + ':' + str(resi)  # resi_prev)
                        chains[chain_curr]['seq'] = resname
                    resi_prev = resi
                    chain_prev = chain_curr
                curri = resi
        chains[chain_prev]['header'] += '-' + str(resi_prev)
        seq = ''
        for c in list(chains.keys()):
            seq += '> ' + os.path.basename(self.fn) + ' ' + chains[c]['header'] + '\n'
            seq += chains[c]['seq'] + '\n'
        return seq.strip()

    def get_info_chains(self):
        """return A:3-21 B:22-32
        """
        seq = ''
        curri = int(self.lines[0][22:26])
        seq = self.lines[0][19]
        chains = OrderedDict()
        curri = -100000000000000  # ugly
        chain_prev = None
        for l in self.lines:
            if l.startswith('ATOM') or l.startswith('HETATM'):
                resi = int(l[22:26])
                if curri != resi:
                    resname = l[17:20].strip()
                    if len(resname) == 'GTP':  # DG -> g GTP
                        resname = 'g'
                    if len(resname) > 1:  # DG -> g GTP
                        resname = resname[-1].lower()
                    seq += resname
                    chain_curr = l[21]
                    if chain_prev != chain_curr and chain_prev:
                        chains[chain_prev]['header'] += '-' + str(resi_prev)
                    if chain_curr in chains:
                        chains[chain_curr]['seq'] += resname
                    else:
                        chains[chain_curr] = dict()
                        chains[chain_curr]['header'] = chain_curr + ':' + str(resi)  # resi_prev)
                        chains[chain_curr]['seq'] = resname
                    resi_prev = resi
                    chain_prev = chain_curr
                curri = resi
        chains[chain_prev]['header'] += '-' + str(resi_prev)
        seq = ''
        for c in list(chains.keys()):
            seq += chains[c]['header'] + ' '
        return seq.strip()

    def detect_file_format(self):
        pass

    def detect_molecule_type(self):
        aa = []
        na = []
        for r in self.res:
            if r in AMINOACID_CODES:
                aa.append(r)
            if r in RESS:
                na.append(r)

        aa = float(len(aa)) / len(self.res)
        na = float(len(na)) / len(self.res)

        if aa == 0 and na == 0:
            return 'error'
        if aa > na:
            return '>protein< vs na', aa, na
        else:
            return 'protein vs >na<', aa, na

    def get_head(self):
        return '\n'.join(self.lines[:5])

    def get_tail(self):
        return '\n'.join(self.lines[-5:])

    def get_preview(self):
        t = '\n'.join(self.lines[:5])
        t += '\n-------------------------------------------------------------------\n'
        t += '\n'.join(self.lines[-5:])
        return t

    def remove_hydrogen(self):
        lines = []
        for l in self.lines:
            if l[77:79].strip() == 'H':
                continue
            if l[12:16].strip() in HYDROGEN_NAMES:
                # if l[12:16].strip().startswith('H'):
                continue
            else:
                # print l[12:16]
                lines.append(l)
        self.lines = lines

    def remove_water(self):
        """Remove HOH and TIP3"""
        lines = []
        for l in self.lines:
            if l[17:21].strip() in ['HOH', 'TIP3', 'WAT']:
                continue
            else:
                lines.append(l)
        self.lines = lines

    def remove_ion(self):
        """
    TER    1025        U A  47
    HETATM 1026 MG    MG A 101      42.664  34.395  50.249  1.00 70.99          MG
    HETATM 1027 MG    MG A 201      47.865  33.919  48.090  1.00 67.09          MG
        :rtype: object
        """
        lines = []
        for l in self.lines:
            element = l[76:78].strip().upper()
            element2 = l[17:20].strip().upper()
            if element in IONS:
                continue
            if element2 in IONS:
                continue
            else:
                lines.append(l)
        self.lines = lines

    def fixU__to__U(self):
        lines = []
        for l in self.lines:
            if l.startswith('ATOM') or l.startswith('HETATM'):
                rn = l[17:20]
                rn = rn.replace('G  ', '  G')
                rn = rn.replace('U  ', '  U')
                rn = rn.replace('C  ', '  C')
                rn = rn.replace('A  ', '  A')
                l = l[:16] + ' ' + rn + ' ' + l[21:]
            # print l.strip()
            # print l2
            #l = l.replace(' U   ', '   U ')
            #l = l.replace(' G   ', '   G ')
            #l = l.replace(' A   ', '   A ')
            #l = l.replace(' C   ', '   C ')
            lines.append(l)
        print ('fixU__to__U OK')
        self.report.append('  Fix: U__ -> __U')
        self.lines = lines

    def resn_as_dna(self):
        lines = []
        for l in self.lines:
            if l.startswith('ATOM') or l.startswith('HETATM'):
                # print l
                nl = l.replace('DA5', ' DA')  # RA should be the last!!!!
                nl = nl.replace('DA3', ' DA')
                nl = nl.replace(' DA', ' DA')
                nl = nl.replace(' rA', ' DA')

                nl = nl.replace('DC5', ' DC')
                nl = nl.replace('DC3', ' DC')
                nl = nl.replace(' DC', ' DC')
                nl = nl.replace(' rC', ' DC')

                nl = nl.replace('DG5', ' DG')
                nl = nl.replace('DG3', ' DG')
                nl = nl.replace(' DG', ' DG')
                nl = nl.replace(' rG', ' DG')

                nl = nl.replace('DU5', ' DU')
                nl = nl.replace('DU3', ' DU')
                nl = nl.replace(' DU', ' DU')
                nl = nl.replace(' rU', ' DU')

                nl = nl.replace('DT5', ' DT')
                nl = nl.replace('DT3', ' DT')
                nl = nl.replace(' DT', ' DT')
                nl = nl.replace(' rT', ' DT')

                nl = nl.replace('C5M', 'C7 ')

                if l[17:20].strip() == 'G':
                    nl = nl[:17] + ' DG' + nl[20:]

                if l[17:20].strip() == 'C':
                    nl = nl[:17] + ' DC' + nl[20:]

                if l[17:20].strip() == 'T':
                    nl = nl[:17] + ' DT' + nl[20:]

                if l[17:20].strip() == 'U':
                    nl = nl[:17] + ' DU' + nl[20:]

                if l[17:20].strip() == 'A':
                    nl = nl[:17] + ' DA' + nl[20:]

                lines.append(nl)
            if l.startswith("END") or l.startswith("TER"):
                lines.append(l)

        print ('resn_as_dna')
        self.report.append('  resn_as_dna')
        self.lines = lines

    def fix_O_in_UC(self):
        """.. warning: remove RU names before using this function"""
        lines = []
        for l in self.lines:
            # if l[12:16].strip() in
            # if l[12:16].strip().startswith('H'):
            nl = l.replace('O     U',
                           'O2    U')
            nl = nl.replace('O     C',
                            'O2    C')
            lines.append(nl)
        self.lines = lines

    def fix_op_atoms(self):
        """Replace OXP' to OPX1, e.g ('O1P' -> 'OP1')"""
        lines = []
        for l in self.lines:
            nl = l.replace('*', '\'')
            nl = nl.replace('O1P', 'OP1')
            nl = nl.replace('O2P', 'OP2')
            nl = nl.replace('O3P', 'OP3')
            lines.append(nl)
        self.lines = lines

    def get_report(self):
        """
        Returns:
            string: report, messages collected on the way of parsing this file
        """
        return '\n'.join(self.report)

    def is_rna(self):
        wrong = []
        for r in self.res:
            if r.upper().strip() in ['RC', 'RU', 'RA', 'RG', 'RT']:
                if r not in wrong_res:
                    wrong_res.append(r)
        return wrong_res

    def check_res_if_std_dna(self):
        wrong_res = []
        for r in self.res:
            if r.upper().strip() in ['A', 'T', 'C', 'G']:
                if r not in wrong_res:
                    wrong_res.append(r)
        return wrong_res

    def check_res_if_supid_rna(self):
        wrong_res = []
        for r in self.res:
            if r.upper().strip() in ['RC', 'RU', 'RA', 'RG', 'RT']:
                if r not in wrong_res:
                    wrong_res.append(r)
        return wrong_res


    def is_rna(self):
        for r in self.res:
            if r.upper().strip() in ['RC', 'RU', 'RA', 'RG', 'RT']:
                if r not in wrong_res:
                    wrong_res.append(r)
        return wrong_res

    def renum_atoms(self):
        """Renum atoms, from 1 to X for line; ATOM/HETATM"""
        lines = []
        c = 1
        for l in self.lines:
            l = l[:6] + str(c).rjust(5) + l[11:]
            c += 1
            lines.append(l)
        self.lines = lines

    def std_resn(self):
        """'Fix' residue names which means to change them to standard, e.g. RA5 -> A

        Works on self.lines, and returns the result to self.lines.

        Will change things like::

            # URI -> U, URA -> U
            1xjr_clx_charmm.pdb:ATOM    101  P   URA A   5      58.180  39.153  30.336  1.00 70.94
            rp13_Dokholyan_1_URI_CYT_ADE_GUA_hydrogens.pdb:ATOM  82  P   URI A   4     501.633 506.561 506.256  1.00  0.00         P
        """
        lines = []
        for l in self.lines:
            nl = l.replace('RA5', '  A')  # RA should be the last!!!!
            nl = nl.replace('RA3', '  A')
            nl = nl.replace('ADE', '  A')
            nl = nl.replace(' RA', '  A')
            nl = nl.replace(' rA', '  A')

            nl = nl.replace('RC5', '  C')
            nl = nl.replace('RC3', '  C')
            nl = nl.replace('CYT', '  C')
            nl = nl.replace(' RC', '  C')
            nl = nl.replace(' rC', '  C')

            nl = nl.replace('RG5', '  G')
            nl = nl.replace('RG3', '  G')
            nl = nl.replace('GUA', '  G')
            nl = nl.replace(' RG', '  G')
            nl = nl.replace(' rG', '  G')

            nl = nl.replace('RU5', '  U')
            nl = nl.replace('RU3', '  U')
            nl = nl.replace('URA', '  U')
            nl = nl.replace('URI', '  U')
            nl = nl.replace('URY', '  U')
            nl = nl.replace(' RU', '  U')
            nl = nl.replace(' rU', '  U')

            nl = nl.replace('RT5', '  T')
            nl = nl.replace('RT3', '  T')
            nl = nl.replace('THY', '  T')
            nl = nl.replace(' RT', '  T')
            nl = nl.replace(' rT', '  T')

            lines.append(nl)

        self.lines = lines

    def check_res_if_std_prot(self):
        wrong = []
        for r in self.res:
            if r not in AMINOACID_CODES:
                wrong.append(r)
        return wrong

    def write(self, outfn='', verbose=False):
        """Write ```self.lines``` to a file (and add END file)

        Args:
            outfn (str): file to save, if outfn is '', then simply use self.fn
            verbose (Boolen): be verbose or not

        Returns:
            None

        """
        if outfn == '':
            outfn = self.fn
        f = open(outfn, 'w')
        # test if there is anything to write, if not, it's likely that the
        # file is not a PDB file, e.g. .outCR
        if not self.lines:
            raise Exception('Nothing to write. Is the input a PDB file? ', self.fn)
        for l in self.lines:
            f.write(l + '\n')
        if not l.startswith('END'):
            f.write('END')
        f.close()
        if verbose:
            print('Write %s' % outfn)

    def get_atom_num(self, line):
        """Extract atom number from a line of PDB file
        Arguments:
          * line = ATOM line from a PDB file
        Output:
          * atom number (int)
        """
        return int(''.join([x for x in line[6:11] if x.isdigit()]))

    def get_res_num(self, line):
        """Extract residue number from a line of PDB file
        Arguments:
          * line = ATOM line from a PDB file
        Output:
          * residue number as an integer
        """
        return int(''.join([x for x in line[22:27] if x.isdigit()]))

    def get_res_code(self, line):
        """Get residue code from a line of a PDB file
        """
        #if not line.startswith('ATOM'):
        #    return None
        return line[17:20]

    def shift_atom_names(self):
        nlines = []
        for l in self.lines:
            if l.startswith('ATOM'):
                atom_name = self.get_atom_code(l)
                l = self.set_atom_code(l, atom_name)
            nlines.append(l)
        self.lines = nlines

    def prune_elements(self):
        nlines = []
        for l in self.lines:
            if l.startswith('ATOM'):
                l = l[:76] + ' ' + l[78:]
            nlines.append(l)
        self.lines = nlines

    def get_atom_code(self, line):
        """Get atom code from a line of a PDB file
        """
        if not line.startswith('ATOM'):
            return None
        return line[12:16].replace(' ', '').strip()

    def get_atom_coords(self, line):
        """Get atom coordinates from a line of a PDB file
        """
        if not line.startswith('ATOM'):
            return None
        return tuple(map(float, line[31:54].split()))

    def set_atom_coords(self, line, x, y, z):
        """Get atom coordinates from a line of a PDB file
        """
        line = line[:30] + (f"{x:>8.3f}") + line[38:]
        line = line[:38] + (f"{y:>8.3f}") + line[46:]
        line = line[:46] + (f"{z:>8.3f}") + line[54:]
        return  line

    def set_line_bfactor(self, line, bfactor):
        if not line.startswith('ATOM'):
            return None
        return line[:60] + (" %5.2f" % bfactor) + line[66:]

    def set_atom_occupancy(self, line, occupancy):
        """set occupancy for line"""
        return line[:54] + (" %5.2f" % occupancy) + line[60:]

    def set_atom_code(self, line, code):
        """Add atom name/code:
        
           ATOM      1  OP2   C A   1      29.615  36.892  42.657  1.00  1.00          O
                        ^^^                                                            ^ and element
        """
        return line[:12] + ' ' + code + ' ' * (3 - len(code)) + line[16:77] + code[0] + line[78:]

    def set_res_code(self, line, code):
        """
        Args:
            lines
            code
        path (str): The path of the file to wrap
        field_storage (FileStorage): The :class:Y instance to wrap
            temporary (bool): Whether or not to delete the file when the File
            instance is destructed

        Returns:
            BufferedFileStorage: A buffered writable file descriptor
        """
        return line[:17] + code.rjust(3) + line[20:]

    def get_chain_id(self, line):
        return line[21:22]

    def get_all_chain_ids(self):
        """
        Returns:
           set: chain ids, e.g. set(['A', 'B'])
        """
        chain_ids = []
        for l in self.lines:
            chain_id = self.get_chain_id(l)
            if chain_id and chain_id not in chain_ids:
                chain_ids.append(chain_id)
        return chain_ids

    def get_atom_index(self, line):
        try:
            return int(line[6:11])
        except:
            return None

    def set_atom_index(self, line, index):
        return line[:6] + str(index).rjust(5) + line[11:]

    def reindex_atom_index(self):
        self.nlines = []
        for i, l in enumerate(self.lines):
            nl = self.set_atom_index(l, i + 1)  # start from 1
            self.nlines.append(nl)
        self.lines = self.nlines
        return self.nlines

    def get_res_index(self, line):
        return int(line[22:26])

    def set_res_index(self, line, index):
        return line[:23] + str(index).rjust(3) + line[26:]

    def set_chain_id(self, line, chain_id):
        return line[:21] + chain_id + line[22:]

    def get_rnapuzzle_ready(self, renumber_residues=True, fix_missing_atoms=True,
                            rename_chains=True,
                            ignore_op3 = False,
                            report_missing_atoms=True, keep_hetatm=False, backbone_only=False,
                            no_backbone = False, bases_only = False, save_single_res = False,
                            ref_frame_only = False,
                            p_only = False,
                            check_geometry = False,
                            conect = False,
                            conect_no_linkage = False,
                            verbose=False):  # :, ready_for="RNAPuzzle"):
        """Get rnapuzzle (SimRNA) ready structure.

        Clean up a structure, get current order of atoms.

        :param renumber_residues: boolean, from 1 to ..., second chain starts from 1 etc.
        :param fix_missing_atoms: boolean, superimpose motifs from the minilibrary and copy-paste missing atoms, this is super crude, so should be used with caution.

        Submission format @http://ahsoka.u-strasbg.fr/rnapuzzles/

        Run :func:`rna_tools.rna_tools.lib.RNAStructure.std_resn` before this function to fix names.
        
        .. image:: ../pngs/rebuild_op1op2_backbone.png
        Figure: (Starting from left) input structure, structure with rebuilded atoms, and reference. The B fragment is observed in the reference used here as a “benchmark”, fragment A is reconstructed atoms (not observed in the reference"). 201122

        - 170305 Merged with get_simrna_ready and fixing OP3 terminal added
        - 170308 Fix missing atoms for bases, and O2'

        .. image:: ../pngs/fix_missing_o_before_after.png
        Fig. Add missing O2' atom (before and after).

        .. image:: ../pngs/fix_missing_superposition.png
        Fig. The residue to fix is in cyan. The G base from the library in red. Atoms O4', C2', C1' are shared between the sugar (in cyan) and the G base from the library (in red). These atoms are used to superimpose the G base on the sugar, and then all atoms from the base are copied to the residues.

        .. image:: ../pngs/fix_missing_bases.png
        **Fig.** Rebuild ACGU base-less. It's not perfect but good enough for some applications.

        .. warning:: It was only tested with the whole base missing!

        .. warning:: requires: Biopython

        Selection of atoms:
        
        - posphate group (3x, OP1 ,P, OP2),
        - connector (2x O5', C5'), /5x
        - sugar (5x, C4', O4', C3', O3', C1', C2'), /10
        - extra oxygens from sugar (2x, O2' O3'), for now it's /12!
        - A (10x), G (11x), C (8x), U(8x), max 12+11=23

        And 27 unique atoms: {'N9', 'O2', 'OP2', "O2'", "O4'", 'C8', "O3'", "C1'", 'C2', 'C6', "C5'", 'N6', 'C5', "C4'", 'C4', "O5'", "C3'", 'O6', 'N2', 'N7', 'OP1', 'N1', 'N4', 'P', "C2'", 'N3', 'O4'}.
        """

        if verbose:
            logger.setLevel(logging.DEBUG)

        try:
            from Bio import PDB
            from Bio.PDB import PDBIO
            import warnings
            warnings.filterwarnings('ignore', '.*Invalid or missing.*',)
            warnings.filterwarnings('ignore', '.*with given element *',)
        except:
            sys.exit('Error: Install biopython to use this function (pip biopython)')

        import copy
        # for debugging
        #renumber_residues = True
        # if ready_for == "RNAPuzzle":

        if p_only:
            G_ATOMS = "P".split()
            A_ATOMS = "P".split()
            U_ATOMS = "P".split()
            C_ATOMS = "P".split()
        elif backbone_only:
            G_ATOMS = "P OP1 OP2 O5' C5'".split()
            A_ATOMS = "P OP1 OP2 O5' C5'".split()
            U_ATOMS = "P OP1 OP2 O5' C5'".split()
            C_ATOMS = "P OP1 OP2 O5' C5'".split()
            #G_ATOMS = "P OP1 OP2 O5' C5' C4' O4' C3' O3' C2' O2' C1'".split()
            #A_ATOMS = "P OP1 OP2 O5' C5' C4' O4' C3' O3' C2' O2' C1'".split()
            #U_ATOMS = "P OP1 OP2 O5' C5' C4' O4' C3' O3' C2' O2' C1'".split()
            #C_ATOMS = "P OP1 OP2 O5' C5' C4' O4' C3' O3' C2' O2' C1'".split()

        elif ref_frame_only:
            G_ATOMS = "P OP1 OP2".split()
            A_ATOMS = "P OP1 OP2".split()
            U_ATOMS = "P OP1 OP2".split()
            C_ATOMS = "P OP1 OP2".split()
            
        elif no_backbone:
            G_ATOMS = "C5' C4' O4' C3' O3' C2' O2' C1' N9 C8 N7 C5 C6 O6 N1 C2 N2 N3 C4".split() 
            A_ATOMS = "C5' C4' O4' C3' O3' C2' O2' C1' N9 C8 N7 C5 C6 N6 N1 C2 N3 C4".split()     
            U_ATOMS = "C5' C4' O4' C3' O3' C2' O2' C1' N1 C2 O2 N3 C4 O4 C5 C6".split()
            C_ATOMS = "C5' C4' O4' C3' O3' C2' O2' C1' N1 C2 O2 N3 C4 N4 C5 C6".split()

        elif bases_only:
            G_ATOMS = "N9 C8 N7 C5 C6 O6 N1 C2 N2 N3 C4".split()
            A_ATOMS = "N9 C8 N7 C5 C6 N6 N1 C2 N3 C4".split()
            U_ATOMS = "N1 C2 O2 N3 C4 O4 C5 C6".split()
            C_ATOMS = "N1 C2 O2 N3 C4 N4 C5 C6".split()
        else:
            G_ATOMS = "P OP1 OP2 O5' C5' C4' O4' C3' O3' C2' O2' C1' N9 C8 N7 C5 C6 O6 N1 C2 N2 N3 C4".split() # 23 
            A_ATOMS = "P OP1 OP2 O5' C5' C4' O4' C3' O3' C2' O2' C1' N9 C8 N7 C5 C6 N6 N1 C2 N3 C4".split()    # 22
            U_ATOMS = "P OP1 OP2 O5' C5' C4' O4' C3' O3' C2' O2' C1' N1 C2 O2 N3 C4 O4 C5 C6".split()          # 20
            C_ATOMS = "P OP1 OP2 O5' C5' C4' O4' C3' O3' C2' O2' C1' N1 C2 O2 N3 C4 N4 C5 C6".split()          # 20

        # hmm.. is it the same as RNApuzzle???
        # if ready_for == "SimRNA":
        #    G_ATOMS = "P OP1 OP2 O5' C5' C4' O4' C3' O3' C2' O2' C1' N9 C8 N7 C5 C6 O6 N1 C2 N2 N3 C4".split()
        #    A_ATOMS = "P OP1 OP2 O5' C5' C4' O4' C3' O3' C2' O2' C1' N9 C8 N7 C5 C6 N6 N1 C2 N3 C4".split()
        #    U_ATOMS = "P OP1 OP2 O5' C5' C4' O4' C3' O3' C2' O2' C1' N1 C2 O2 N3 C4 O4 C5 C6".split()
        #    C_ATOMS = "P OP1 OP2 O5' C5' C4' O4' C3' O3' C2' O2' C1' N1 C2 O2 N3 C4 N4 C5 C6".split()

        tf = tempfile.NamedTemporaryFile(delete=False)
        ftmp = tf.name
        self.write(ftmp, verbose=False)

        parser = PDB.PDBParser()
        #try:
        struct = parser.get_structure('', ftmp)
        #except:
        #    print('Error in ' + self.fn)
        #    sys.exit(1)
        model = struct[0]

        s2 = PDB.Structure.Structure(struct.id)
        m2 = PDB.Model.Model(model.id)

        chains2 = []

        missing = []
        fixed = []
        protein_chains_remmoved = []

        new_chains = list(string.ascii_uppercase)
        remarks = []
        if ignore_op3:
             remarks.append("REMARK 250  don't add OP3 at the start of chain")
        # get path to mini db with models to rebuilt structures
        currfn = __file__
        if currfn == '':
            path = '.'
        else:
            path = os.path.dirname(currfn)
        if os.path.islink(currfn):  # path + os.sep + os.path.basename(__file__)):
            path = os.path.dirname(os.readlink(
                path + os.sep + os.path.basename(currfn)))

        # for each chain #
        for chain in model.get_list():
            logger.debug('chain: %s' % chain)

            # is it RNA? ############################
            protein_like = 0
            for c, r in enumerate(chain, 1):
                if r.resname in AMINOACID_CODES:
                    protein_like += 1
            if (protein_like / float(c + 1)) > .8:  # 90%
                protein_chains_remmoved.append(chain.get_id())
            # ######################################

            res = []
            for r in chain:
                res.append(r)

            res = copy.copy(res)

            # start chains from A..BCD. etc

            if rename_chains:
                try:
                    chain.id = new_chains.pop(0)
                except ValueError:
                    # ValueError: Cannot change id from `A` to `A`.
                    # The id `A` is already used for a sibling of this entity.
                    # so keep it as it was
                    pass

            c2 = PDB.Chain.Chain(chain.id)

            c = 1  # new chain, goes from 1 !!! if renumber True
            prev_r = '' # init prev_r 

            conects = []
            atom_index = 0
            for r in res:
                #
                #  deal with heteratm
                #
                if r.id[0].startswith('H_') or r.id[0].startswith('W'):
                    if keep_hetatm:
                        c2.add(r)
                    else:
                        # str(r) % r.id[0].replace('H_', '').strip())
                        remarks.append('REMARK 250 Hetatom to be removed from file: ' + str(r))
                    continue
                # hack for amber/qrna
                r.resname = r.resname.strip()
                if r.resname == 'RC3':
                    r.resname = 'C'
                if r.resname == 'RU3':
                    r.resname = 'U'
                if r.resname == 'RG3':
                    r.resname = 'G'
                if r.resname == 'RA3':
                    r.resname = 'A'

                if r.resname == 'C3':
                    r.resname = 'C'
                if r.resname == 'U3':
                    r.resname = 'U'
                if r.resname == 'G3':
                    r.resname = 'G'
                if r.resname == 'A3':
                    r.resname = 'A'

                if r.resname == 'RC5':
                    r.resname = 'C'
                if r.resname == 'RU5':
                    r.resname = 'U'
                if r.resname == 'RG5':
                    r.resname = 'G'
                if r.resname == 'RA5':
                    r.resname = 'A'

                if r.resname == 'C5':
                    r.resname = 'C'
                if r.resname == 'U5':
                    r.resname = 'U'
                if r.resname == 'G5':
                    r.resname = 'G'
                if r.resname == 'A5':
                    r.resname = 'A'

                if r.resname.strip() == 'RC':
                    r.resname = 'C'
                if r.resname.strip() == 'RU':
                    r.resname = 'U'
                if r.resname.strip() == 'RG':
                    r.resname = 'G'
                if r.resname.strip() == 'RA':
                    r.resname = 'A'

                # unmodified rna 2MG -> G and take only G atoms
                if (r.resname.strip() not in ['C', 'U', 'G', 'A']) and \
                        (r.resname.strip()[-1] in ['C', 'U', 'G', 'A']):
                    r.resname = r.resname.strip()[-1].strip()

                r2 = PDB.Residue.Residue(r.id, r.resname.strip(), r.segid)
                if renumber_residues:
                    r2.id = (r2.id[0], c, r2.id[2])  # renumber residues
                #
                # experimental: fixing missing OP3.
                # Only for the first residues.
                #
                if c == 1:
                    # if p_missing
                    p_missing = True
                    # if p_missing:
                    #    try:
                    #        x = r["O5'"]
                    #        x.id =       ' P'
                    #        x.name =     ' P'
                    #        x.fullname = ' P'
                    #        print "REMARK 000 FIX O5' -> P fix in chain ", chain.id
                    #    except:
                    #        pass
                    for a in r:
                        if a.id == 'P':
                            p_missing = False
                    logger.debug('p_missing %s' % p_missing)

                    if p_missing and fix_missing_atoms:
                        currfn = __file__
                        if currfn == '':
                            path = '.'
                        else:
                            path = os.path.dirname(currfn)
                        if os.path.islink(currfn):  # path + os.sep + os.path.basename(__file__)):
                            path = os.path.dirname(os.readlink(
                                path + os.sep + os.path.basename(currfn)))

                        po3_struc = PDB.PDBParser().get_structure('', path + '/data/PO3_inner.pdb')
                        po3 = [po3_atom for po3_atom in po3_struc[0].get_residues()][0]

                        r_atoms = [r["O4'"], r["C4'"], r["C3'"]]
                        po3_atoms = [po3["O4'"], po3["C4'"], po3["C3'"]]

                        sup = PDB.Superimposer()
                        sup.set_atoms(r_atoms, po3_atoms)
                        rms = round(sup.rms, 3)

                        sup.apply(po3_struc.get_atoms())  # to all atoms of po3

                        r.add(po3['P'])
                        r.add(po3['OP1'])
                        r.add(po3['OP2'])
                        try:
                            r.add(po3["O5'"])
                        except:
                            del r["O5'"]
                            r.add(po3["O5'"])

                        fixed.append(['add OP3 at the beginning of the chain ', chain.id, r, r.id[1]])

                    p_missing = False  # off this function

                    # save it
                    #io = PDB.PDBIO()
                    #io.set_structure( po3_struc )
                    # io.save("po3.pdb")

                #
                # fix missing O2'
                #
                o2p_missing = True
                for a in r:
                    logger.debug('o2p_missing: %s %s %s' % (r, o2p_missing, a.id))
                    if a.id == "O2'":
                        o2p_missing = False
                logger.debug('o2p_missing: %s', o2p_missing)

                if o2p_missing and fix_missing_atoms:
                    currfn = __file__
                    if currfn == '':
                        path = '.'
                    else:
                        path = os.path.dirname(currfn)
                    if os.path.islink(currfn):  # path + os.sep + os.path.basename(__file__)):
                        path = os.path.dirname(os.readlink(
                            path + os.sep + os.path.basename(currfn)))

                    o2p_struc = PDB.PDBParser().get_structure('', path + '/data/o2prim.pdb')
                    o2p = [o2p_atom for o2p_atom in o2p_struc[0].get_residues()][0]

                    try:
                        r_atoms = [r["C3'"], r["C2'"], r["C1'"]]
                    except:
                        ic(r)
                    o2p_atoms = [o2p["C3'"], o2p["C2'"], o2p["C1'"]]

                    sup = PDB.Superimposer()
                    sup.set_atoms(r_atoms, o2p_atoms)
                    rms = round(sup.rms, 3)

                    sup.apply(o2p_struc.get_atoms())  # to all atoms of o2p

                    r.add(o2p["O2'"])
                    logger.debug('fixing o2p for ' % r)
                    fixed.append(['add O2\' ', chain.id, r, c])

                o2p_missing = False  # off this function
                ######## fixing of missing OP1 and OP2 atoms in backbone ###########
                if fix_missing_atoms:
                    if 'OP1' not in r:
                        if prev_r:
                            op4 = PDB.PDBParser().get_structure('', path + '/data/op4.pdb')
                            op4a = [a for a in op4[0].get_residues()][0]
                            if 'P' not in r:
                                print("Error missing P of residue " + chain.id +  ':' + str(r.id[1]) + ". Sorry, I can't rebuild missing atoms!")
                                exit()
                            r_atoms = [r["O5'"], r["P"], prev_r["O3'"]] #  r["C5'"], 
                            op4_atoms = [op4a["O5'"], op4a["P"], op4a["O3'"]] # op4a["C5'"]] #, 

                            sup = PDB.Superimposer()
                            sup.set_atoms(r_atoms, op4_atoms)
                            sup.apply(op4.get_atoms())

                            r.add(op4a["OP1"])
                            r.add(op4a["OP2"])
                            fixed.append(['add the missing OP1 and OP2', chain.id, r, r.id[1]])

                        else:
                            remarks.append("REMARK 250 Warning: Can't fix missing OP1 or/and OP2 atoms of " + str(r))
                #
                # fix missing C (the whole base at the moment)
                #
                if str(r.get_resname()).strip() == "C" and fix_missing_atoms:
                    for a in r:
                        if a.id == "N1":
                            break
                    else:
                        C_struc = PDB.PDBParser().get_structure('', path + '/data/C.pdb')
                        C = [C_atom for C_atom in C_struc[0].get_residues()][0]

                        r_atoms = [r["O4'"], r["C2'"], r["C1'"]]
                        C_atoms = [C["O4'"], C["C2'"], C["C1'"]]

                        sup = PDB.Superimposer()
                        sup.set_atoms(r_atoms, C_atoms)
                        rms = round(sup.rms, 3)

                        sup.apply(C_struc.get_atoms())  # to all atoms of C

                        r.add(C["N1"])
                        r.add(C["C2"])
                        r.add(C["O2"])
                        r.add(C["N3"])
                        r.add(C["C4"])
                        r.add(C["N4"])
                        r.add(C["C5"])
                        r.add(C["C6"])

                        fixed.append(['add the whole base C', chain.id, r, r.id[1]])

                #
                # fix missing U (the whole base at the moment)
                #
                if str(r.get_resname()).strip() == "U" and fix_missing_atoms:
                    for a in r:
                        if a.id == "N1":
                            break
                    else:
                        U_struc = PDB.PDBParser().get_structure('', path + '/data/U.pdb')
                        U = [U_atom for U_atom in U_struc[0].get_residues()][0]

                        r_atoms = [r["O4'"], r["C2'"], r["C1'"]]
                        U_atoms = [U["O4'"], U["C2'"], U["C1'"]]

                        sup = PDB.Superimposer()
                        sup.set_atoms(r_atoms, U_atoms)
                        rms = round(sup.rms, 3)

                        sup.apply(U_struc.get_atoms())  # to all atoms of U

                        r.add(U["N1"])
                        r.add(U["C2"])
                        r.add(U["O2"])
                        r.add(U["N3"])
                        r.add(U["C4"])
                        r.add(U["O4"])
                        r.add(U["C5"])
                        r.add(U["C6"])

                        fixed.append(['add the whole base U', chain.id, r, r.id[1]])
                #
                # fix missing G (the whole base at the moment)
                #
                if str(r.get_resname()).strip() == "G" and fix_missing_atoms:
                    for a in r:
                        if a.id == "N1":
                            break
                    else:
                        G_struc = PDB.PDBParser().get_structure('', path + '/data/G.pdb')
                        G = [G_atom for G_atom in G_struc[0].get_residues()][0]

                        r_atoms = [r["O4'"], r["C2'"], r["C1'"]]
                        G_atoms = [G["O4'"], G["C2'"], G["C1'"]]

                        sup = PDB.Superimposer()
                        sup.set_atoms(r_atoms, G_atoms)
                        rms = round(sup.rms, 3)

                        sup.apply(G_struc.get_atoms())  # to all atoms of G

                        r.add(G["N9"])
                        r.add(G["C8"])
                        r.add(G["N7"])
                        r.add(G["C5"])
                        r.add(G["C6"])
                        r.add(G["O6"])
                        r.add(G["N1"])
                        r.add(G["C2"])
                        r.add(G["N2"])
                        r.add(G["N3"])
                        r.add(G["C4"])

                        fixed.append(['add the whole base G', chain.id, r, r.id[1]])
                #
                # fix missing A (the whole base at the moment)
                #
                if str(r.get_resname()).strip() == "A" and fix_missing_atoms:
                    for a in r:
                        if a.id == "N1":
                            break
                    else:
                        A_struc = PDB.PDBParser().get_structure('', path + '/data/A.pdb')
                        A = [A_atom for A_atom in A_struc[0].get_residues()][0]

                        r_atoms = [r["O4'"], r["C2'"], r["C1'"]]
                        A_atoms = [A["O4'"], A["C2'"], A["C1'"]]

                        sup = PDB.Superimposer()
                        sup.set_atoms(r_atoms, A_atoms)
                        rms = round(sup.rms, 3)

                        sup.apply(A_struc.get_atoms())  # to all atoms of A

                        r.add(A["N9"])
                        r.add(A["C8"])
                        r.add(A["N7"])
                        r.add(A["C5"])
                        r.add(A["C6"])
                        r.add(A["N6"])
                        r.add(A["N1"])
                        r.add(A["C2"])
                        r.add(A["N3"])
                        r.add(A["C4"])

                        fixed.append(['add the whole base A', chain.id, r, r.id[1]])

                #
                # strip residues of extra atoms, not in G_ATOMS in this case
                #
                if str(r.get_resname()).strip() == "G":
                    for an in G_ATOMS:
                        if c == 1 and ignore_op3:
                            if an in ['P', 'OP1', 'OP2']:
                                continue
                        try:
                            if c == 1 and an == "O5'" and p_missing:
                                r2.add(x)
                            else:
                                r2.add(r[an])
                        except KeyError:
                            # print 'Missing:', an, r, ' new resi', c
                            missing.append([an, chain.id, r, r.id[1]])
                    c2.add(r2)

                elif str(r.get_resname()).strip() == "A":
                    for an in A_ATOMS:
                        if c == 1 and ignore_op3:
                            if an in ['P', 'OP1', 'OP2']:
                                continue
                        try:
                            if c == 1 and an == "O5'" and p_missing:
                                r2.add(x)
                            else:
                                r2.add(r[an])
                        except KeyError:
                            # print 'Missing:', an, r, ' new resi', c
                            missing.append([an, chain.id, r, r.id[1]])
                    c2.add(r2)

                elif str(r.get_resname()).strip() == "C":
                    for an in C_ATOMS:
                        if c == 1 and ignore_op3:
                            if an in ['P', 'OP1', 'OP2']:
                                continue
                        try:
                            if c == 1 and an == "O5'" and p_missing:
                                r2.add(x)
                            else:
                                r2.add(r[an])
                        except:
                            # print 'Missing:', an, r, ' new resi', c
                            missing.append([an, chain.id, r, r.id[1]])
                    c2.add(r2)

                elif str(r.get_resname()).strip() == "U":
                    for an in U_ATOMS:
                        if c == 1 and ignore_op3:
                            if an in ['P', 'OP1', 'OP2']:
                                continue
                        try:
                            if c == 1 and an == "O5'" and p_missing:
                                r2.add(x)
                            else:
                                r2.add(r[an])
                        except KeyError:
                            # print 'Missing:', an, r,' new resi', c
                            missing.append([an, chain.id, r, r.id[1]])
                    c2.add(r2)


                # save each residue a sa single ife
                if save_single_res:
                    from Bio.PDB import Structure
                    # Create an empty structure
                    structure = Structure.Structure("my_structure")
                    model = Model.Model(0)
                    chain = Chain.Chain('A')
                    chain.add(r2)
                    model.add(chain)
                    structure.add(model)

                    io = PDBIO()
                    io.set_structure(structure)
                    io.save(f"{self.fn}_{r2.id[1]}.pdb")

                # add CONET
                if conect:
                    ic(atom_index, r2)
                    conects.extend(generate_conect_records(r2.get_resname().strip(), atom_index, conect_no_linkage))
                    atom_index += len(r2)
                    print(conect)

                prev_r = r  # hack to keep preview residue to be used in the function
                            # e.g., to get an atom from this residue
                c += 1
            chains2.append(c2)

        io = PDBIO()
        s2.add(m2)
        for chain2 in chains2:
            m2.add(chain2)
        # print c2
        # print m2
        io.set_structure(s2)

        tf = tempfile.NamedTemporaryFile(delete=False)
        fout = tf.name
        io.save(fout)

        if fixed:
            remarks.append('REMARK 250 Fixed atoms/residues:')
            for i in fixed:
                remarks.append(
                    ' '.join(['REMARK 250  -', str(i[0]), 'in chain:', str(i[1]), str(i[2]), 'residue #', str(i[3])]))

        if missing and report_missing_atoms:
            remarks.append('REMARK 250 Missing atoms:')
            for i in missing:
                remarks.append(' '.join(['REMARK 250   +', str(i[0]),
                                         'chain:', str(i[1]), str(i[2]), 'residue #', str(i[3])]))
            #raise Exception('Missing atoms in %s' % self.fn)

        if protein_chains_remmoved:
            remarks.append('REMARK 250 Chains that seem to be proteins removed and : ' +
                           ' '.join(protein_chains_remmoved))
        #

        # fix ter 'TER' -> TER    1528        G A  71
        #
        s = RNAStructure(fout)
        if check_geometry:
            s.check_geometry()
        self.lines = s.lines
        c = 0
        # ATOM   1527  C4    G A  71       0.000   0.000   0.000  1.00  0.00           C
        nlines = []
        no_ters = 0
        for l in self.lines:
            ## align atoms to the left #######################################################
            # ATOM   3937    P   C B 185      11.596  -7.045  26.165  1.00  0.00           P
            # ATOM   3937  P     C B 185      11.596  -7.045  26.165  1.00  0.00           P
            if l.startswith('ATOM'):
                atom_code = self.get_atom_code(l)
                l = self.set_atom_code(l, atom_code)
            ##################################################################################
            if l.startswith('TER'):
                #                pass  # leave it for now this
                atom_l = self.lines[c - 1]
                new_l = 'TER'.ljust(80)   # TER    1528        G A  71 <<<'
                new_l = self.set_atom_index(new_l, str(self.get_atom_index(atom_l) + 1 + no_ters))
                new_l = self.set_res_code(new_l, self.get_res_code(atom_l))
                new_l = self.set_chain_id(new_l, self.get_chain_id(atom_l))
                new_l = self.set_res_index(new_l, self.get_res_index(atom_l))
                nlines.append(new_l)
                #nlines.append(l)
                no_ters += 1
            else:
                if self.get_atom_index(l):
                    l = self.set_atom_index(l, self.get_atom_index(
                        l) + no_ters)  # 1 ter +1 2 ters +2 etc
                nlines.append(l)
            c += 1
        self.lines = nlines
        if conect:
            self.lines += conects
        return remarks

    def set_occupancy_atoms(self, occupancy):
        """
        :param occupancy:
        """
        nlines = []
        for l in self.lines:
            if l.startswith('ATOM'):
                l = self.set_atom_occupancy(l, 0.00)
                nlines.append(l)
            else:
                nlines.append(l)
        self.lines = nlines

    def edit_occupancy_of_pdb(txt, pdb, pdb_out, v=False):
        """Make all atoms 1 (flexi) and then set occupancy 0 for seletected atoms.
        Return False if error. True if OK
        """
        struc = PDB.PDBParser().get_structure('struc', pdb)

        txt = txt.replace(' ', '')
        if v:
            print (txt)
        l = re.split('[,:;]', txt)
        if v:
            print (l)

        for s in struc:
            for c in s:
                for r in c:
                    for a in r:
                        a.set_occupancy(1)  # make it flaxi

        for i in l:  # ['A', '1-10', '15', '25-30', 'B', '1-10']

            if i in string.ascii_letters:
                if v:
                    print('chain', i)
                chain_curr = i
                continue

            if i.find('-') > -1:
                start, ends = i.split('-')
                if start > ends:
                    print('Error: range start > end ' + i)  # >>sys.stderr
                    return False
                index = list(range(int(start), int(ends) + 1))
            else:
                index = [int(i)]

            for i in index:
                # change b_factor
                try:
                    atoms = struc[0][chain_curr][i]
                except KeyError:
                    if i == chain_curr:
                        print('Error: Chain ' + chain_curr +
                              ' not found in the PDB structure')  # >>sys.stderr,
                    else:
                        print('Error: Residue ' + chain_curr + ':' + str(i) +
                              ' found in the PDB structure')  # >>sys.stderr,
                        return False
                for a in atoms:
                    a.set_occupancy(0)

        io = PDBIO()
        io.set_structure(struc)
        io.save(pdb_out)
        print('Saved ', pdb_out)
        return True

    def view(self):
        os.system('pymol ' + self.fn)

    def remove(self, verbose):
        """Delete file, self.fn"""
        os.remove(self.fn)
        if verbose:
            'File %s removed' % self.fn

    def __repr__(self):
        return 'RNAStructure %s' % self.fn


    def get_remarks_text(self):
        """Get remarks as text for given file.
        This function re-open files, as define as self.fn to get remarks.

        Example::

            r = RNAStructure(fout)
            remarks = r.get_remarks_txt()
            r1 = r.get_res_txt('A', 1)
            r2 = r.get_res_txt('A', 2)
            r3 = r.get_res_txt('A', 3)
            with open(fout, 'w') as f:
                f.write(remarks)
                f.write(r1)
                f.write(r2)
                f.write(r3)

            remarks is

            REMARK 250 Model edited with rna-tools
            REMARK 250  ver 3.5.4+63.g4338516.dirty 
            REMARK 250  https://github.com/mmagnus/rna-tools 
            REMARK 250  Fri Nov 13 10:15:19 2020

        """
        txt = ''
        for l in open(self.fn):
            if l.startswith("REMARK"):
                txt += l
        return txt

    def get_res_text(self, chain_id, resi):
        """Get a residue of given resi of chain_id and return as a text

        Args:
            chain_id (str): e.g., 'A'
            resi (int): e.g., 1

        Returns:
             txt: 

        Example::

            r = RNAStructure(fn)
            print(r.get_res_txt('A', 1))

            ATOM      1  O5'   G A   1      78.080 -14.909  -0.104  1.00  9.24           O  
            ATOM      2  C5'   G A   1      79.070 -15.499  -0.956  1.00  9.70           C  
            ATOM      3  C4'   G A   1      78.597 -16.765  -1.648  1.00  9.64           C  
            ATOM      4  O4'   G A   1      78.180 -17.761  -0.672  1.00  9.88           O  
            (...)

        """
        txt = ''
        for l in self.lines:
            if l.startswith("ATOM"):
                if self.get_res_num(l) == resi and self.get_chain_id(l) == chain_id:
                    txt += l + '\n'
        return txt

    def mq(self, method="RASP", verbose=False):

        if method.lower() == "rasp":
            from rna_tools.tools.mq.RASP import RASP
            r = RASP.RASP()
            return [float(i) for i in r.run(self.fn, potentials=['all'])]
            # ['-42058.4', '466223', '-0.0902109', '0', '0', '0']

        if method.lower() == "dfire":
            from rna_tools.tools.mq.Dfire import Dfire
            r = Dfire.Dfire()
            return r.run(self.fn, verbose)
        
        if method.lower() == "rna3dcnn":
            from rna_tools.tools.mq.RNA3DCNN import RNA3DCNN
            r = RNA3DCNN.RNA3DCNN()
            return r.run(self.fn, verbose)

        if method.lower() == "qrna":
            from rna_tools.tools.mq.QRNA import QRNA
            r = QRNA.QRNA()
            return r.run(self.fn, verbose)

        if method.lower() == "clashscore":
            from rna_tools.tools.mq.ClashScore import ClashScore
            r = ClashScore.ClashScore()
            return r.run(self.fn, verbose)

        if method.lower() == "analyzegeometry":
            from rna_tools.tools.mq.AnalyzeGeometry import AnalyzeGeometry
            r = AnalyzeGeometry.AnalyzeGeometry()
            return r.run(self.fn, verbose)

        raise MethodUnknown('Define corrent method')

    def get_empty_line(self):
        l = "ATOM      1  C5'   A A   3      25.674  19.091   3.459  1.00  1.00           X"
        return l
    
    def add_line(self, l):
        self.lines.append(l)

def add_header(version=None):
    now = time.strftime("%c")
    txt = 'REMARK 250 Model edited with rna-tools\n'
    txt += 'REMARK 250  ver %s \nREMARK 250  https://github.com/mmagnus/rna-tools \nREMARK 250  %s' % (
        version, now)
    return txt


def edit_pdb(f, args):
    """Edit your structure.

    The function can take ``A:3-21>A:1-19`` or even syntax like this
    ``A:3-21>A:1-19,B:22-32>B:20-30`` and will do an editing.

    The output is printed, line by line. Only ATOM lines are edited!

    Examples::

        $ rna_pdb_tools.py --edit 'A:3-21>A:1-19' 1f27_clean.pdb > 1f27_clean_A1-19.pdb

    or even::

        $ rna_pdb_tools.py --edit 'A:3-21>A:1-19,B:22-32>B:20-30' 1f27_clean.pdb > 1f27_clean_renumb.pdb

    """
    # open a new file
    s = RNAStructure(f)
    output = ''
    if not args.no_hr:
        output += add_header() + '\n'
        output += 'REMARK 250    HEADER --edit ' + args.edit + '\n'

    # --edit 'A:3-21>A:1-19,B:22-32>B:20-30'
    if args.edit.find(',') > -1:
        # more than one edits
        edits = args.edit.split(',')  # ['A:3-21>A:1-19', 'B:22-32>B:20-30']
        selects = []
        for e in edits:
            selection_from, selection_to = select_pdb_fragment(
                e.split('>')[0]), select_pdb_fragment(e.split('>')[1])
            if len(selection_to) != len(selection_from):
                raise Exception('len(selection_to) != len(selection_from)')
            selects.append([selection_from, selection_to])
    else:
        # one edit
        e = args.edit
        selection_from, selection_to = select_pdb_fragment(
            e.split('>')[0]), select_pdb_fragment(e.split('>')[1])
        if len(selection_to) != len(selection_from):
            raise Exception('len(selection_to) != len(selection_from)')
        selects = [[selection_from, selection_to]]

    # go ever all edits: ['A:3-21>A:1-19','B:22-32>B:20-30']
    for l in s.lines:
        if l.startswith('ATOM'):
                # get chain and resi
            chain = l[21:22].strip()
            resi = int(l[22:26].strip())

            if_selected_dont_print = False
            # for selections
            for select in selects:
                selection_from, selection_to = select
                if chain in selection_from:
                    if resi in selection_from[chain]:
                            # [1,2,3] mapping from [4,5,10], you want to know how to map 1
                            # 1 is [0] element of first list, so you have to index first list
                            # to get 0, with this 0 you can get 4 out of second list [4,5,10][0] -> 4
                        nl = list(l)
                        chain_new = list(selection_to.keys())[0]  # chain form second list
                        nl[21] = chain_new  # new chain
                        index = selection_from[chain].index(int(resi))  # get index of 1
                        resi_new = str(selection_to[chain_new][index]).rjust(
                            4)  # 'A' [1,2,3] -> '  1'
                        nl[22:26] = resi_new
                        nl = ''.join(nl)
                        if_selected_dont_print = True
                        output += nl + '\n'
            if not if_selected_dont_print:
                output += l + '\n'
        else:  # if not atom
            output += l + '\n'
    return output


def collapsed_view(args):
    """Collapsed view of pdb file. Only lines with C5' atoms are shown and TER, MODEL, END.

    example::

        [mm] rna_tools git:(master) $ python rna-pdb-tools.py --cv input/1f27.pdb
        ATOM      1  C5'   A A   3      25.674  19.091   3.459  1.00 16.99           C
        ATOM     23  C5'   C A   4      19.700  19.206   5.034  1.00 12.65           C
        ATOM     43  C5'   C A   5      14.537  16.130   6.444  1.00  8.74           C
        ATOM     63  C5'   G A   6      11.726  11.579   9.544  1.00  9.81           C
        ATOM     86  C5'   U A   7      12.007   7.281  13.726  1.00 11.35           C
        ATOM    106  C5'   C A   8      12.087   6.601  18.999  1.00 12.74           C
        TER"""
    r = RNAStructure(args.file)
    for l in r.lines:
        at = r.get_atom_code(l)
        if at == "P": # C5'":
            print(l)
        if l.startswith('TER') or l.startswith('MODEL') or l.startswith('END'):
            print(l)


def fetch(pdb_id, path="."):
    """fetch pdb file from RCSB.org
    https://files.rcsb.org/download/1Y26.pdb

    Args:
    - pdb_id, but also a chain can be specified, 1jj2:A+B+C
    
    Returns:
    - a path to a file

    TODO: na_pdb_tools.py --extract A:1-25+B:30-57 1jj2.pdb"""

    chains = ''
    pdb_id = pdb_id.replace('_', ':') # to accept also 1jj2_A
    if ':' in pdb_id:
        pdb_id, chains = pdb_id.split(':') # >>> 'X:A+B+C'.split(':') ['X', 'A+B+C']

    if pdb_id == 'rp':
        os.system('wget https://github.com/RNA-Puzzles/standardized_dataset/archive/master.tar.gz -O - | tar -xz')
        return
    
    import urllib3
    http = urllib3.PoolManager()

    # try:
    pdb_id = pdb_id.replace('.pdb', '')
    response = http.request('GET', 'https://files.rcsb.org/download/' + pdb_id + '.pdb')
    if not response.status == 200:
        raise PDBFetchError()

    # except urllib3.HTTPError:
    #    raise Exception('The PDB does not exists: ' + pdb_id)
    txt = response.data

    if path != '.':
        npath = path + os.sep + pdb_id + '.pdb'
    else:
        npath = pdb_id + '.pdb'
    print('downloading... ' + npath)
    with open(npath, 'wb') as f:
        f.write(txt)
    if chains:
        for chain in chains.split('+'):
            cmd = f'rna_pdb_tools.py --extract-chain {chain} {pdb_id}.pdb > {pdb_id}_{chain}.pdb'
            print(cmd)
            exe(cmd)
    # print('ok')
    return npath


def fetch_ba(pdb_id, path="."):
    """fetch biological assembly pdb file from RCSB.org

    >>> fetch_ba('1xjr')
    ...
    """
    try:
        import urllib3
    except ImportError:
        print('urllib3 is required')
        return
    http = urllib3.PoolManager()
    # try:
    response = http.request('GET', url='https://files.rcsb.org/download/' +
                            pdb_id.lower() + '.pdb1')
    if not response.status == 200:
        raise PDBFetchError()
    txt = response.data

    npath = path + os.sep + pdb_id + '_ba.pdb'
    print('downloading...' + npath)
    with open(npath, 'wb') as f:
        f.write(txt)
    print('ok')
    return pdb_id + '_ba.pdb'


def fetch_cif_ba(cif_id, path="."):
    """fetch biological assembly cif file from RCSB.org"""
    import urrlib3
    http = urllib3.PoolManager()
    # try:
    response = http.request('GET', url='https://files.rcsb.org/download/' +
                            cif_id.lower() + '-assembly1.cif')
    if not response.status == 200:
        raise PDBFetchError()
    txt = response.data

    npath = path + os.sep + cif_id + '_ba.cif'
    print('downloading...' + npath)
    with open(npath, 'wb') as f:
        f.write(txt)
    print('ok')
    return cif_id + '_ba.cif'

def fetch_cif(cif_id, path="."):
    """fetch biological assembly cif file from RCSB.org"""
    import urllib3
    http = urllib3.PoolManager()
    # try:
    if '_' in cif_id:
        cif_id = cif_id.split('_')[0]  
    ic(cif_id)
    cif_id = cif_id.replace('.cif', '')
    url = 'https://files.rcsb.org/download/' + cif_id.lower() + '.cif'
    print(url)
    response = http.request('GET', url)
    if not response.status == 200:
        raise PDBFetchError()
    txt = response.data

    npath = path + os.sep + cif_id + '.cif'
    #print('downloading... ' + npath)
    with open(npath, 'wb') as f:
        f.write(txt)
    return cif_id + '.cif'

def replace_chain(struc_fn, insert_fn, chain_id):
    """Replace chain of the main file (struc_fn) with some new chain (insert_fn) of given chain id.

    Args:
       struc_fn (str): path to the main PDB file
       insert_fn (str): path to the file that will be injected in into the main PDB file
       chain_id (str): chain that will be inserted into the main PDB file

    Returns:
       string: text in the PDB format
    """
    struc = RNAStructure(struc_fn)
    insert = RNAStructure(insert_fn)

    output = ''
    inserted = False
    for l in struc.lines:
        if l.startswith('ATOM'):
            chain = l[21]
            if chain == chain_id:
                if not inserted:
                    for insertl in insert.lines:
                        if not insertl.startswith('HEADER') and not insertl.startswith('END'):
                            output += insertl + '\n'
                    inserted = True
                continue
            # insert pdb
            output += l + '\n'
    return output.strip()


def replace_atoms(struc_fn, insert_fn, verbose=False):
    """Replace XYZ coordinate of the file (struc_fn)  with XYZ from another file (insert_fn).

    This can be useful if you want to replace positions of atoms, for example, one base only. The lines are muted based on atom name, residue name, chain, residue index (marked with XXXX below).::
    
    ATOM     11  N1    A 2  27     303.441 273.472 301.457  1.00  0.00           N   # file
    ATOM      1  N1    A 2  27     300.402 273.627 303.188  1.00 99.99           N   # insert 
    ATOM     11  N1    A 2  27     300.402 273.627 303.188  1.00  0.00           N   # inserted
                 XXXXXXXXXXXXXXXX    # part used to find lines to be replaced

     ATOM      1  P     A 2  27     295.653 270.783 300.135  1.00119.29           P   # next line

    Args:
       struc_fn (str): path to the main PDB file
       insert_fn (str): path to the file that will be injected in into the main PDB file

    Returns:
       string: text in the PDB format
    """
    struc = RNAStructure(struc_fn)
    insert = RNAStructure(insert_fn)

    output = ''
    for l in struc.lines:
        inserted = False
        if l.startswith('ATOM'):
            idx = l[13:26]#.strip() # P     A 2  27
            for li in insert.lines:
                idxi = li[13:26]#.strip()
                if idx == idxi:
                    ln = l[:30] + li[30:54] + l[54:] + '\n' # only coords replace (!)
                    if verbose:
                        print(l)
                        print(li)
                        print(ln)
                        print()
                    inserted = True
                    output += ln
            if not inserted:
                output += l + '\n'
                inserted = False
    return output.strip()

def set_chain_for_struc(struc_fn, chain_id, save_file_inplace=False, skip_ter=True):
    """Quick & dirty function to set open a fn PDB format, set chain_id
    and save it to a file. Takes only lines with ATOM and TER."""
    txt = ''
    for line in open(struc_fn):
        if skip_ter:
            if line.startswith('ATOM') or line.startswith('TER'):
                # if TER line is only TER, not like TER atom chain etc
                # then just keep TER there and don't add any chain to id
                if line == 'TER':
                    pass
                else:
                    l = line[:21] + chain_id + line[22:]
                txt += l
            else:
                txt += line
        else:
            if line.startswith('ATOM'):
                l = line[:21] + chain_id + line[22:]
                txt += l
            elif line.startswith('TER'):
                continue
            else:
                txt += line
    if save_file_inplace:
        with open(struc_fn, 'w') as f:
             f.write(txt)
    return txt.strip()

def load_rnas(path, verbose=True):
    """Load structural files (via glob) and return a list of RNAStructure objects.
    
    Examples::

        rnas = rtl.load_rnas('../rna_tools/input/mq/*.pdb')
    
    """
    rs = []
    import glob
    for f in glob.glob(path):
        r = RNAStructure(f)
        rs.append(r)
    return rs

# main
if '__main__' == __name__:
    f1 = "input/t2-4-ACA.pdb"
    f2 = "input/to-replace.pdb"
    r1 = RNAStructure(f1)
    r2 = RNAStructure(f2)    
    t = replace_atoms(f1, f2)
    with open('output/replaced.pdb', 'w') as f: f.write(t)

    fn = "input/1a9l_NMR_1_2_models.pdb"
    r = RNAStructure(fn)
    t = r.get_res_text('A', 1)
    with open('output/1a9l_NMR_1_2_models_R1.pdb', 'w') as f: f.write(t)

    fn = "input/remarks.pdb"
    r = RNAStructure(fn)
    t = r.get_remarks_text()
    with open('output/remarks_only.pdb', 'w') as f: f.write(t)

    fn = 'input/image'
    print('fn:', fn)
    struc = RNAStructure(fn)
    print(' pdb?:', struc.is_pdb())
    # print( atoms:', struc.get_no_lines())

    fn = 'input/na.pdb'
    s = RNAStructure(fn)
    print(s.detect_molecule_type())
    #res = get_all_res(na)
    # print 'what is?', what_is(res)
    # print res
    print('non standard:', s.check_res_if_std_na())
    print('is protein:', s.detect_molecule_type())

    fn = 'input/prot.pdb'
    s = RNAStructure(fn)
    print('non standard:', s.check_res_if_std_prot())
    print('is protein:',  s.detect_molecule_type())

    fn = 'input/rna-ru.pdb'
    s = RNAStructure(fn)
    print('non standard:', s.check_res_if_supid_rna())
    print('is protein:', s.detect_molecule_type())

    fn = 'input/na_highAtomNum.pdb'
    print(fn)
    s = RNAStructure(fn)
    s.renum_atoms()
    s.write('output/na_highAtomNum.pdb')

    fn = 'input/na_solvet_old_format.pdb'
    print(fn)
    s = RNAStructure(fn)
    s.fix_op_atoms()
    s.remove_hydrogen()
    s.remove_ion()
    s.remove_water()
    s.write('output/na_solvet_old_format.pdb')

    fn = 'input/na_solvet_old_format.pdb'
    print(fn)
    s = RNAStructure(fn)
    s.std_resn()
    s.remove_hydrogen()
    s.remove_ion()
    s.remove_water()
    s.write('output/na_solvet_old_format.pdb')

    #fn = 'input/na_solvet_old_format__.pdb'
    #s = RNAStructure(fn)
    # s.std_resn()
    # s.remove_hydrogen()
    # s.remove_ion()
    # s.remove_water()
    # s.renum_atoms()
    # s.fix_op_atoms()
    # s.write('output/na_solvet_old_format__.pdb')

    fn = 'input/1xjr.pdb'
    s.std_resn()
    s.remove_hydrogen()
    s.remove_ion()
    s.remove_water()
    s.renum_atoms()
    s.fix_op_atoms()
    s.write('output/1xjr.pdb')

    fn = 'input/decoy0165_amb.pdb'
    print(fn)
    s = RNAStructure(fn)
    s.std_resn()
    s.remove_hydrogen()
    s.remove_ion()
    s.remove_water()
    s.renum_atoms()
    s.fix_O_in_UC()
    s.fix_op_atoms()
    s.write('output/decoy0165_amb_clx.pdb')

    fn = 'input/farna.pdb'
    print(fn)
    s = RNAStructure(fn)
    s.std_resn()
    s.remove_hydrogen()
    s.remove_ion()
    s.remove_water()
    s.fix_op_atoms()
    s.renum_atoms()
    s.write('output/farna.pdb')

    fn = 'input/farna.pdb'
    print(fn)

    r = RNAStructure(fn)
    print(r.is_mol2())

    if True:
        print('================================================')
        print ("input/1xjr_clx_fChimera_noIncludeNumbers.mol2")
        r = RNAStructure("input/1xjr_clx_fChimera_noIncludeNumbers.mol2")
        print(r.is_mol2())
        r.mol2toPDB('/tmp/x.pdb')

        r = RNAStructure('/tmp/x.pdb')
        print(r.get_report)
        r.std_resn()
        r.remove_hydrogen()
        r.remove_ion()
        r.remove_water()
        r.fix_op_atoms()
        r.renum_atoms()
        r.fixU__to__U()
        r.write("output/1xjr_clx_fChimera_noIncludeNumbers.mol2")

    if True:
        r = RNAStructure("input/2du3_prot_bound.mol2")
        print(r.is_mol2())
        outfn = r.mol2toPDB()
        print(r.get_report)

    print('================================================')
    fn = "input/3e5fA-nogtp_processed_zephyr.pdb"
    r = RNAStructure(fn)
    print(r.is_mol2())
    #outfn = r.mol2toPDB()
    print(r.is_amber_like())
    print(r.get_report)

    print(r.get_preview())

    r.std_resn()

    print(r.get_preview())

    r.remove_hydrogen()
    r.remove_ion()
    r.remove_water()
    #renum_atoms(t, t)
    #fix_O_in_UC(t, t)
    #fix_op_atoms(t, t)
    r.write('output/3e5fA-nogtp_processed_zephyr.pdb')

    print()
    fn = "input/1xjr_clx_charmm.pdb"
    print(fn)
    s = RNAStructure(fn)
    s.std_resn()
    s.remove_hydrogen()
    s.remove_ion()
    s.remove_water()
    s.write('output/1xjr_clx_charmm.pdb')

    #renum_atoms(t, t)
    #fix_O_in_UC(t, t)
    #fix_op_atoms(t, t)

    print()
    fn = "input/dna_fconvpdb_charmm22.pdb"
    print(fn)
    r = RNAStructure(fn)
    r.get_preview()
    r.resn_as_dna()
    r.remove_hydrogen()
    r.remove_ion()
    r.remove_water()
    r.std_resn()
    print(r.get_head())
    print(r.get_tail())
    print(r.get_preview())
    r.write("output/dna_fconvpdb_charmm22.pdb")

    print()
    fn = "input/1a9l_NMR_1_2_models.pdb"
    print(fn)
    r = RNAStructure(fn)
    r.write("output/1a9l_NMR_1_2_models_lib.pdb")
    # r.get_text() # get #1 model

    import doctest
    doctest.testmod()
