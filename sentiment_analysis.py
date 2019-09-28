# Imports the Google Cloud client library
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types
import json
import pandas as pd

# Instantiates a client
client = language.LanguageServiceClient()


df = pd.read_json('data/1000_posts.json')

entities_result = []
annotations_result = []
counter = 0
for index, row in df.iloc[0:1,:].iterrows():
	counter+=1
	print(counter)
    texts = [row['init_post']] + row['comments']
	
	for text in texts:
        document = types.Document(
                    content=text,
                    type=enums.Document.Type.PLAIN_TEXT,
                    language='en')
        entities = client.analyze_entity_sentiment(document).entities
        entities_result.append(entities)
        
        annotations = client.analyze_sentiment(document=document)
        annotations_result.append({"score": annotations.document_sentiment.score,
               "magnitude": annotations.document_sentiment.magnitude})

processed_docword_sentiment = {}
for i in range(len(entities_result)):
    for j in range(len(entities_result[i])):
        if(entities_result[i][j].name not in processed_docword_sentiment.keys()):
            processed_docword_sentiment[entities_result[i][j].name] = {'score':[entities_result[i][j].sentiment.score],
                                                             'magnitude':[entities_result[i][j].sentiment.magnitude]}
        else:
            processed_docword_sentiment[entities_result[i][j].name]['score'].append(entities_result[i][j].sentiment.score)
            processed_docword_sentiment[entities_result[i][j].name]['magnitude'].append(entities_result[i][j].sentiment.magnitude)


with open('data/document_entity_sentiment.json', 'w') as outfile:
    json.dump(processed_docword_sentiment, outfile, indent=4, ensure_ascii=False)
    
with open('data/document_sentiment.json', 'w') as outfile:
    json.dump(annotations_result, outfile, indent=4, ensure_ascii=False)