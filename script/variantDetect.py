#!/usr/bin/python
import os
import os.path
import subprocess
import fileinput
import argparse
import sys
import time
import gzip
import shutil


#Load modules
#module load smrtlink/11.0
#module load singularity


#Check the input files 
def input_file (path):
	if os.path.isfile(path):
		return
	else:
		print("Doesn't exist. Please check the file location")
		sys.exit()


def merge_bams():
	#Current_path
	current_path = os.path.abspath(os.getcwd())
	print(current_path)
	time.sleep(2)
	
	#Argument
	xmls = ""
	xmls = input("Enter the paths of the dataset xmls with a space separated each: ")
	name = ""
	name = input("Specify explicit name for the new dataset merged: ")
	
	#Command line
	merge = "dataset --log-level DEBUG --skipCounts" + " merge --remove-parentage --unique-collections --no-sub-datasets --name " + name + " merged.consensusreadset.xml " + xmls + " && " + "dataset newuuid --random merged.consensusreadset.xml"
	os.system(merge)
	
	#Output
	subprocess.call("ls merged.consensusreadset.xml", shell = True)
	time.sleep(2)


def align():
	#Current_path
	current_path = os.path.abspath(os.getcwd())
	print(current_path)
	print("***Aligning reads...***")
	time.sleep(2)
	
	#Argument
	global ref
	ref = ""
	ref = input("Enter the paths of the genome reference (.fa/fasta): ")
	bam = ""
	bam = input("Enter the paths of the raw bam (.bam/.xml): ")
	global name
	name = ""
	name = input("Specify the sample name: ")
	global aligned_bam
	aligned_bam = name + ".aligned.bam"
	
	#Command line
	align = "pbmm2 align " + ref + " " + bam + " " + aligned_bam + " --sort --preset CCS --sample " + name
	os.system(align)
	
	#Output
	subprocess.call("ls *.bam", shell = True)
	time.sleep(2)
	

def pbsv():
	#Current_path
	current_path = os.path.abspath(os.getcwd())
	print(current_path)
	print("***Analyzing structural variants...***")
	time.sleep(2)
	
	#Argument
	global out
	out = name + ".svsig.gz"
	global sv_vcf_name 
	sv_vcf_name = name + ".sv.vcf"
	
	while True:
		answer = input("Do you have and want to provide one tandem repeat annotation .bed file of your reference? (yes/no): ")
		if answer.lower().startswith("y"):
			tandem = ""
			tandem = input("Enter" + " " + """ '--tandem-repeats YOUR.annotation.bed' """ + " " + "(.bed): ")
			#Command line (discover)
			pbsv_discover = "pbsv discover " + tandem + " " + aligned_bam + " " + out
			os.system(pbsv_discover)
			#Output
			subprocess.call("ls *.svsig.gz", shell = True)
			time.sleep(2)
			break
		elif answer.lower().startswith("n"):
			print("***Run pbsv discover without the tandem repeats annotations...***")
			time.sleep(2)
			#Command line (discover)
			pbsv_discover = "pbsv discover " + aligned_bam + " " + out
			os.system(pbsv_discover)
			#Output
			subprocess.call("ls *.svsig.gz", shell = True)
			time.sleep(2)
			break
	
	#Command line (call)
	pbsv_call = "pbsv call " + ref + " " + out + " " + sv_vcf_name
	os.system(pbsv_call)
	
	#Output
	subprocess.call("ls *.sv.vcf", shell = True)
	time.sleep(2)
	
	
def count_sv_variant_types():
	#Current_path
	current_path = os.path.abspath(os.getcwd())
	print(current_path)
	print("***Counting each type of structural variants...***")
	time.sleep(2)
	
	#Command line
	#This code is created by Kamil S Jaron (https://bioinformatics.stackexchange.com/questions/264/is-there-an-easy-way-to-create-a-summary-of-a-vcf-file-v4-1-with-structural-va)
	count_sv = "cat" + " " + sv_vcf_name + " " + "| perl -ne" + " " + """ 'print "$1\n" if /[;\t]SVTYPE=([^;\t]+)/' """ + " " + "| sort | uniq -c > count_sv_variant_type.txt"
	os.system(count_sv)
	
	#Output
	subprocess.call("ls *.txt", shell = True)
	time.sleep(2)
	

def deepvariant():
	#Current_path
	current_path = os.path.abspath(os.getcwd())
	print(current_path)
	print("***Analyzing single nucleotide variants...***")
	time.sleep(2)
	
	#Argument
	model_type = ""
	model_type = input("Enter the type of the sequencing platforms (WGS,WES,PACBIO or HYBRID_PACBIO_ILLUMINA): ")
	out_vcf = name + ".snv.vcf"
	out_gvcf = name + ".snv.g.vcf"
		
	#Command line
	deepvariant_snv = "/opt/singularity/3.7.0/bin/singularity run " + "/opt/singularity-images/deepvariant-1.3.0.simg " + "run_deepvariant " + "--model_type=" + model_type + " " +  "--ref=" + ref + " --reads=" + aligned_bam + " " + "--output_vcf=" + out_vcf + " " + "--output_gvcf=" + out_gvcf + " " + "--num_shards=16" + " " + "--logging_dir=./log" + " " + "--runtime_report" + " " + "--use_hp_information=true"
	os.system(deepvariant_snv)
	
	#Output
	subprocess.call("ls *.vcf", shell = True)
	time.sleep(2)


