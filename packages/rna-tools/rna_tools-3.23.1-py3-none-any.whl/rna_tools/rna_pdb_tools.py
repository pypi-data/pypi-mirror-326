#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""rna_pdb_tools - a swiss army knife to manipulation of RNA pdb structures

Usage::

   $ rna_pdb_tools.py --delete A:46-56 --inplace *.pdb

    $ rna_pdb_tools.py --get-seq *
    # BujnickiLab_RNApuzzle14_n01bound
    > A:1-61
    # BujnickiLab_RNApuzzle14_n02bound
    > A:1-61
    CGUUAGCCCAGGAAACUGGGCGGAAGUAAGGCCCAUUGCACUCCGGGCCUGAAGCAACGCG
    [...]

See `rna_pdb_merge_into_one.py` to merge PDB files in the order as you like into one NMR-like (multimodel) file

Examples::

    rna_pdb_tools.py --backbone-only   --get-rnapuzzle-ready  --inplace --suffix=bo examples/4GXY_min.pdb

To extract specific atoms for each residue and write them to separate PDB file (next to the input files, following syntax "<input>_<resid>.pdb")::

    rna_pdb_tools.py --rpr input/4GXY_min.pdb --save-single-res --ref-frame-only

Atoms presets::

  --backbone-only       used only with --get-rnapuzzle-ready, keep only backbone (= remove bases)
  --ref-frame-only      used only with --get-rnapuzzle-ready, keep only reference frames, OP1 OP2 P
  --no-backbone         used only with --get-rnapuzzle-ready, remove atoms of backbone (define as P OP1 OP2 O5')
  --bases-only          used only with --get-rnapuzzle-ready, keep only atoms of bases
      
.. image:: ../pngs/276411138-236435ff-2944-4bec-ab75-dca0d1e3aacf.jpg


-v is for verbose, --version for version ;)
"""
import argparse
import textwrap
import os
import shutil
import sys
import tempfile
import glob
import os
from rna_tools.rna_tools_lib import edit_pdb, add_header, get_version, \
                          collapsed_view, fetch, fetch_ba, fetch_cif, replace_chain, RNAStructure, \
                          select_pdb_fragment, sort_strings, set_chain_for_struc
from rna_tools.tools.rna_x3dna.rna_x3dna import x3DNA


def get_parser():
    version = os.path.basename(os.path.dirname(os.path.abspath(__file__))), get_version(__file__)
    version = version[1].strip()
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument('--version', help='', action='version', version=version)

    parser.add_argument('-r', '--report', help='get report',
                        action='store_true')

    parser.add_argument('--no-progress-bar', help='for --no-progress-bar for --rpr', action='store_true')

    parser.add_argument('--renum-atoms', help='renumber atoms, tested with --get-seq',
                        action='store_true')

    parser.add_argument('--renum-nmr', help='',
                        action='store_true')

    parser.add_argument('--conect', help='add conect to rpr file',  action='store_true')

    parser.add_argument('--conect-no-linkage', help='dont add conect from our residue to another',  action='store_true')

    parser.add_argument('--renum-residues-dirty', help='',  action='store_true')

    parser.add_argument('--undo', help='undo operation of action done --inplace, , rename "backup files" .pdb~ to pdb, ALL files in the folder, not only ~ related to the last action (that you might want to revert, so be careful)',  action='store_true')

    parser.add_argument('--delete-anisou', help='remove files with ANISOU records, works with --inplace',
                        action='store_true')

    parser.add_argument('--remove0', help='remove atoms of X=0 position',
                        action='store_true')

    parser.add_argument('--fix', help='fix a PDB file, ! external program, pdbfixer used to fix missing atoms',
                        action='store_true')

    parser.add_argument('--to-mol2', help='fix a PDB file, ! external program, pdbfixer used to fix missing atoms',
                        action='store_true')

    parser.add_argument('--split-alt-locations', help='splits atoms, e.g. for alt locs A and B, it splits atoms two MODELS (all localizations A goes into MODEL1 and all localizations B goes into MODEL2',
                        action='store_true')

    parser.add_argument('-c', '--clean', help='get clean structure',
                        action='store_true')

    parser.add_argument('--is-pdb', help='check if a file is in the pdb format',
                        action='store_true')

    parser.add_argument('--is-nmr', help='check if a file is NMR-style multiple model pdb',
                        action='store_true')

    parser.add_argument('--nmr-dir', help='make NMR-style multiple model pdb file from a set of files \n\n' +
                        "  rna_pdb_tools.py --nmr-dir . 'cwc15_u5_fragments*.pdb' > ~/Desktop/cwc15-u5.pdb\n\n" +
                        "please use '' for pattern file recognition, this is a hack to deal with folders with\n"
                        "thousands of models, if you used only *.pdb then the terminal will complain that you\n"
                        "selected to many files.")

    parser.add_argument('--un-nmr', help="""split NMR-style multiple model pdb files into individual models [biopython],

   rna_pdb_tools.py  --un-nmr  split.pdb
   2
   /Users/magnus/Desktop/3hl2/split_1.pdb
   /Users/magnus/Desktop/3hl2/split_2.pdb

""",
                        action='store_true')

    parser.add_argument('--orgmode', help='get a structure in org-mode format <sick!>',
                        action='store_true')

    parser.add_argument('--get-chain', help='get chain, one or many, e.g, A, but now also ABC works')

    parser.add_argument('--fetch', action='store_true', help='fetch file from the PDB db, e.g., 1xjr,\nuse \'rp\' to fetch, fetch a given join, 4w90:C or 4w90_C'  +
                        'the RNA-Puzzles standardized_dataset [around 100 MB]')

    parser.add_argument('--fetch-cif',  action='store_true', help='')
    
    parser.add_argument('--fetch-header', action='store_true', help='')

    parser.add_argument('--fetch-ba', action='store_true',
                        help='fetch biological assembly from the PDB db')

    parser.add_argument('--fetch-chain', action='store_true', help='fetch a structure in extract chain, e.g. 6bk8 H')

    parser.add_argument('--fetch-fasta', action='store_true', help='fetch a fasta/sequence for given PDB ID, e.g. 6bk8')

    parser.add_argument('--get-seq', help='get seq', action='store_true')

    parser.add_argument('--rgyration', help='get seq', action='store_true')

    parser.add_argument('--color-seq', help='color seq, works with --get-seq', action='store_true')

    parser.add_argument('--ignore-files', help='files to be ingored, .e.g, \'solution\'')
    
    parser.add_argument('--compact',
                        help=textwrap.dedent("""with --get-seq, get it in compact view'
