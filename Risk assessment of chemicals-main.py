import sys

reprotoxic_hazard_codes = {
    "Repr": ["H360", "H360D", "H360F", "H360FD", "H360Fd", "H360Df", "H361", "H361d", "H361f", "H361fd", "H362"],
    "Carc": ["H350", "H350i", "H351"],
    "Muta": ["H340", "H341"],
    "STOT": ["H370", "H371", "H372", "H373"]
}


import requests
import re
import tkinter as tk
from tkinter import simpledialog, messagebox
from PIL import Image, ImageTk

# === Dictionaries ===
ghs_hazard_statements = {
    "H200": "Unstable explosive",
    "H201	Explosive": "mass explosion hazard",
    "H202	Explosive": "severe projection hazard",
    "H203	Explosive": "fire, blast or projection hazard",
    "H204": "Fire or projection hazard",
    "H205": "May mass explode in fire",
    "H206	Fire, blast or projection hazard": "increased risk of explosion if desensitizing agent is reduced",
    "H207": "Fire or projection hazard; increased risk of explosion if desensitizing agent is reduced",
    "H208": "Fire hazard; increased risk of explosion if desensitizing agent is reduced",
    "H209": "Explosive",
    "H210": "Very sensitive",
    "H211": "May be sensitive",
    "H220": "Extremely flammable gas",
    "H221": "Flammable gas",
    "H222": "Extremely flammable material",
    "H223": "Flammable material",
    "H224": "Extremely flammable liquid and vapour",
    "H225": "Highly flammable liquid and vapour",
    "H226": "Flammable liquid and vapour",
    "H227": "Combustible liquid",
    "H228": "Flammable solid",
    "H229	Pressurized container": "may burst if heated",
    "H230": "May react explosively even in the absence of air",
    "H231": "May react explosively even in the absence of air at elevated pressure and/or temperature",
    "H232": "May ignite spontaneously if exposed to air",
    "H240": "Heating may cause an explosion",
    "H241": "Heating may cause a fire or explosion",
    "H242": "Heating may cause a fire",
    "H250": "Catches fire spontaneously if exposed to air",
    "H251	Self-heating": "may catch fire",
    "H252	Self-heating in large quantities": "may catch fire",
    "H260": "In contact with water releases flammable gases which may ignite spontaneously",
    "H261": "In contact with water releases flammable gas",
    "H270	May cause or intensify fire": "oxidizer",
    "H271	May cause fire or explosion": "strong oxidizer",
    "H272	May intensify fire": "OXIDISER",
    "H280	Contains gas under pressure": "may explode if heated",
    "H281	Contains refrigerated gas": "may cause cryogenic burns or injury",
    "H282	Extremely flammable chemical under pressure": "May explode if heated",
    "H283	Flammable chemical under pressure": "May explode if heated",
    "H284	Chemical under pressure": "May explode if heated",
    "H290": "May be corrosive to metals",
    "H300": "Fatal if swallowed",
    "H300+H310": "Fatal if swallowed or in contact with skin",
    "H300+H310+H330": "Fatal if swallowed, in contact with skin or if inhaled",
    "H300+H330": "Fatal if swallowed or if inhaled",
    "H301": "Toxic if swallowed",
    "H301+H311": "Toxic if swallowed or in contact with skin",
    "H301+H311+H331": "Toxic if swallowed, in contact with skin or if inhaled",
    "H301+H331": "Toxic if swallowed or if inhaled",
    "H302": "Harmful if swallowed",
    "H302+H312": "Harmful if swallowed or in contact with skin",
    "H302+H312+H332": "Harmful if swallowed, in contact with skin or if inhaled",
    "H302+H332": "Harmful if swallowed or inhaled",
    "H303": "May be harmful if swallowed",
    "H303+H313": "May be harmful if swallowed or in contact with skin",
    "H303+H313+H333": "May be harmful if swallowed, in contact with skin or if inhaled",
    "H303+H333": "May be harmful if swallowed or if inhaled",
    "H304": "May be fatal if swallowed and enters airways",
    "H305": "May be harmful if swallowed and enters airways",
    "H310": "Fatal in contact with skin",
    "H310+H330": "Fatal in contact with skin or if inhaled",
    "H311": "Toxic in contact with skin",
    "H311+H331": "Toxic in contact with skin or if inhaled",
    "H312": "Harmful in contact with skin",
    "H312+H332": "Harmful in contact with skin or if inhaled",
    "H313": "May be harmful in contact with skin",
    "H313+H333": "May be harmful in contact with skin or if inhaled",
    "H314": "Causes severe skin burns and eye damage",
    "H315": "Causes skin irritation",
    "H315+H320": "Causes skin and eye irritation",
    "H316": "Causes mild skin irritation",
    "H317": "May cause an allergic skin reaction",
    "H318": "Causes serious eye damage",
    "H319": "Causes serious eye irritation",
    "H320": "Causes eye irritation",
    "H330": "Fatal if inhaled",
    "H331": "Toxic if inhaled",
    "H332": "Harmful if inhaled",
    "H333": "May be harmful if inhaled",
    "H334": "May cause allergy or asthma symptoms or breathing difficulties if inhaled",
    "H335": "May cause respiratory irritation",
    "H336": "May cause drowsiness or dizziness",
    "H340": "May cause genetic defects",
    "H341": "Suspected of causing genetic defects",
    "H350": "May cause cancer",
    "H350i": "May cause cancer by inhalation",
    "H351": "Suspected of causing cancer",
    "H360": "May damage fertility or the unborn child",
    "H360D": "May damage the unborn child",
    "H360Df": "May damage the unborn child. Suspected of damaging fertility.",
    "H360F": "May damage fertility",
    "H360FD": "May damage fertility. May damage the unborn child.",
    "H360Fd": "May damage fertility. Suspected of damaging the unborn child.",
    "H361": "Suspected of damaging fertility or the unborn child",
    "H361d": "Suspected of damaging the unborn child",
    "H361f": "Suspected of damaging fertility",
    "H361fd": "Suspected of damaging fertility. Suspected of damaging the unborn child.",
    "H362": "May cause harm to breast-fed children",
    "H370": "Causes damage to organs",
    "H371": "May cause damage to organs",
    "H372": "Causes damage to organs through prolonged or repeated exposure",
    "H373": "May cause damage to organs through prolonged or repeated exposure",
    "H400": "Very toxic to aquatic life",
    "H401": "Toxic to aquatic life",
    "H402": "Harmful to aquatic life",
    "H410": "Very toxic to aquatic life with long lasting effects",
    "H411": "Toxic to aquatic life with long lasting effects",
    "H412": "Harmful to aquatic life with long lasting effects",
    "H413": "May cause long lasting harmful effects to aquatic life",
    "H420": "Harms public health and the environment by destroying ozone in the upper atmosphere",
    "H441": "Very toxic to terrestrial invertebrates",
    "EUH201": "Contains lead. Should not be used on surfaces liable to be chewed or sucked by children.",
    "EUH201A": "Warning! Contains lead.",
    "EUH202": "Cyanoacrylate. Danger. Bonds skin and eyes in seconds. Keep out of the reach of children.",
    "EUH203": "Contains chromium(VI). May produce an allergic reaction.",
    "EUH204": "Contains isocyanates. May produce an allergic reaction.",
    "EUH205": "Contains epoxy constituents. May produce an allergic reaction.",
    "EUH206": "Warning! Do not use together with other products. May release dangerous gases (chlorine).",
    "EUH207": "Warning! Contains cadmium. Dangerous fumes are formed during use. See information supplied by the manufacturer. Comply with the safety instructions.",
    "EUH208": "Contains <name of sensitising substance>. May produce an allergic reaction.",
    "EUH209": "Can become highly flammable in use.",
    "EUH209A": "Can become flammable in use.",
    "EUH210": "Safety data sheet available on request.",
    "EUH211": "Warning! Hazardous respirable droplets may be formed when sprayed. Do not breathe spray or mist.",
    "EUH212": "Warning! Hazardous respirable dust may be formed when used. Do not breathe dust.",
    "EUH401": "To avoid risks to human health and the environment, comply with the instructions for use",
}


