import time
from typing import Dict
import requests
import sys


BANNER_SEARCH_URL = "https://api.criminalip.io/v1/banner/search"
CRIMINALIP_API_KEY = "<YOUR_API_KEY>"
outfile = "result.txt"

def criminalip_banner_search_one(query:str, offset:int=0)-> Dict:
	params = {"query": query, "offset": offset}
	headers = {"x-api-key": CRIMINALIP_API_KEY}
	response = requests.get(BANNER_SEARCH_URL, headers=headers, params=params)

	print(response.json())
	return response.json()

def criminalip_banner_search_all(query:str, maximum:int)-> Dict:
	response = criminalip_banner_search_one(query=query, offset=0)
	
	if response['status'] == 200:
		answer = response['data']
		cnt = response['data']['count']
		for i in range(10,min(cnt,maximum),10):
			response = criminalip_banner_search_one(query=query, offset=i)
			if response['status'] == 400:
				break
			answer['result'] += response['data']['result']
		
		answer['result'] = answer['result'][:min(len(answer['result']),maximum)]
		print(answer)
		return answer
	else:
		print(f"API Status:{response['status']}")
		return {'count': 0, 'filters': {}, 'invalid_filters': [], 'result': []}

def criminalip_eyes():
	query = input("\n[+] Enter your Criminal IP Query : ")
	maximum = int(input("\n[+] Enter maximum number of result : "))
	
	try:
		results = criminalip_banner_search_all(query, maximum)
		
		with open(outfile, "a", encoding='utf-8') as f:
			if results["count"] > 0:
				f.write("\nTotal record found		: {}".format(results["count"]) + "\n")
				
			for i, result in enumerate(results["result"]):
				f.write("+" * 60 + "\n")
				f.write("\n[=] Result: {}. Search query: {}".format(i, query) + "\n")
				f.write("[+] IP		   : {}".format(result["ip_address"]) + "\n")
				f.write("[+] Port		 : {}".format(result["open_port_no"]) + "\n")
				f.write("[+] Organization : {}".format(result["org_name"]) + "\n")
				f.write("[+] AS Name	  : {}".format(result["as_name"]) + "\n")
				f.write("[+] Location	 : {}, {}".format(result["country"], result["city"]) + "\n")
				f.write("[+] Hostname	 : {}".format(result["hostname"]) + "\n")
				f.write("[+] Product	  : {}, {}".format(result["product"], result["product_version"]) + "\n")
				f.write("[+] Score In	 : {}".format(result["score"]) + "\n")
				f.write("[+] Score Out	: {}".format(result["score_out"]) + "\n")
				f.write("[+] Socket Type  : {}".format(result["socket_type"]) + "\n")
				f.write("[+] SSL Expired  : {}".format(result["ssl_expired"]) + "\n")
				
				f.write("[+] Collected on : {}".format(result["scan_dtime"]) + "\n")
				f.write("[+] Banner	   : \n\n" + (result["banner"]))
				f.flush()
			
			f.write("+" * 60 + "\n")
			f.write("\nTotal record printed : {}".format(results["count"]) + "\n")

	except KeyboardInterrupt:
		print ("\n")
		print ("\033[1;91m[!] User Interruption Detected..!\033[0")
		time.sleep(0.5)
		print ("\n\n\t\033[1;91m[!] ByeBye\033[0m\n\n")
		time.sleep(0.5)
		sys.exit(1)
	



if __name__ == "__main__":
	criminalip_eyes()