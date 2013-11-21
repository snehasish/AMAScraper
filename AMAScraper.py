"""
AMA Scraper - Written to scrape proper Q and A from the Intel AMA
Date : 27 December 2012
Author : Snehasish Kumar

Distributed under The MIT License (MIT)
"""

import praw


# Globals
op          = 'jecb'
posturl     = 'http://www.reddit.com/r/IAmA/comments/15iaet/iama_cpu_architect_and_designer_at_intel_ama/'
tabcount    = 1
fname       = 'intel-ama.md'
f 			= None

def tabs():
	""" Return tabs """
	global tabcount
	return '\t'*tabcount

def didOPReply(cm):
	""" Check replies to argument comment to see if OP has replied """
	if len(cm.replies) > 0:
		for r in cm.replies:
			if r.author:
				if r.author.name == op:
					return True
	return False

def getOPReply(cm):
	""" Return OP's reply """
	for r in cm.replies:
		if r.author.name == op:
			return r

def ParseComments(cm):
	""" Parse the comment and write to a file """
	global tabcount

	# Write Question and Response to file if OP replies
	if didOPReply(cm):
		f.write(tabs() + 'Question\n' + tabs() + formatCommentBody(cm.body) + '\n\n')
		f.write(tabs() + 'Answer\n' + tabs() + formatCommentBody(getOPReply(cm).body) + '\n\n')

		tabcount = tabcount + 1
		# Recusively look for followup questions
		for y in getOPReply(cm).replies:
			ParseComments(y)
		tabcount = tabcount - 1
	


def formatCommentBody(cmb):
	""" Replace the newline with newline + # tabs for proper formatting, also replace html encodes """
	return u''.join(cmb).encode('utf-8').replace('\n','\n'+'\t'*tabcount).replace('&gt;','>').replace('&amp;','&')

def main():
	""" Set proper user_agent variable and run """
	global f
	reddit = praw.Reddit(user_agent='IntelAMA_Comment_Pull by A Grad Student')
	submission = reddit.get_submission(url=posturl)

	# Get all comments takes time as it is throttled by PRAW to conform to Reddit guidelines
	forest_comments = submission.all_comments
	f = open(fname,'w')

	for x in forest_comments:
		ParseComments(x)
		if didOPReply(x):
			# Draw a delimiter
			f.write(tabs() + '='*80 +'\n\n')
	
	f.close()


if __name__ == "__main__":
    main()
