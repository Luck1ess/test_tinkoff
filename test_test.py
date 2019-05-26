import requests
import pytest

url1 = 'https://api.tinkoff.ru/api/search/fulltext?context=travel&version=1.3'
url2 = 'https://api.tinkoff.ru/travel/api/flight/search'

def make_params_1(text, searchTypes=["country", "city", "airport"]):
    return {"searchTypes": searchTypes, "text":text}

def segment(From, to, date):
    return {"from": From, "to": to, "date": date}

def make_params_2(flights, adults=1, infants=0, children=0, cabin="Y"):
    segments = []
    for i in range(len(flights)):
        segments.append(segment(flights[i][0], flights[i][1], flights[i][2]))
    return {"segments" : segments, "passengers": {"adults": adults, "infants": infants, "children": children}, "cabin": cabin}
#cabin:"F" - первый класс, cabin: "C" - бизнес класс, cabin: "Y" - эконом


@pytest.mark.parametrize('text', ['', 'USA', 'wednjcfk', 'domo', 'москва'])
@pytest.mark.parametrize('searchTypes', [["country","city","airport"], ["city","airport"], ["country","airport"]
	,["country","city"], ["country"], ["city"], ["airport"]])
def test_connection1(text, searchTypes):
	r = requests.post(url1, json=make_params_1(text, searchTypes))
	assert r.status_code == 200 
	r.close()


@pytest.mark.parametrize('adults', [1, 2])
@pytest.mark.parametrize('children', [0, 1])
@pytest.mark.parametrize('infants', [0, 1])
@pytest.mark.parametrize('cabin', ["Y", "C", "F"])
@pytest.mark.parametrize('city1', ['DME', 'ZRH'])
@pytest.mark.parametrize('city2', ['NYC'])
@pytest.mark.parametrize('city3', ['TYO'])
def test_connection2(adults, children, infants, cabin, city1, city2, city3):
	r = requests.post(url2, json=make_params_2([[city1, city2, '2019-06-06'], [city2, city3, '2019-06-07']], adults = adults, children = children, infants = infants, cabin = cabin))
	assert r.status_code == 200 
	r.close()


@pytest.mark.parametrize('text', ['', 'USA', 'wednjcfk', 'domo', 'москва'])
@pytest.mark.parametrize('searchTypes', [["country","city","airport"], ["city","airport"], ["country","airport"]
	,["country","city"], ["country"], ["city"], ["airport"]])
def test_is_json1(text, searchTypes):
	r = requests.post(url1, json=make_params_1(text, searchTypes))
	try:
		r.json()
	except ValueError:
		assert False
	assert True


@pytest.mark.parametrize('adults', [1, 2])
@pytest.mark.parametrize('children', [0, 1])
@pytest.mark.parametrize('infants', [0, 1])
@pytest.mark.parametrize('cabin', ["Y", "C", "F"])
@pytest.mark.parametrize('city1', ['DME', 'ZRH'])
@pytest.mark.parametrize('city2', ['NYC'])
@pytest.mark.parametrize('city3', ['TYO'])
def test_is_json2(adults, children, infants, cabin, city1, city2, city3):
	r = requests.post(url2, json=make_params_2([[city1, city2, '2019-06-06'], [city2, city3, '2019-06-07']], adults = adults, children = children, infants = infants, cabin = cabin))
	try:
		m = r.json()
	except ValueError:
		assert False
	assert True


@pytest.mark.parametrize('text', ['', 'USA', 'wednjcfk', 'domo', 'москва'])
@pytest.mark.parametrize('searchTypes', [["country","city","airport"], ["city","airport"], ["country","airport"]
	,["country","city"], ["country"], ["city"], ["airport"]])
def test_params_1(text, searchTypes):
	keys1 = ['payload', 'trackingId', 'time', 'status']
	keys2 = ['tookInMillis', 'hitsCount', 'sortedByScoreObjects', 'suggests']
	keys3 = ['highlights', 'score', 'objectType', 'objectSource']
	keys31 = ['field', 'value']
	keys4 = ['coordinates', 'name', 'scoring', 'code', 'country_code', 'city_name', 'type', 'city_code', 'country_name']
	keys41 = ['lat', 'lon']
	keys42 = ['ru', 'en']
	keys43 = ['importance', 'traffic', 'countryImportance']
	r = requests.post(url1, json=make_params_1(text, searchTypes))
	j = r.json()
	for i in keys1:
		if i not in j.keys():
			assert False
	j1 = j['payload']
	for i in keys2:
		if i not in j1.keys():
			assert False
	j2 = j1['sortedByScoreObjects']
	if len(j2) > 0:
		for i in j2:
			for v in keys3:
				if v not in i.keys():
					assert False
			if len(i['highlights']) > 0:
				j22 = i['highlights'][0]
				for v in keys31:
					if v not in j22.keys():
						assert False
			j3 = i['objectSource']
			for v in keys4:
				if v not in j3.keys():
					assert False
			j31 = j3['coordinates']
			for v in keys41:
				if v not in j31.keys():
					assert False
			j32 = j3['name']
			j321 = j3['city_name']
			j322 = j3['country_name']
			for v in keys42:
				if v not in j32.keys() or v not in j321.keys() or v not in j322.keys():
					assert False
			j33 = j3['scoring']
			for v in keys43:
				if v not in j33.keys():
					assert False
	assert True


