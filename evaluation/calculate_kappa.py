from sklearn.metrics import confusion_matrix, cohen_kappa_score
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from collections import defaultdict
from pathlib import Path
import sys
import os

interlingua_repo_dir = '/Users/jimenezsilvara/Documents/Developer/interlingua/'
sys.path.insert(0, interlingua_repo_dir)
import interlingua


def calculate_kappa(file, key, response, lbs):

    cm = confusion_matrix(key, response, labels = lbs)

    true_positives = cm[0,0]
    false_postives = cm[1,0]
    false_negatives = cm[0,1]
    true_negatives = cm[1,1]

    total_true = true_positives + true_negatives
    total_false = false_postives + false_negatives
    total = total_true + total_false

    a_0 = (true_positives + true_negatives) / total
    cat_1 = (2 * true_positives) / ((2 * true_positives) + false_postives + false_negatives)
    cat_2 = (2 * true_negatives) / (false_postives + false_negatives + (2 * true_negatives))

    expected_matrix = np.array([[sum(cm[0,:])/total, sum(cm[:,0])/total],
                                [sum(cm[1,:])/total, sum(cm[:,1])/total]])

    a_e = (expected_matrix[0,0] * expected_matrix[0,1]) + (expected_matrix[1,0] * expected_matrix[1,1])
    
    cohens_kappa = round((a_0 - a_e) / (1 - a_e), 4)


    print('{}'.format(file))
    print('confusion matrix \n {}'.format(cm))
    print('observed agreement: {}'.format(round(total_true /total, 4)))
    print('positive specific agreement: {}'.format(round(cat_2, 4)))
    print('negative specific agreement: {}'.format(round(cat_1, 4)))
    print('chance agreement: {}'.format(round(a_e, 4)))
    print('cohens kappa: {}'.format(cohens_kappa))

    print('-' * 50)

    return [file, round(total_true /total, 4), round(cat_2, 4), round(cat_1, 4), round(a_e, 4), cohens_kappa]



def match_file_ids(files, strict_matches = True, filter_documents = []):
    """
    Given a list of document paths, match all documents by their file id

    :param files: list of document paths
    :type list:

    :strict_matches: used to test if the function shoulf return the complete set of documents or only those that had
    a pair
    :type boolean

    :filter_documents: list of document ids to keep
    :type list

    :ignore_cases: list of the annotation types to ignore

    """
    temp = defaultdict(list)

    for file in files:
        temp[file.stem].append(file)

    # filtering out documents that did not match
    if strict_matches:
        matches = {x[0].stem : x for x in temp.values() if len(x) > 1}
    else:
        matches = {x[0].stem : x for x in temp.values()}

    if filter_documents :
        matches = {k : v for k, v in matches.items() if v in filter_out}


    return(matches)

def main():

    base_dir = Path(__file__).resolve().parent.parent.parent
    files = [x for x in Path(base_dir / 'annotations').glob('**/*.xml')]

    irr_path = base_dir / 'documentation'/ 'irr'

    # print(attributes)
    documents = match_file_ids(files)

    columns = ['file_id', 'observed_agreement', 'positive_specific_agreement',
               'negative_specific_agreement', 'chance_agreement', 'cohens_kappa']
    out = []

    micro_a = []
    micro_b = []
    for file_name, files in documents.items():
        files.extend([file_name] * len(files))
        a = [
                [
                    annotation.type
                ]   for annotation in interlingua.AnnotationFile(str(files[0])).annotation_sets_dict['ipir'].annotations
            ]

        micro_a.extend(a)

        b = [
                [
                    annotation.type
                ]   for annotation in interlingua.AnnotationFile(str(files[1])).annotation_sets_dict['ipir'].annotations
            ]

        micro_b.extend(b)

        files.extend([file_name] * len(b))

        out.append(calculate_kappa(file_name, a, b, lbs=['IPIR_yes', 'IPIR_no']))

    df = pd.DataFrame(out, columns=columns)

    macro_avrg = pd.Series(data={'observed_agreement':df['observed_agreement'].mean(), 
                  'positive_specific_agreement':df['positive_specific_agreement'].mean(),
                  'negative_specific_agreement':df['negative_specific_agreement'].mean(),
                  'chance_agreement':df['chance_agreement'].mean(), 'cohens_kappa':df['cohens_kappa'].mean()})

    print('-' * 50)
    print('\nmacro average\n{}'.format(macro_avrg))


    print('-' * 50)

    #df.to_csv(irr_path / 'irr_individual_files.csv', index=False)

    #macro_avrg.to_csv(irr_path / 'irr_macro_avrg.csv')

    micro_avrg = pd.DataFrame()
    micro_avrg['attribute'] = columns
    micro_avrg['values'] = calculate_kappa('micro', micro_a, micro_b, 
        lbs=['IPIR_yes', 'IPIR_no'])


    #micro_avrg.iloc[1:].to_csv(irr_path / 'irr_micro_avrg.csv', index=False, header=False)




if __name__ == "__main__":
    main()
