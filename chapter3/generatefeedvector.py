import feedparser
import re

# Returns title and dictionary of word counts for an RSS feed
def getwordcounts(url):
	# Parse the feed
	print 'Download: ', url
	d = feedparser.parse(url)

	if not hasattr(d, 'feed') and hasattr(d.feed, 'title'):
		print 'Fail:'
		return '',{}

	wc={}

	# Loop over all the entries
	for entry in d.entries:
		if 'summary' in entry: summary=entry.summary
		else: summary=entry.description

		# Extract a list of words
		words = getwords(entry.title + ' ' + summary)
		for word in words:
			wc.setdefault(word,0)
			wc[word]+=1

	return d.feed.title, wc

def getwords(html):
	# Remove all the HTML tags
	txt=re.compile(r'<[^>]+>').sub('',html)

	# Split words by all non-alpha characters
	words=re.compile(r'[^A-Z^a-z]+').split(txt)

	# Convert to lowercase
	return [word.lower() for word in words if word!='']

#testUrl = 'https://www.reddit.com/r/pics.rss'
#getwordcounts(testUrl)

def main():
	apcount={}
	wordcounts={}
	feedlist=[]
	for i, feedurl in enumerate(file('feedlist.txt')):
		if feedurl != '':
			feedlist.append(feedurl)

	for i, feedurl in enumerate(feedlist):
		try:
			print 'Loadng: ', i, ' : ', feedurl
			title, wc = getwordcounts(feedurl)
			wordcounts[title]=wc
			for word, count in wc.items():
				apcount.setdefault(word, 0)
				if count > 1:
					apcount[word] += 1
			print 'OK'
		except:
			print 'Fail'
			feedlist.remove(feedurl)

	wordlist=[]
	for w, bc in apcount.items():
		frac=float(bc)/len(feedlist)
		if frac>0.1 and frac<0.5: wordlist.append(w)

	print wordlist
	out=file('blogdata.txt','w')
	out.write('Blog')
	for word in wordlist: out.write('\t%s' % word)
	out.write('\n')
	for blog,wc in wordcounts.items():
		out.write(blog.encode('utf8'))
		for word in wordlist:
			if word in wc: out.write('\t%d' % wc[word])
			else: out.write('\t0')
		out.write('\n')

main()