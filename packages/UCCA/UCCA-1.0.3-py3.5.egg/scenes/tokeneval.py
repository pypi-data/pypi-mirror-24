import re

import nltk

from scenes import classify_scene
from ucca import layer0, layer1


def get_terminals_labels(passages):
    terminals = []
    labels = []
    for passage in passages:
        l0 = passage.layer(layer0.LAYER_ID)
        l1 = passage.layer(layer1.LAYER_ID)
        heads = [x for x in l1.all
                 if x.extra.get('hidden_scene') or x.extra.get('noun_scene')]
        positive_nouns = [head.get_terminals()[0] for head in heads]
        negative_nouns = [x for x in l0.all
                          if re.match(r'NN.+', x.extra.get('postag', ''))
                          and x not in positive_nouns]
        labels.extend([1] * len(positive_nouns) + [0] * len(negative_nouns))
        terminals.extend(positive_nouns + negative_nouns)
    return terminals, labels


def get_context(terminals, context=2):
    tokens = []
    for main_terminal in terminals:
        l0 = main_terminal.root.layer(layer0.LAYER_ID)
        main_position = main_terminal.position
        pre_context = [l0.by_position(i).text
                       for i in range(main_position - 1,
                                      main_position - context - 1, -1)
                       if i >= 1]
        post_context = [l0.by_position(i).text
                        for i in range(main_position + 1,
                                       main_position + context + 1, 1)
                        if i <= len(l0.all)]
        tokens.append((main_terminal.text, tuple(pre_context),
                       tuple(post_context)))
    return tokens


def lemmatize(token, targets):
    wn = nltk.stem.wordnet.WordNetLemmatizer()
    lemma = token
    if lemma in targets:
        return lemma
    if lemma.istitle():
        lemma = token.lower()
    if lemma in targets:
        return lemma
    lemma = wn.lemmatize(lemma)
    return lemma


def evaluate_with_type(tokens, token_labels, targets, target_labels):
    tp, tn, fp, fn = [], [], [], []  # True/Flase positive/negative labels
    found, not_found = [], []
    for token, token_label in zip(tokens, token_labels):
        lemma = lemmatize(token, targets)
        # finding in targets with lemma, but recording results with the orig
        if lemma in targets:
            found.append((token, token_label))
            target_label = target_labels[targets.index(lemma)]
            if target_label == token_label == 0:
                tn.append(token)
            elif target_label == token_label == 1:
                tp.append(token)
            elif token_label == 0:
                fp.append(token)
            else:
                fn.append(token)
        else:
            not_found.append((token, token_label))
    return found, not_found, tp, tn, fp, fn


def evaluate_with_classifier(tokens, token_labels, targets,
                             token_features, classifier):
    tp, tn, fp, fn = [], [], [], []  # True/Flase positive/negative labels
    found, not_found = [], []
    pred = classify_scene.predict_labels(classifier, token_features).tolist()
    for token, token_label, guessed_label in zip(tokens, token_labels, pred):
        lemma = lemmatize(token, targets)
        if lemma in targets:
            found.append((token, token_label))
            if guessed_label == token_label == 0:
                tn.append(token)
            elif guessed_label == token_label == 1:
                tp.append(token)
            elif token_label == 0:
                fp.append(token)
            else:
                fn.append(token)
        else:
            not_found.append((token, token_label))
    return found, not_found, tp, tn, fp, fn