severity_lookup = {
    "1": ["H302", "H319"],
    "2": ["H301", "H314", "H331"],
    "3": ["H300", "H318", "H370"]
}

severity_labels = {
    "1": "🟡 Slight / Minor",
    "2": "🟠 Harmful",
    "3": "🔴 Severe"
}

risk_matrix = {
    (1, 1): (1, "🟢 Insignificant Risk"),
    (1, 2): (2, "🟢 Low Risk"),
    (1, 3): (3, "🟡 Moderate Risk"),
    (2, 1): (2, "🟢 Low Risk"),
    (2, 2): (3, "🟡 Moderate Risk"),
    (2, 3): (4, "🟠 Significant Risk"),
    (3, 1): (3, "🟡 Moderate Risk"),
    (3, 2): (4, "🟠 Significant Risk"),
    (3, 3): (5, "🔴 UNACCEPTABLE RISK – STOP WORK 🚫")
}

fire_risk_matrix = {
    ("Low", "Low"): (1, "🟦 Very Low Fire/Explosion Risk"),
    ("Low", "Medium"): (2, "🟢 Low Fire/Explosion Risk"),
    ("Low", "High"): (3, "🟡 Medium Fire/Explosion Risk"),
    ("Moderate", "Low"): (2, "🟢 Low Fire/Explosion Risk"),
    ("Moderate", "Medium"): (3, "🟡 Medium Fire/Explosion Risk"),
    ("Moderate", "High"): (4, "🟠 High Fire/Explosion Risk"),
    ("High", "Low"): (3, "🟡 Medium Fire/Explosion Risk"),
    ("High", "Medium"): (4, "🟠 High Fire/Explosion Risk"),
    ("High", "High"): (5, "🔴 Very High Fire/Explosion Risk")
}


