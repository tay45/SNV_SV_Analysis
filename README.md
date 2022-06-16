Single Nucleotide Variant (SNV) and Structural Variant (SV) Analysis Pipeline

The primary function of this pipeline is to analyze SNVs and SVs using the PacBio sequencing reads. This pipeline is basically consisted of the deepvariant (https://github.com/google/deepvariant) for SNVs and the pbsv (https://github.com/PacificBiosciences/pbsv) for SVs. Here, the dataset (merge) and the pbmm2 in the command-line tools of the SMRT Link v11.0 (https://www.pacb.com/support/software-downloads/) have added for building a whole process of the variant detections from preparing proper inputs. Using the interactive input functions on this pipeline, users either can choose one of the analysis types between SNV and SV or can carry out both, sequentially. Technically, the deepvariant in the SNV analysis can accept any types of sequencing outputs regardless sequencing platforms. Hence, users, who have any sequencing reads from different platforms, can solely select the deepvariant, as well.

It is designed for executing in the Apollo server (apollo-acc.coh.org) of the City of Hope (Duarte, CA) using the interactive job mode (http://apollo.coh.org/user-guide/interactivejobs/). Before executing the analysis, the below modules must be loaded in advance to the server.

    module load smrtlink/11.0
    module load singularity

To execute the pipeline, you need to download the python scripts of the pipeline (git clone https://github.com/tay45/SNV_SV_Analysis.git), first. And, copy the scripts to the folder to run the analysis (../running_folder/variantDetect.py). The folder should contain raw read (ccs.bam) and index (ccs.bam.pbi) files.

And, execute the below command line in the shell.

    python3 variantDetect.py

The input must be HiFi reads (ccs.bam; QV>20). If the raw data is the continuous long reads (CLRs) in movieX.subreads.bam, please produce the ccs.bam via the below command line to generate the correct input.

    ccs movieX.subreads.bam movieX.ccs.bam --min-rq 0.9
    
If the user wanted to use the SV analysis using the sequencing reads being not from the PacBio platform, an aligned bam on a reference sequence is required as the input.  

During the running of the pipeline, it asks your intention of the analysis (e.g., whether or not you want to provide a tandem repeat bed file of the reference in the SV analysis) to decide the direction the next step or ask you to enter a necessary file (e.g., a genome reference) to proceed the next analysis.

The 'supporting_files' folder (/net/isi-dcnl/ifs/user_data/Seq/PacBio/thkang/Pipelines/SV_SNV/supporting_files) contains a human reference genome and its tandem repeat bed files requiring for the pbsv execution as optional.

    Genome reference: GRCh38.p12.genome.fa
    Tandem_repeats_bed: human_GRCh38_no_alt_analysis_set.trf.bed

Regarding the outputs;

    merged.consensusreadset.xml: Merged output from different SMRT Cells.
    *.aligned.bam: Aligned bam from pbmm2
    *.snv.vcf: The out of deepvariant.
    *.snv.g.vcf: The out of deepvariant (Genomic Variant Call Format).
    log folder: logs of deepvariant.    
    *.svsig.gz: The output of pbsv (discover).
    *.sv.vcf: The output of pbsv (call).
    count_sv_variant_type.txt: Counting each type of SVs.

For executing this pipeline in other platforms, please satisfy the prerequisite through installing below tools.

    SMRT Link v11.0 (https://www.pacb.com/support/software-downloads/)
    deepvariant (https://github.com/google/deepvariant)
