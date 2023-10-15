import requests
from bs4 import BeautifulSoup
import datetime

places = [
	'Half-Moon-Bay-California',
	'Huntington-Beach',
	'Providence-Rhode-Island',
	'Wrightsville-Beach-North-Carolina'
]
today = datetime.datetime.today().strftime("%Y-%m-%d")

def convert_datetime(time):
	'''
	Input = string of time e.g. '4:07pm'
	Todays date is appended to input
	Output = returns a datetime object 
	'''
	try:
		date_time = ' '.join([str(today), time])
		format = '%Y-%m-%d %I:%M%p'
	except:
		print('error=convert_datetime')

	return datetime.datetime.strptime(date_time, format)


def get_tide_payload(place):
	'''
	Get website payload
	Output = str
	'''
	try:
		url = f'https://www.tide-forecast.com/locations/{place}/tides/latest'
		page = requests.get(url)
		soup = BeautifulSoup(page.content, 'html.parser')
		results = soup.find('p', class_='tide-header-summary')
		if results:
			pass
	except:
		print(f"error=get_tide_payload: There were no results for {place}")

	return results.prettify()


def prep_tide_times(raw_times):
	'''
	Input = string of payload from tide site
	Output = list of strings
	'''
	try:
		times = raw_times \
			.strip('<p class="tide-header-summary">\n ') \
			.replace('.',',') \
			.split(',')[:-1]
	except:
		print('error=prep_tide_times: There was a problem with the site payload')

	return times


def times_to_dict(times):
	'''
	Input = list of strings
	Output = dict of time(datetime object) and height of tide(str)
	sample: {datetime.datetime(2023, 10, 13, 4, 14): 'low', 
			datetime.datetime(2023, 10, 13, 10, 31): 'high',
			}
	'''
	try:
		tide_times = [convert_datetime(i[-7:]) for i in times[:-1]]
		hi_lo_dict = {}
		if times:
			for t in range(len(times)):
				if 'low' in times[t]:
					hi_lo_dict[tide_times[t]] = 'low'
				elif 'high' in times[t]:
					hi_lo_dict[tide_times[t]] = 'high'
	except:
		print('error=times_to_dict there was an error creating tide_dict')
	
	return hi_lo_dict


def get_daylight_times(raw_times):
	'''
	Calculates sunrise and sunset 
	Output = list of datetime objects
	'''
	try:
		daylight_times = raw_times[-1].split(' and ')
		sunrise = convert_datetime(daylight_times[0][-7:])
		sunset = convert_datetime(daylight_times[1][-7:])
	except:
		print('error=get_daylight_times there was error getting daylight_times')
		
	return [sunrise, sunset]


def main_get_daylight_times_and_heights(places):
	# Return daylight times and heights
	for place in places:
		print('#######################')
		print(f'For location: {" ".join(place.split("-"))}')
		print('The tides during daylight hours were:')
		tide_site_payload = get_tide_payload(place)
		prepped_payload = prep_tide_times(tide_site_payload)
		tide_dict = times_to_dict(prepped_payload)
		daylight_times = get_daylight_times(prepped_payload)
		sunrise = daylight_times[0]
		sunset = daylight_times[1]
		results = {}
		if tide_dict:
			for k, v in tide_dict.items():
				if sunrise <= k <= sunset:
					results[k] = v
			if results:
				for k, v in results.items():
					print(f'A {v} tide at {k.time()}')
			else:
				print('Error: There were no tides during daylight hours.')
		else:
			print(f'Error: There was no tide data for {place}')


main_get_daylight_times_and_heights(places)