# === Functional Helpers ===

def check_reproductive_toxicants(h_codes):
    flagged = []
    for group in reprotoxic_hazard_codes.values():
        for code in group:
            if code in h_codes:
                flagged.append(code)
    return flagged

def classify_temperature(temp_celsius):
    if temp_celsius < 60:
        return "Low"
    elif 60 <= temp_celsius <= 100:
        return "Medium"
    else:
        return "High"

def extract_all_h_codes(obj):
    h_codes = set()
    if isinstance(obj, dict):
        for value in obj.values():
            h_codes.update(extract_all_h_codes(value))
    elif isinstance(obj, list):
        for item in obj:
            h_codes.update(extract_all_h_codes(item))
    elif isinstance(obj, str):
        h_codes.update(re.findall(r"H\d{3}", obj))
    return h_codes


# === NEW: Determine probability based on physical form, amount, and volatility/dust ===
def determine_probability_by_use(state, amount, unit, volatility_or_dust):
    amount = float(amount)
    vol_dust = volatility_or_dust.lower()
    unit = unit.lower()
    state = state.lower()

    if state == "liquid":
        if unit in ["ml"]:
            amount_l = amount / 1000
        elif unit in ["l"]:
            amount_l = amount
        elif unit in ["m3", "m³"]:
            amount_l = amount * 1000
        else:
            return 1

        if amount_l < 0.1 and vol_dust in ["medium", "high"]:
            return 1
        elif (0.1 <= amount_l <= 10 and vol_dust in ["medium", "high"]) or (amount_l > 10 and vol_dust == "low"):
            return 2
        elif amount_l > 10 and vol_dust in ["medium", "high"]:
            return 3

    elif state == "solid":
        if unit in ["g", "gr"]:
            amount_kg = amount / 1000
        elif unit in ["kg"]:
            amount_kg = amount
        elif unit in ["ton", "tonne"]:
            amount_kg = amount * 1000
        else:
            return 1

        if amount_kg < 0.1 and vol_dust == "high":
            return 1
        elif (0.1 <= amount_kg <= 100 and vol_dust == "low") or (amount_kg <= 10 and vol_dust in ["medium", "high"]):
            return 2
        elif amount_kg > 100 and vol_dust in ["medium", "high"]:
            return 3

    return 1

def get_chemical_name(cid):
    try:
        url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/{cid}/property/IUPACName/JSON"
        res = requests.get(url, timeout=10)
        return res.json()["PropertyTable"]["Properties"][0]["IUPACName"]
    except:
        return "Unknown Chemical"

