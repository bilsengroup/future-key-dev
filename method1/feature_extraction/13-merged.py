import pandas as pd
import json
from copy import deepcopy

# Load the CSV file
file_path = 'combined_embedings.csv'
df = pd.read_csv(file_path)

# read the 10-result.json file
with open('11-result.json', 'r') as f:
    devs = json.load(f)

# Remove square brackets and split the string to convert to floats
df['embeddings'] = df.iloc[:, 1].apply(lambda x: list(map(float, x.strip('[]').split())))

# Create a DataFrame with the embeddings split into separate columns
embeddings_df = pd.DataFrame(df['embeddings'].tolist())

# Rename columns to have a prefix and index
embeddings_df.columns = [f'f{i+1}' for i in range(embeddings_df.shape[1])]

# If there are more than 600 columns, truncate to the first 600
if embeddings_df.shape[1] > 600:
    embeddings_df = embeddings_df.iloc[:, :600]

# Concatenate the original DataFrame with the new embeddings DataFrame
data = pd.concat([df.drop(columns='embeddings'), embeddings_df], axis=1)
# delete the second column which contains all embeddings
data = data.drop(columns=data.columns[1])

features = {f'f{i}': 0 for i in range(1,601)}
new_features_dict = {'additional_features': features}
for dev in devs.values():
    dev.update(deepcopy(new_features_dict))

# iterate rows of data

for index, row in data.iterrows():
    found = False
    # get the dev key
    dev_key = row['0']
    for dev in devs:
        if dev_key in devs[dev]['devKeys']:
            found = True
            embeddings = row.values[1:]
            embeddings = embeddings.tolist()
            for i, embedding in enumerate(embeddings):
                devs[dev]['additional_features'][f'f{i+1}'] = embedding

            break
    if not found:
        print(f'{dev_key} not found')


# save the updated devs dictionary to a new file
with open('13-result.json', 'w') as f:
    json.dump(devs, f)
