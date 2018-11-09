#!/bin/sh
#
#	Submit file data/sumissions/${1} with message ${2}
#
#	To get & set `kaggle` command see: github.com/Kaggle/kaggle-api
#
#  	Run from main path: ./scripts/submit.sh sample_submission.csv "This is the sample submission"
#
kaggle competitions submit -f data/submissions/${1} -m "${2}" digit-recognizer