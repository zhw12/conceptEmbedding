# !/bin/bash

Green='\033[0;32m'
NC='\033[0m'

source conf.d/segphrase.conf

mkdir -p tmp/$DATASET

echo -e "${Green}Training SegPhrase${NC}"
./domain_keyphrase_extraction.sh

cp SegPhrase/results/$DATASET/salient.csv tmp/$DATASET/keyphrases.csv
cp SegPhrase/results/$DATASET/segmentation.model tmp/$DATASET/segmentation.model

echo -e "${Green}Identifying Phrases in Input File${NC}"
./SegPhrase/bin/segphrase_parser tmp/$DATASET/segmentation.model \
  tmp/$DATASET/keyphrases.csv $RETAIN_PHRASES_RATIO $RAW_TEXT ./tmp/$DATASET/segmented_text.txt 1

cp tmp/$DATASET/keyphrases.csv $RESULT_DIR
cp ./tmp/$DATASET/segmented_text.txt $RESULT_DIR
cp tmp/$DATASET/segmentation.model $RESULT_DIR