def deepvariant_2():
	#Current_path
	current_path = os.path.abspath(os.getcwd())
	print(current_path)
	print("***Analyzing single nucleotide variants...***")
	time.sleep(2)
	
	#Argument
	model_type = ""
	model_type = input("Enter the type of the sequencing platforms (WGS,WES,PACBIO or HYBRID_PACBIO_ILLUMINA): ")
	ref = ""
	ref = input("Enter the paths of the genome reference (.fa/fasta): ")
	aligned_bam = ""
	aligned_bam = input("Enter the paths of the aligned bam (.bam): ")
	out_vcf = aligned_bam + ".snv.vcf"
	out_gvcf = aligned_bam + ".snv.g.vcf"
		
	#Command line
	deepvariant_snv = "/opt/singularity/3.7.0/bin/singularity run " + "/opt/singularity-images/deepvariant-1.3.0.simg " + "run_deepvariant " + "--model_type=" + model_type + " " +  "--ref=" + ref + " --reads=" + aligned_bam + " " + "--output_vcf=" + out_vcf + " " + "--output_gvcf=" + out_gvcf + " " + "--num_shards=16" + " " + "--logging_dir=./log" + " " + "--runtime_report" + " " + "--use_hp_information=true"
	os.system(deepvariant_snv)
	
	#Output
	subprocess.call("ls *.vcf", shell = True)
	time.sleep(2)
	

#Confirm the setting of requiring modules
while True:
	answer = input("Have you loaded the required modules before running the pipeline? (yes/no): ")
	if answer.lower().startswith("y"):
		print("***Start the pipeline...***")
		time.sleep(2)
		break
	elif answer.lower().startswith("n"):
		print("***Please load 'smrtlink/11.0' and 'singularity' using 'module load' in Apollo...***")
		time.sleep(2)
		sys.exit()
		
		
#Choose the type of the variants between SNV and SV
while True:
	answer = input("Which type of the variants do you want to analyze? (SNV or SV): ")
	if answer.lower().startswith("snv"):
		print("***Start the SNV pipeline...***")
		time.sleep(2)
		break
	elif answer.lower().startswith("sv"):
		print("***Start SV the pipeline...***")
		time.sleep(2)
		#Whether merging SMRT Cells is necessary
		while True:
			answer = input("Do you have multiple raw-squencing datasets to merge? (yes/no): ")
			if answer.lower().startswith("y"):
				print("***Start the SV pipeline...***")
				time.sleep(2)
				merge_bams()
				align()
				pbsv()
				count_sv_variant_types()
				#Whether SNV analysis is necessary
				while True:
					answer = input("Do you want to analyze small variants as well? (yes/no): ")
					if answer.lower().startswith("y"):
						print("***Start the SNV pipeline...***")
						time.sleep(2)
						deepvariant()
						print("***Completing the process...***")
						time.sleep(2)
						sys.exit()
					elif answer.lower().startswith("n"):
						print("***Completing the process...***")
						time.sleep(2)
						sys.exit()
			elif answer.lower().startswith("n"):
				print("***Start the SV pipeline...***")
				time.sleep(2)
				align()
				pbsv()
				count_sv_variant_types()
				while True:
					answer = input("Do you want to analyze small variants as well? (yes/no): ")
					if answer.lower().startswith("y"):
						print("***Start the SNV pipeline...***")
						time.sleep(2)
						deepvariant()
						print("***Completing the process...***")
						time.sleep(2)
						sys.exit()
					elif answer.lower().startswith("n"):
						print("***Completing the process...***")
						time.sleep(2)
						sys.exit()
		
	
#Whether merging SMRT Cells is necessary
while True:
	answer = input("Is this analysis for the PacBio sequencing reads? (yes/no): ")
	if answer.lower().startswith("y"):
		print("***Start the SNV pipeline...***")
		time.sleep(2)
		while True:
			answer = input("Do you have multiple raw-squencing datasets to merge? (yes/no): ")
			if answer.lower().startswith("y"):
				merge_bams()
				align()
				deepvariant()
				#Whether SV analysis is necessary
				while True:
					answer = input("Do you want to analyze structual variants as well? (yes/no): ")
					if answer.lower().startswith("y"):
						print("***Start the SV pipeline...***")
						time.sleep(2)
						pbsv()
						count_sv_variant_types()
						print("***Completing the process...***")
						time.sleep(2)
						sys.exit()
					elif answer.lower().startswith("n"):
						print("***Completing the process...***")
						time.sleep(2)
						sys.exit()
			elif answer.lower().startswith("n"):
				print("***Start the SNV pipeline...***")
				time.sleep(2)
				align()
				deepvariant()
				while True:
					answer = input("Do you want to analyze structual variants as well? (yes/no): ")
					if answer.lower().startswith("y"):
						print("***Start the SV pipeline...***")
						time.sleep(2)
						pbsv()
						count_sv_variant_types()
						print("***Completing the process...***")
						time.sleep(2)
						sys.exit()
					elif answer.lower().startswith("n"):
						print("***Completing the process...***")
						time.sleep(2)
						sys.exit()	
	elif answer.lower().startswith("n"):
		print("***Start the SNV pipeline...***")
		time.sleep(2)
		deepvariant_2()
		print("***Completing the process...***")
		time.sleep(2)
		sys.exit()
