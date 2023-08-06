from glob import glob
from os.path import join as pjoin
import os.path as osp

from luigi import Parameter
from sciluigi import WorkflowTask
from bioluigi.files import FastqFile, ReadsFile
from bioluigi.hts import Bowtie2, SortBam, BamUnalignedToFastq
from bioluigi.kmers import (
    MashDist, MashSketch, KallistoIndexFromMashDist, KallistoQuantWithIndex,
    KallistoPseudoalign)


class SingleSpeciesShotgunLibrary(WorkflowTask):
    input_glob = Parameter()
    output_dir = Parameter()
    species_bowtie2_index_path = Parameter()
    species_gff_path = Parameter()
    vector_kallisto_index_path = Parameter()
    insert_length = IntParameter()
    insert_stddev = IntParameter()
    # contaminant_kallisto_idx = Parameter()

    def workflow(self):
        input_files = glob(self.input_glob)
        if len(input_files) == 0:
            raise ValueError("No input files match {}".format(input_target.path))

        t7_depletion_dir = pjoin(self.output_dir, 't7_depletion')
        alignment_dir = pjoin(self.output_dir, 'aln')

        tasks = []
        for input_file in input_files:
            fastq_file = self.new_task(
                'fastq_{}'.format(input_file), FastqFile, path=input_file)

            # deplete T7 reads
            align_T7 = self.new_task(
                'align_T7_{}'.format(input_file), KallistoPseudoalign,
                output_dir=t7_depletion_dir,
                index_path=self.vector_kallisto_index_path,
                fragment_length=self.insert_length,
                fragment_stddev=self.insert_stddev)
            align_T7.in_fastq = fastq_file.out_fastq

            # create new fastq sans T7 reads
            drop_T7 = self.new_task(
                'drop_T7_{}'.format(input_file), BamUnalignedToFastq,
                output_dir=t7_depletion_dir)
            drop_T7.in_bam = align_T7.out_bam

            # align new fastq to target species
            align_species = self.new_task(
                'align_species_{}'.format(input_file), Bowtie2,
                index=self.species_bowtie2_index_path,
                output_dir=alignment_dir)
            align_species.in_fastq = drop_T7.out_fastq

            # sort resulting bam file
            sort_alns = self.new_task(
                'sort_alns_{}'.format(input_file), SortBam,
                output_dir=alignment_dir)
            sort_alns.in_bam = align_species.out_bam

            join

            tasks.append(sort)
        return tasks


class MetagenomicShotgunLibrary(WorkflowTask):
    input_glob = Parameter()
    output_dir = Parameter()
    mash_sketch_path = Parameter()

    def workflow(self):
        input_files = glob(self.input_glob)
        if len(input_files) == 0:
            raise ValueError("No input files found in {}".format(input_target.path))

        sketch_dir = pjoin(self.output_dir, 'sketches')
        dist_dir = pjoin(self.output_dir, 'dists')
        abund_dir = pjoin(self.output_dir, 'abundances')

        tasks = []
        for i, input_file in enumerate(input_files):
            reads_file = self.new_task(
                'reads_{}'.format(i), ReadsFile, path=input_file)

            sketch_reads = self.new_task(
                'sketch_reads_{}'.format(i), MashSketch, sketch_size=50000,
                min_kmer_copies=2, output_dir=sketch_dir)
            sketch_reads.in_reads = reads_file.out_reads

            mash_dist = self.new_task(
                'mash_dist_{}'.format(i), MashDist,
                reference=self.mash_sketch_path, output_dir=dist_dir)
            mash_dist.in_msh = sketch_reads.out_msh

            kallisto_idx = self.new_task(
                'kallisto_idx_{}'.format(i), KallistoIndexFromMashDist,
                output_dir=idx_dir)
            kallisto_idx.in_dist = mash_dist.out_dist

            abundances = self.new_task(
                'abundance_{}'.format(i), KallistoQuantWithIndex,
                fragment_length=500, fragment_stddev=50, output_dir=abund_dir)
            abundances.in_fastq = reads_file.out_reads
            abundances.in_index = kallisto_idx.out_idx

            tasks.append(abundances)
        return tasks
