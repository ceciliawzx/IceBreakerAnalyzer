import pycountry


# Manually defined countries dict
countries_dict = {
    'uk': 'United Kingdom',
    'england': 'United Kingdom',
    'britain': 'United Kingdom',
    'scotland': 'United Kingdom',
    'wales': 'United Kingdom',
    'northern ireland': 'United Kingdom',

    'us': 'United States',
    'usa': 'United States',
    'america': 'United States',

    'south korea': 'South Korea',
    'north korea': 'North Korea',
    'korea': 'South Korea',

    'vietnam': 'Viet Nam',

    'moldova': 'Moldova, Republic of',

    'macedonia': 'North Macedonia',

    'czech republic': 'Czechia',
    'czechia': 'Czech Republic',

    'uae': 'United Arab Emirates',

    'the netherlands': 'Netherlands',
    'holland': 'Netherlands',

    'burma': 'Myanmar',
    'myanmar': 'Myanmar',  # Allowing for both common names

    'ivory coast': 'Côte d\'Ivoire',
    'cote d\'ivoire': 'Côte d\'Ivoire',  # Allowing for common French and English names

    'eswatini': 'Eswatini',
    'swaziland': 'Eswatini',  # Country name changed to Eswatini

    'east timor': 'Timor-Leste',
    'timor-leste': 'Timor-Leste',  # Allowing for both common names

    'falkland islands': 'Falkland Islands (Malvinas)',
    'malvinas': 'Falkland Islands (Malvinas)',  # Allowing for both common names

    'caboverde': 'Cabo Verde',
    'cape verde': 'Cabo Verde',
}


def normalize_country_name(name):
    # Attempt to directly match the country with pycountry
    for country in pycountry.countries:
        if name.lower() in (country.name.lower(), country.alpha_2.lower(), country.alpha_3.lower()):
            return country.name

    # If no direct match, check the special cases
    return countries_dict.get(name.lower(), name)
