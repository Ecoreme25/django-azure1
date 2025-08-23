input_file = "data.json"
output_file = "data_clean.json"

# Read with UTF-16 and re-encode to UTF-8
with open(input_file, "r", encoding="utf-16") as f:
    content = f.read()

with open(output_file, "w", encoding="utf-8") as f:
    f.write(content)