def get_chemical_synonyms(cid):
    try:
        url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/{cid}/synonyms/JSON"
        res = requests.get(url, timeout=10)
        all_names = res.json()["InformationList"]["Information"][0]["Synonym"]
        return all_names[:5]
    except:
        return []

def get_boiling_point(cid):
    try:
        url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/data/compound/{cid}/JSON/"
        res = requests.get(url, timeout=15)
        data = res.json()
        sections = data.get("Record", {}).get("Section", [])
        for section in sections:
            if section.get("TOCHeading") == "Chemical and Physical Properties":
                for subsection in section.get("Section", []):
                    if subsection.get("TOCHeading") == "Experimental Properties":
                        for prop in subsection.get("Section", []):
                            if "Boiling Point" in prop.get("TOCHeading", ""):
                                for info in prop.get("Information", []):
                                    raw = info.get("Value", {}).get("StringWithMarkup", [{}])[0].get("String", "")
                                    match = re.search(r"([-+]?[0-9]*\.?[0-9]+) ?°F", raw)
                                    if match:
                                        fahrenheit = float(match.group(1))
                                        celsius = round((fahrenheit - 32) * 5 / 9, 2)
                                        return f"{celsius} °C"
                                    match_c = re.search(r"([-+]?[0-9]*\.?[0-9]+) ?°C", raw)
                                    if match_c:
                                        return f"{match_c.group(1)} °C"
                                    return raw
        return "Not found"
    except:
        return "Not found"

def estimate_volatility(cid):
    try:
        url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/data/compound/{cid}/JSON/"
        res = requests.get(url, timeout=15)
        data = res.json()
        sections = data.get("Record", {}).get("Section", [])
        for section in sections:
            if section.get("TOCHeading") == "Chemical and Physical Properties":
                for subsection in section.get("Section", []):
                    if subsection.get("TOCHeading") == "Experimental Properties":
                        for prop in subsection.get("Section", []):
                            if "Vapor Pressure" in prop.get("TOCHeading", ""):
                                for info in prop.get("Information", []):
                                    value = info.get("Value", {}).get("StringWithMarkup", [{}])[0].get("String", "")
                                    if "mmHg" in value:
                                        vp_value = float(value.split(" ")[0])
                                        if vp_value > 100:
                                            return "High"
                                        elif 10 <= vp_value <= 100:
                                            return "Moderate"
                                        else:
                                            return "Low"
        return None
    except:
        return None

def get_pubchem_data(cas):
    try:
        cid_url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/{cas}/cids/JSON"
        cid = requests.get(cid_url, timeout=10).json()["IdentifierList"]["CID"][0]
        chem_name = get_chemical_name(cid)
        data_url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/data/compound/{cid}/JSON/"
        data = requests.get(data_url, timeout=10).json()
        h_codes = extract_all_h_codes(data)
        return chem_name, sorted(h_codes), cid
    except:
        return "Unknown", [], None

def get_severity_level(h_codes):
    levels = []
    for h in h_codes:
        for level, codes in severity_lookup.items():
            if h in codes:
                levels.append(int(level))
    return max(levels) if levels else 1

def show_risk_matrix_image(image_path="hazard_matrix_popup.png"):
    try:
        root = tk.Tk()
        root.title("Hazard Risk Matrix")
        img = Image.open(image_path)
        img = img.resize((650, 500))
        img_tk = ImageTk.PhotoImage(img)
        label = tk.Label(root, image=img_tk)
        label.image = img_tk
        label.pack(pady=10)
        tk.Button(root, text="Close", command=root.destroy, font=("Arial", 12), bg="#d9534f", fg="white").pack(pady=10)
        root.mainloop()
    except Exception as e:
        print(f"⚠️ Could not show image popup: {e}")





def estimate_volatility_from_boiling_point(bp_celsius, temp_celsius):
    try:
        bp = float(bp_celsius)
        temp = float(temp_celsius)

        # Curve 1 (Low/Mod): 2nd degree polynomial
        bp_line1 = 21.83 + 6.60 * temp - 0.0122 * (temp ** 2)

        # Curve 2 (Mod/High): 3rd degree polynomial
        bp_line2 = 6.19 + 2.24 * temp - 0.00528 * (temp ** 2) + 0.0000222 * (temp ** 3)

        if bp >= bp_line1:
            return "Low"
        elif bp_line2 <= bp < bp_line1:
            return "Moderate"
        else:
            return "High"
    except:
        return None





