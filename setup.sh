#!/bin/bash
source bin/activate
export AWS_ACCESS_KEY_ID='YOURKEY'
export AWS_ACCESS_SECRET_KEY='YOURSECRET'
export AWS_REGION='us-west-2' # default region 
pip install -r requirements.txt