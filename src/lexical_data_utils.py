from nltk.corpus import framenet as fn
from .path_utils import get_relevant_info

from .LexicalDataD2TAnnotationTool import dir_path, create_lexicon_data_annotation_tool
from .LexicalDataD2TAnnotationTool import add_frame_to_info, add_lu_to_info
from .LexicalDataD2TAnnotationTool import premon
from .LexicalDataD2TAnnotationTool import add_lemma_to_pos_to_lu_urls
from .LexicalDataD2TAnnotationTool import initialize_typical_frames, create_lexical_lookup_per_eventtype

from .FrameNetNLTK import load


def add_lexical_data(repo_dir,
                     dfn_major_version,
                     dfn_minor_version,
                     project,
                     verbose=0):
    """
    create the lexical data needed for the frame annotation tool

    :param str repo_dir: use DFNDataReleases.dir_path
    :param int dfn_major_version: major version, e.g. 0
    :param int dfn_minor_version: minor version, e.g., 1
    :param str project: the project, e.g, HistoricalDistanceData
    :param int verbose: debugging level
    """
    relevant_info = get_relevant_info(repo_dir=repo_dir,
                                      project=project,
                                      verbose=verbose)

    # create lexical data folder
    create_lexicon_data_annotation_tool(path_readme=f'{dir_path}/doc/lexicon_data_for_frame_annotation_tool/README.md',
                                        path_ud_information=f'{dir_path}/doc/lexicon_data_for_frame_annotation_tool/part_of_speech_ud_info.json',
                                        path_mapping_ud_pos_to_fn_pos=f'{dir_path}/doc/lexicon_data_for_frame_annotation_tool/ud_pos_to_fn_pos.json',
                                        output_folder=relevant_info['lexical_data'],
                                        verbose=verbose)

    # add lexicon data
    add_frame_to_info(output_folder=relevant_info['lexical_data'],
                      fn_en=fn,
                      premon=premon,
                      verbose=verbose)

    add_lu_to_info(your_fn=fn,
                   language='en',
                   premon=premon,
                   namespace='http://rdf.cltl.nl/efn/',
                   major_version=1,
                   minor_version=7,
                  output_folder=relevant_info['lexical_data'],
                   verbose=verbose)

    add_lemma_to_pos_to_lu_urls(output_folder=relevant_info['lexical_data'],
                                language='en',
                                verbose=verbose)

    fn_nl = load(relevant_info['dfn'][float(f'{dfn_major_version}.{dfn_minor_version}')])

    add_lu_to_info(your_fn=fn_nl,
                   language='nl',
                   premon=premon,
                   namespace='http://rdf.cltl.nl/dfn/',
                   major_version=dfn_major_version,
                   minor_version=dfn_minor_version,
                   output_folder=relevant_info['lexical_data'],
                   verbose=verbose)

    add_lemma_to_pos_to_lu_urls(output_folder=relevant_info['lexical_data'],
                                language='nl',
                                verbose=verbose)


    # add typicality scores and lexical lookup per event type
    for event_type, incs in relevant_info['type2inc'].items():
        initialize_typical_frames(output_folder=relevant_info['lexical_data'],
                                  fn_en=fn,
                                  premon=premon,
                                  event_type=event_type,
                                  overwrite=True,
                                  verbose=verbose)

        create_lexical_lookup_per_eventtype(event_type=event_type,
                                            language='nl',
                                            premon=premon,
                                            output_folder=relevant_info['lexical_data'],
                                            overwrite=True,
                                            verbose=verbose)

        create_lexical_lookup_per_eventtype(event_type=event_type,
                                            language='en',
                                            premon=premon,
                                            output_folder=relevant_info['lexical_data'],
                                            overwrite=True,
                                            verbose=verbose)


