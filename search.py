from nltk.stem.porter import *
import getopt, json, math, heapq

#######################################################################
# Read query - execute query - output result
#######################################################################

def search():
	query_file = file(QUERY_DIR, 'r')
	queries = []
	for line in query_file:
		query = parse_query(line)
		result = evaluate(query)
		output(result)
	query_file.close()


def output(result):
	out_file.write(' '.join(map(str, result)) + '\n')

def parse_query(raw):
	# after tokenising the query,
	# we collect terms into a dictionary of term - term frequency
	# for later calculation of query tf
	query = raw.strip().split()
	query = [normalise_word(w) for w in query]
	query_dict = {}
	for token in query:
		if token in query_dict:
			query_dict[token] += 1
		else:
			query_dict[token] = 1
	return query_dict

#######################################################################
# Evaluation
#######################################################################

def evaluate(query):
	master = {}
	for q in query:
		postings = lookup(q)
		master = merge(master, postings, q)
	# master dict is now of the following structure:
	# {
	#    docID1: {token1: tf1, token2: tf2, ...}
	#    ...
	# }
	
	top = []
	for doc in master:
		# candidate is a tuple (cosine similarity score, docID)
		candidate = (- cos_sim(query, master[doc], DOC_LENGTHS[doc]), doc)
		heapq.heappush(top, candidate)

	result = []
	while top and len(result) < 20:
		candidate = heapq.heappop(top)
		result.append(candidate)
	sorted(result,  cmp=compare)
	return [x[1] for x in result[:10]]

# sort the candidates first by score, then by docID
def compare(doc1, doc2):
	if (doc1[0] == doc2[0]):
		return int(doc1[1]) - int(doc2[1])
	elif doc1[0] < doc2[0]:
		return -1
	elif doc1[0] < doc2[0]:
		return 0
	else:
		return 1

# cosine similarity caocluated by ltc.lnc
# note that doc_length is computed during indexing
# for better performance in normalisation
def cos_sim(query, doc, doc_length):
	dot_product = 0
	q_sum_of_sqr = 0
	for token, q_rawtf in query.iteritems():
		q_w = float(1) + math.log(q_rawtf, 10)
		if token not in doc:
			d_w = 0
		else:
			d_tf = float(1) + math.log(doc[token], 10)
			d_df = freq(token)
			d_idf = math.log(float(COLLECTION_SIZE) / d_df, 10) if d_df != 0 else 1
			d_w = d_tf*d_idf
		dot_product += q_w * d_w
		q_sum_of_sqr += q_w ** 2
	return float(dot_product) / doc_length / math.sqrt(q_sum_of_sqr)

#######################################################################
# Set operations
#######################################################################

def merge(master, second, token):
	"""
	merge a second postings into the master postings list
	"""
	
	for doc, tf in second.iteritems():
		if doc in master:
			master[doc][token] = tf
		else:
			master[doc] = {token: tf}
	return master

#######################################################################
# Utilities
#######################################################################

# return the size of the postings for a given token
def freq(word):
	if word in dictionary:
		return dictionary[word]['freq']
	else:
		return 0

def lookup(word):
	if word in dictionary:
		postings_file.seek(dictionary[word]['start'])
		raw = postings_file.read(dictionary[word]['size'])
		return json.loads(raw)
	else:
		return {}

stemmer = PorterStemmer()
# case folding, stemming
def normalise_word(word):
	return stemmer.stem(word.lower())

def usage():
    print "usage: " + sys.argv[0] + " -d dictionary-file -p postings-file -q file-of-queries -o output-file-of-results"

#######################################################################
# Main
#######################################################################

try:
    opts, args = getopt.getopt(sys.argv[1:], 'd:p:q:o:')
except getopt.GetoptError, err:
    usage()
    sys.exit(2)
QUERY_DIR = DICT_DIR = POSTING_DIR = OUT_DIR = None
for o, a in opts:
    if o == '-q':
        QUERY_DIR = a
    elif o == '-o':
    	OUT_DIR = a
    elif o == '-d':
        DICT_DIR = a
    elif o == '-p':
        POSTING_DIR = a
    else:
        pass # no-op
if QUERY_DIR == None or DICT_DIR == None or POSTING_DIR == None or OUT_DIR == None:
    usage()
    sys.exit(2)

out_file = file(OUT_DIR, 'w')
dict_file = file(DICT_DIR, 'r')
dictionary = {}
for line in dict_file:
	# format: token freq start_pos end_pos
	data = line.split()
	dictionary[data[0]] = {
		'freq':  int(data[1]),
		'start': int(data[2]),
		'size':   int(data[3]) - int(data[2])
	}

dict_file.close()
postings_file = file(POSTING_DIR, 'r')
DOC_LENGTHS = json.loads(postings_file.readline())
COLLECTION_SIZE = len(DOC_LENGTHS)

search()

out_file.close()
postings_file.close()