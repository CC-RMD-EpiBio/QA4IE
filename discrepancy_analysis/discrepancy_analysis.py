
import pandas as pd
from collections import Counter

def create_clusters(l = [], exclude = [], hierarchy_present = True):

    """
        clustering algorithm. Groups related annotations together

        param:
            l: list of all annotations for a single document

        return:
            a list containing annotations related to a specific cluster
    """
    if hierarchy_present:
        if exclude:
            l = [i for i in l if i['entity']['mention'] in exclude]

        if l:
            l.sort(key = lambda x: x['entity']['start'])
            
            union_left = l[0]['entity']['start']
            union_right = l[0]['entity']['end']
            result = []
            group = [l[0]]

            for interval in l[1:]:
                current_left = interval['entity']['start']
                current_right = interval['entity']['end']
                if current_left > union_right:
                    result.append(group)
                    group = [interval]
                    union_left = interval['entity']['start']
                    union_right = interval['entity']['end']
                else:
                    group.append(interval)
                    union_right = max(current_right, union_right)
            result.append(group)

            return result
    else:

        if exclude:
            l = [i for i in l if i['mention'] in exclude]

        if l:
            l.sort(key = lambda x: x['start'])
            
            union_left = l[0]['start']
            union_right = l[0]['end']
            result = []
            group = [l[0]]

            for interval in l[1:]:
                current_left = interval['start']
                current_right = interval['end']
                if current_left > union_right:
                    result.append(group)
                    group = [interval]
                    union_left = interval['start']
                    union_right = interval['end']
                else:
                    group.append(interval)
                    union_right = max(current_right, union_right)
            result.append(group)

            return result

    return []

def align_annotators_in_cluster(annotators_in_cluster, alignment, entity_type, annotators_in_document, file, cluster_id):
  
    annotator_freq = {x:annotators_in_cluster.count(x) for x in annotators_in_cluster}
    alignment['entity_type'].append(entity_type)   
    alignment['file'].append(file)  
    alignment['cluster'].append(cluster_id) 

    try: 
        split_combine = annotator_freq[max(annotator_freq, key=annotator_freq.get)]
    except ValueError:
        pass
    else:
        not_in = [a for a in annotators_in_document if not a in annotators_in_cluster]
        # Adding empty space if an annotator is not in the cluster
        for x in not_in:
            try:
                alignment[x].append(None) # entity level alignment
            except KeyError as e:
                alignment[x] = [None]
        # adding space for split/combine case
        for key in annotator_freq:
            diff = abs(annotator_freq[key] - split_combine)
            for i in range(diff):
                alignment[key].append(None)
        # adding document name and cluster columns to match length
        for i in range(split_combine - 1):
            for x in not_in:
                try:
                    alignment[x].append(None) # entity level alignment
                except KeyError as e:
                    alignment[x] = [None]
            alignment['entity_type'].append(entity_type)  
            alignment['file'].append(file)  
            alignment['cluster'].append(cluster_id)   

def apply_hierarchical_structure(schema = None, annotations = []):
    '''
    given a nested hierarchical structure, nest the annotations into said structure

    :param structure: dictionaray with the structure
    :type dict:

    :param annotations: the individual annotations
    :type list:

    :param ignore_set: a list of annotation sets to ignore
    :type list:

    :param set_name: the name of the current annotation set
    :type str:


    '''
    
    #assert structure, 'please provide a hierarchical structure'

    # if set_name in ignore_sets:
    #     return annotations

    assert schema, 'please provide a schema'

    annotations.sort(key = lambda x: x['start'])
    
    structured_annotation_list = []

    for annotation in annotations:
        structured_annotation_dict = {}
        subentity_dictionary = {}
        try:
            current_entity_structure = schema[annotation['mention']]
            if current_entity_structure.has_sub_entities():
              try:
                  # children[i].start >= p.start and children[i].end <= p.end
                  sub_entity_list = [a for a in annotations
                      if a['start'] >= annotation['start'] and 
                         a['end'] <= annotation['end'] and 
                         a['mention'] in current_entity_structure.get_sub_entity_names()]
              
                  for sub_entity in sub_entity_list:
                      try:
                          subentity_dictionary[sub_entity['mention']].append(sub_entity)
                      except KeyError:
                          subentity_dictionary[sub_entity['mention']] = [sub_entity]
              except KeyError:
                  pass

            structured_annotation_dict = {'entity': annotation,
                                          'sub_entities': subentity_dictionary,
                                          'annotator' : annotation['annotator']}

            if structured_annotation_dict:

                structured_annotation_list.append(structured_annotation_dict)

        except KeyError as e:
            pass

    return structured_annotation_list

def cluster_annotations(annotations):

	return create_clusters(annotations)

