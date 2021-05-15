# Levenshtein

This is an exercise concerning string similarity and lexical analogy based on experimental data from Albright and Hayes (2003).

It is a version of the 'wug test'.

## Description of files:

`Test.csv` contains the Albright and Hayes data, where:
- **Orth** - orthographic representation of each wug (in present tense)
- **Present** - phonetic transcription of present tense of wug
- **Rating** - participants’ average acceptability rating on scale of 1-7 for each wug
- **Reg_Past** - phonetic form of regular past tense
- **Reg_Rating** - participants’ average rating for regular past tense form
- **Irreg_Past** - phonetic form of irregular past tense form of wug
- **Irreg_Rating** - participants’ average rating for irregular past tense form
- **Class** - label indicating morphological transformation required to form irregular past tense

`Train.csv` is a dictionary of over 4,000 English verbs. It contains the following information for each entry:
- orthographic form of present
- phonetic form of present
- orthographic form of past
- phonetic form of past
- morphological transformation class

## Models:

The analogical model implemented by Albright and Hayes (2003) is contained in `analogy.py`.
* defines similarity between two words *i* and *j* based on Levenshtein distance

### Further documentation forthcoming...
