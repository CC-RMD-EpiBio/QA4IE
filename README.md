# QA4IE: A Quality Assurance Tool for Information Extraction and Text Classification

This open source package implements a series of components required for comprehensive quality assurance on annotations created using GATE

This system was described in the following paper:

+ paper link.

## Setup/Installation

The `requirements.txt` file lists all required Python3 packages installable with pip3. Just run
```
pip3 install -r requirements.txt
```
to install all packages.

## Package components

- **Error Checks:** description.
  + See ```script```
- **Validations:** description.
  + See ```script```
- **Statistics:** description.
  + See ```script```
- **Evaluation:** description.
  + See ```script```
- **Discrepancy Analysis:** description.
  + See ```script```
  
 ## Setting the config file
 
 The code is completely reliant on information gathered from a config file. The config file for QA4IE is structured to contain the following information:
 
 -**Annotation Directory:** the absolute path to the annotations in xml format. These annotations should be saved with a specific structure in order to work. It needs to be a single directory that contains multiple sub directories. These sub directories should contain the annotations from each annotators and should be named in a way that represents each annotator (i.e. initials). A caveat to consider is that the xml files themselves should be consistently named, in a way that the only difference between the paths should be the file's parent directory. As an example consider the following, `annotations/anno1/file_1.xml` and `annotations/anno2/file_1.xml`. If the files are named differently, the code will treat them as different files. In the case of an annotator containing different files than others, these files will be ignored by the tool. 
 
-**Output Directory:** the absolute path to a results/report directory.
 
 -**Task:** this section should either be `sequence_labeling` or `classification`
  
 -**Encoding:** the encoding of the xml files
 
 The config file allows to add an unlimited amount of annotation types. The following is an example of how to create these types in the config file.
 
 ```
 [type_main]
 overlaps =
 sub_entities= type_a|type_b|type_c
 features= foo:b|a|r||foo_2:b_2|a_2|r_2
 
 [type_a]
 overlaps = type_b|type_c
 features= foo:b|a|r
 
 [type_b]
 overlaps = type_a|type_c
 features= foo:b|a|r

 [type_c]
 overlaps = type_a|type_b
 features= foo:b|a|r
 ```
Under each annotation type there is up to 3 options that one could add. Where overlaps should contain thee other annotation types for which an overlap is allowed. This option is only necessary for main entities and not sub entities. The code will determine hierarchical overlaps and allow them based on the information from the sub_entities. 

The sub_entities should only go under an annotation that is considered to be a main or parent entity of other sub entities and should be defined in the config file. The order of these entities in the config file does not affect the code at all. 

To add features to a specific entity to have to used several separators. Colons (`:`) will separate the attribute name from the possible values. Pipes (`|`) will separate each value for a specific attribute. Double pipes (`||`) separate different attributes in the features dictionary

## Demo script/data

This package includes `n` small datasets for code demonstration purposes:

- ```demo_data/demo_dataset_1``` dataset description
- ```demo_data/demo_dataset_2``` dataset description
- ```demo_data/demo_dataset_3``` dataset description
- ```demo_data/demo_dataset_n``` dataset description

The included `demo_script` script utilizes the provided datasets to make a complete complete end-to-end quality assurance process, with the following steps:

1. step 1
2. step 2
3. step 3
4. step 4
5. step n

To use the tool you will first need to update the information inside the config file. Afterwards, to run the tool just run,
```
python app.py <path_to_config_file>
```
where the path_to_config_file is a placeholder for the absolute path to the config file

## Reference

If you use this software in your own work, please cite the following paper:
```
@inproceedings{,
  title = "",
  author = "",
  booktitle = "",
  month = ,
  year = "",
  address = "",
  publisher = "",
  url = "",
  doi = "",
  pages = "",
}
```

## License

All source code, documentation, and data contained in this package are distributed under the terms in the LICENSE file (modified BSD).

<img src="https://clinicalcenter.nih.gov/themes/internet/images/NIH_CC_logo.png"/>
