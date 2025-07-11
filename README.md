# DayZLootAnalyzer

**DayZLootAnalyzer** is a diagnostic tool for analyzing the loot economy of a DayZ server. It compares loot definitions (`types.xml`) with spawn logic (`proto.xml`) and building placements (`mapgrouppos.xml`) to identify imbalances, saturation issues, and underutilized zones.

---

## 🔍 What It Does

- Parses all loot-related XML files from your server setup
- Calculates spawn capacity based on building placements and lootmax values
- Matches loot items to usage zones and container tags
- Flags underrepresented and oversaturated areas
- Outputs a timestamped JSON report with detailed metrics

---

## 📁 Folder Structure

Place your files in the following structure next to the executable:

```
DayZLootAnalyzer/
├── DayZLootAnalyzer.exe         # The compiled executable
├── input/                       # Input folder for all XML files
│   ├── types/                   # Contains one or more types.xml files
│   ├── proto/                   # Contains proto.xml
│   └── mapgrouppos/             # Contains mapgrouppos.xml
├── output/                      # Will be created automatically for JSON reports
```

---

## 🚀 How to Use

1. Drop your XML files into the correct folders under `input/`
2. Run `DayZLootAnalyzer.exe`
3. Check the `output/` folder for a timestamped JSON report

---

## 📊 Report Contents

The report includes:

- Total nominal loot count
- Total spawn slot capacity
- Saturation ratios per usage zone
- Flags for underrepresented and overrepresented areas

Example:
```json
"Farm": {
  "nominal": 180,
  "spawn_slots": 120,
  "groups": 20,
  "saturation": 1.5
}
```
---

## 🧠 Why Use This?
Identify loot imbalance before it affects gameplay

Tune nominal values and lootmax settings with confidence

Catch broken or misconfigured mods early

Improve loot diversity and distribution across your map

---

## 🛠️ Built With
Python 3.8+

PyInstaller (for executable packaging)

No external dependencies required