def select_volatility_option(vp_based, bp_based, process_temp, boiling_point):
    result = {"value": None}

    def draw_graph(temp, bp):
        fig, ax = plt.subplots(figsize=(5, 4), dpi=100)
        x = np.linspace(0, 160, 200)
        y1 = 21.83 + 6.60 * x - 0.0122 * (x ** 2)
        y2 = 6.19 + 2.24 * x - 0.00528 * (x ** 2) + 0.0000222 * (x ** 3)

        ax.plot(x, y1, label='Low/Moderate Boundary')
        ax.plot(x, y2, label='Moderate/High Boundary')
        ax.scatter(temp, bp, color='red', label='Your Chemical')
        ax.set_title('Volatility Zones')
        ax.set_xlabel('Process Temperature (°C)')
        ax.set_ylabel('Boiling Point (°C)')
        ax.grid(True)
        ax.legend()
        canvas = FigureCanvas(fig)
        buf = io.BytesIO()
        canvas.print_png(buf)
        buf.seek(0)
        return Image.open(buf)

    def set_choice(choice):
        result["value"] = choice
        popup.destroy()

    popup = tk.Tk()
    popup.title("Select Volatility Estimate")
    popup.geometry("700x800")

    tk.Label(popup, text="Choose which method to use for volatility estimation:", font=("Arial", 14)).pack(pady=10)
    tk.Label(popup, text=f"📈 Method A (Vapor Pressure): {vp_based}", font=("Arial", 12)).pack()
    tk.Label(popup, text=f"🌡️ Method B (Boiling Point vs Temp): {bp_based}", font=("Arial", 12)).pack()

    # Draw and display graph
    try:
        img = draw_graph(process_temp, float(boiling_point))
        img_tk = ImageTk.PhotoImage(img)
        img_label = tk.Label(popup, image=img_tk)
        img_label.image = img_tk
        img_label.pack(pady=10)
    except:
        tk.Label(popup, text="Could not generate graph.").pack()

    btn_frame = tk.Frame(popup)
    btn_frame.pack(pady=10)
    tk.Button(btn_frame, text="Use Method A", command=lambda: set_choice(vp_based),
              font=("Arial", 12), bg="skyblue", width=15).pack(side="left", padx=20)
    tk.Button(btn_frame, text="Use Method B", command=lambda: set_choice(bp_based),
              font=("Arial", 12), bg="lightgreen", width=15).pack(side="right", padx=20)

    # Exit button
    tk.Button(popup, text="Exit", command=popup.destroy,
              font=("Arial", 12), bg="tomato", width=20).pack(pady=10)

    popup.mainloop()
    return result["value"]
    return result["value"]
    return result["value"]


def get_unit_input(state):
    result = {"value": None}
    def set_unit(unit):
        result["value"] = unit
        popup.destroy()
    popup = tk.Tk()
    popup.title("Select Unit")
    popup.geometry("500x250")
    tk.Label(popup, text="Select the unit for amount used:", font=("Arial", 14)).pack(pady=20)
    btn_frame = tk.Frame(popup)
    btn_frame.pack(pady=10)

    if state == "liquid":
        options = [("ml", "skyblue"), ("L", "lightblue"), ("m³", "deepskyblue")]
    else:
        options = [("g", "lightgreen"), ("kg", "mediumseagreen"), ("ton", "darkseagreen")]

    for unit_text, color in options:
        tk.Button(btn_frame, text=unit_text, command=lambda u=unit_text: set_unit(u),
                  font=("Arial", 12), width=8, bg=color).pack(side="left", padx=15)
    popup.mainloop()
    return result["value"]


