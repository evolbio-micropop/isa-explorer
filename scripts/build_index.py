import pandas as pd
import glob
import json
from isatools.io.isatab_parser import InvestigationParser
import os
import logging

logging.basicConfig(format='%(asctime)s %(infolevel)s: %(message)s')
LOGGER = logging.getLogger()

class MDMIndexer(object):
    """ """
    """ STUB """

    def build_index(self, directory, verbose=False):
        """ Build the index file by scanning the given directory content for isa-tab files.

        :param directory: The directory to scan.
        :type  directory: os.pathLike

        :param verbose: Legacy log level support, default: False
        :type  verbose: bool
        """

        index = []
        isa_dirs = os.listdir(directory)
        for count, isa_dir in enumerate(isa_dirs):

            # Setup metadata directory.
            isatab_metadata_directory = os.path.normpath(os.path.join(directory, isa_dir))

            # check directory exists.
            if not os.path.isdir(isatab_metadata_directory):
                raise IOError("ISATab metadata directory %s not found. Please provide a correct path." % isatab_metadata_directory)

            investigation_file = glob.glob(os.path.join(isatab_metadata_directory, "i_*.txt"))
            LOGGER.debug("Investigation files %s found.", investigation_file)

            if len(investigation_file) == 0:
                raise IOError("ISATab investigation file %s not found.")

            inv_parser = InvestigationParser()
            files = []

            if len(investigation_file) > 0:

                with open(investigation_file[0], "r") as in_handle:
                    try:
                        isa_tab = inv_parser.parse(in_handle)
                    except UnicodeDecodeError:
                        LOGGER.error("UnicodeDecodeError in file %s - skipped", investigation_file)
                        continue

                    title = ''
                    authors_string = ','
                    affiliation_string = ','

                    if len(isa_tab.studies) > 1:
                        # pull out investigation information
                        title = isa_tab.metadata["Investigation Title"]

                    elif len(isa_tab.studies) == 1:

                        study_record = isa_tab.studies[0]

                        title = study_record.metadata['Study Title']
                        sub_date = study_record.metadata['Study Public Release Date']

                        files.append(study_record.metadata['Study File Name'])

                        keywords = study_record.metadata['Comment[Subject Keywords]']

                        repository = study_record.metadata['Comment[Data Repository]']

                        repository_count = len(repository.split(";"))
                        record_uri = study_record.metadata['Comment[Data Record URI]']

                        authors_list = study_record.contacts

                        authors_string = authors_string.join(
                            a['Study Person First Name'] + ' ' + a['Study Person Last Name'] for a in authors_list)
                        affiliation_string = affiliation_string.join(a['Study Person Affiliation'] for a in authors_list if
                                                                     a['Study Person Affiliation'] not in affiliation_string)


                        assays = ';'.join(a['Study Assay Measurement Type'] for a in study_record.assays)
                        for a in study_record.assays:
                            files.append(a['Study Assay File Name'])
                            assays += ';' + a['Study Assay Measurement Type']

                        technologies = ';'.join(a['Study Assay Technology Type'] for a in study_record.assays)
                        for a in study_record.assays:
                            files.append(a['Study Assay File Name'])
                            technologies += ';' + a['Study Assay Technology Type']

                        designs = ';'.join(a['Study Design Type'] for a in study_record.design_descriptors)

                        values = self.extract_metadata_from_files(
                                                                   isatab_metadata_directory,
                                                                   files,
                                                                   [
                                                                     'organism',
                                                                     'environment type',
                                                                     'geographical location'
                                                                   ],
                                                                 )

                        index_record = {'id':               count,
                                        'title':            title,
                                        'date':             sub_date,
                                        'authors':          authors_string,
                                        'affiliations':     affiliation_string,
                                        'location':         investigation_file[0],
                                        'keywords':         keywords,
                                        'repository':       repository,
                                        'repository_count': repository_count,
                                        'record_uri':       record_uri,
                                        "assays":           assays,
                                        'technologies':     technologies,
                                        'designs':          designs,
                                        'dir':              isa_dir,
                                       }

                        for key in values:
                            index_record[key] = ';'.join(str(a) for a in values[key])

                        index.append(index_record)

        with open('isatab-index.json', 'w') as outfile:
            json.dump(index, outfile)

