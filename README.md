# Concept Embedding


## Notes

This software requires [SegPhrase](https://github.com/shangjingbo1226/SegPhrase) to extract domain keyphrases. It has been included in this repository but users should check the SegPhrase related documentations for proper instruction.

## Requirements

We will take Ubuntu for example.

* g++ 4.8
```
$ sudo apt-get install g++-4.8
```
* python 2.7
```
$ sudo apt-get install python
```
* other python packages
```
$ sudo pip install -r requirements.txt
```

## Build
Build SegPhrase by Makefile in the terminal.
```
$ cd SegPhrase
$ make
```

## Run
We provide a pipeline for running the concept extraction, segmentation and embedding learning together.
```
$ ./segmentating_embedding.sh
```
The concept extraction and segmentation are in `segPhrase.sh`, which calls `domain_keyphrase_extraction.sh` for concept extraction.

 Segmented text processing and phrase-to-token convertion is in `convertSegphraseToPhraseAsWord.py`.

Concept embedding learning is in `learnEmbedding.py`.

You could use `cleanTmp.sh` to delete temp files.


## Parameters
The running parameters are located in `conf.d` folder, including `segphrase.conf` and `learning_embedding.conf`. 

`segphrase.conf` contains the parameters for concept extraction and segmentation.

`learning_embedding.conf` contains the parameters for learning concept embedding.

### segphrase.conf
```
DATASET=dataset
```
DATASET refers to the name you assign to the dataset, which related to the location for temp files.
```
RAW_TEXT=data/input.txt
```
RAW_TEXT is the input of SegPhrase, where each line is a single document. 

```
AUTO_LABEL=1
DATA_LABEL=SegPhrase/data/wiki.label.auto
```

When AUTO_LABEL is set to 1, SegPhrase will automatically generate labels and
save it to DATA_LABEL. Otherwise, it will load labels from DATA_LABEL.

```
WORDNET_NOUN=1
```

When WORDNET_NOUN is set to 1, SegPhrase will resort to wordnet synsets to keep
only noun candidates as the last step of training. This requires you to install
nltk in python.

```
KNOWLEDGE_BASE=SegPhrase/data/wiki_labels_quality.txt
KNOWLEDGE_BASE_LARGE=SegPhrase/data/wiki_labels_all.txt
```

We have two knowledge bases, the smaller one contains high quality phrases for
positive labels while the larger one is used to exclude medium quality phrases
for negative labels.

```
SUPPORT_THRESHOLD=10
```

A hard threshold of raw frequency is specified for frequent phrase mining, which
will generate a candidate set.

```
OMP_NUM_THREADS=4
```

You can also specify how many threads can be used for SegPhrase.

```
DISCARD_RATIO=0.00
```

The discard ratio (between 0 and 1) controls how many positive labels can be
broken. It is typically small, for example, 0.00, 0.05, or 0.10. It should be
EXACTLY 2 digits after decimal point.

```
MAX_ITERATION=5
```

This is the number of iterations of Viterbi training.

```
ALPHA=0.85
```

Alpha is used in the label propagation from phrases to unigrams.

```
RETAIN_PHRASES_RATIO=0.5
```

RETAIN_PHRASES_RATIO is the ratio of phrases kept when doing the segmentation.

### learning_embedding.conf

```
file=results/segmented_text.txt_phraseAsWord.txt
```

file is the input file of `learning_embedding.py`, where each line is a single document.
By default, it points to the segmented result where each phrase is converted into one token.

```
result_dir=results
```

result_dir is the output file directory of `learning_embedding.py`.

```
embed_size=200
```

embed_size is the dimensionality of the learned embedding vectors.

```
sg=1
```

sg is the training algorithm of learning embedding, where sg = 0 corresponds to CBOW, sg = 1 corresponds to skip-gram. 

```
max_vocab_size=None
```

max_vocab_size is maximum num of vocabulary used during vocabulary building. It should be None or a number, e.g. 60000, where None means using all vocabulary.

```
workers=8
```

workers is num of threads used to learn the embedding.



## Input Format
The input should be a text file with one document per line. 

For multiple files, we provide a python file `concatFiles.py` for concatenating them into one file.

The usage of concatFiles.py is `python concatFiles.py input_dir output_file`.

Since Segphrase parser uses square brackets to identify phrases in the segmented text, these brackets should be cleaned from input files to avoid misidentification. Besides, Segphrase will fail to automatically generate label if the dataset is too small.

## Output Format
The output  consists of
* ```keyphrases.csv```
The extracted keyphrases by Segphrase.
* ```segmented_text.txt_phraseAsWord```
The segmented text, each phrase is represented as words joined by underscore.
* ```concept_embedding*.json```
The concept/phrase embedding. It is a json file where each term follows the structure of ```concept : list form of concept embedding array```.
* ```model*.model```
The dump of gensim word2vec model.
* ```segmentation.model```
The Segphrase segmentation model.
* ```segmented_text.txt```
The original segmentation result of Segphrase model.