def align_all_clusters(doc_clusters, types, file, all_annotators):

    def dedup_dict_list(list_of_dicts: list, columns: list) -> list:
        return list({''.join(row[column] for column in columns): row
                    for row in list_of_dicts}.values())

    alignment = {'file' : [],
                 'entity_type' : [],
                 'cluster' : []}   

    for i in range(len(doc_clusters)):
        for _type in types:
            # filter by type
            current_cluster = [anno for anno in doc_clusters[i] if anno['entity']['mention'] == _type]
            
            if current_cluster: # only perform this section if cluster has annotations
                annos_clus = [anno['entity']['annotator'] for anno in current_cluster] # get all the annotators in the clustter (strings)
                types_in_cluster = '/'.join(set([x['entity']['mention'] for x in current_cluster])) # all annotation types in the cluster (parent entity level)
                
                for annotation in current_cluster:
                    try:
                        alignment[annotation['entity']['annotator']].append(annotation['entity']) # entity level alignment
                    except KeyError as e:
                        alignment[annotation['entity']['annotator']] = [annotation['entity']]

                align_annotators_in_cluster(annos_clus, alignment, 
                                             types_in_cluster, all_annotators, 
                                             file, i + 1)
                
                try:
                    sub_types_in_cluster = [y for x in current_cluster for y in x['sub_entities'].keys()]
                    sub_types_in_cluster = list(set(sub_types_in_cluster))
                    
                    for sub_type in sub_types_in_cluster:
                        current_sub_cluster = []

                        for annotation in current_cluster:
                            try:
                                for a in annotation['sub_entities'][sub_type]:
                                    current_sub_cluster.append(a)
                            except KeyError:
                                pass
                        sub_entity_clusters = create_clusters(current_sub_cluster, hierarchy_present = False)


                        for sub_entity_cluster in sub_entity_clusters:
                            annos_sub_clus = [anno['annotator'] for anno in sub_entity_cluster]  

                            
                            for z in range(len(sub_entity_cluster)):

                                annotation = sub_entity_cluster[z]

                                alignment[annotation['annotator']].append(annotation) # entity level alignment

                            align_annotators_in_cluster(annos_sub_clus, alignment, 
	                                                     sub_type, all_annotators, 
	                                                     file, i + 1)                      
                except KeyError as e:
                    pass

    return alignment

def determine_discrepancies(dic):

	mention_discrepancy = []
	discrepancy_print = ''
	discrepancy_level = 0
	feature_discrepancies = []
	feature_discrepancy_print = ''

	all_feature_discrepancies = []
	all_mention_discrepancies = []

	rows = [dic[k] for k in dic if k not in ['entity_type', 'file', 'cluster']]
	cluster_rows = [dic[k] for k in dic if k in ['cluster']]
	entity_rows = [dic[k] for k in dic if k in ['entity_type']]

	alignment_length = len(rows[0]) # all should have the same length
	for y in range(alignment_length):

		temp_row = [x[y] for x in rows]
		

		# for a, b in zip([x for x in temp_row[0:] if not x is None], [x for x in temp_row[:-1] if not x is None]):
		# 	if not a['text_span'] == b['text_span']:
		# 		mention_discrepancy.append('length')
		# 		discrepancy_print +='length\n'


		text_spans = list(set([x['text_span'] for x in temp_row if not x is None]))

		if len(text_spans) > 1:
			mention_discrepancy.append('length')
			discrepancy_print +='length\n'


		if None in temp_row:
			discrepancy_print += 'not annotated by all\n'
			mention_discrepancy.append('not annotated by all')

			if y > 0:
				current_cluster = [x[y] for x in cluster_rows][0]
				previous_cluster = [x[y-1] for x in cluster_rows][0]
				current_entity = [x[y] for x in entity_rows][0]
				previous_entity = [x[y-1] for x in entity_rows][0]

				if current_cluster == previous_cluster:
					if current_entity == previous_entity:
						discrepancy_print += 'split combine\n'
						mention_discrepancy.append('split combine')
			
			if y < alignment_length-1:
				current_cluster = [x[y] for x in cluster_rows][0]
				current_entity = [x[y] for x in entity_rows][0]
				next_entity = [x[y+1] for x in entity_rows][0]
				next_cluster = [x[y+1] for x in cluster_rows][0]

				if current_cluster == next_cluster:
					if current_entity == next_entity:
						discrepancy_print += 'split combine\n'
						mention_discrepancy.append('split combine')

		else:
			discrepancy_print += ''

		temp_row = [x for x in temp_row if x is not None]

		attr_diff = [list(dict(set(x['features'].items()) - set(temp_row[0]['features'].items())).keys()) for x in temp_row[1:] if x is not None]

		if attr_diff:
			attr_diff = attr_diff[attr_diff.index(max(attr_diff, key=len))] 
			for value in attr_diff:
				feature_discrepancy_print += '{x}\n'.format(x=value.lower()) 
				feature_discrepancies.append(value.lower())
			
		else:
			feature_discrepancy_print += ''
			
		all_mention_discrepancies.append(discrepancy_print)
		all_feature_discrepancies.append(feature_discrepancy_print)
		feature_discrepancy_print = ''
		discrepancy_print = ''

	dic['text_discrepancy'] = all_mention_discrepancies
	dic['feature_discrepancy'] = all_feature_discrepancies
	return mention_discrepancy, feature_discrepancies

def create_df(dict_):

	df = pd.DataFrame(dict_)

	return df

def format_cells(dict_):
	rows = [dict_[k] for k in dict_ if k not in ['entity_type', 'file', 'cluster', 'text_discrepancy', 'feature_discrepancy']]
	for y in range(len(rows)):
		for x in range(len(rows[y])):
			if not rows[y][x] is None:
				rows[y][x] = '{}\n\n"{}"\n\n({}-{})\n\nid={}\n\n{}'.format(rows[y][x]['mention'],
                                                                   rows[y][x]['text_span'], 
	                                                                
	                                                                rows[y][x]['start'], 
	                                                                rows[y][x]['end'], 
	                                                                rows[y][x]['id'],
                                                                  '\n'.join(['{} : {}'.format(k, 
                                                                                            v) for k, v in rows[y][x]['features'].items()]))


