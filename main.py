from subprocess import check_output, run, CalledProcessError
from re import findall
from pandas import DataFrame
from tabulate import tabulate

# Read the sni.txt file and split it into a list of domain names
with open("sni.txt", "r") as my_file:
    data = my_file.read()
    sni_list = data.split("\n")

# Remove any empty strings from the sni_list
sni_list = list(filter(None, sni_list))

# Test all the domains in sni.txt file and put the results in a list called result
result = []
try:
    for i in sni_list:
        x = check_output(f"./tlsping {i}:443", shell=True).rstrip().decode('utf-8')
        result.append(x)
except CalledProcessError:
    pass

# Extract all the avg tlsping values from the domains
avg_value_list = []
for j in result:
    # Use regular expressions to extract the "avg" value
    avg_value = findall(r"avg/.*?ms.*?(\d+\.?\d*)ms", j )[0]
    avg_value_list.append(avg_value)

# Create a dictionary with the domain names as keys and the avg values as values
domain_ping_dict = {sni_list[i]: float(avg_value_list[i]) for i in range(len(sni_list))}

# Sort the dictionary by the values in ascending order
sorted_dict = dict(sorted(domain_ping_dict.items(), key=lambda item: item[1]))

# Convert the sorted dictionary to a pandas DataFrame and print it using tabulate
df = DataFrame(sorted_dict.items(), columns=['domains', 'pings(ms)'])
run('clear')
print(tabulate(df, headers='keys', tablefmt='psql'))

