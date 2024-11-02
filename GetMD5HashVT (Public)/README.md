# Get MD5 Hash of IOC on Virustotal
## Purposes:
Search and convert the hash type of the Indicator Value (SHA1, SHA256) to MD5  
Final ouput is used for importing into solutions that only accept MD5 Hash values for banning
## Requirements:
Virustotal APIkey (obtained by creating a Virustotal account)  
Template for a csv file as shown below:  

|Indicator Value|Type|
|---|---|
|abcdefgh|MD5|
|abcdefghijkl|SHA1|
|abcdefghijklmnop|SHA256|
...

## Output:
Export a .csv file containing result of converting each Indicator Value type to MD5  
Return N/A if there's no result for the specific Indicator Value  
Example:

|Indicator Value|Type|MD5 Hash|
|---|---|---|
|abcdefgh|MD5|abcdefgh|
|abcdefghijkl|SHA1|bcdefghi|
|abcdefghijklmnop|SHA256|fghijklm|
|askldjalskdjasdjakd|SHA256|N/A|

