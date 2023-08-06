
import numpy as np
import os, sys

sys.dont_write_bytecode = True

# sys.path.remove('/Users/Reddy/anaconda/lib/python2.7/site-packages/pyradigm')
# sys.path.extend(['/Users/Reddy/opensource/pyradigm/pyradigm'])

from pyradigm import MLDataset

import neuropredict
import rhst
import visualize
import freesurfer

# out_dir = '/Users/Reddy/Downloads/pingyong/results'
out_dir = '/Users/Reddy/Downloads/test_neuropredict_results'
if not os.path.exists(out_dir):
    os.mkdir(out_dir)
res_path = os.path.join(out_dir, 'rhst_results.pkl')
# neuropredict.visualize_results(res_path, out_dir, ['ChoCrarea_L', 'ChoCrarea_R', 'NAACrarea_L', 'NAACrarea_R'])
# neuropredict.export_results(res_path, out_dir)



feat_generator = np.random.randn

# out_dir = os.path.abspath('../tests')
# meta_file = os.path.join(out_dir,'meta.csv')

meta = list()

def make_random_MLdataset(max_num_classes = 20,
                          max_class_size = 50,
                          max_dim = 100,
                          stratified = True):
    "Generates a random MLDataset for use in testing."

    num_classes = np.random.randint(2, max_num_classes, 1)
    if not stratified:
        class_sizes = np.random.random_integers(min(50, max_class_size),
                                                max(50, max_class_size),
                                                size=[num_classes, 1])
    else:
        class_sizes = np.repeat(np.random.randint(min(50, max_class_size),
                                                  max(50, max_class_size)),
                                                  num_classes)

    num_features = np.random.randint(min(3, max_dim), max(3, max_dim), 1)[0]
    feat_names = [ str(x) for x in range(num_features)]

    class_ids = list()
    labels = list()
    for cl in range(num_classes):
        class_ids.append('class-{}'.format(cl))
        labels.append(int(cl))

    ds = MLDataset()
    for cc, class_ in enumerate(class_ids):
        subids = [ 'sub{:03}-class{:03}'.format(ix,cc) for ix in range(class_sizes[cc]) ]
        for sid in subids:
            ds.add_sample(sid, feat_generator(num_features), int(cc), class_, feat_names)

    return ds


# # code to generate two classes with the same features
# clset = rand_ds.class_set
# class_one = rand_ds.get_class(clset[0])
# class_two = rand_ds.get_class(clset[1])
# same_data_two_classes = rand_ds.get_class(clset[0])
#
# ids_class1 = class_one.sample_ids
# for idx, id in enumerate(class_two.sample_ids):
#     # id from class 2, but data from class 1
#     same_data_two_classes.add_sample(id, class_one.data[ids_class1[idx]], class_two.labels[id], class_two.classes[id])
#
# out_path = os.path.join(out_dir, 'same_data_two_classes.pkl')
# # same_data_two_classes.save(out_path)

def test_chance_classifier_binary():

    rand_ds = make_random_MLdataset(max_num_classes=3, stratified=True,
        max_class_size = 100, max_dim = 100)

    out_path = os.path.join(out_dir, 'two_classes_random_features.pkl')
    rand_two_class = rand_ds.get_class(rand_ds.class_set[0:2])
    rand_two_class.save(out_path)

    out_list = os.path.join(out_dir, 'same_data_two_classes_list_datasets.txt')
    with open(out_list, 'w') as lf:
        lf.writelines('\n'.join([out_path, ]))

    method_names = ['random']
    res_path = rhst.run(out_list, method_names, out_dir,
                        train_perc=0.5, num_repetitions=50)

    neuropredict.visualize_results(res_path, out_dir, method_names)

    dataset_paths, method_names, train_perc, num_repetitions, num_classes, \
        pred_prob_per_class, pred_labels_per_rep_fs, test_labels_per_rep, \
        best_min_leaf_size, best_num_predictors, \
        feature_importances_rf, feature_names, \
        num_times_misclfd, num_times_tested, \
        confusion_matrix, class_set, accuracy_balanced, auc_weighted, positive_class = rhst.load_results(res_path)

    # TODO replace hard coded chance accuracy calculation with programmatic based on class sample sizes
    # assert np.median(accuracy_balanced) == np.median(rhst.chance_accuracy(class_sizes))
    if abs(np.median(accuracy_balanced)-0.5) > 0.05:
        raise ValueError('Accuracy to discriminate between two inseparable classes significantly differs from 0.5')

    if abs(np.median(auc_weighted)-0.5) > 0.05:
        raise ValueError('AUC to discriminate between two inseparable classes significantly differs from 0.5')



test_chance_classifier_binary()
#
# random_dataset = make_random_MLdataset( max_num_classes = 3)
# class_set, label_set, class_sizes = random_dataset.summarize_classes()
#
# out_path = os.path.join(out_dir, 'random_dataset.pkl')
# random_dataset.save(out_path)
#
# out_list = os.path.join(out_dir, 'list_datasets.txt')
# with open(out_list, 'w') as lf:
#     lf.writelines('\n'.join([out_path, ]))
#
# # res_path = rhst.run(out_list, out_dir, num_repetitions=20)
# dataset_paths, method_names, train_perc, num_repetitions, num_classes, \
#            pred_prob_per_class, pred_labels_per_rep_fs, test_labels_per_rep, \
#            best_min_leaf_size, best_num_predictors, \
#            feature_importances_rf, feature_names, \
#            num_times_misclfd, num_times_tested, \
#            confusion_matrix, class_set, accuracy_balanced, auc_weighted = rhst.load_results(res_path)
# print ''