$ rna_pdb_tools.py --get-seq --compact *.pdb
# 20_Bujnicki_1
ACCCGCAAGGCCGACGGCGCCGCCGCUGGUGCAAGUCCAGCCACGCUUCGGCGUGGGCGCUCAUGGGU # A:1-68
# 20_Bujnicki_2
ACCCGCAAGGCCGACGGCGCCGCCGCUGGUGCAAGUCCAGCCACGCUUCGGCGUGGGCGCUCAUGGGU # A:1-68
# 20_Bujnicki_3
ACCCGCAAGGCCGACGGCGCCGCCGCUGGUGCAAGUCCAGCCACGCUUCGGCGUGGGCGCUCAUGGGU # A:1-68
# 20_Bujnicki_4

"""), action='store_true')

    parser.add_argument('--hide-warnings', help='hide warnings, works with --get-chain, it hides warnings that given changes are not detected in a PDB file', action='store_true')

    parser.add_argument('--get-ss', help='get secondary structure', action='store_true')

    parser.add_argument('--rosetta2generic', help='convert ROSETTA-like format to a generic pdb',
                        action='store_true')

    parser.add_argument('--no-hr', help='do not insert the header into files',
                        action='store_true')

    parser.add_argument('--renumber-residues', help='by defult is false',
                        action='store_true')

    parser.add_argument('--dont-rename-chains',
                        help=textwrap.dedent("""used only with --get-rnapuzzle-ready.
By default:
   --get-rnapuzzle-ready rename chains from ABC.. to stop behavior switch on this option
"""),
                        action='store_true')

    parser.add_argument('--dont-fix-missing-atoms',
                        help="""used only with --get-rnapuzzle-ready""",
                        action='store_true')

    parser.add_argument('--inspect',
                        help="inspect missing atoms (technically decorator to --get-rnapuzzle-ready without actually doing anything but giving a report on problems)",
                        action='store_true')
    
    parser.add_argument('--collapsed-view', help='',
                        action='store_true')

    parser.add_argument('--cv', help='alias to collapsed_view',
                        action='store_true')

    parser.add_argument('-v', '--verbose', help='tell me more what you\'re doing, please!',
                        action='store_true')

    parser.add_argument('--mutate', help=textwrap.dedent("""mutate residues,
e.g.,
      --mutate "A:1a+2a+3a+4a,B:1a"
to mutate to adenines the first four nucleotides of the chain A
and the first nucleotide of the chain B"""))

    parser.add_argument('--edit',
                        dest="edit",
                        default='',
                        help="edit 'A:6>B:200', 'A:2-7>B:2-7'")

    parser.add_argument('--rename-chain',
                        help="edit 'A>B' to rename chain A to chain B")

    parser.add_argument('--swap-chains', help='B>A, rename A to _, then B to A, then _ to B')

    parser.add_argument('--set-chain', help='set chain for all ATOM lines and TER (quite brutal function)')

    parser.add_argument('--replace-chain',
                        default='',
                        help=textwrap.dedent("""a file PDB name with one chain that will be used to
replace the chain in the original PDB file,
the chain id in this file has to be the same with the chain id of the original chain"""))

    parser.add_argument('--delete',  # type="string",
                        dest="delete",
                        default='',
                        help="delete the selected fragment, e.g. A:10-16, or for more than one fragment --delete 'A:1-25+30-57'")

    parser.add_argument('--extract',  # type="string",
                        dest="extract",
                        default='',
                        help="extract the selected fragment, e.g. A:10-16, or for more than one fragment --extract 'A:1-25+30-57', or even 'A:1-25+B:30-57'")

    parser.add_argument('--extract-chain',
                         help="extract chain, e.g. A")

    parser.add_argument('--uniq', help=textwrap.dedent("""
rna_pdb_tools.py --get-seq --uniq '[:5]' --compact --chain-first * | sort
A:1-121        ACCUUGCGCAACUGGCGAAUCCUGGGGCUGCCGCCGGCAGUACCC...CA # rp13nc3295_min.out.1
A:1-123        ACCUUGCGCGACUGGCGAAUCCUGAAGCUGCUUUGAGCGGCUUCG...AG # rp13cp0016_min.out.1
A:1-123        ACCUUGCGCGACUGGCGAAUCCUGAAGCUGCUUUGAGCGGCUUCG...AG # zcp_6537608a_ALL-000001_AA
A:1-45 57-71   GGGUCGUGACUGGCGAACAGGUGGGAAACCACCGGGGAGCGACCCGCCGCCCGCCUGGGC # solution
"""))

    parser.add_argument('--chain-first', help="", action='store_true')
    parser.add_argument('--oneline', help="", action='store_true')

    parser.add_argument('--replace-htm', help="", action='store_true')

    parser.add_argument('--fasta',
                        help= textwrap.dedent("""with --get-seq, show sequences in fasta format,
can be combined with --compact (mind, chains will be separated with ' ' in one line)

$ rna_pdb_tools.py --get-seq --fasta --compact input/20_Bujnicki_1.pdb
> 20_Bujnicki_1
ACCCGCAAGGCCGACGGC GCCGCCGCUGGUGCAAGUCCAGCCACGCUUCGGCGUGGGCGCUCAUGGGU

"""), action='store_true')

    parser.add_argument('--cif2pdb', help="convert cif to PDB, fancy way", action='store_true')
    parser.add_argument('--pdb2cif', help="[PyMOL Python package required]", action='store_true')

    parser.add_argument('--mdr', help='get structures ready for MD (like rpr but without first)',
                        action='store_true')

    x = parser.add_argument_group('RNAPUZZLE-READY')
    x.add_argument('--get-rnapuzzle-ready',
                        help=textwrap.dedent("""get RNApuzzle ready (keep only standard atoms).'
