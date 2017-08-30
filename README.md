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

### Disambiguation by Field of Study

All or nearly all of the identities are missing "department" fields, but we can do a lot toward inferring their department by parsing their "title" fields. Then we search various properties of an asset for a string match. The steps I imagined were as follows: 
  - create a lookup table keying each identities on his or her "sparse name" — FIRSTINITIAL_LASTNAME.
  - Use RegExp to pull the word after a "Professor of | Professor in | Department of | Associate in" pattern. 
    - (Later we could use syntactic parsing to pull the full noun phrase that was the object of the preposition "of/in" in the above cases, getting cases like "Professor of Psychiatry and Behavioral Sciences".)
  - Use a stemmer to get the base of that word (e.g. psychiatric -> psychiatry), and add it to the lookup table.
  - For each asset
    - If an author matches the sparse name of one of our identities, then stem each word in the asset's abstract, title and journal, and check for a match against the identity's stemmed field of study.
      - (Later we could do semantic distance measurements instead of string matching, so that "osteoporosis <--> orthopedics" still gets you something. We would record the maximum of these semantic distance calculations.)
    - This field-of-study match should be a feature in our ultimate matching model.
    
The first step above was as far as I got in `disambiguation_by_field.py`.

### Disambiguation by Association with Known Author

The email-based disambiguation provides us with a large number of surefire connections between identities and assets. We can use this certainty to bootstrap better guesses about identities we're less certain of. 

Let's say we have two authors on a paper: one whose identity is confirmed, and the other whose identity is ambiguous among several possibilites. We can grade each of those possiblities on association with the confirmed author — shared field of study, shared university affiliation, similar doctoral graduation year. Zachary told me after the challenge that previous coauthorship is something that Green Sight is already working on as a disambiguation predictor. 

In a case like this, each separate datum on coauthorship would become a feature in a vector representation of a possible match: "shared_field_with_coauthor", "shared_affiliation_with_coauthor", "prior_publications_with_coauthor", etc., plus derived metrics like the proportion of the identity's prior publications were with the coauthor, the proportion of the coauthor's that were with the identity, and so on. 




