import csv
import glob
import os

#directory = raw_input("INPUT Folder:")
#output = raw_input("OUTPUT Folder:")

directory = "example_out/"
output = "example_out/"

txt_files = os.path.join(directory, '*.txt')

for txt_file in glob.glob(txt_files):
    with open(txt_file, "rt") as input_file:
        in_txt = csv.reader(input_file, delimiter=' ') #use tab as a delimiter
        filename = os.path.splitext(os.path.basename(txt_file))[0] + '.csv'

        with open(os.path.join(output, filename), 'wt') as output_file:
            out_csv = csv.writer(output_file)
            out_csv.writerows(in_txt)

