import glob
import re
from tabulate import tabulate

INPUT_PATH = "./inputs"
OUTPUT_PATH = "./outputs"

ris_output_file = f"{OUTPUT_PATH}/ris_cleaned.ris"

file_pattern = "pubmed-*.txt"
output_file = f"{OUTPUT_PATH}/pubmed_cleaned.txt"
faulty_output_file = f"{OUTPUT_PATH}/pubmed_faulty.txt"

duplicates_count = 0
faulty_count = 0
unique_count = 0
total_count = 0

# Function to extract DOI from a line with the [doi] suffix
def extract_doi(line):
    match = re.search(r'(10\.\d{4,9}/[-._;()/:A-Z0-9]+)\s\[doi\]', line, re.IGNORECASE)
    return match.group(1).strip() if match else None

# Read DOIs from the merged_output.ris file
merged_dois = set()
with open(ris_output_file, 'r') as ris_file:
    for line in ris_file:
        if line.startswith('DO  -'):
            merged_dois.add(line.strip()[5:].strip())

# Process pubmed-*.txt files
for filename in glob.glob(f'{INPUT_PATH}/{file_pattern}'):
    with open(filename, 'r') as infile, \
         open(output_file, 'w') as outfile, \
         open(faulty_output_file, 'w') as faultfile:
        
        entry = []
        doi_found = False
        for line in infile:
            if line.strip() == '' and entry:
                # Process the completed entry
                doi_in_entry = None
                for entry_line in entry:
                    if 'LID -' in entry_line or 'AID -' in entry_line:
                        doi_in_entry = extract_doi(entry_line)
                        if doi_in_entry:
                            break
                
                if doi_in_entry:
                    if doi_in_entry not in merged_dois:
                        outfile.write(''.join(entry) + '\n\n')
                        unique_count += 1
                    else:
                        duplicates_count += 1
                else:
                    faultfile.write(''.join(entry) + '\n\n')
                    faulty_count += 1
                
                entry = []
                total_count += 1
                doi_found = False
            else:
                entry.append(line)

        # Check the last entry if the file doesn't end with a newline
        if entry:
            doi_in_entry = None
            for entry_line in entry:
                if 'LID -' in entry_line or 'AID -' in entry_line:
                    doi_in_entry = extract_doi(entry_line)
                    if doi_in_entry:
                        break

            if doi_in_entry:
                if doi_in_entry not in merged_dois:
                    outfile.write(''.join(entry) + '\n\n')
            else:
                faultfile.write(''.join(entry) + '\n\n')

data = [
    ["Total", total_count],
    ["Duplicates", duplicates_count],
    ["Unique", unique_count],
    ["Faulty", faulty_count]
]

print("\n> PubMed Processor")
print(tabulate(data, headers=["Description", "Count"], tablefmt="grid"))