import argparse
import pickle
import random

import numpy as np

from scenes import classify_scene


def get_data_objects(labels_fd, fmat_fd):
    """Gets file obj of 2 pickle files and returns (targets, labels, fmat)."""
    targets, labels = pickle.load(labels_fd)
    fmat = pickle.load(fmat_fd)
    labels_fd.close()
    fmat_fd.close()
    return targets, labels, fmat


def filter_data(targets, labels, fmat, ratio):
    """Filters the negative examples to be in ratio with the positive ones.

    Takes the negative examples randomly, and all positive examples.

    Args:
        targets: list of target phrases
        labels: numpy.array of 0/1, for negative/positive examples
        fmat: feature matrix (numpy.array of scores) of the targets
        ratio: desired ratio between positive and negative examples

    Returns:
        a tuple of filtered (targets, labels, fmat)

    """

    pos_targets = [t for t, la in zip(targets, labels) if la == 1]
    neg_targets = [t for t, la in zip(targets, labels) if la == 0]
    pos_fmat = fmat[[i for i, la in enumerate(labels) if la == 1]]
    neg_fmat = fmat[[i for i, la in enumerate(labels) if la == 0]]

    # Creates a random permutation of indices of negative examples with the
    # right ratio to positive ones
    neg_indices = list(range(len(neg_targets)))
    random.shuffle(neg_indices)
    neg_indices = neg_indices[:len(pos_targets) * ratio]
    new_targets = [neg_targets[i] for i in neg_indices]
    new_targets += pos_targets
    new_fmat = np.append(neg_fmat[np.array(neg_indices)], pos_fmat).reshape(
        len(neg_indices) + len(pos_fmat), len(neg_fmat[0]))
    new_labels = np.append(np.zeros(len(neg_indices), dtype=np.int32),
                           np.ones(len(pos_targets), dtype=np.int32))

    return new_targets, new_labels, new_fmat


def run_kfold_evaluation(orig_targets, orig_labels, orig_fmat, method,
                         ratio, c_param, nu_param, learn_rate, n_estimators,
                         detailed=False):

    targets, labels, fmat = filter_data(orig_targets, orig_labels, orig_fmat,
                                        ratio)

    stats, details = classify_scene.evaluate(fmat, labels, targets, method, 10,
                                             c_param, nu_param, learn_rate,
                                             n_estimators)
    # We use zip(*stats) because stats are [(prec1, rec1, acc1), ((prec2 ...))]
    # and this turns them into [(prec1, prec2 ...), (rec1, rec2 ..)] which is
    # what we want to use mean() on
    results = [np.mean([x for x in stat if x is not None])
               for stat in zip(*stats)]
    out = [results]
    if detailed:
        out.append(details)
    return out


def run_bl_evaluation(orig_targets, orig_labels, orig_fmat, ratio, coll, wikt):
    targets, labels, fmat = filter_data(orig_targets, orig_labels, orig_fmat,
                                        ratio)
    return classify_scene.evaluate_bl(labels, classify_scene.baseline(targets, coll, wikt))


def main():
    argparser = argparse.ArgumentParser()
    argparser.add_argument('labels', type=argparse.FileType('rb'))
    argparser.add_argument('fmat', type=argparse.FileType('rb'))
    argparser.add_argument('method', choices=('bl', 'c_svc', 'nu_svc_linear',
                                           'nu_svc_sigmoid', 'lr', 'gboost'),
                        help='classification method')
    argparser.add_argument('--detailed', action='store_true')
    argparser.add_argument('--collins', help='path to collins dict in pickle')
    argparser.add_argument('--wiktionary', help='path to wiktionary defs')
    argparser.add_argument('--ratio', type=float, default=2)
    argparser.add_argument('--runs', type=int, default=1,
                        help='times to run evaluation and average')
    argparser.add_argument('-c', type=float, default=1,
                        help='C parameter for c_svc')
    argparser.add_argument('--nu', type=float, default=0.5,
                        help='nu parameter for nu_svc*')
    argparser.add_argument('--learnrate', type=float, default=0.1,
                        help='learning (shrinkage) rate for GB')
    argparser.add_argument('--nestimators', type=int, default=100,
                        help='number of estimators for GB')
    args = argparser.parse_args()

    orig_targets, orig_labels, orig_fmat = get_data_objects(args.labels,
                                                            args.fmat)
    all_results = []
    if args.runs > 1:
        args.detailed = False  # don't use it
    for _ in range(args.runs):
        if args.method == 'bl':
            results = run_bl_evaluation(
                orig_targets, orig_labels, orig_fmat, args.ratio, args.collins,
                args.wiktionary)
            args.detailed = False  # no detailed results for baseline
        else:
            out = run_kfold_evaluation(orig_targets, orig_labels, orig_fmat,
                                       args.method, args.ratio,
                                       args.c, args.nu, args.learnrate,
                                       args.nestimators, args.detailed)
            if args.detailed:
                results, details = out
            else:
                results = out[0]
        all_results.append(results)

    results = [np.mean(stat) for stat in zip(*all_results)]
    results.append(2*results[0]*results[1] / (results[0] + results[1]))
    print("Precision: {} Recall: {} Accuracy: {} Fscore: {}".format(*results))
    if args.detailed:
        print("Detailed Results:")
        for true_label in [0, 1]:
            for pred_label in [0, 1]:
                print("\n\nTrue: {} Pred: {} Targets:\n".format(true_label,
                                                                pred_label),
                      *details[true_label][pred_label], sep='\t')


if __name__ == '__main__':
    main()
