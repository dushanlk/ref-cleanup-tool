import glob
import re
from tabulate import tabulate

INPUT_PATH = "./inputs"
OUTPUT_PATH = "./outputs"

file_pattern = "*.ris"  # Pattern to match multiple .ris files
output_file = f"{OUTPUT_PATH}/ris_cleaned.ris"
faulty_output_file = f"{OUTPUT_PATH}/ris_faulty.ris"

def parse_ris_entries(file_content):
    """Parse RIS content and return entries as a list of dictionaries."""
    entries = []
    current_entry = {}
    for line in file_content.strip().splitlines():
        if line.strip() == "ER  -":  # End of a record
            if current_entry:
                entries.append(current_entry)
            current_entry = {}
        elif line.strip():  # Only process non-empty lines
            tag, value = line[:2], line[6:].strip()
            if tag not in current_entry:
                current_entry[tag] = value
            else:
                current_entry[tag] += " " + value  # Concatenate values for repeated fields
    return entries

def load_ris_files(file_pattern):
    """Load and parse multiple RIS files based on the given file pattern."""
    all_entries = []
    for filename in glob.glob(f"{INPUT_PATH}/{file_pattern}"):
        with open(filename, "r", encoding="utf-8") as file:
            content = file.read()
            entries = parse_ris_entries(content)
            all_entries.extend(entries)
    return all_entries

def remove_duplicates(entries):
    """Separate entries into unique ones based on DOI, and handle entries without DOIs."""
    unique_entries = {}
    no_doi_entries = []

    duplicates_count = 0
    
    for entry in entries:
        doi = entry.get("DO", "")
        if doi:
            # Check if entry already exists with this DOI
            if doi in unique_entries:
                duplicates_count += 1
                # Replace with entry having a longer 'AB' content
                if len(entry.get("AB", "")) > len(unique_entries[doi].get("AB", "")):
                    unique_entries[doi] = entry
            else:
                unique_entries[doi] = entry
        else:
            no_doi_entries.append(entry)  # Collect entries without DOIs
    
    return list(unique_entries.values()), no_doi_entries, duplicates_count

def save_to_ris(entries, output_file):
    """Save entries back to a .ris file format."""
    with open(output_file, "w", encoding="utf-8") as file:
        for entry in entries:
            for tag, value in entry.items():
                for line in value.split("\n"):
                    file.write(f"{tag}  - {line}\n")
            file.write("ER  - \n\n")  # End each entry with ER

# Load entries from all files
entries = load_ris_files(file_pattern)

# Separate entries into unique ones with DOIs and those without
unique_entries, no_doi_entries, duplicates_count = remove_duplicates(entries)

# Save entries with DOIs to the main output file
save_to_ris(unique_entries, output_file)

# Save entries without DOIs to the faulty output file
save_to_ris(no_doi_entries, faulty_output_file)

# print("RIS processor")
# print("=============")
# print(f"> Processed {len(entries)} entries & {duplicates_count} duplicates detected.")
# print(f"> Saved {len(unique_entries)} unique entries with DOIs to {output_file}.")
# print(f"> Saved {len(no_doi_entries)} entries without DOIs to {faulty_output_file}.")

data = [
    ["Total", len(entries)],
    ["Duplicates", duplicates_count],
    ["Unique", len(unique_entries)],
    ["Faulty", len(no_doi_entries)]
]

print("\n> RIS processor")
print(tabulate(data, headers=["Description", "Count"], tablefmt="grid"))