Be default it does not renumber residues, use --renumber-residues
[requires BioPython]"""), action='store_true')

    x.add_argument('--rpr', help='alias to get_rnapuzzle ready)',
                        action='store_true')


    rpr = parser.add_argument_group('CAN BE COMBINED WITH')# --get-rnapuzzle-ready (or --rpr) can be combined with')

    rpr.add_argument('--keep-hetatm', help='keep hetatoms', action='store_true')

    rpr.add_argument('--inplace', help=textwrap.dedent("""in place edit the file! [experimental,
only for get_rnapuzzle_ready, --delete, --get-ss, --get-seq, --edit-pdb]"""),
                        action='store_true')

    rpr.add_argument('--here', help=textwrap.dedent("""save a file next to the original file with auto suffix
for --extract it's .extr.pdb"""),
                        action='store_true')

    rpr.add_argument('--suffix', help=textwrap.dedent("""when used with --inplace allows you to change a name of a new file, --suffix del will give <file>_del.pdb (mind added _)"""))

    rpr.add_argument('--replace-hetatm', help="replace 'HETATM' with 'ATOM' [tested only with --get-rnapuzzle-ready]",
                        action="store_true")

    rpr.add_argument('--dont-report-missing-atoms',
                        help="""used only with --get-rnapuzzle-ready""",
                        action='store_true')

    rpr.add_argument('--backbone-only',
                        help="""used only with --get-rnapuzzle-ready, keep only backbone (= remove bases)""",
                        action='store_true')

    rpr.add_argument('--p-only',
                        help="""used only with --get-rnapuzzle-ready, keep p backbone (= remove bases)""",
                        action='store_true')

    rpr.add_argument('--ref-frame-only',
                        help="""used only with --get-rnapuzzle-ready, keep only reference frames, OP1 OP2 P""",
                        action='store_true')

    rpr.add_argument('--no-backbone',
                        help="""used only with --get-rnapuzzle-ready, remove atoms of backbone (define as P OP1 OP2 O5')""",
                        action='store_true')

    rpr.add_argument('--bases-only',
                        help="""used only with --get-rnapuzzle-ready, keep only atoms of bases""",
                        action='store_true')

    rpr.add_argument('--save-single-res',
                        help="""used only with --get-rnapuzzle-ready, for each residue create a new pdb output file, you can combine it with --bases-only etc.""",
                        action='store_true')

    parser.add_argument('file', help='file', nargs='+')
    #parser.add_argument('outfile', help='outfile')
    return parser


