import glob
import sys

if len(sys.argv) > 2:

    input_dir = sys.argv[1]
    output_file = sys.argv[2]

    # list of all files in the directory
    filenames = glob.glob(input_dir + '/*')  

    with open(output_file, 'w') as outfile:
        for fname in filenames:
            with open(fname) as infile:
                for line in infile:
                    outfile.write(line)