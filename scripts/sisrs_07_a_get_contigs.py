import os
import sys
import itertools


path_to_contigs_LocList_file = "/Users/yanahrytsenko/Documents/GitHub/SISRS/SISRS_Run_yana/Composite_Genome" #sys.argv[1] #/data3/schwartzlab/yana/SISRS_reRun/SISRS_Walkthrough_test_BOBs_scripts/SISRS_Run/Composite_Genome/
path_to_taxon_dirs = "/Users/yanahrytsenko/Documents/GitHub/SISRS/SISRS_Run_yana" #sys.argv[2] #/data3/schwartzlab/yana/SISRS_reRun/SISRS_Walkthrough_test_BOBs_scripts/SISRS_Run

#get list of taxon dirs except Composite_Genome
taxon_list = []
taxon_list = os.listdir(path_to_taxon_dirs)


taxon_list.remove('Composite_Genome') #remove this directory from the list for easy traversal

#process each taxon's contigs
for dir in taxon_list:

    taxon_LocList_file = path_to_taxon_dirs + '/' + dir + '/' + dir + '_LocList'
    taxon_contigs_file = path_to_taxon_dirs + '/' + dir + '/' + dir + '_contigs'
    contigs_LocList_file = path_to_contigs_LocList_file + '/' + 'contigs_LocList'

    contigs_dict = {} #store contigs in a dictionary
    with open(contigs_LocList_file, 'r') as in_file:
        for line in in_file:
            split1_line = line.strip().split('-')
            split2_line = split1_line[1].split('/')

            key = split2_line[0]
            val = split2_line[1]
            contigs_dict[key] = val

    in_file.close()

    with open (taxon_LocList_file, 'r') as in_file2, open(taxon_contigs_file, 'a+') as out_file:

        #out_file.write(">" + dir + '\n') #>AotNan
        mylist = in_file2.read().splitlines()

        i = 0

        for key in sorted(contigs_dict.keys()):

            out_file.write(">" + key + '\n')

            contig_string = ""

            lines = mylist[i : i + int(contigs_dict[key])] #get a slice of the file

            contig_string = contig_string.join(lines)

            out_file.write(contig_string + '\n')

            i += int(contigs_dict[key])

    in_file2.close()
    out_file.close()