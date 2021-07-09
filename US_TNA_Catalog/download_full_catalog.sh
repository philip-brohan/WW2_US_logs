#!/usr/bin/bash

# Download and unpack the US TNA catalog
# https://registry.opendata.aws/nara-national-archives-catalog/
# It's on aws, so need awscli in the environment and configured.
# It's also large - a 10Gb download and 230Gb of JSON when unzipped.

cd $SCRATCH/WW2_US_logs/US_TNA_Catalog/
aws s3 cp s3://nara-national-archives-catalog/zip/nac_export_authorities_2020-11-20.zip .
unzip -DD nac_export_authorities_2020-11-20.zip
aws s3 cp s3://nara-national-archives-catalog/zip/nac_export_descriptions_2020-11-20.zip .
unzip -DD nac_export_descriptions_2020-11-20.zip



