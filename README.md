# DFN Data Releases

This repository builds upon the output of obtaining event type using either:
* https://github.com/cltl/multilingual-wiki-event-pipeline
* or https://github.com/cltl/MWEP_on_one_incident

The event data has two key components:
* instance of IncidentCollection (as defined in https://github.com/cltl/multilingual-wiki-event-pipeline/blob/master/classes.py)
* a folder containing [NAF](https://github.com/newsreader/NAF) files

For example, a folder could have the following structure:

* OUTPUT_FOLDER
    * bin
        EVENT_ID.bin (this is the instance of IncidentCollection)
    * wiki_output (this is the NAF folder)
        * LANGUAGE
            *naf

### Prerequisites

Python 3.6 was used to create this project. It might work with other versions of Python.

### Installing

### Resources
A number of GitHub repositories need to be cloned. This can be done calling:
```bash
bash install.sh
```

### Python modules
A number of external modules need to be installed, which are listed in **requirements.txt**.
Depending on how you installed Python, you can probably install the requirements using one of following commands:
```bash
pip install -r requirements.txt
```
## How to create a data release

### Step 1: obtain event type
This repository builds upon the output of obtaining event type using either:
* https://github.com/cltl/multilingual-wiki-event-pipeline
* or https://github.com/cltl/MWEP_on_one_incident

### Step 2: incorporate the event data into this repository

Load the Python package from the parent directory of this folder.

```python
from DFNDataReleases import integrate_data
import DFNDataReleases

package_dir = DFNDataReleases.dir_path


integrate_data(json_dir=f'{package_dir}/structured',
               source_naf_dir=f'{package_dir}/test/example_mwep_output/Q17374096/wiki_output',
               target_naf_dir=f'{package_dir}/unstructured',
               path_inc_coll_obj=f'{package_dir}/test/example_mwep_output/Q17374096/bin/Q17374096.bin',
               mwep_repo_dir=DFNDataReleases.mwep_repo_dir,
               project='Test',
               overwrite=False,
               start_from_scratch=True,
               verbose=2)
```
The function has the following parameters:
* **json_dir**: this is where the structured data is written (should be 'structured'):
    * inc2doc_index.json: contains a mapping from an Incident ID (e.g., Q51336711) to the ReferenceTexts that refer to it (as found in the folder **unstructured**).
    * inc2str_index.json: contains a mapping from an Incident ID to the structured data of the incident as represented using [SEM](https://semanticweb.cs.vu.nl/2009/11/sem/).
    * proj2inc_index.json: contains a mapping from a project, e.g., v1, to the Incidents that belong to it.
    * type2inc_index.json: contains a mapping from an event type to the Incidents that belong to it.
* **source_naf_dir**: the folder containing per language the NAF files
* **target_naf_dir**: the folder containing all the NAF files of one data release (should be 'unstructured')
* **path_inc_coll_obj**: path to pickled IncidentCollection object (see explanation above).
* **mwep_repo_dir**: is always DFNDataReleases.mwep_repo_dir
* **project**: the name of the project to which all incidents that are being added below, e.g, "v1" or "test" or "v2".
* **overwrite**: if True, if you try to add an incident that was already present:
    *  we overwrite any information in the structured and unstructured data
* **start_from_scratch**: if True, remove all existing structured and unstructured data
* **verbose**: 1: descriptive stats 2: more stats 3: lots of stats

After running the example, you observe two folders in this directory:
* **unstructured**
* **structured**

### Step 2: create a folder in release_notes
Create a subfolder in the folder **release_notes**, e.g, **release_notes/test**

### Step 3: Licenses
Your structured and unstructured data may rely on different licenses.
Please add the LICENSE files to the same directory as this README.
Please describe the license of the data in **release_notes/YOUR_RELEASE/release_notes.md
 
### Step 4: TODO: SEM

### Step 5: TODO: Descriptive statistics

### Step 6: TODO: commit, push, and create a GitHub release

#### Scenario 1: create new data release
* step 1: use **git rm** to remove files that are no longer part of the new data release
    * please note that the files are still part of older commits, which is exactly what we want!
* step 2: use the **integreate_data** to recreate or update the **structured** and **unstructured** folder
* step 3: use **git add** to add the new files to the commit. Commit the files in **structured** and **unstructured**
* step 4: please create a GitHub release of this commit on GitHub. This facilitates going back to it.
* TODO: SEM
* TODO: descriptive statistics 

### Scenario 2: you have annotated the data
* step 1: use **git add** to add the annotated files to the commit and push 
* step 2: please create a GitHub release of this commit on GitHub. This facilitates going back to it.
* TODO: SEM
* TODO: descriptive statistics
 
### Step 7: TODO: Annotation tool

## Authors
* **Marten Postma** (m.c.postma@vu.nl)

## License
This project is licensed under the Apache 2.0 License - see the [LICENSE.md](LICENSE.md) file for details
