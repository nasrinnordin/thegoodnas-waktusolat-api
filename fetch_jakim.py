import urllib.request
import json
import os

# Senarai penuh 60 Zon JAKIM
zones = [
    "JHR01", "JHR02", "JHR03", "JHR04",
    "KDH01", "KDH02", "KDH03", "KDH04", "KDH05", "KDH06", "KDH07",
    "KTN01", "KTN02", "MLK01",
    "NGS01", "NGS02", "NGS03",
    "PHG01", "PHG02", "PHG03", "PHG04", "PHG05", "PHG06", "PHG07",
    "PLS01", "PNG01",
    "PRK01", "PRK02", "PRK03", "PRK04", "PRK05", "PRK06", "PRK07",
    "SBH01", "SBH02", "SBH03", "SBH04", "SBH05", "SBH06", "SBH07", "SBH08", "SBH09",
    "SGR01", "SGR02", "SGR03",
    "SWK01", "SWK02", "SWK03", "SWK04", "SWK05", "SWK06", "SWK07", "SWK08", "SWK09",
    "TRG01", "TRG02", "TRG03", "TRG04",
    "WLY01", "WLY02"
]

def format_ampm(time_24):
    h, m = map(int, time_24.split(':'))
    period = "pm" if h >= 12 else "am"
    h_12 = h - 12 if h > 12 else h
    h_12 = 12 if h_12 == 0 else h_12
    return f"{h_12}:{m:02d} {period}"

headers = {'User-Agent': 'Mozilla/5.0'}

for zone in zones:
    url = f"https://www.e-solat.gov.my/index.php?r=esolatApi/TakwimSolat&period=year&zone={zone}"
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode('utf-8'))
            
            formatted_data = []
            for item in data['prayerTime']:
                formatted_data.append({
                    "Tarikh Miladi": item["date"],
                    "Imsak": format_ampm(item["imsak"][:5]),
                    "Subuh": format_ampm(item["fajr"][:5]),
                    "Zohor": format_ampm(item["dhuhr"][:5]),
                    "Asar": format_ampm(item["asr"][:5]),
                    "Maghrib": format_ampm(item["maghrib"][:5]),
                    "Isyak": format_ampm(item["isha"][:5])
                })
            
            with open(f"{zone}.json", "w") as f:
                json.dump(formatted_data, f, indent=2)
            
            print(f"Berjaya ditarik: {zone}")
    except Exception as e:
        print(f"Ralat untuk {zone}: {e}")
