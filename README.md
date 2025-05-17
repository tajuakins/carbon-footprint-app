# School Carbon Footprint Tracker 🌿

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.0%2B-FF4B4B)](https://streamlit.io)
[![License: CC BY 4.0](https://img.shields.io/badge/License-CC_BY_4.0-lightgrey)](https://creativecommons.org/licenses/by/4.0/)

A Python-based web application that helps students and classes track their carbon footprint and learn about sustainability.

![App Screenshot](screenshot.png) *(Replace with actual screenshot)*

## Features ✨

- **Carbon Footprint Calculation**:
  - Home energy (electricity & natural gas)
  - Transportation (car travel & flights)
  - Digital device usage
- **Visual Dashboard**:
  - Interactive charts showing emission breakdown
  - Comparison to global averages
  - Progress tracking over time
- **Educational Resources**:
  - Personalized tips to reduce emissions
  - Links to carbon offset programs
- **Classroom Tools**:
  - Track multiple students/classes
  - Compare performance across groups
  - Export data for analysis

## Installation 🛠️

1. **Prerequisites**:
   - Python 3.8+
   - pip package manager

2. **Install dependencies**:
   ```bash
   pip install streamlit pandas matplotlib

3. **Run the application**:
   ```bash
   streamlit run carbon_footprint_app.py
   ```
## Usage Guide 📝
1. **Enter your details in the sidebar**:
- Student/class name
- Your monthly CO₂ goal
- Energy, transportation, and digital usage data
2. **Click "Calculate Carbon Footprint"** to see your results
3. **Explore the tabs**:
- 📊 Results: See your total footprint and breakdown
- 📈 Comparison: Compare to global averages
- 📅 Progress: View your historical data
- 🏫 Class Dashboard: View class-wide data (if available)
4. **Download your data using the sidebar buttons**

## Data & Methodology 🔍
The app uses standard emission factors:

**Category**	**Emission Factor**
- Electricity	0.92 kg CO₂e per kWh
- Natural Gas	5.3 kg CO₂e per therm
- Gas Car	0.404 kg CO₂e per mile
- Digital Activities	Varies by activity
*Global average comparison based on 1000 kg CO₂e/month per person.*

## Educational Value 🎓
This tool helps students:

Understand their environmental impact

- Learn about different emission sources
- Develop data analysis skills
- Set and track sustainability goals

## Contributing 🤝
Contributions are welcome! Please open an issue or pull request for:
- Bug fixes
- Additional features
- Improved emission factors
- Better visualizations

## License 📜
This work is licensed under a Creative Commons Attribution 4.0 International License.

You are free to:

- **Share** — copy and redistribute the material in any medium or format
- **Adapt** — remix, transform, and build upon the material

for any purpose, even commercially, as long as you give **appropriate credit** (include the project name, author, and license link), provide a link to the license, and indicate if changes were made.

## Acknowledgements 🙏
- Emission factors from reputable environmental sources
- Inspired by educational sustainability programs
- Built with Streamlit, Pandas, and Matplotlib