class Indexer(object):

    def build_index(self, directory, verbose=False):
        """ Build the index file by scanning the given directory content for isa-tab files.

        :param directory: The directory to scan.
        :type  directory: os.pathLike

        :param verbose: Legacy log level support, default: False
        :type  verbose: bool
        """

        index = []
        isa_dirs = os.listdir(directory)
        for count, isa_dir in enumerate(isa_dirs):

            # Setup metadata directory.
            isatab_metadata_directory = os.path.normpath(os.path.join(directory, isa_dir))

            # check directory exists.
            if not os.path.isdir(isatab_metadata_directory):
                raise IOError("ISATab metadata directory %s not found. Please provide a correct path." % isatab_metadata_directory)

            investigation_file = glob.glob(os.path.join(isatab_metadata_directory, "i_*.txt"))
            LOGGER.debug("Investigation files %s found.", investigation_file)

            if len(investigation_file) == 0:
                raise IOError("ISATab investigation file %s not found.")

            inv_parser = InvestigationParser()
            files = []

            if len(investigation_file) > 0:

                with open(investigation_file[0], "r") as in_handle:
                    try:
                        ###############################################
                        import ipdb
                        ipdb.set_trace()
                        ###############################################

                        isa_tab = inv_parser.parse(in_handle)
                    except UnicodeDecodeError:
                        LOGGER.error("UnicodeDecodeError in file %s - skipped", investigation_file)
                        continue

                    title = ''
                    authors_string = ','
                    affiliation_string = ','

                    if len(isa_tab.studies) > 1:
                        # pull out investigation information
                        title = isa_tab.metadata["Investigation Title"]

                    elif len(isa_tab.studies) == 1:

                        LOGGER.debug("Study metadata: %s", str(isa_tab.studies[0].metadata))
                        study_record    = isa_tab.studies[0]
                        title           = study_record.metadata['Study Title']
                        sub_date        = study_record.metadata['Study Public Release Date']
                        files.append(study_record.metadata['Study File Name'])

                        keywords            = study_record.metadata['Comment[Subject Keywords]']
                        repository          = study_record.metadata['Comment[Data Repository]']
                        repository_count    = len(repository.split(";"))
                        record_uri = study_record.metadata['Comment[Data Record URI]']
                        authors_list = study_record.contacts
                        authors_string = authors_string.join(
                            a['Study Person First Name'] + ' ' + a['Study Person Last Name'] for a in authors_list)
                        affiliation_string = affiliation_string.join(a['Study Person Affiliation'] for a in authors_list if
                                                                     a['Study Person Affiliation'] not in affiliation_string)


                        assays = ';'.join(a['Study Assay Measurement Type'] for a in study_record.assays)
                        for a in study_record.assays:
                            files.append(a['Study Assay File Name'])
                            assays += ';' + a['Study Assay Measurement Type']

                        technologies = ';'.join(a['Study Assay Technology Type'] for a in study_record.assays)
                        for a in study_record.assays:
                            files.append(a['Study Assay File Name'])
                            technologies += ';' + a['Study Assay Technology Type']

                        designs = ';'.join(a['Study Design Type'] for a in study_record.design_descriptors)

                        values = self.extract_metadata_from_files(
                                                                   isatab_metadata_directory,
                                                                   files,
                                                                   [
                                                                     'organism',
                                                                     'environment type',
                                                                     'geographical location'
                                                                   ],
                                                                 )

                        index_record = {'id':               count,
                                        'title':            title,
                                        'date':             sub_date,
                                        'authors':          authors_string,
                                        'affiliations':     affiliation_string,
                                        'location':         investigation_file[0],
                                        'keywords':         keywords,
                                        'repository':       repository,
                                        'repository_count': repository_count,
                                        'record_uri':       record_uri,
                                        "assays":           assays,
                                        'technologies':     technologies,
                                        'designs':          designs,
                                        'dir':              isa_dir,
                                       }

                        for key in values:
                            index_record[key] = ';'.join(str(a) for a in values[key])

                        index.append(index_record)

        with open('isatab-index.json', 'w') as outfile:
            json.dump(index, outfile)

    def extract_metadata_from_files(self, directory, files, metadata):
        """
        Provided a file and a list of columns to interrogate, this function extracts the metadata.
        :param directory: The directory to scan.
        :param files: The files to extract metadata from.
        :param metadata: Which metadata to extract.
        :return: The extracted metadata dictionary.
        """

        values = {}
        factors = []
        for f in files:
            file_contents = pd.read_csv(os.path.join(directory, f), delimiter='\t')
            columns_of_interest = []
            for col in file_contents.columns:
                for metadata_col in metadata:
                    if metadata_col in col.lower():
                        columns_of_interest.append(col)

                    if 'factor value' in col.lower():
                        factor_type = col[col.find('[')+1: len(col)-1]
                        factors.append(factor_type)

            data = file_contents[columns_of_interest]

            for column in data:
                if column not in values:
                    values[column] = set()

                values[column] = values[column].union(set(data[column].dropna()))

        values['factors'] = set(factors)
        return values



if __name__ == "__main__":
    """ Entry point for the command line interface. """

    # Parse arguments.
    import argparse
    parser = argparse.ArgumentParser()

    # Directory: mandatory.
    parser.add_argument("directory",
                     help="The directory containing ISATab metadata files.",
                     type=str,
                     metavar="DIR")

    # Verbosity level (optional, -v for info, -vv for debug)
    parser.add_argument("-v",
                     "--verbose",
                     action='count',
                     help="Print verbose log information.",
                     )

    args = parser.parse_args()

    # Set logging level according to arguments.
    if args.verbose == 1:
         LOGGER.setLevel(logging.INFO)
    elif args.verbose == 2:
        LOGGER.setLevel(logging.DEBUG)
    else:
        LOGGER.setLevel(logging.WARNING)

    # Construct the indexer.
    indexer = Indexer()

    # Run the indexer.
    indexer.build_index(args.directory)
