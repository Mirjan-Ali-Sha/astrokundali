import os, json
import numerology.core as core  # assuming our code is in core.py

def test_numerology_profile():
    # Sample input: name and birthdate
    first_name = "John"
    last_name = "Doe"
    birthdate = "2000-01-01"

    # Calculate life path number
    life_num = core.calculate_life_path(birthdate)
    assert life_num == 4  # 2+0+0+0+1+1 = 4

    # Load life_path.json for interpretation
    fn = os.path.join(os.path.dirname(core.__file__), "data", "life_path.json")
    with open(fn, 'r') as f:
        life_data = json.load(f)
    life_text = life_data["life_path"].get(str(life_num), "")
    print(f"Life Path {life_num}: {life_text}")

    # Calculate destiny number
    full_name = first_name + last_name
    destiny_num = core.calculate_destiny(full_name)
    # Example: J(1)+O(6)+H(8)+N(5)+D(4)+O(6)+E(5) = 35 -> 3+5 = 8
    assert destiny_num == 8

    # Load destiny.json for interpretation
    fn = os.path.join(os.path.dirname(core.__file__), "data", "destiny.json")
    with open(fn, 'r') as f:
        dest_data = json.load(f)
    dest_text = dest_data["destiny"].get(str(destiny_num), "")
    print(f"Destiny {destiny_num}: {dest_text}")

    # Basic checks (interpretation strings should be non-empty)
    assert life_text != ""
    assert dest_text != ""


from astrokundali import AstroData, AstroChart, plot_kundali, houses_to_json

raw = AstroData(
  1997,3,12,22,5,0, 5,30, 22.8389605,87.9410503, ayanamsa="lahiri" 
).get_rashi_data()

chart = AstroChart(raw, house_system="equal")
houses = chart.build()

plot_kundali(houses)
print(houses_to_json(houses))

# test_numerology_profile()
from .astro_data import AstroData

# Build raw data
data = AstroData(2009,3,30,9,36,0, 5,30, 19.0760,72.8777, ayanamsa='lahiri')
raw   = data.get_rashi_data()

# Create and compute chart
chart  = AstroChart(data, house_system='porphyry')
houses = chart.compute()

# Plot & export JSON
plot_kundali(houses)
print(houses_to_json(houses))

from astrokundali import AstroData, AstroChart, plot_kundali

data   = AstroData(1997,3,12,22,5,0, 5,30, 22.8389605,87.9410503, ayanamsa='lahiri')
chart  = AstroChart(data, house_system='whole_sign')
houses = chart.compute()
plot_kundali(houses)


# plot_lagna_chart, plot_moon_chart, plot_hora_chart,
# plot_drekkana_chart, plot_chaturthamsha_chart, plot_saptamamsha_chart, plot_dashamamsha_chart,
# plot_dwadashamsha_chart, plot_nakshatra_chart, plot_vimshamsha_chart, plot_shashtiamsha

# from astrokundali import match_kundli            
# from astrokundali import AstroData
# A = AstroData(1990,1,1,10,0,0,5,30,19.07,72.88)  
# B = AstroData(1992,6,15,16,30,0,5,30,28.61,77.23)
# result = match_kundli(A, B)
# result_summary = pprint(result)
# pprint(result)
# import pandas as pd
# df = pd.DataFrame(result['table'])
# print(df)

# sign_numbers --sign names --planet names
# 1 --Aries (Mesh) --Mars (Mongol)
# 2 --Taurus (Vrishabh) --Venus (Shukra)
# 3 --Gemini (Mithun) --Mercury (Budh)
# 4 --Cancer (Kark) --Moon (Chandra)
# 5 --Leo (Simha) --Sun (Surya)
# 6 --Virgo (Kanya) --Mercury (Budh)
# 7 --Libra (Tula) --Venus (Shukra)
# 8 --Scorpio (Vrishchik) --Mars (Mongol)
# 9 --Sagittarius (Dhanu) --Jupiter (Brihaspati)
# 10 --Capricorn (Makar) --Saturn (Shani)
# 11 --Aquarius (Kumbh) --Saturn (Shani)
# 12 --Pisces (Meen) --Jupiter (Brihaspati)

# Planet_Names --Planet drishti
# 1 --Sun (Surya) --7
# 2 --Moon (Chandra) --7
# 3 --Mars (Mangal) --4, 7, 8
# 4 --Mercury (Budh) --7
# 5 --Jupiter (Brihaspati) --5, 7, 9
# 6 --Venus (Shukra) --7
# 7 --Saturn (Shani) --3, 7, 10
# 8 --Rahu (Rahu) --5, 7, 9
# 9 --Ketu (Ketu) --5, 7, 9