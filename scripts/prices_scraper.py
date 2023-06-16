import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import os
import time

csgo_weapons = [
    "Glock-18",
    "P2000",
    "USP-S",
    "Dual Berettas",
    "P250",
    "Tec-9",
    "Five-SeveN",
    "CZ75-Auto",
    "Desert Eagle",
    "R8 Revolver",
    "Nova",
    "XM1014",
    "Sawed-Off",
    "Mag-7",
    "M249",
    "Negev",
    "MAC-10",
    "MP9",
    "MP7",
    "MP5-SD",
    "UMP-45",
    "P90",
    "PP-Bizon",
    "Galil AR",
    "FAMAS",
    "AK-47",
    "M4A4",
    "M4A1-S",
    "SSG 08",
    "SG 553",
    "AWP",
    "G3SG1",
    "SCAR-20",
    "SSG 08",
    "Navaja Knife",
    "Stiletto Knife",
    "Talon Knife",
    "Ursus Knife",
    "Bayonet",
    "Flip Knife",
    "Gut Knife",
    "Karambit",
    "M9 Bayonet",
    "Huntsman Knife",
    "Butterfly Knife",
    "Falchion Knife",
    "Shadow Daggers",
    "Bowie Knife",
    "Navaja Knife",
    "Stiletto Knife",
    "Talon Knife",
    "Ursus Knife",
    "Skeleton Knife",
    "Nomad Knife"
]

# Start the timer
start_time = time.time()

for weapon in csgo_weapons:
    url = "https://csgostash.com/weapon/" + weapon
    print("[+] " + url)

    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")

    span = soup.find_all("div", {"class": "price"})
    
    if span:
        x = span[0].text.replace("€", "").replace("\n", "").replace("-", "").replace(",", "")
    
        l = []
        j = -1

        names = soup.find_all("h3")

        for i in range(len(names) - 2):
            print("[*] \t" + names[i].text)
            d = {}
            span = soup.find_all("div", {"class": "price"})
            j = j + 1
            normal = str(span[j].text.replace("€", "").replace("\n", "").replace("-", "").replace(",", "").replace("'", ""))
            j = j + 1
            stattrak = span[j].text.replace("€", "").replace("\n", "").replace("-", "").replace(",", "")
            if len(stattrak) == 1:  # in case no stattrak is present
                stattrak = "N/A"

            # To convert the string price to integer prices, lowest to highest grade
            norm_price = [int(price) for price in normal.split() if price.isdigit()]

            if len(norm_price) == 2:
                d["Name"] = names[i].text
                d["Battle Scarred"] = norm_price[0]
                d["Factory New"] = norm_price[1]
                try:  # in case no stattrak is present
                    stattrak_values = re.findall(r'\d+', stattrak)
                    d["StatTrak Battle Scarred"] = int(stattrak_values[0])
                except IndexError:
                    d["StatTrak Battle Scarred"] = "N/A"
                try:
                    d["StatTrak Factory New"] = int(stattrak_values[1])
                except IndexError:
                    d["StatTrak Factory New"] = "N/A"
                l.append(d)

        if l:
            df = pd.DataFrame(l)

            # Rearranging columns and sorting ascending according to battle scarred price, and setting names as index
            df = df[['Name', 'Battle Scarred', 'Factory New', 'StatTrak Battle Scarred', 'StatTrak Factory New']]
            df = df.set_index("Name")
            df = df.sort_values(["Battle Scarred"])

            # Get the current script directory
            script_dir = os.path.dirname(os.path.abspath(__file__))
            # Construct the file path for saving the CSV file
            csv_file_path = os.path.join(script_dir, weapon + ".csv")

            # Create the directory if it doesn't exist
            os.makedirs(os.path.dirname(csv_file_path), exist_ok=True)

            # Save the DataFrame to CSV
            df.to_csv(csv_file_path, index=False)
            print("[+] Saved " + csv_file_path)


# End the timer
end_time = time.time()

# Calculate the elapsed time in seconds
elapsed_time = end_time - start_time

# Convert elapsed time to a human-readable format
hours = int(elapsed_time // 3600)
minutes = int((elapsed_time % 3600) // 60)
seconds = int(elapsed_time % 60)

# Print the elapsed time
print(f"Done, after: {hours} hours, {minutes} minutes and {seconds} seconds")