# main
if __name__ == '__main__':
    # get version
    version = os.path.basename(os.path.dirname(os.path.abspath(__file__))), get_version(__file__)
    version = version[1].strip()

    # get parser and arguments
    parser = get_parser()

    args = parser.parse_args()

    # quick fix for one files vs file-s
    if list == type(args.file) and len(args.file) == 1:
        args.file = args.file[0]

    if args.report:
        s = RNAStructure(args.file)
        print(s.get_report)
        print(s.get_preview())
        print(s.get_info_chains())

    if args.clean:
        s = RNAStructure(args.file)
        s.decap_gtp()
        s.std_resn()
        s.remove_hydrogen()
        s.remove_ion()
        s.remove_water()
        s.renum_atoms()
        s.fix_O_in_UC()
        s.fix_op_atoms()
        # print s.get_preview()
        # s.write(args.outfile)
        if not args.no_hr:
            print(add_header(version))
        print(s.get_text())

    if args.get_seq:
        # quick fix - make a list on the spot
        if list != type(args.file):
            args.file = [args.file]
        ##################################
        analyzed = []
        for f in args.file:
            #####################################
            if args.uniq:
                subname = eval('f' + args.uniq)
                if subname in analyzed:
                    continue
                else:
                    analyzed.append(subname)
            ########
            s = RNAStructure(f)
            if not s.is_pdb():
                print('Error: Not a PDB file %s' % f)
                sys.exit(1)
            s.decap_gtp()
            s.std_resn()
            s.remove_hydrogen()
            s.remove_ion()
            s.remove_water()
            if args.renum_atoms:
                s.renum_atoms()
            s.fix_O_in_UC()
            s.fix_op_atoms()

            output = ''

            # with # is easier to grep this out
            if args.fasta:
                # s.fn vs s.name
                output += s.get_seq(compact=args.compact, chainfirst=args.chain_first, fasta=args.fasta, addfn=s.name, color=args.color_seq) + '\n'
            elif args.oneline:
                output += s.get_seq(compact=args.compact, chainfirst=args.chain_first, color=args.color_seq).strip() + ' # '+ os.path.basename(f.replace('.pdb', '')) + '\n'
            else:
                output += '# ' + os.path.basename(f.replace('.pdb', '')) + '\n'
                output += s.get_seq(compact=args.compact, chainfirst=args.chain_first, color=args.color_seq) + '\n'

            try:
                sys.stdout.write(output)
                sys.stdout.flush()
            except IOError:
                pass

    if args.get_ss:
        # quick fix - make a list on the spot
        if list != type(args.file):
            args.file = [args.file]
        ##################################
        for f in args.file:
            output = f + '\n'
            p = x3DNA(f)
            output += p.get_secstruc() + '\n'
            try:
                sys.stdout.write(output)
                sys.stdout.flush()
            except IOError:
                pass

    # getchain
    if args.get_chain:
        s = RNAStructure(args.file)
        ## s.std_resn()
        ## s.remove_hydrogen()
        ## s.remove_ion()
        ## s.remove_water()
        ## s.renum_atoms()
        ## s.fix_O_in_UC()
        ## s.fix_op_atoms()
        # print s.get_preview()
        warningmsg = ''
        for chain in list(args.get_chain):
            chain_txt = s.get_chain(chain)
            if not chain_txt.strip():
                warningmsg += 'Warning: Chain %s not detected!' % chain
            else:
                print(chain_txt)
        if not args.hide_warnings:
            if warningmsg:
                print(warningmsg)

    if args.rosetta2generic:
        s = RNAStructure(args.file)
        s.std_resn()
        s.remove_hydrogen()
        s.remove_ion()
        s.remove_water()
        s.fix_op_atoms()
        s.renum_atoms()
        # print s.get_preview()
        # s.write(args.outfile)
        if not args.no_hr:
            print(add_header(version))
        print(s.get_text())

    remarks_only = False
    if args.inspect:
        args.get_rnapuzzle_ready = True
        fix_missing_atom = False
        remarks_only = True
        args.dont_rename_chains = True
        args.renumber_residues = False

    if args.get_rnapuzzle_ready or args.rpr or args.mdr:  # rnapuzzle
        # quick fix - make a list on the spot
        if list != type(args.file):
            args.file = [args.file]
        ##################################
        # progress bar only in --inplace mode!
        if args.inplace:
            if not args.no_progress_bar:
                import progressbar
                bar = progressbar.ProgressBar(max_value=len(args.file))
                bar.update(0)

        for c, f in enumerate(args.file):
            if args.verbose:
                print(f)
            if args.inplace:
                shutil.copy(f, f + '~')

            # keep previous edits
            previous_edits = []
            with open(f) as fx:
                for l in fx:
                    if l.startswith('HEADER --'):
                        previous_edits.append(l.strip())
            ######################

            s = RNAStructure(f)
            if args.replace_hetatm:
                s.replace_hetatms()

            s.remove_hydrogen()
            s.decap_gtp()
            s.std_resn()
            s.fix_op_atoms()

            s.remove_ion()
            s.remove_water()
            # s.renum_atoms()

            s.shift_atom_names()
            s.prune_elements()

            # s.write('tmp.pdb')
            
            rename_chains = False if args.dont_rename_chains else True

            report_missing_atoms = not args.dont_report_missing_atoms
            fix_missing_atom = not args.dont_fix_missing_atoms

            ignore_op3 = False
            if args.mdr:
                ignore_op3 = True

            remarks = s.get_rnapuzzle_ready(args.renumber_residues, fix_missing_atoms=fix_missing_atom,
                                            rename_chains=rename_chains,
                                            report_missing_atoms=report_missing_atoms,
                                            backbone_only=args.backbone_only,
                                            no_backbone=args.no_backbone,
                                            bases_only=args.bases_only,
                                            p_only=args.p_only,
                                            keep_hetatm=args.keep_hetatm,
                                            ignore_op3=ignore_op3,
                                            save_single_res=args.save_single_res,
                                            ref_frame_only = args.ref_frame_only,
                                            conect=args.conect,
                                            conect_no_linkage=args.conect_no_linkage,
                                            verbose=args.verbose)

            if args.inplace:
                if args.suffix:
                    f = f.replace('.pdb', '_' + args.suffix + '.pdb')
                    if args.verbose: print(f)
                        
                with open(f, 'w') as f:
                    if not args.no_hr:
                        f.write(add_header(version) + '\n')
                    if previous_edits:
                        f.write('\n'.join(previous_edits) + '\n')
                    if remarks:
                        f.write('\n'.join(remarks) + '\n')
                    f.write(s.get_text())
                # progress bar only in --inplace mode!
                if not args.no_progress_bar:
                   bar.update(c)

            else:
                output = ''
                if not args.no_hr:
                    output += add_header(version) + '\n'
                if remarks:
                    output += '\n'.join(remarks) + '\n'
                output += s.get_text() + '\n'

                if remarks_only:
                    sys.stdout.write('\n'.join(remarks))
                    sys.stdout.flush()
                else:
                    if args.here:
                        if '_rpr' not in f:  # good idea?
                            nf = f.replace('.pdb', '_rpr.pdb')
                            with open(nf, 'w') as fio:
                                print(nf)
                                fio.write(output)
                    else:
                        try:
                            sys.stdout.write(output)
                            sys.stdout.flush()
                        except IOError:
                            pass
        # hmm... fix for problem with renumbering, i do renumbering
        # and i stop here
        # i'm not sure that this is perfect
        sys.exit(0)


    if args.renumber_residues:
        s = RNAStructure(args.file)
        s.remove_hydrogen()
        s.remove_ion()
        s.remove_water()
        s.get_rnapuzzle_ready(args.renumber_residues)
        s.renum_atoms()
        if not args.no_hr:
            print(add_header(version))
        print(s.get_text())

