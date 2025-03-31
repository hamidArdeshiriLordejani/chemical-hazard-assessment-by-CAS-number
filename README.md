# 🧪 Chemical Hazard Assessment Tool (GHS + PubChem)

This is a Python-based tool designed to assist users in evaluating the **health and fire/explosion risks** of chemicals based on CAS numbers and GHS hazard codes.

It includes:

- ✅ CAS number lookup via **PubChem**
- 🔍 Automatic retrieval of:
  - Chemical name
  - Formula, molecular weight
  - IUPAC name, SMILES, InChI, boiling point
  - PubChem link
- 📊 Health risk scoring using hazard codes
- 🧨 Fire/explosion risk estimation
- 🧠 User-friendly interface (Tkinter GUI)
- 🔗 Final report with toxicity alerts

---

## 📸 Example

After entering a CAS number (e.g., Acetone `67-64-1`), the tool will:

1. Show full chemical details from PubChem  
2. Let the user continue or exit  
3. Calculate risk levels and display a final hazard assessment

---

## 🧠 How It Works

1. The user enters a CAS number
2. PubChem is queried via `pubchempy`
3. If found:
   - A popup shows all available chemical info
   - Boiling point and hazard codes are used to estimate volatility, exposure, and risk
4. The user sees a **final GHS risk summary**

---

## ⚙️ Requirements

- Python 3.7+
- Modules:
  - `pubchempy`
  - `tkinter`
  - `PIL` (Pillow)
  - `requests`

Install them using:

```bash
pip install pubchempy pillow requests

🚀 Run It
python GOOD-GUI2_FINAL_PUBCHEM_LINK_ONLY.py

📄 License
MIT — free to use and modify. Give credit if you fork or reuse this tool!