def get_physical_state():
    result = {"value": None}
    def set_state(state):
        result["value"] = state
        popup.destroy()
    popup = tk.Tk()
    popup.title("Physical State")
    popup.geometry("400x200")
    tk.Label(popup, text="Is the chemical a liquid or solid?", font=("Arial", 14)).pack(pady=20)
    btn_frame = tk.Frame(popup)
    btn_frame.pack(pady=10)
    tk.Button(btn_frame, text="Liquid", command=lambda: set_state("liquid"),
              font=("Arial", 12), width=10, bg="skyblue").pack(side="left", padx=20)
    tk.Button(btn_frame, text="Solid", command=lambda: set_state("solid"),
              font=("Arial", 12), width=10, bg="lightgreen").pack(side="right", padx=20)
    popup.mainloop()
    return result["value"]

# === GUI Popup Functions with Font/Color ===
def get_user_input(prompt, title="Input"):
    def on_submit():
        result["value"] = entry.get()
        popup.destroy()
    result = {"value": None}
    popup = tk.Tk()
    popup.title(title)
    popup.geometry("450x150")
    tk.Label(popup, text=prompt, font=("Arial", 12)).pack(pady=10)
    entry = tk.Entry(popup, font=("Arial", 12), width=40)
    entry.pack(pady=5)
    entry.focus()
    tk.Button(popup, text="Submit", command=on_submit, font=("Arial", 12)).pack(pady=10)
    popup.mainloop()
    if result["value"] is None:
        messagebox.showwarning("Cancelled", "Operation cancelled by user.")
        exit(0)
    return result["value"].strip()

def get_user_confirmation(prompt, title="Confirmation"):
    result = {"value": False}
    popup = tk.Tk()
    popup.title(title)
    popup.geometry("500x200")
    tk.Label(popup, text=prompt, font=("Arial", 12), wraplength=450).pack(pady=20)
    def yes():
        result["value"] = True
        popup.destroy()
    def no():
        result["value"] = False
        popup.destroy()
    btn_frame = tk.Frame(popup)
    btn_frame.pack()
    tk.Button(btn_frame, text="Yes", command=yes, width=10, font=("Arial", 12), bg="green", fg="white").pack(side="left", padx=10)
    tk.Button(btn_frame, text="No", command=no, width=10, font=("Arial", 12), bg="red", fg="white").pack(side="right", padx=10)
    popup.mainloop()
    return result["value"]







def show_message(msg, title="Information", color="black"):
    popup = tk.Tk()
    popup.title(title)
    popup.geometry("700x500")
    popup.minsize(700, 500)

    outer_frame = tk.Frame(popup)
    outer_frame.pack(expand=True, fill="both", padx=10, pady=10)

    text_frame = tk.Frame(outer_frame)
    text_frame.pack(expand=True, fill="both")

    scrollbar = tk.Scrollbar(text_frame)
    scrollbar.pack(side="right", fill="y")

    text_box = tk.Text(text_frame, font=("Arial", 12), wrap="word", yscrollcommand=scrollbar.set,
                       height=20, bg="white", fg=color)
    text_box.insert("1.0", msg)
    text_box.config(state="disabled")
    text_box.pack(side="left", expand=True, fill="both")

    scrollbar.config(command=text_box.yview)

    button_frame = tk.Frame(popup)
    button_frame.pack(pady=10)
    tk.Button(button_frame, text="Continue", command=popup.destroy,
              font=("Arial", 12), bg="lightblue", width=15).pack(side="left", padx=20)
    tk.Button(button_frame, text="Exit", command=lambda: (popup.destroy(), sys.exit()),
              font=("Arial", 12), bg="tomato", width=15).pack(side="right", padx=20)

    popup.mainloop()

# === MAIN FUNCTION ===


