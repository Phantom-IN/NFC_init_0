import re

url_pattern = r'Href Attribute:\s*(https?://\S+)'
def extract_url(line):
    match = re.search(url_pattern, line)
    if match:
        return match.group(1)
    else:
        return None

input_file = 'hrefs.txt'
output_file = 'output.txt'

with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
    for line in infile:
        url = extract_url(line)
        if url:
            outfile.write(url + '\n')

print("URLs extracted and saved in", output_file)
