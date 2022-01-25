# QA4IE: A Quality Assurance Tool for Information Extraction

This open source package implements a series of components required for comprehensive quality assurance on annotations created using GATE


## Setup/Installation

The `requirements.txt` file lists all required Python3 packages installable with pip3. Just run
```
pip3 install -r requirements.txt
```
to install all packages.

## Tool components

- **Document Validation**

- **Annotation Validation**

- **Statistics** 
 
- **Evaluation** 

- **Discrepancy Analysis** 

  
 ## Setting the config file
 
 The code is completely reliant on information gathered from a config file. The config file for QA4IE is structured to contain the following information:
 
 - **Annotation Directory:** the absolute path to the annotations in xml format. These annotations should be saved with a specific structure in order to work. It needs to be a single directory that contains multiple sub directories. These sub directories should contain the annotations from each annotators and should be named in a way that represents each annotator. A caveat to consider is that the xml files themselves should be consistently named, in a way that the only difference between the paths should be the file's parent directory. As an example consider the following, `annotations/anno1/file_1.xml` and `annotations/anno2/file_1.xml`. If the files are named differently, the code will treat them as different files. In the case of an annotator containing different files than others, these files will be ignored by the tool. 
 
- **Output Directory:** the absolute path to a results/report directory.
 
- **Task:** this section should be `sequence_labeling`. In the future, there will be an additional option for `classification`.
  
- **Encoding:** the encoding of the xml files
 
 The config file allows to add an unlimited amount of annotation types. The following is an example of how to create these types in the config file.
 
 ```
 [type_main]
 overlaps =
 sub_entities= type_a|type_b|type_c
 features= att_1:=:val_1|val_2|val_3||att_2:=:val_1|val_2
 
 [type_a]
 overlaps = type_b|type_c
 features= att_1:=:val_1|val_2|val_3||att_2:=:val_1|val_2
 
 [type_b]
 overlaps = type_a|type_c
 features= att_1:=:val_1|val_2|val_3||att_2:=:val_1|val_2

 [type_c]
 overlaps = type_a|type_b
 features= att_1:=:val_1|val_2|val_3||att_2:=:val_1|val_2
 ```
Under each annotation type there is up to 3 options that one could add. Where overlaps should contain thee other annotation types for which an overlap is allowed. This option is only necessary for main entities and not sub entities. The code will determine hierarchical overlaps and allow them based on the information from the sub_entities. 

The sub_entities should only go under an annotation that is considered to be a main or parent entity of other sub entities and should be defined in the config file. The order of these entities in the config file does not affect the code at all. 

To add features to a specific entity to have to used several separators. (`:=:`) will separate the attribute name from the possible values. (`|`) will separate each value for a specific attribute. (`||`) separate different attributes in the features dictionary

## Demo script/data

This package includes 1 small dataset for code demonstration purposes:

- ```data/annotations``` synthetic notes annotated using the mobility schema

To use the tool you will first need to update the information inside the config file. Including the absolute paths for your input and output directories. Once that's done just run,
```
python app.py <path_to_config_file>
```
where `<path_to_config_file>` is a placeholder for the absolute path to the config file

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
