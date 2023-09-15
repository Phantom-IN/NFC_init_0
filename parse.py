import re

# Define a regular expression pattern to extract URLs
url_pattern = r'Href Attribute:\s*(https?://\S+)'

# Function to extract URLs from a line of text
def extract_url(line):
    match = re.search(url_pattern, line)
    if match:
        return match.group(1)
    else:
        return None

# Input file name
input_file = 'hrefs.txt'
# Output file name
output_file = 'output.txt'

# Open the input and output files
with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
    # Iterate through each line in the input file
    for line in infile:
        # Extract the URL from the line
        url = extract_url(line)
        if url:
            # Write the URL to the output file
            outfile.write(url + '\n')

print("URLs extracted and saved in", output_file)
