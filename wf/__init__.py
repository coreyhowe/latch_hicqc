"""
Generate HiC QC report
"""


import subprocess
from pathlib import Path
import os

from latch import small_task, medium_task, large_task, large_gpu_task, workflow
from latch.types import LatchFile, LatchDir
from typing import Optional


@small_task
def report_task(bam: LatchFile, output_dir: LatchDir) -> LatchFile:

    out_basename = str(output_dir.remote_path)
    outname = Path(str(os.path.basename(bam.local_path))).stem

    _report_cmd = [
        "python3",
        "hic_qc/hic_qc.py", 
        "-b", 
        bam.local_path, 
        "-n", 
        "-1",
        "-o",
        outname,
    ]
    
    
    subprocess.run(_report_cmd)
    
    return LatchFile(f"{outname}_qc_report.pdf",f"{out_basename}/{outname}_qc_report.pdf" )


@workflow
def hic_qc(bam: LatchFile, output_dir: LatchDir) -> LatchFile:
    """simple QC method for Hi-C libraries

# HiC QC

This script is intended as a simple QC method for Hi-C libraries, 
based on reads in a BAM file aligned to some genome/assembly.
 For our full recommendations on aligning and QCing Hi-C data,
please see [here.](https://phasegenomics.github.io/2019/09/19/hic-alignment-and-qc.html)

The most informative Hi-C reads are the ones that are 
long-distance contacts, or contacts between contigs of an assembly. 
This tool quantifies such contacts and makes plots of contact 
distance distributions. The most successful Hi-C libraries have
 many long-distance and among-contig contacts.

Hi-C connectivity drops off in approximately a power-law with
 increasing linear sequence distance. Consequently, one expects
  Hi-C reads to follow a characteristic distribution, wherein
there is a spike of many read pairs at distances close to 
zero, which drops off smoothly (in log space) with increasing
 distance. If there are odd spikes or discontinuities, or if
  there are few long-distance contacts, there may be a problem
 either with the library or the assembly.

Read more at the Phase Genomics [github](https://github.com/phasegenomics/hic_qc)


__metadata__:
        display_name: simple QC method for Hi-C libraries
        author:
            name: Corey Howe
            email: coreyhowe99 at gmail dot com
            github: https://github.com/coreyhowe/latch_hicqc
        repository: https://github.com/phasegenomics/hic_qc
        license:
            id: AGPL-3.0

Args:

        bam:
          HiC BAM file 

          __metadata__:
            display_name: HiC BAM file 

        output_dir:
          Output directory

          __metadata__:
            display_name: Output directory
    """
    return report_task(bam=bam, output_dir=output_dir)