def test_lang_1():
	r1 = requests.post(url1, json=make_params_1('Москва'))
	r2 = requests.post(url1, json=make_params_1('Moscow'))
	f1 = False
	f2 = True
	k1 = 0
	k2 = 0
	j1 = r1.json()
	j2 = r2.json()
	for i in j1['payload']['sortedByScoreObjects']:
		if i['objectSource']['city_name']['en'] == 'Moscow':
			f1 = True
			k1+=1
	for i in j2['payload']['sortedByScoreObjects']:
		if i['objectSource']['city_name']['ru'] == 'Москва':
			f2 = True
			k2+=1
	assert f1 == f2 and k1 == k2


@pytest.mark.parametrize('adults', [1, 2])
@pytest.mark.parametrize('children', [0, 1])
@pytest.mark.parametrize('infants', [0, 1])
@pytest.mark.parametrize('cabin', ["Y", "C", "F"])
@pytest.mark.parametrize('city1', ['DME', 'ZRH'])
@pytest.mark.parametrize('city2', ['NYC'])
@pytest.mark.parametrize('city3', ['TYO'])
def test_params_2(adults, children, infants, cabin, city1, city2, city3):
	keys1 = ['trackingId', 'responseTimeMs', 'time', 'status', 'detachKey', 'payload']
	keys2 = ['offers', 'flights', 'info']
	keys3 = ['uuid', 'price', 'flights', 'alliance', 'price_per_pax', 'validating_carrier', 'refundable']
	keys31 = ['amount', 'currency']
	keys4 = ['flight_segments', 'duration']
	keys41 = ['number', 'duration', 'vehicle', 'availability', 'cabin', 'booking_class', 'ancillary_services', 'carriers', 'departure', 'baggage', 'arrival', 'technical_stops']
	keys42 = ['operating', 'marketing']
	keys43 = ['city', 'airport', 'terminal', 'time']
	keys44 = ['count', 'baggage']
	keys45 = ['amount', 'unit_desc']
	keys46 = ['city', 'airport', 'terminal', 'time']
	keys5 = ['carrierNames', 'vehicleNames', 'cities', 'airportNames']
	r = requests.post(url2, json=make_params_2([[city1, city2, '2019-06-06'], [city2, city3, '2019-06-07']], adults = adults, children = children, infants = infants, cabin = cabin))
	j1 = r.json()
	for i in keys1:
		if i not in j1.keys():
			assert False
	j2 = j1['payload']
	for i in keys2:
		if i not in j2.keys():
			assert False
	j3 = j2['offers']
	if len(j3) > 0:
		for j in j3:
			for i in keys3:
				if i not in j.keys():
					assert False
			for i in keys31:
				if i not in j['price'].keys():
					assert False
			j31 = j['price_per_pax']
			for i in keys31:
				if i not in j31['adult'].keys():
					assert False
			if children > 0:
				for i in keys31:
					if i not in j31['child'].keys():
						assert False
			if infants > 0:
				for i in keys31:
					if i not in j31['infant'].keys():
						assert False
	j4 = j2['flights']
	if len(j4) > 0 :
		for j in j4:
			for i in keys4:
				if i not in j.keys():
					assert False
			u = j['flight_segments']
			if len(u)>0:
				for seg in u:
					for i in keys41:
						if i not in seg.keys():
							assert False
					for i in keys42:
						if i not in seg['carriers'].keys():
							assert False
					for i in keys43:
						if i not in seg['departure'].keys():
							assert False
					if len(seg['baggage']) > 0:
						for bag in seg['baggage']:
							for i in keys44:
								if i not in bag.keys():
									assert False
							for i in keys45:
								if i not in bag['baggage'].keys():
									assert False
					for i in keys46:
						if i not in seg['arrival'].keys():
							assert False
	j5 = j2['info']
	for i in keys5:
		if i not in j5.keys():
			assert False
























