# FrameNet input to annotation tool

This directory contains the following content:
* part_of_speech
    * **part_of_speech_ud_info.json**
    * **ud_pos_to_fn_pos.json**
* lexicons
    * **frame_to_info.json**
    **LANGUAGE**
        * **lu_to_info.json**
        * **lemma_to_pos_to_lus.json**
* typicality
    * **lexical_lookup**
        **LANGUAGE**
            * **EVENT_TYPE.json**
    * **typicality_scores**:
        * **EVENT_TYPE.json**

## **part_of_speech_ud_info.json**
Contains a mapping from an UD part of speech tag to a URL and an explanation label.

## **ud_pos_to_fn_pos.json**
Contains a mapping from a UD part of speech tag to a FrameNet part of speech tag.

## **frame_to_info.json**

A frame [PreMOn](https://premon.fbk.eu/) URI is mapped to its definition, and Frame Element information, e.g.,
```json
 "http://premon.fbk.eu/resource/fn17-access_scenario": {
        "definition": "A Theme is or is not capable of entering or accessing a Useful_location because of/despite a Barrier.",
        "frame_elements": [
            {
                "definition": "The Theme whose motion is blocked or free.  ",
                "fe_label": "Theme",
                "fe_type": "Core",
                "rdf_uri": "http://premon.fbk.eu/resource/fn17-access_scenario@theme"
            },
            {
                "definition": "The place or thing that the Theme is headed towards, despite a potential or actual Barrier.",
                "fe_label": "Useful_location",
                "fe_type": "Core",
                "rdf_uri": "http://premon.fbk.eu/resource/fn17-access_scenario@useful_location"
            },
            {
                "definition": "An entity that (at least potentially) prevents the Theme from getting to the Useful_location. ",
                "fe_label": "Barrier",
                "fe_type": "Core",
                "rdf_uri": "http://premon.fbk.eu/resource/fn17-access_scenario@barrier"
            }
        ],
        "frame_label": "Access_scenario",
        "framenet_url": "https://framenet2.icsi.berkeley.edu/fnReports/data/frame/Access_scenario.xml"
    },
```

## **language_specific_info**

### **lu_to_info.json**
for each lexical unit, it's URL is mapped to its properties:

```json
"http://rdf.cltl.nl/fn_nl-0.1-1600871382355": {
        "frame_label": "Abundance",
        "frame_uri": "http://premon.fbk.eu/resource/fn17-abundance",
        "lexical_entries": [
            [
                "overvloedig",
                "A"
            ]
        ],
        "lu_definition": "in overvloed",
        "lu_id": 1600871382355,
        "lu_name": "overvloedig.a"
    },
    "http://rdf.cltl.nl/fn_nl-0.1-1600871385555": {
        "frame_label": "Accoutrements",
        "frame_uri": "http://premon.fbk.eu/resource/fn17-accoutrements",
        "lexical_entries": [
            [
                "broche",
                "N"
            ]
        ],
        "lu_definition": "met een speld erachter dat je op een kledingstuk kunt spelden",
        "lu_id": 1600871385555,
        "lu_name": "broche.n"
    },```

###  **lemma_to_pos_to_lus.json**

mapping from lemma to pos to list of lu urls.
```json
"murder": {
        "N": [
            "http://rdf.cltl.nl/fn_en-1.7-7839",
            "http://rdf.cltl.nl/fn_en-1.7-9052"
        ],
        "V": [
            "http://rdf.cltl.nl/fn_en-1.7-8639"
        ]
    },
    "murderer": {
        "N": [
            "http://rdf.cltl.nl/fn_en-1.7-9087"
        ]
    },
```

## typicality

* typicality_scores
    * Contains one JSON file per event type mapping a PreMOn Frame URI -> typicality score
* lexical_lookup
    * LANGUAGE
        * one JSON file per event type:

```json 
'ordered_frames'
        list of lists
        [
            [PreMOn URI, dropdown label, typicality_score],
            ..
        ]

    'lexical_lookup'
        LEMMA
            POS
                [typicality_score, PreMON frame URI, LU_NAME, LU_URI, dropdown label]
            'all_frames':
                [PreMOn frame URI, PreMOn URI, ...]
```            