# args.renumber_resides_dirty
    if args.renum_residues_dirty:
        # quick fix - make a list on the spot
        if list != type(args.file):
            args.file = [args.file]
        ##################################
        for f in args.file:
            if args.inplace:
                shutil.copy(f, f + '~')

            s = RNAStructure(f)

            output = ''
            #if not args.no_hr:
            #    output += add_header(version) + '\n'
            #    output += 'HEADER --delete ' + args.delete + '\n'  # ' '.join(str(selection))
            c = 1
            old_resi = -1
            for l in s.lines:
                if l.startswith('ATOM') or l.startswith("HETATOM"):
                    resi = int(l[23:26].strip())
                    if resi != old_resi:
                        old_resi = resi
                        c += 1
                    # print(resi, c)
                    #resi = c
                    #if chain in selection:
                    #    if resi in selection[chain]:
                    #        continue  # print chain, resi
                    output += l[:23] + str(c).rjust(3) + l[26:] + '\n'
            # write: inplace
            if args.inplace:
                with open(f, 'w') as f:
                    f.write(output)
            else:  # write: to stdout
                try:
                    sys.stdout.write(output)
                    sys.stdout.flush()
                except IOError:
                    pass


    if args.undo:
        # quick fix - make a list on the spot
        dir = args.file #os.path.abso(os.path.dirname(args.file))
        for f in glob.glob(dir + '/*.pdb~'):
            if args.verbose:
                print(f, '->',f.replace('.pdb~', '.pdb'))
            os.rename(f, f.replace('.pdb~', '.pdb'))

    if args.delete:
        # quick fix - make a list on the spot
        if list != type(args.file):
            args.file = [args.file]
        ##################################
        for f in args.file:
            if args.inplace:
                shutil.copy(f, f + '~')

            selection = select_pdb_fragment(args.delete)
            s = RNAStructure(f)

            output = ''
            if not args.no_hr:
                output += add_header(version) + '\n'
                output += 'HEADER --delete ' + args.delete + '\n'  # ' '.join(str(selection))
            for l in s.lines:
                if l.startswith('ATOM'):
                    chain = l[21]
                    resi = int(l[23:26].strip())
                    if chain in selection:
                        if resi in selection[chain]:
                            continue  # print chain, resi
                    output += l + '\n'

            # write: inplace
            if args.inplace:
                os.rename(f, f.replace('.pdb', '.pdb~'))                
                if args.suffix:
                    f = f.replace('.pdb', '_' + args.suffix + '.pdb')
                with open(f, 'w') as f:
                    f.write(output)
            else:  # write: to stdout
                try:
                    sys.stdout.write(output)
                    sys.stdout.flush()
                except IOError:
                    pass

    if args.replace_chain:
        # quick fix - make a list on the spot
        if list != type(args.file):
            args.file = [args.file]
        ##################################
        for f in args.file:
            if args.inplace:
                shutil.copy(f, f + '~')

            # --replace_chain <file> without A:<file> it will be easier than --x "A:<file>"
            s = RNAStructure(args.replace_chain)
            chain_ids = (s.get_all_chain_ids())
            if len(chain_ids) > 1:
                raise Exception('There is more than one chain in the inserted PDB file. There should be only one chain, the one you want to insert to the PDB.')
            out = replace_chain(f, args.replace_chain, list(chain_ids)[0])
            print(out)

    if args.mutate:
        # quick fix - make a list on the spot
        if list != type(args.file):
            args.file = [args.file]
        ##################################
        from rna_tools.tools.mini_moderna3.moderna import *

        for f in args.file:
            if args.ignore_files:
                if args.ignore_files in f:
                    continue
                
            if args.inplace:
                shutil.copy(f, f + '~')  # create a backup copy if inplace

            # create a working copy of the main file
            ftf = tempfile.NamedTemporaryFile(delete=False).name  # f temp file
            shutil.copy(f, ftf)  # create a backup copy if inplace

            # go over each chain
            # rna_pdb_tools.py --mutate 'A:1CB:1G,A:1U+B:1A' CG_AB.pdb > ~/Desktop/a.pdb
            args.mutate = args.mutate.upper()
            for m in args.mutate.split(','):  # A:1A, B:1A
                chain, resi_mutate_to = m.strip().split(':')  # A:1A+2C
                resi_mutate_to_list = resi_mutate_to.split('+')  # A:1A+2C

                model = load_model(f, chain)
                # go over each mutation in this chain
                for resi_mutate_to in resi_mutate_to_list:
                    resi = resi_mutate_to[:-1]
                    mutate_to = resi_mutate_to[-1]
                    if args.verbose:
                        print('Mutate', model[resi], 'to', mutate_to)
                    exchange_single_base(model[resi], mutate_to)

                # multi mutation in one chain
                tf = tempfile.NamedTemporaryFile(delete=False)
                model.write_pdb_file(tf.name)

                # work on the copy of f, ftf
                output = replace_chain(ftf, tf.name, chain)
                with open(ftf, 'w') as tmp:
                    tmp.write(output)

            # write: inplace
            if args.inplace:
                # ftf now is f, get ready for the final output
                if args.suffix:
                    f = f.replace('.pdb', '_' + args.suffix + '.pdb')
                # rpr on the file
                shutil.copy(ftf, f)
                os.system('rna_pdb_tools.py --rpr --no-progress-bar --inplace ' + f)
            else:  # write: to stdout
                try:
                    sys.stdout.write(output)
                    sys.stdout.flush()
                except IOError:
                    pass


