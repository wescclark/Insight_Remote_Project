import re
import nltk
from nltk.corpus import stopwords

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pickle
import requests
import io
import base64

punctuation = '!"#?$%“”&\'()’*+,—./:;<=>@[\\]^_`{|}~…' 
stoplist = stopwords.words('english')

api_key = 'AIzaSyBc2-0Wh_JJXbsnyGlv_3uG-c-BK7_i8Pk'

def dict_replace(dictionary, key):
    return(dictionary[key])

def processText(text):
    #text = [item for item in text]
    processed = text.lower()
    processed = ''.join(word for word in processed
                    if word not in punctuation)
    processed = re.sub(r' +', " ", processed).strip()
    return processed

def removeStopwords(text):
    #text = [item for item in text]
    removed = text.lower().split()
    removed = ' '.join(word for word in removed
                      if word not in stoplist)
    removed = re.sub(r' +', " ", removed).strip()
    return removed

def ModelIt(video_id  = 'dQw4w9WgXcQ'):
	with open('RF_CLF_50est_50dim.p', 'rb') as pickle_file:
		rf_clf = pickle.load(pickle_file)
	with open('svd_model.p', 'rb') as pickle_file:
		svd = pickle.load(pickle_file)
	with open('tfidf_model.p', 'rb') as pickle_file:
		tfidf = pickle.load(pickle_file)
	with open('knn_reg.p','rb') as pickle_file:
		knn_reg = pickle.load(pickle_file)
		print('done')
	with open('country_dict.p','rb') as pickle_file:
		country_dict = pickle.load(pickle_file)
	
		
		r = requests.get('https://www.googleapis.com/youtube/v3/videos?part=snippet%2CcontentDetails%2Cstatistics&id=' + video_id + '&key='+api_key)
		data_json = r.json()
		
		string = ''
		for i in data_json['items'][0]['snippet']['tags']:
			temp = i + ' '
			string += temp
		
		string = processText(removeStopwords(string))
		string_list = []
		string_list.append(string)
		
		tag_desc = tfidf.transform(string_list)
		new_tag_svd_tfidf = svd.transform(tag_desc)
		demo_data = rf_clf.predict(new_tag_svd_tfidf)
		
		country_demo = knn_reg.predict(new_tag_svd_tfidf)
		arr = np.argsort(country_demo[0])[::-1][:4]
		country_string = ''
		total = 100
		for i in arr:
			country_string += dict_replace(country_dict,i)+':\t'+str("{0:.2f}".format(country_demo[0][i]*100)) + ',   '
			total -= country_demo[0][i]*100
		country_string += 'The rest' + ':\t' + str("{0:.2f}".format(total)) + '.'
		
		img = io.BytesIO()
		

		N = 7
		men_means = demo_data[0][:7]
		women_means = demo_data[0][7:]

		ind = np.arange(N)  # the x locations for the groups
		width = 0.35       # the width of the bars

		fig, (ax1,ax2) = plt.subplots(1,2, figsize = (13,6))
		
		labels = 'Male', 'Female'
		colors = 'b','darkorange'
		sizes = [np.sum(demo_data[0][:7]), np.sum(demo_data[0][7:])]
		explode = (.1, .1)  # only "explode" the 2nd slice (i.e. 'Hogs')
		
		pie = ax1.pie(sizes, labels=labels, colors = colors, explode=explode, shadow=True, autopct='%1.1f%%')


		#plt.pie(sizes, explode=explode , colors = colors, shadow=True, startangle=90)
		#ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

		#ax1.legend(pie[0], labels, prop={'size':12})
		#plt.legend(loc='best')




		rects1 = ax2.bar(ind, men_means, width, color='b', )

		#women_means = (25, 32, 34, 20, 25)
		women_std = (3, 5, 2, 3, 3)
		rects2 = ax2.bar(ind + width, women_means, width, color='darkorange', )

		ax2.spines['top'].set_visible(False)
		ax2.spines['right'].set_visible(False)
		ax2.spines['bottom'].set_visible(True)
		ax2.spines['left'].set_visible(False)

		# add some text for labels, title and axes ticks
		ax2.set_ylabel('Percent',fontsize=15)
		ax2.set_title('Age Demographics',fontsize = 15)
		#ax.set_ylim([0,25])
		ax2.set_xticks(ind + width / 2)
		ax2.set_xticklabels(('13-17', '18-24', '25-34', '35-44', '45-54', '55-64', '65-'),fontsize=13)
		ax2.legend((rects1[0], rects2[0]), ('Male', 'Female'),fontsize=12)
		
		#plt.subplots_adjust(left=0.05, right=0.95, bottom=0.05, top=1.05)
		plt.tight_layout()
		#plt.savefig(img, format='png')
		plt.savefig(img, format='png', bbox_inches='tight')
		img.seek(0)
		img_png = img.getvalue()
		plot_url = base64.b64encode(img_png)
		
	return(string, plot_url.decode('utf-8'),country_string)
	
	
