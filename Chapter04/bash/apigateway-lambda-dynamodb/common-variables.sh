#!/bin/sh
# Copyright (c) 2017-2019 Starwolf Ltd and Richard Freeman. All Rights Reserved.
# Licensed under the Apache License, Version 2.0

export profile="demo"
# echo profile=$profile
export region="us-west-1"
# echo region=$region
# export aws_account_id=$(aws sts get-caller-identity --query 'Account' --profile $profile | tr -d '\"')
export aws_account_id="357298582725"
# echo aws_account_id=$aws_account_id
export template="lambda-dynamo-data-api"
# echo template=$template
export bucket="deploying-serverless-server"
# echo bucket=$bucket
export prefix="tmp/sam"
# echo prefix=$prefix

# Lambda settings
export zip_file="lambda-dynamo-data-api.zip"
# echo zip_file=$zip_file
export files="lambda_return_dynamo_records.py"
# echo files=$files
