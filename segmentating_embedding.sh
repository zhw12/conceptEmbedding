#!/bin/bash

source conf.d/segphrase.conf

mkdir -p $RESULT_DIR

./segPhrase.sh

python convertSegphraseToPhraseAsWord.py $RESULT_DIR/segmented_text.txt

echo "Learning embedding of concepts"
python learnEmbedding.py $RESULT_DIR/segmented_text.txt_phraseAsWord.txt

echo "Done"
