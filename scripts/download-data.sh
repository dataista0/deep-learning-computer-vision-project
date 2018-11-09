#!/bin/sh
#
#	Download kaggle digit-recognizer competition dataset to data/base/
# 
#	To get & set `kaggle` command see: github.com/Kaggle/kaggle-api
#
#  	Run from main path: ./scripts/download-data.sh
#
kaggle competitions download -p data/base/ digit-recognizer