#!/usr/bin/python

prog_desc = "wrapper to run reports against mutliple accounts passing environment specific variables"

import os, sys
from datetime import datetime
import subprocess

def main():

    # profile is the profile name in your ~/.aws/config file
    profiles_to_run= [
     {'profile': 'default', 'region': 'us-west-2', 'which_report' : 'generate_csv_all_instance_tags_read_only.py'},
     {'profile': 'xxxxxxxx', 'region': 'us-west-2', 'which_report' : 'generate_csv_all_instance_tags_read_only.py'},
     {'profile': 'xxxxxxxx', 'region': 'us-west-2', 'which_report' : 'generate_csv_all_instance_tags_read_only.py'},
     {'profile': 'xxxxxx-apne-cf2', 'region': 'ap-northeast-1', 'which_report' : 'generate_csv_all_instance_tags_read_only.py'},
     {'profile': 'xxxxxxxx', 'region': 'us-west-2', 'which_report' : 'generate_csv_all_instance_tags_read_only.py'},
     {'profile': 'xxxxxxxx', 'region': 'us-west-2', 'which_report' : 'generate_csv_all_instance_tags_read_only.py'},
     {'profile': 'xxxxxxxx', 'region': 'us-west-2', 'which_report' : 'generate_csv_all_instance_tags_read_only.py'},
     {'profile': 'xxxxxxxx', 'region': 'us-west-2', 'which_report' : 'generate_csv_all_instance_tags_read_only.py'},
     {'profile': 'xxxxxxxx', 'region': 'us-west-2', 'which_report' : 'generate_csv_all_instance_tags_read_only.py'},
     {'profile': 'xxxxxxxx', 'region': 'us-west-2', 'which_report' : 'generate_csv_all_instance_tags_read_only.py'},
     {'profile': 'xxxxxxxx', 'region': 'us-west-2', 'which_report' : 'generate_csv_all_instance_tags_read_only.py'},
     {'profile': 'xxxxxxxx', 'region': 'ap-northeast-1', 'which_report' : 'generate_csv_all_instance_tags_read_only.py'},
     {'profile': 'xxxxxxxx', 'region': 'eu-central-1', 'which_report' : 'generate_csv_all_instance_tags_read_only.py'},
     {'profile': 'xxxxxxxx', 'region': 'ap-northeast-1', 'which_report' : 'generate_csv_all_instance_tags_read_only.py'},
     {'profile': 'xxxxxxxx', 'region': 'eu-central-1', 'which_report' : 'generate_csv_all_instance_tags_read_only.py'},
     {'profile': 'xxxxxxxx', 'region': 'us-east-1', 'which_report' : 'generate_csv_all_instance_tags_read_only.py'}

    ]

    # dir where reports are written out to
    report_dir = "./reports/"+str(datetime.now().strftime('%Y-%m-%d-%H')+"/")


    # create the dir
    os.system("mkdir -p {0}".format(report_dir))

    # iterate thru each profile to generate report (and whatever else)
    for profile in profiles_to_run:
        if 'read_only' not in profile['which_report']:
            cmd =  "python aws_tag_validation.py --dryrun=false --region={1} --profile={0}".format(profile['profile'],profile['region'])
            execute_log(cmd)

        csv_name = profile['profile']+"_tag_report.csv"
        cmd = "python {2} --region={1} --profile={0} {4} --output={3}".format(profile['profile'],profile['region'],profile['which_report'],report_dir+csv_name,"--use_cloudwatch=false")
        print cmd
        os.system(cmd)
        #os.system("python generate_csv_all_instance_tags_read_only.py --profile {0}".format(profile))

        #os.system("open {0} -a \"Microsoft Excel\"".format(csv_name))
        cmd =  "open {0} -a \"Microsoft Excel\"".format(report_dir+csv_name)
        print cmd
        #os.system(cmd)

        # concatonate_reports into one MEGA report!
        concatonate_reports(report_dir)

def execute_log(cmd):
    print cmd
    ## TODO: add code to log cmd to file
    os.system(cmd)

def unused():
    pass

# concatonate all the csv reports
def concatonate_reports(report_dir):
    filenames = []
    output_file = report_dir + str(datetime.now().strftime('%Y-%m-%d'))+"_combined_accounts_tagging_report.csv"

    # walk report dir to get report filenames
    files = [ f for f in os.listdir(report_dir) if os.path.isfile(os.path.join(report_dir,f)) ]
    for f in files:
        if "combined_accounts" not in f: #  avoid recursive read error
            filenames.append(f)

    # grab header
    with open(os.path.join(report_dir,filenames[0])) as infile:
        header = infile.readline()

    # open each file and combine them.
    # remove header on each report.
    with open(output_file, 'w') as outfile:
        outfile.write(header)
        for fname in filenames:
            with open(os.path.join(report_dir,fname)) as infile:
                infile.next() # skip header line
                for line in infile:
                    outfile.write(line)


if __name__ == "__main__":
    main()
