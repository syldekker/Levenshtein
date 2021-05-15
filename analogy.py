import sys
from math import e
from collections import defaultdict
import re
import random
from min_edit import min_edit


### calculates pearson correlation btwn two lists of numbers
def pearson(v1, v2):
    if len(v1) != len(v2): return None
    s1 = sum(v1)
    s2 = sum(v2)
    m1 = s1 / len(v1)
    m2 = s2 / len(v2)
    xy = 0.0
    xx = 0.0
    yy = 0.0
    for i in range(len(v1)):
        xy += (v1[i] - m1) * (v2[i] - m2)
        xx += (v1[i] - m1) * (v1[i] - m1)
        yy += (v2[i] - m2) * (v2[i] - m2)
    return xy / ((xx ** .5) * (yy ** .5))


def get_training(f):
    ###	returns the training data as three dictionaries:
    ### the verb's orthographic singular form is the key of each one
    ### pres[verb] gives the phonetic transcription of the verb's present form
    ### past[verb] gives the phonetic transcription of the verb's past form
    ### label[verb] gives the morphological rule category
    pres = defaultdict(lambda: '')
    past = defaultdict(lambda: '')
    label = defaultdict(lambda: '')
    for v in f.readlines():
        orth, p_pres, o_past, p_past, cat = v.split(',')
        pres[orth] = p_pres
        past[orth] = p_past
        label[orth] = cat.strip()
    f.close()
    return (pres, past, label)


### takes a phonetic transcription of a wug verb, a dictionary
### of actual verb forms to compare it to, and a number n.
### returns all neighbors within n as a dictionary of {neighbor: distance} pairs
### if n is negative (by default), all neighbors are returned
def get_neighbors(wugphon='', dict={}, n=-1):
    neighbors = defaultdict(lambda: 0.0)
    for v in dict:
        d = min_edit(wugphon, dict[v])
        if d <= n or n < 0:
            neighbors[v] = d
    return neighbors


### takes dictionary of {neighbor: distance} pairs and returns overall similarity
def similarity(neighbors):
    s = .5
    sim = 0.0
    for n, d in neighbors.items():
        sim += e ** (-d / s)
    return sim


### takes two lists of responses and returns the proportion that match
def accuracy(v1, v2):
    tot = len(v1)
    matches = 0.0
    for x, y in zip(v1, v2):
        if x == y: matches += 1
    return matches / tot


def main():
    train_f = open(sys.argv[1], encoding='utf-8')
    test_f = open(sys.argv[2], encoding='utf-8')
    # store training data in three dictionaries for easy access
    pres, past, label = get_training(train_f)

    # lists to create while looping through wug words
    responses = []  # will contain human forced choice responses
    ratings = []  # will contain human wellformedness ratings
    sims = []  # will contain predicted ratings based on similarity
    preds = []  # will contain predicted forced choice responses based on analogy

    pres_by_class = defaultdict(dict)

    for orth, cat in label.items():            # for each cat (class), find matching
        pres_by_class[cat][orth] = pres[orth]  # {orthographic: phonetic} pairs

    for wug in test_f.readlines():
        f = wug.split(',')
        # skip header line
        if "Orth" in wug: continue
        # extract & store wug data from test file
        orth, phon, rating, reg_past, reg_score, irreg_past, irreg_score, irreg_class = f[0], f[1], float(f[2]), f[
            3], float(f[4]), f[5], float(f[6]), f[7].strip()
        # add rating for this wug to the list
        ratings.append(float(rating))
        # determine participants' preferred past category
        response = ""
        if reg_score < irreg_score:
            response = irreg_class  # participants preferred irregular
        else:  # participants preferred the regular
            # determine & store the regular transformation
            if reg_past[-2:] == 'Id':
                response = "NULL->Id"
            elif reg_past[-1:] == 'd':
                response = "NULL->d"
            elif reg_past[-1:] == 't':
                response = "NULL->t"
        # store participants' preferred past category
        responses.append(response)

        ### PART 2
        pres_neighbors = get_neighbors(wugphon=phon, dict=pres)
        # calculate similarity over all neighbors
        sim = similarity(pres_neighbors)
        # add similarity for this wug to the list
        sims.append(sim)
       # print(sim)
       # print(pres)
       # print(pres_neighbors)
        # print(orth, sim, rating)

        ### PART 3 - compute and store analogical predictions
        ### your code goes here (if you wish, you can also write new functions
        ### or code outside this loop, but that's not necessary).

        class_sims = dict()
        for c, d in pres_by_class.items():                      # create {class:sim} pairs
            wug_neighbors = get_neighbors(phon, d)
            class_sim = similarity(wug_neighbors)
            class_sims[c] = class_sim

        pred = max(class_sims, key=lambda x: class_sims[x])     # out of all {class:sim} pairs,


        preds.append(pred)

        if response == pred:
            match = "Match!!!"
        else:
            match = "No match."

        print(" Wug: " + orth, "\n Preferred past tense: " + response,
              "\n Predicted past tense: " + pred, "\n " + match,
              "\n Close neighbors of " + orth + ": " + str(list(get_neighbors(wugphon=phon, dict=pres, n=2))), "\n")

    test_f.close()
    print("\n Correlation of Ratings x Similarities:", pearson(ratings, sims))

    ### uncomment the next line after PART 3 is done
    print("\n Accuracy of Analogical Predictions:", accuracy(responses, preds))


if __name__ == "__main__":
    main()