# extract
    if args.extract:
        # quick fix - make a list on the spot
        if list != type(args.file):
            args.file = [args.file]
        ##################################
        for f in args.file:
            if args.inplace:
                shutil.copy(f, f + '~')

            selection = select_pdb_fragment(args.extract)
            s = RNAStructure(f)

            output = ''
            if not args.no_hr:
                output += add_header(version) + '\n'
                output += 'HEADER extract ' + args.extract + '\n'  # ' '.join(str(selection))
            for l in s.lines:
                if l.startswith('ATOM'):
                    chain = l[21]
                    resi = int(l[23:26].strip())
                    if chain in selection:
                        if resi in selection[chain]:
                            # continue  # print chain, resi
                            output += l + '\n'

            # write: inplace
            if args.inplace:
                with open(f, 'w') as f:
                    f.write(output)
            elif args.here:
                if '_extr' not in f:  # good idea?
                    nf = f.replace('.pdb', '_extr.pdb')
                    with open(nf, 'w') as fio:
                        print(nf)
                        fio.write(output)
            else:  # write: to stdout
                try:
                    sys.stdout.write(output)
                    sys.stdout.flush()
                except IOError:
                    pass


    if args.extract_chain:
        # quick fix - make a list on the spot
        if list != type(args.file):
            args.file = [args.file]
        ##################################
        for f in args.file:
            if args.inplace:
                shutil.copy(f, f + '~')

            selection = select_pdb_fragment(args.extract)
            s = RNAStructure(f)

            output = ''
            if not args.no_hr:
                output += add_header(version) + '\n'
                output += 'HEADER extract ' + args.extract + '\n'  # ' '.join(str(selection))
            for l in s.lines:
                if l.startswith('ATOM') or l.startswith('TER') or l.startswith('HETATM'):
                    chain = l[21]
                    if chain in args.extract_chain:
                        output += l + '\n'

            # write: inplace
            if args.inplace:
                with open(f, 'w') as f:
                    f.write(output)
            else:  # write: to stdout
                try:
                    sys.stdout.write(output)
                    sys.stdout.flush()
                except IOError:
                    pass

    if args.is_pdb:
        s = RNAStructure(args.file)
        output = str(s.is_pdb())
        sys.stdout.write(output + '\n')

    if args.un_nmr:
        s = RNAStructure(args.file)
        str(s.un_nmr())

    if args.is_nmr:
        struc = RNAStructure(args.file)
        output = str(struc.is_nmr(args.verbose))
        sys.stdout.write(output + '\n')

    #edit
    if args.edit:
        if list != type(args.file):
            args.file = [args.file]
        ##################################
        for f in args.file:
            if args.verbose:
                print(f)
            if args.inplace:
                shutil.copy(f, f + '~')

            output = edit_pdb(f, args)

            if args.inplace:
                with open(f, 'w') as f:
                    f.write(output)
            else:  # write: to stdout
                try:
                    sys.stdout.write(output)
                    sys.stdout.flush()
                except IOError:
                    pass


    if args.fetch:
        if list != type(args.file):
            args.file = [args.file]
        ##################################
        for f in args.file:
            fn = fetch(f)
            
    if args.fetch_fasta:


        pdb_id = args.file
        pdb_id = pdb_id.replace('.pdb', '')

        import urllib3
        http = urllib3.PoolManager()

        response = http.request('GET', 'https://www.rcsb.org/fasta/entry/' + pdb_id.upper())
        if not response.status == 200:
            raise PDBFetchError()
        else:
            txt = response.data.decode("utf-8").strip()
            print(txt)            
            if 'No valid PDB IDs were submitted' in txt:
                pass
            else:
                with open(pdb_id + '.fa', 'w') as f:
                    f.write(txt)

        
    if args.fetch_chain:
        fn = fetch(args.file[0])
        chain = args.file[1]
        nfn = fn.replace('.pdb','') + '_' + chain + '.pdb' # 6bk8_H.pdb
        #cmd = 'rna_pdb_tools.py --get-chain %s %s' > %s' % (chain, fn, nfn)
        cmd = 'rna_pdb_tools.py --get-chain %s %s' % (chain, fn)
        os.system(cmd)
        # print(nfn)

    if args.fetch_ba:
        fetch_ba(args.file)

    if args.fetch_header:

        import requests
        if list != type(args.file):
            args.file = [args.file]
        ##################################


        def get_pdb_header(pdb_id):
            url = f"https://files.rcsb.org/download/{pdb_id}.pdb"
            response = requests.get(url)
            response.raise_for_status()  # Check if the request was successful

            header_lines = []
            for line in response.text.splitlines():
                if line.startswith("TITLE"): #or line.startswith("COMPND") or line.startswith("SOURCE"):
                    header_lines.append(line)
                elif line.startswith("ATOM"):  # Stop once ATOM records begin
                    break
            
            return " ".join([l.replace('TITLE', '').strip() for l in header_lines])

        for f in args.file:
                f = f.replace('.pdb', '').replace('.cif', '')
                pdb_id = f.split('_')[0] # _A.cif
                header = get_pdb_header(pdb_id)
                print(f'{pdb_id} {header}')

    if args.fetch_cif:
        if list != type(args.file):
            args.file = [args.file]
        ##################################
        for f in args.file:
            fetch_cif(f)

    if args.collapsed_view or args.cv:
        collapsed_view(args)

    if args.delete_anisou:
        # quick fix - make a list on the spot
        if list != type(args.file):
            args.file = [args.file]
        ##################################
        for f in args.file:
            if args.inplace:
                shutil.copy(f, f + '~')

            s = RNAStructure(f)

            output = ''
            if not args.no_hr:
                output += add_header(version) + '\n'

            for l in s.lines:
                if l.startswith('ANISOU'):
                    continue
                else:
                    output += l + '\n'

            if args.inplace:
                with open(f, 'w') as f:
                    f.write(output)
            else:  # write: to stdout
                try:
                    sys.stdout.write(output)
                    sys.stdout.flush()
                except IOError:
                    pass


    if args.swap_chains:
        # quick fix - make a list on the spot
        if list != type(args.file):
            args.file = [args.file]
        ##################################
        for f in args.file:
            if args.inplace:
                shutil.copy(f, f + '~')
            # rename_chain 'A>B'
            s = RNAStructure(f)
            output = ''
            if not args.no_hr:
                output += add_header(version) + '\n'

            chain_id_old, chain_id_new = args.swap_chains.split('>')
            if chain_id_old == chain_id_new:
                output = open(f).read() # return the file ;-) itself unchanged
            else:
                s.rename_chain(chain_id_new, '_')
                s.rename_chain(chain_id_old, chain_id_new)
                output += s.rename_chain('_', chain_id_old)

            if args.inplace:
                with open(f, 'w') as f:
                    f.write(output)
            else:  # write: to stdout
                try:
                    sys.stdout.write(output)
                    sys.stdout.flush()
                except IOError:
                    pass

    if args.rename_chain:
        # quick fix - make a list on the spot
        if list != type(args.file):
            args.file = [args.file]
        ##################################
        for f in args.file:
            if args.inplace:
                shutil.copy(f, f + '~')
            # rename_chain 'A>B'
            s = RNAStructure(f)
            chain_id_old, chain_id_new = args.rename_chain.split('>')
            output = ''
            if not args.no_hr:
                output += add_header(version) + '\n'
            output += s.rename_chain(chain_id_old, chain_id_new)
            if args.inplace:
                with open(f, 'w') as f:
                    f.write(output)
            else:  # write: to stdout
                try:
                    sys.stdout.write(output)
                    sys.stdout.flush()
                except IOError:
                    pass


    if args.split_alt_locations:
        # quick fix - make a list on the spot
        if list != type(args.file):
            args.file = [args.file]
        ##################################
        for f in args.file:
            if args.inplace:
                shutil.copy(f, f + '~')

            #s = RNAStructure(f)
            s = open(f)
            output = ''
            if not args.no_hr:
                output += add_header(version) + '\n'

            # First, collect all alternative locations.
            alts = set()
            for l in s:
                if l.startswith('ATOM'):
                    if l[16].strip():
                        alts.add(l[16])
            s.close()

            if args.verbose:
                print('alts:', alts)

            for index, alt in enumerate(alts):
                output += 'MODEL %i' % (index + 1)
                s = open(f)
                for l in s:
                    if l.startswith('ATOM') or l.startswith('HETATM'):
                        # if empty, then print this line
                        if l[16] == ' ':
                            output += l
                        if l[16] == alt:
                            output += l
                    else:
                        output += l
                output += 'ENDMDL\n'
                s.close()

            if args.inplace:
                with open(f, 'w') as f:
                    f.write(output)
            else:  # write: to stdout
                try:
                    sys.stdout.write(output)
                    sys.stdout.flush()
                except IOError:
                    pass

    if args.orgmode:
        if args.inplace:
            shutil.copy(args.file, args.file + '~')
        s = RNAStructure(args.file)
        s.decap_gtp()
        s.std_resn()
        s.remove_hydrogen()
        s.remove_ion()
        s.remove_water()
        s.fix_op_atoms()
        s.renum_atoms()
        s.shift_atom_names()
        s.prune_elements()
        # print s.get_preview()
        # s.write(args.outfile)
        # for l in s.lines:
        #    print l

        remarks = s.get_rnapuzzle_ready(
            args.renumber_residues, fix_missing_atoms=True, rename_chains=True, verbose=args.verbose)

        with open(args.file + '~', 'w') as f:
            if not args.no_hr:
                f.write(add_header(version) + '\n')

            f.write('\n'.join(remarks) + '\n')
            f.write(s.get_text())

        try:
            from Bio import PDB
            from Bio.PDB import PDBIO
            import warnings
            warnings.filterwarnings('ignore', '.*Invalid or missing.*',)
            warnings.filterwarnings('ignore', '.*with given element *',)
        except:
            sys.exit('Error: Install biopython to use this function (pip biopython)')

        parser = PDB.PDBParser()
        struct = parser.get_structure('', args.file + '~')
        model = struct[0]

        # chains [['A', 'seq', [residues]]]
        chains = []
        for c in model.get_list():
            seq = ''
            chain = []
            for r in c:
                chain.append(str(r.get_resname().strip()) + str(r.id[1]))
                seq += r.get_resname().strip()
            chains.append([c.id, seq, chain])

        t = []
        #[['A', 'CCGCCGCGCCAUGCCUGUGGCGG', ['C1', 'C2', 'G3', 'C4', 'C5', 'G6', 'C7', 'G8', 'C9', 'C10', 'A11', 'U12', 'G13', 'C14', 'C15', 'U16', 'G17', 'U18', 'G19', 'G20', 'C21', 'G22', 'G23']], ['B', 'CCGCCGCGCCAUGCCUGUGGCGG', ['C1', 'C2', 'G3', 'C4', 'C5', 'G6', 'C7', 'G8', 'C9', 'C10', 'A11', 'U12', 'G13', 'C14', 'C15', 'U16', 'G17', 'U18', 'G19', 'G20', 'C21', 'G22', 'G23']]]
        for c in chains:
            t.append('* ' + c[0] + ':' + c[2][0][1:] + '-' + c[2][-1][1:] + ' ' + c[1])
            for r in c[2]:
                t.append('** ' + c[0] + ':' + r)
        print('\n'.join(t))

    if args.fix:
        # quick fix - make a list on the spot
        if list != type(args.file):
            args.file = [args.file]
        ##################################
        for f in args.file:
            cmd = 'pdbfixer ' + f + ' --add-atoms all --add-residues'
            print(cmd)
            os.system(cmd)
            if args.inplace:
                shutil.move("output.pdb", f)
            else:
                shutil.move("output.pdb", f.replace('.pdb', '_fx.pdb'))
                            
    if args.to_mol2:
        # quick fix - make a list on the spot
        if list != type(args.file):
            args.file = [args.file]
        ##################################
        for f in args.file:
            cmd = 'obabel -i pdb ' + f + ' -o mol2 -O ' + f.replace('.pdb', '.mol2')
            print(cmd)
            os.system(cmd)


    if args.nmr_dir:
        files = sort_strings(glob.glob(args.nmr_dir + '/' + args.file))

        c = 1

        for f in files:
            #s = RNAStructure(f)
            print("MODEL        " + str(c))
            # at some point I could use RNAStructure for this
            print(open(f).read())
            #print(s.get_text(add_end=False))
            print('ENDMDL')
            c += 1
        print('END')

    if args.set_chain:
        if list != type(args.file):
            args.file = [args.file]

        for f in args.file:
            txt = set_chain_for_struc(f, args.set_chain)
            if args.inplace:
                shutil.move(f, f.replace('.pdb', '.pdb~'))
                with open(f, 'w') as fi:
                    fi.write(txt)
            else:
                print(txt)

    if args.remove0:
        if list != type(args.file):
            args.file = [args.file]

        for f in args.file:
            s = RNAStructure(f)
            txt = ''
            for l in s.lines:
                if s.get_atom_coords(l) == (0.0, 0.0, 0.0):
                    continue
                else:
                    txt += l + '\n'

            if args.inplace:
                shutil.move(f, f.replace('.pdb', '.pdb~'))
                with open(f, 'w') as fi:
                    fi.write(txt)
            else:
                print(txt)

    if args.replace_htm:
        if list != type(args.file):
            args.file = [args.file]

        for f in args.file:
            with open(f) as fn:
                txt = fn.read()
            txt = txt.replace('HETATM', 'ATOM  ')
            if args.inplace:
                shutil.move(f, f.replace('.pdb', '.pdb~'))
                with open(f, 'w') as fi:
                    fi.write(txt)
            else:
                print(txt)

    if args.rgyration:
        if list != type(args.file):
            args.file = [args.file]
        # quick fix - make a list on the spot
        if list != type(args.file):
            args.file = [args.file]
        ##################################
        analyzed = []
        for f in args.file:
            #####################################
            if args.uniq:
                subname = eval('f' + args.uniq)
                if subname in analyzed:
                    continue
                else:
                    analyzed.append(subname)

            s = RNAStructure(f)
            if not s.is_pdb():
                print('Error: Not a PDB file %s' % f)
                sys.exit(1)
            s.decap_gtp()
            s.std_resn()
            s.remove_hydrogen()
            s.remove_ion()
            s.remove_water()
            if args.renum_atoms:
                s.renum_atoms()
            s.fix_O_in_UC()
            s.fix_op_atoms()

            output = ''

            # with # is easier to grep this out
            if args.fasta:
                # s.fn vs s.name
                output += s.get_seq(compact=args.compact, chainfirst=args.chain_first, fasta=args.fasta, addfn=s.name, color=args.color_seq) + '\n'
            elif args.oneline:
                output += s.get_seq(compact=args.compact, chainfirst=args.chain_first, color=args.color_seq).strip() + ' # '+ os.path.basename(f.replace('.pdb', '')) + '\n'
            else:
                N = len(s.get_seq(compact=args.compact, chainfirst=args.chain_first, color=args.color_seq))
                output += '' + os.path.basename(f.replace('.pdb', '')).ljust(60) + ' seq len: ' + str(N) + ' '
            try:
                sys.stdout.write(output)
                sys.stdout.flush()
            except IOError:
                pass

            import math
            def calc_rg():
                    """modified after https://github.com/sarisabban/Rg"""
                    coord = list()
                    mass = list()
                    for line in s.lines:
                            try:
                                    line = line.split()
                                    x = float(line[6])
                                    y = float(line[7])
                                    z = float(line[8])
                                    coord.append([x, y, z])
                                    atom = line[2][0]
                                    if atom == 'C':
                                            mass.append(12.0107)
                                    elif atom == 'O':
                                            mass.append(15.9994)
                                    elif atom == 'N':
                                            mass.append(14.0067)
                                    elif atom == 'S':
                                            mass.append(32.065)
                                    elif atom == 'P':
                                            mass.append(30.97)
                            except:
                                    pass

                    xm = [(m*i, m*j, m*k) for (i, j, k), m in zip(coord, mass)]
                    tmass = sum(mass)
                    rr = sum(mi*i + mj*j + mk*k for (i, j, k), (mi, mj, mk) in zip(coord, xm))
                    mm = sum((sum(i) / tmass)**2 for i in zip(*xm))
                    rg = math.sqrt(rr / tmass-mm)
                    return(round(rg, 3))

            def radius_of_gyration(N):
                    return round(5.5 * (N ** (1/3)), 2)

            rg = calc_rg()
            rgn = radius_of_gyration(N)
            print(f'radius of gyration: {rg}; expected for this seqlen ({N}): {rgn}, {round(rg / rgn * 100, 2)}%')

    if args.renum_nmr:
        if list != type(args.file):
            args.file = [args.file]
        txt = ''
        for f in args.file:
            c = 1
            for l in open(f):
                if l.startswith('MODEL'):
                    txt += "MODEL       " + str(c) + '\n'
                    c += 1
                elif l.strip() == 'END':
                    pass
                else:
                    txt += l
        if args.inplace:
            shutil.move(f, f.replace('.pdb', '.pdb~'))
            with open(f) as fi:
                fi.write(txt)
        else:
            print(txt)
            
    from rna_tools.rna_tools_config import PYMOL_PATH
    sys.path.insert(0, PYMOL_PATH)
    if args.cif2pdb:
        # quick fix - make a list on the spot
        if list != type(args.file):
            args.file = [args.file]
        ##################################
        for cif_file in args.file:
            from Bio.PDB import MMCIFParser, PDBIO
            parser = MMCIFParser()
            structure = parser.get_structure("structure_id", cif_file)
            pdb_file = cif_file.replace('.cif', '_fCIF.pdb')


            try:
                # Save to PDB format
                io = PDBIO()
                io.set_structure(structure)
                io.save(pdb_file)

                print(f'saved: {pdb_file}')
                # open a file add remarks
                new_file = ''
                with open(pdb_file, 'r') as f:
                    if not args.no_hr:
                        new_file += add_header(version) + '\n'
                    new_file += f.read()

                with open(pdb_file, 'w') as f:
                    f.write(new_file)

            except:
                print('Warning: some of the chains in this mmCIF file has chain names with more char than 1, e.g. AB, and the PDB format needs single-letter code, e.g. A.')

                def has_high_rna_content(chain, threshold=0.8):
                    # RNA nucleotides: A, C, G, U, and X (you can modify as needed)
                    rna_nucleotides = ['A', 'C', 'G', 'U', 'X']
                    total_residues = 0
                    rna_residues = 0

                    # Count the total number of residues and RNA-like residues
                    for residue in chain:
                        total_residues += 1
                        if residue.get_resname().strip() in rna_nucleotides:
                            rna_residues += 1

                    # Calculate the proportion of RNA residues
                    if total_residues == 0:
                        return False  # Avoid division by zero if chain has no residues

                    rna_percentage = rna_residues / total_residues

                    # Check if the percentage of RNA residues is greater than or equal to the threshold (80% by default)
                    return rna_percentage >= threshold

                from Bio.PDB.MMCIFParser import MMCIFParser
                from Bio.PDB import MMCIFParser, Structure, Model, Chain
                
                # Initialize the parser
                parser = MMCIFParser()

                # Parse the structure
                structure = parser.get_structure("structure", cif_file)

                # Create a list of single-letter chain identifiers
                import string
                letters = list(string.ascii_uppercase)

                for model in structure:
                    for chain in model:
                        if has_high_rna_content(chain):
                            # New structure
                            new_structure = Structure.Structure("new_structure")
                            new_model = Model.Model(0)  # Create a new model
                            new_structure.add(new_model)  # Add the new model to the new structure

                            chain_id_new = letters.pop(0)
                            chain_id = chain.get_id()

                            atom_count = 0
                            for residue in chain:
                                  for atom in residue:
                                       atom_count += 1

                            remarks = []
                            remarks.append(f'REMARK rna chain {chain.id} -> {chain_id_new}')

                            pdb_file = cif_file.replace('.cif', f'_{chain_id}_n{chain_id_new}_fCIF.pdb')
                            print(f'rna chain {chain.id} -> {chain_id_new} {pdb_file} # of atoms: {atom_count}')

                            chain.id = chain_id_new
                            new_model.add(chain)

                            io = PDBIO()
                            io.set_structure(new_structure)
                            
                            io.save(pdb_file)
                            # open a file add remarks
                            new_file = ''
                            with open(pdb_file, 'r') as f:
                                if not args.no_hr:
                                    new_file += add_header(version) + '\n'
                                if remarks:
                                    new_file += '\n'.join(remarks) + '\n'
                                new_file += f.read()

                            with open(pdb_file, 'w') as f:
                                f.write(new_file)

    if args.pdb2cif:
        try:
            from pymol import cmd
        except ImportError:
            print('This functionality needs PyMOL. Install it or if installed, check your setup')
            sys.exit(1)

        # quick fix - make a list on the spot
        if list != type(args.file):
            args.file = [args.file]
        ##################################
        for f in args.file:
            cmd.load(f)
            fo = f.replace('.pdb', '.cif')
            cmd.save(fo, '(all)')
            cmd.delete('all')
            print(fo, 'saved')
