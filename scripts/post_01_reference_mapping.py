import os
from os import path
import sys
from glob import glob
import subprocess
import stat
from itertools import islice

script_dir = sys.path[0]
ref_species = sys.argv[1]
processors = str(int(sys.argv[2]))

#Set directories based off of script folder location
post_processing_dir = path.dirname(path.abspath(script_dir))+"/Post_SISRS_Processing"

if(not path.isdir(post_processing_dir+"/logFiles")):
    os.mkdir(post_processing_dir+"/logFiles")
post_log_dir = post_processing_dir+"/logFiles"

sisrs_dir = path.dirname(path.abspath(script_dir))+"/SISRS_Run"
ref_sisrs_dir = sisrs_dir + "/" + ref_species

ref_genome_dir = path.dirname(path.abspath(script_dir))+"/Reference_Genome"
ref_genome_file = [x for x in glob(ref_genome_dir+"/*") if os.path.isfile(x)][0]
ref_genome_name = os.path.basename([x for x in glob(ref_genome_dir+"/*") if os.path.isfile(x)][0].split(".")[0])
ref_genome_ext = [x for x in glob(ref_genome_dir+"/*") if os.path.isfile(x)][0].split(".")[1]

print("Building Bowtie2 Index for Reference Genome...\n")

bowtie_command = [
    'bowtie2-build',
    '{}'.format(ref_genome_dir+'/'+ref_genome_name+"."+ref_genome_ext),
    '{}'.format(ref_genome_dir+'/'+ref_genome_name),
    '-p',
    '{}'.format(processors)]
#os.system(" ".join(bowtie_command))
print(" ".join(bowtie_command))

reference_mapping_command = """
#!/bin/sh
bowtie2 -p PROCESSORS -x REF_GENOME_DIR/REF_GENOME_NAME -f -U REF_SISRS_DIR/contigs.fa | samtools view -Su -@ PROCESSORS -F 4 - | samtools sort -@ PROCESSORS - -o POST_PROCESSING_DIR/REF_TAXA_Temp.bam

samtools view -@ PROCESSORS -H POST_PROCESSING_DIR/REF_TAXA_Temp.bam > POST_PROCESSING_DIR/REF_TAXA_Header.sam

samtools view -@ PROCESSORS POST_PROCESSING_DIR/REF_TAXA_Temp.bam | grep -v "XS:" | cat POST_PROCESSING_DIR/REF_TAXA_Header.sam - | samtools view -@ PROCESSORS -b - > POST_PROCESSING_DIR/REF_TAXA.bam

rm POST_PROCESSING_DIR/*Temp.bam
rm POST_PROCESSING_DIR/*Header.sam

samtools view POST_PROCESSING_DIR/REF_TAXA.bam | awk 'BEGIN {OFS = "\t"} { print $1, $3, $4, $2, $6}' > POST_PROCESSING_DIR/REF_TAXA_MapData.tsv
"""

keyList = ['PROCESSORS','REF_GENOME_DIR','REF_GENOME_NAME','REF_SISRS_DIR','REF_TAXA','POST_PROCESSING_DIR']

keyDict = {'PROCESSORS':processors,
           'REF_GENOME_DIR':ref_genome_dir,
           'REF_GENOME_NAME':ref_genome_name,
           'REF_SISRS_DIR':ref_sisrs_dir,
           'REF_TAXA':ref_species,
           'POST_PROCESSING_DIR':post_processing_dir}

for key in keyList:
    reference_mapping_command = reference_mapping_command.replace(key,keyDict[key])

with open(post_log_dir+"/01_Reference_Mapping.sh", "w") as text_file:
    print(reference_mapping_command, file=text_file)

with open(post_log_dir+"/err_01_Reference_Mapping","w") as errfile:
    cmd = post_log_dir+"/01_Reference_Mapping.sh"
    subprocess.call(['sh',cmd],stderr=errfile)
