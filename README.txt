This is the README file for A0099314Y's and A0099332Y's submission

== General notes about this assignment ==

Indexing:

The strategy for indexing is very similar to HW3, except that we now store
(doc ID, term freq) tuple in the postings list instead of just doc ID.

We also pre-processes the vector length (by calculating L2 norm) for each
document for normalisation during searching phase.

Searching:

For all terms appearing in the query, we do an OR-ing on all postings list
fetched. We then calculates the cosine similarity between the query and all
documents in the postings lists, using ltc.lnc ranking scheme. In particular,
the cosine normalisation is done with both query vector length and document
vector length. The latter is pre-computed during indexing phase

== Files included with this submission ==

.
|-- ESSAY.txt ............. answer to essay questions
|-- README.txt ............ this file
|-- dictionary.txt ........ dictonary for all documents
|-- index.py .............. python script to index all documents
|-- postings.txt .......... postings list and document length file
`-- search.py ............. python script to perform query searching
 

== Statement of individual work ==

Please initial one of the following statements.

[x] I, A0099314Y, certify that I have followed the CS 3245 Information
Retrieval class guidelines for homework assignments.  In particular, I
expressly vow that I have followed the Facebook rule in discussing
with others in doing the assignment and did not take notes (digital or
printed) from the discussions.  

[x] I, A0099332Y, certify that I have followed the CS 3245 Information
Retrieval class guidelines for homework assignments.  In particular, I
expressly vow that I have followed the Facebook rule in discussing
with others in doing the assignment and did not take notes (digital or
printed) from the discussions.  

== References ==
