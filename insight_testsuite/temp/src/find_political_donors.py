import os
import sys
from dateutil.parser import parser
import pandas as pd
from find_median_for_streaming_data import running_medium


def deleteContent(fName):
    """
    :param fName: File name that needs to have contents erased
    :return: None
    """
    with open(fName, "w"):
        pass


def create_statistics_file_by_zip_cd(input_file, outfile1):
    """
    :param input_file: File that contains donors data
    :return: medianvals_by_zip.txt

    output file summarizes the median amount, count, total_amount based on zip code at any point of the incoming record
    groupby by zipcode

    """

    infile = open(input_file, 'r')
    outfile1 = open(outfile1, 'w')
    zip_dic = {}
    running_medium_dict ={}

    for line in infile:
        skip = False
        fields = line.split('|')
        # Read  individual fields
        cmte_id = fields[0]
        zip_code = fields[10][0:5]
        trans_dt = fields[13]
        trans_amt = fields[14]
        other_id = fields[15]
        # skip reading the line if other_id field has value or cmte_id missing or trans_amt is missing
        if fields[15] not in (None, '') or fields[0] in (None, '') or fields[14] in (None, ''):
            skip = True
        if not skip:
            # process only valid zip code records
            if valid_zip_cd(zip_code):
                count = 1
                tot_sum = int(trans_amt)
                median_num = int(trans_amt)
                if zip_code not in zip_dic:
                    zip_dic[zip_code] = [median_num, count, tot_sum]
                    # creat a  class instance for each unique zip code to have median and add it to dict
                    r = running_medium()
                    r.calc_running_median(median_num)
                    running_medium_dict[zip_code] = r

                else:
                    zip_dic[zip_code] = [running_medium_dict[zip_code].calc_running_median(median_num, zip_dic[zip_code][0]), zip_dic[zip_code][1] + count,
                                         zip_dic[zip_code][2] + tot_sum]

                zip_newrec = cmte_id + '|' + zip_code + '|' + '|'.join(str(x) for x in zip_dic[zip_code]) + '\n'

                outfile1.writelines(zip_newrec)
    outfile1.close()
    infile.close()


def create_statistics_file_by_trans_dt(in_file, out_file):
    """
    :param in_file:   input file
    :param out_file:  medianvals_by_date.txt
    :return: out_file final statistical donor amount data (median, total count, sum ) grouped by each cmte_id and transaction_date.
    """
    infile = open(in_file, 'r')
    outfile = open(out_file, 'w')
    cust_date = {}
    running_medium_dict={}
    for line in infile:
        skip = False
        fields = line.split('|')

        # Read  individual fields
        cmte_id = fields[0]
        zip_code = fields[10][0:5]
        trans_dt = fields[13]
        trans_amt = fields[14]
        other_id = fields[15]
        # skip reading the line if other_id field has value or cmte_id missing or trans_amt is missing
        if fields[15] not in (None, '') or fields[0] in (None, '') or fields[14] in (None, ''):
            skip = True
        if not skip:
            # Read only records with valid transaction date
            if valid_trans_dt(trans_dt):
                # grouping key
                key = cmte_id+'|'+trans_dt
                count = 1
                tot_sum = int(trans_amt)
                median_num = int(trans_amt)
                if key not in cust_date:
                    cust_date[key] = [median_num, count, tot_sum]
                    # create class instances for tracking running medium and add it to the dictionary
                    r = running_medium()
                    r.calc_running_median(median_num)
                    running_medium_dict[key] = r
                else:
                    cust_date[key] = [running_medium_dict[key].calc_running_median(median_num, cust_date[key][0]), cust_date[key][1] + count,
                                      cust_date[key][2] + tot_sum]
                    #print r.max_heap_left
                    #print r.min_heap_right
    #print cust_date
    for k,v in cust_date.items():
        trans_newrec = k + '|'+ '|'.join(str(x) for x in cust_date[k]) + '\n'
        #print trans_newrec
        outfile.writelines(trans_newrec)
    infile.close()
    outfile.close()

def sort_file(infile_name):
    """
    :param infile_name: File that needs to be sorted
    :return: sorted data frame
    """
    df = pd.read_csv(infile_name, sep="|", header=None)
    # sort values by customer and transaction date
    df.sort_values(by=[0, 1], inplace=True)
    df.to_csv(infile_name, sep='|', index = False, header = False)
    return df


def valid_trans_dt(date):
    """
    :param date: incoming date field
    :return: True if the date is in mmddyyyy format else False
    """
    date_string = date[0:2] + '-' + date[2:4] + '-' + date[4:]
    try:
        parser(date_string)
        return True
    except ValueError:
        return False


def valid_zip_cd(zip):
    """"
    :param zip: incoming zipcode
    :return: True if the zip is valid 5 digits else False
    """
    return True if len(zip) == 5 else False

if  __name__ == "__main__":
    # Create medianval_by_zip file
    create_statistics_file_by_zip_cd(sys.argv[1], sys.argv[2])
    # Create medianval_by_date file
    create_statistics_file_by_trans_dt(sys.argv[1], sys.argv[3])
    # sort medianval_by_date.txt file based on transaction date.
    sort_file(sys.argv[3])
    #create_statistics_file_by_zip_cd("./input/itcont.txt", "./output/medianvals_by_zip.txt")
    #create_statistics_file_by_trans_dt("./input/itcont.txt", "./output/medianvals_by_date.txt")
    #sort_file("./output/medianvals_by_date.txt")