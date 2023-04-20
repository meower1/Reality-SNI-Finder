import os
import subprocess
import re

result = []
avg_value_list = []
domain_ping_dict = {}

my_file = open("sni.txt", "r")

data = my_file.read()

# replacing end splitting the text when newline ('\n') is seen.
sni_list = data.split("\n")
my_file.close()

#this tests all the domains in sni.txt file and puts them in a list called result

for i in sni_list:
    x = subprocess.check_output(f"./tlsping {i}:443", shell=True).rstrip().decode('utf-8')
    result.append(x)
    
#this extracts all the avg tlsping values from the domains

for j in result:
# use regular expressions to extract the "avg" value
    avg_value = re.findall(r"avg/.*?ms.*?(\d+\.?\d*)ms", j )[0]
    avg_value_list.append(avg_value)

# this puts the sni_list values inside domain_ping_dict as keys and the avg_value_list values as values
print(avg_value_list)
domain_ping_dict = {sni_list[i]: float(avg_value_list[i]) for i in range(len(sni_list))}

#this sorts the dictionary by the values in ascending order
sorted_dict = dict(sorted(domain_ping_dict.items(), key=lambda item: item[1]))

#final result :)
best_sni = list(sorted_dict.keys())[0]
print(best_sni)

os.system("clear")
print("Best SNI is : " + best_sni)
print("\nYou can manaully set this as (dest) and (sni) in your xray config file.")
print("Have a good day o/.\n")

