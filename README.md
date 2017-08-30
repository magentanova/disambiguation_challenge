# Disambiguation Challenge: Synopsis 

## Process

My first step in receiving this challenge was to explore the data. Keeping an open mind, I studied the identities file and the assets file to see what possibilities made themselves apparent. 

I wrote Python scripts to probe the data for patterns, and after eliminating some dead ends, I found something useful: approximately 29% of the publications/assets include an email address for at least one of their authors. 

I put this down in my "low-hanging fruit" column. As I studied the data, I noted other strategies that seemed promising but would require deeper analysis. 

## Strategies

In my work and my planning, I separated the different strategies out and considered them individually. In the long run, these different strategies would all become features in a single statistical/ml model for predicting authorship. This challenge was an opportunity to try them out individually first. This reminds me of the AdaBoost algorithm, which uses a group of weak classifiers as an ensemble. As long as each performs better than chance, and its approach is orthogonal to the others', it will improve the overall performance of the ensemble classifier.   

### Disambiguation by Email

An email address is unique, so this was a one-step process. The only slightly challenging aspect was doing these matches efficiently, since the assets file was so large. A nested loop —— for each identity, we use their email to search every asset for a match —— would have complexity of I * A, where I is the length of identities and A is the length of assets (discounting the small coefficient of names per asset). Instead, I looked through all the assets once and as I did so generated a dictionary that matched an email to a list of publication ids. Then I iterated through identities and used my dictionary to add a "publication_ids" field. This had a much faster complexity of I + A.

My script for this strategy is `disambiguation_by_email.py`, and the output is in `identities_enriched_using_emails.json`. 

Note: This was the only strategy I had time to implement in full. The other strategies were planned, but I didn't do much in the way of coding them. 

### Disambiguation by Field



