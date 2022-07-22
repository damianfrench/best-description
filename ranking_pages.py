def main():#outputs a list of urls ranking them from best to worst in order of how good their descriptions are
	from urllib.request import urlopen
	import json
	import textAnalysis
	pages=[]
	for x in range(1,10):
		url="https://cdn.thomascook.com/search/1.60/uk/en-gb/accommodation/1/{}".format(x)
		response=urlopen(url)
		data_json = json.loads(response.read())
		name=data_json["name"]
		value,summary=textAnalysis.main(data_json)
		pages.append([value,x,summary,name])
	pages.sort()
	print("worst to best:\n")
	for x in range(len(pages)):
		print("https://cdn.thomascook.com/search/1.60/uk/en-gb/accommodation/1/{}".format(pages[x][1])," - ",pages[x][3]," - ",pages[x][0])
		# print(pages[x][2])




if __name__=="__main__":
	main()
