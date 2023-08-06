""".. Line to protect from pydocstyle D205, D400.

BED
---

Reading and writing `BED`_ files.

"""

import os
import shutil
import logging
import tempfile

import pybedtools

import iCount

LOGGER = logging.getLogger(__name__)


def _convert_legacy_bed_format(feature):
    """
    TODO.

    Old iCount legacy format:
    chrome, start, end, [+-]score
    where +/- indicate strand of cross-link site and score indicates the
    intensity of interaction
    use BED6 format, see:
    http://bedtools.readthedocs.io/en/latest/content/general-usage.html
    """
    chrom = feature.chrom
    start = feature.start
    end = feature.stop
    name = '.'
    if feature.name[0] == '-' or feature.name[0] == '+':
        score = feature.name[1:]
        strand = feature.name[0]
    else:
        score = feature.name
        strand = '+'
    return pybedtools.create_interval_from_list(
        [chrom, start, end, name, score, strand],
    )


def convert_legacy(bedgraph_legacy, bed_converted):
    """
    Convert legacy iCount's four-column format into proper BED6 format.

    Old iCount legacy format: chrome, start, end, [+-]value
    Strand can be either '+' or '-', and value indicates the intensity of
    interaction.

    The returned BED file follows the BED6 format, as explained in the
    [bedtools manual](http://bedtools.readthedocs.io/en/latest/content
    /general-usage.html).

    """
    sites = pybedtools.BedTool(bedgraph_legacy).sort().saveas()
    sites1 = sites.each(_convert_legacy_bed_format).saveas(bed_converted)
    return sites1


def merge_bed(sites_grouped, sites):
    """
    Merge multiple files with crosslinks into one.

    Concatenate files into one file. Also, merge crosslinks from different files
    that are on same position and sum their scores.

    Parameters
    ----------
    sites_grouped : str
        Path to output BED6 file containing merged data from input sites files.
    sites : list_str
        List of BED6 files(paths) to be merged.

    Returns
    -------
    str
        Absolute path to outfile.

    """
    iCount.log_inputs(LOGGER, level=logging.INFO)

    if not sites:
        raise ValueError(
            "At least one element expected in files list, but none found.")

    LOGGER.info('Reading input files...')
    joined = tempfile.NamedTemporaryFile(mode='at', delete=False)
    for file_path in sites:
        if not os.path.isfile(file_path):
            raise ValueError("File {} not found.".format(file_path))
        with iCount.files.gz_open(file_path, 'rt') as infile:
            shutil.copyfileobj(infile, joined)
    joined.close()

    # Marge intervals in "joined" file (needs to be sorted before!):
    # s=True - only merge features that are on the same strand
    # d=-1 - join only intervals with at least one base-pair overlap - default
    # (0) merges also touching intervals
    # c=5, o='sum' - when merging intervals, make operation 'sum' on column 5 (score)
    LOGGER.info('Merging files...')
    merged = pybedtools.BedTool(joined.name).sort().merge(
        s=True, d=-1, c=5, o='sum').sort().saveas()

    # Columns are now shuffled to: chrom-start-stop-strand-score
    # Reorder to: chrom-start-stop-empty_name-score-strand
    # which corresponds to BED6

    LOGGER.info('Saving results...')
    result = pybedtools.BedTool(pybedtools.create_interval_from_list(
        i[:3] + ['.', i[4], i[3]]) for i in merged).saveas()
    result.saveas(sites_grouped)

    LOGGER.info('Done. Results saved to: %s', os.path.abspath(result.fn))
    return os.path.abspath(result.fn)
