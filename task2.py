#Task-2: print a dictionary as key=>value format
cities = {
    'New York': 'United States',
    'Paris': 'France',
    'Tokyo': 'Japan',
    'Sydney': 'Australia',
    'London': 'United Kingdom',
    'Rome': 'Italy',
    'Cairo': 'Egypt',
    'Rio de Janeiro': 'Brazil',
    'Beijing': 'China',
    'Moscow': 'Russia'
}

for key, value in cities.items():
    print(key + ' => ' + value)