def main():
    while True:
        cas = get_user_input("Enter CAS number (or type 'done' to exit):", "CAS Number Input")
        if cas.lower() == "done":
            break

        chem_name, h_codes, cid = get_pubchem_data(cas)
        if chem_name == "Unknown":
            show_message("❌ Could not retrieve chemical information. Try another CAS.", "Error", color="red")
            continue

        boiling_point = get_boiling_point(cid)
        synonyms = get_chemical_synonyms(cid)

        info_msg = f"📦 Chemical Name Detected: {chem_name}\n"
        if synonyms:
            info_msg += "🔁 Also known as: " + ", ".join(synonyms) + "\n"
        info_msg += f"🌡️ Boiling Point: {boiling_point}\n\nIs this correct?"

        if not get_user_confirmation(info_msg, "Confirm Chemical"):
            show_message("⚠️ CAS verification failed. Please try again.", "Verification Failed", color="orange")
            continue

        if not h_codes:
            show_message("❌ No H-codes found for this CAS.", "Error", color="red")
            continue

        severity = get_severity_level(h_codes)
        h_msg = "✅ H-codes found:\n"
        for code in h_codes:
            desc = ghs_hazard_statements.get(code, "No description available")
            h_msg += f" - {code}: {desc}\n"
        
        reprotoxic_codes = check_reproductive_toxicants(h_codes)
        if reprotoxic_codes:
            show_message(
                f"⚠️ WARNING: This chemical includes reproductive or organ toxicants.\n\nCodes: {', '.join(reprotoxic_codes)}",
                "⚠️ Toxicity Alert",
                color="red"
            )

            desc = ghs_hazard_statements.get(code, "No description available")
            h_msg += f" - {code}: {desc}\n"

        temp = get_user_input("🌡️ Enter Process Temperature in °C:", "Process Temperature")
        try:
            temp = float(temp)
        except:
            show_message("❌ Invalid temperature.", "Error", color="red")
            continue

        temp_level = classify_temperature(temp)

        vp_based = estimate_volatility(cid)
        boiling_c = boiling_point.replace(" °C", "") if "°C" in boiling_point else None
        bp_based = estimate_volatility_from_boiling_point(boiling_c, temp)
        if vp_based and bp_based:
            user_vol = select_volatility_option(vp_based, bp_based, temp, boiling_c)
        elif vp_based:
            user_vol = vp_based
        elif bp_based:
            user_vol = bp_based
        else:
            user_vol = get_user_input("Enter Volatility (Low / Moderate / High):", "Volatility Input")

        state = get_physical_state()
        amount = get_user_input("Enter amount used (e.g., 100):", "Amount")
        unit = get_unit_input(state)

        fire_score, fire_msg = fire_risk_matrix.get((user_vol, temp_level), (0, "❓ Unknown Fire Risk"))

        if state == "liquid":
            volatility_or_dust = user_vol
        else:
            volatility_or_dust = get_user_input("Enter dust formation level (Low / Medium / High):", "Dustiness")

        probability = determine_probability_by_use(state, amount, unit, volatility_or_dust)
        
        exposure_msg = (
            f"📊 Exposure Probability automatically determined as Level {probability}\n\n"
            f"🟢 Level 1: Improbable\n"
            f"🟡 Level 2: Possible\n"
            f"🔴 Level 3: Probable"
        )
        show_message(exposure_msg, "Exposure Estimate", color="blue")


        risk_score, risk_msg = risk_matrix.get((severity, probability), (0, "❓ Unknown Risk"))

        color = "black"
        if risk_score == 5 or fire_score == 5:
            color = "red"
        elif risk_score == 4 or fire_score == 4:
            color = "orange"
        elif risk_score == 3:
            color = "goldenrod"
        elif risk_score == 2 or fire_score == 2:
            color = "green"


        final_msg = (
            f"🧪 Severity Level: {severity_labels[str(severity)]}\n"
            f"📈 Exposure Probability: {probability}\n"
            f"\n===============================\n"
            f"⚠️ HEALTH RISK SCORE = {risk_score} → {risk_msg}\n"
            f"===============================\n"
            f"\n🔥 Fire/Explosion Risk = {fire_score} → {fire_msg}"
        )
        show_message(h_msg + "\n" + final_msg, "Hazard Assessment Results", color=color)
        
        reprotoxic_codes = check_reproductive_toxicants(h_codes)
        if reprotoxic_codes:
            final_msg += (
                f"\n🚨 Reproductive/Organ Toxicant Detected!\n"
                f"⚠️ Codes: {', '.join(reprotoxic_codes)}"
            )
        else:
            final_msg += "\n🧪 No reproductive or organ toxicant hazard codes found."


        reprotoxic_codes = check_reproductive_toxicants(h_codes)

if __name__ == "__main__":
    main()