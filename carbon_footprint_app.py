import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import datetime
import os
from io import StringIO

# Emission factors
emission_factors = {
    'electricity': 0.92,
    'natural_gas': 5.3,
    'gas_car': 0.404,
    'diesel_car': 0.45,
    'hybrid_car': 0.28,
    'electric_car': 0.12,
    'flight_short': 0.25,
    'flight_medium': 0.2,
    'flight_long': 0.15,
    'digital': {
        'streaming': 0.3,
        'video_call': 0.15,
        'email': 0.0003,
        'cloud': 0.02,
        'laptop': 0.055,
        'phone': 0.018
    },
    'global_avg': 1000
}

# Custom CSS
st.markdown("""
    <style>
    body { font-family: 'Segoe UI', sans-serif; background-color: #f0f7f4; }
    h3, h4 { color: #2c6e49; }
    .stButton>button { background-color: #2c6e49; color: white; }
    .stButton>button:hover { background-color: #1e4d33; }
    .st-emotion-cache-1y4p8pa { background-color: #ffffff; border: 1px solid #cfe3dc; padding: 20px; }
    </style>
    """, unsafe_allow_html=True)

# App title
st.title("🌿 School Carbon Footprint Tracker")

# Sidebar inputs
with st.sidebar:
    st.header("Input Your Data")
    student_name = st.text_input("Student/Class Name:", placeholder="e.g. Class 7B or Maya")
    goal = st.number_input("Your Monthly CO₂ Goal (kg):", value=900, min_value=100, max_value=2000)
    
    st.subheader("🔌 Home Energy")
    electricity = st.number_input("Electricity (kWh/month):", value=400)
    natural_gas = st.number_input("Natural Gas (therms/month):", value=20)
    
    st.subheader("🚗 Transportation")
    car_miles = st.number_input("Car travel (miles/month):", value=600)
    car_type = st.selectbox("Car type:", 
                           ["Gas", "Diesel", "Hybrid", "Electric"],
                           index=0)
    
    st.subheader("✈️ Flights (per year)")
    flights_short = st.number_input("Short flights (<300 miles):", value=2)
    flights_medium = st.number_input("Medium flights (300-1500 miles):", value=2)
    flights_long = st.number_input("Long flights (>1500 miles):", value=1)
    
    st.subheader("💻 Digital Usage")
    streaming_hours = st.number_input("Video streaming (hours/month):", value=20)
    video_calls = st.number_input("Video calls (hours/month):", value=10)
    emails = st.number_input("Emails sent (per month):", value=500)
    cloud_gb = st.number_input("Cloud storage used (GB):", value=50)
    laptop_hours = st.number_input("Laptop use (hours/month):", value=90)
    phone_hours = st.number_input("Phone use (hours/month):", value=120)
    
    if st.button("Calculate Carbon Footprint"):
        st.session_state.calculated = True
    else:
        st.session_state.calculated = False

# Calculation function
def calculate_footprint():
    electricity_co2 = electricity * emission_factors['electricity']
    gas_co2 = natural_gas * emission_factors['natural_gas']
    
    car_type_key = f"{car_type.lower()}_car"
    car_co2 = car_miles * emission_factors[car_type_key]
    
    flights_co2 = ((flights_short * 300 * emission_factors['flight_short']) +
                 (flights_medium * 750 * emission_factors['flight_medium']) +
                 (flights_long * 3000 * emission_factors['flight_long'])) / 12
    
    digital_co2 = (streaming_hours * emission_factors['digital']['streaming'] +
                 video_calls * emission_factors['digital']['video_call'] +
                 emails * emission_factors['digital']['email'] +
                 cloud_gb * emission_factors['digital']['cloud'] +
                 laptop_hours * emission_factors['digital']['laptop'] +
                 phone_hours * emission_factors['digital']['phone'])
    
    df = pd.DataFrame({
        'Category': ['Electricity', 'Natural Gas', 'Car Travel', 'Flights', 'Digital Devices'],
        'CO2_kg': [electricity_co2, gas_co2, car_co2, flights_co2, digital_co2]
    })
    
    df['Percent'] = round(100 * df['CO2_kg'] / df['CO2_kg'].sum(), 1)
    df['Name'] = student_name
    df['Goal'] = goal
    
    total = round(df['CO2_kg'].sum(), 2)
    percent_global = round(100 * total / emission_factors['global_avg'], 1)
    
    return df, total, percent_global

# Results display
if 'calculated' in st.session_state and st.session_state.calculated:
    df, total, percent_global = calculate_footprint()
    df_sorted = df.sort_values('CO2_kg', ascending=False)
    
    # Create tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Results", "📈 Comparison", "📅 Progress", "🏫 Class Dashboard"])
    
    with tab1:
        st.subheader("Your Monthly Carbon Footprint")
        st.write(f"Total monthly footprint: {total} kg CO₂e ({percent_global}% of global average)")
        
        if total <= goal:
            st.success(f"🎉 Great job, {student_name}! You're under your monthly goal by {round(goal - total, 1)} kg CO₂e.")
        else:
            st.warning(f"⚠️ You're over your monthly goal by {round(total - goal, 1)} kg CO₂e. Review your top emission areas below!")

        # Create two columns for charts
        col1, col2 = st.columns(2)
        
        with col1:
            # Enhanced Bar Chart
            st.markdown("**📊 Emission Breakdown**")
            fig1, ax1 = plt.subplots(figsize=(8, 5))
            
            # Eco-friendly color palette
            colors = ['#2c6e49', '#4c956c', '#7fb685', '#a5cc95', '#d8f3dc']
            
            bars = ax1.bar(df_sorted['Category'], df_sorted['CO2_kg'], color=colors)
            ax1.set_title("By Category (kg CO₂e)", fontsize=14)
            ax1.set_ylabel("kg CO₂e")
            
            # Add value labels
            for bar in bars:
                height = bar.get_height()
                ax1.text(bar.get_x() + bar.get_width()/2., height,
                        f'{height:.1f} kg',
                        ha='center', va='bottom', fontsize=10)
            
            # Style improvements
            ax1.spines['top'].set_visible(False)
            ax1.spines['right'].set_visible(False)
            ax1.grid(axis='y', alpha=0.3)
            
            plt.tight_layout()
            st.pyplot(fig1)
        
        with col2:
            # Enhanced Donut Chart with non-overlapping labels
            st.markdown("**📈 Percentage Contribution**")
            fig2, ax2 = plt.subplots(figsize=(8, 5))
            
            # Sort by percentage for better visual flow
            df_pie = df_sorted.sort_values('Percent', ascending=False)
            
            # Explode the largest slice only
            explode = [0.1 if i == 0 else 0 for i in range(len(df_pie))]
            
            # Create the pie chart without autopct first
            wedges = ax2.pie(
                df_pie['CO2_kg'],
                labels=None,
                startangle=90,
                colors=colors,
                explode=explode,
                shadow=True,
                wedgeprops={'linewidth': 1, 'edgecolor': 'white'},
                pctdistance=0.75,
                textprops={'fontsize': 8}
            )[0]
            
            # Add labels outside the pie with connecting lines
            bbox_props = dict(boxstyle="round,pad=0.3", fc="w", ec="gray", lw=0.5)
            kw = dict(arrowprops=dict(arrowstyle="-"),
                      bbox=bbox_props, zorder=0, va="center")
            
            for i, p in enumerate(wedges):
                ang = (p.theta2 - p.theta1)/2. + p.theta1
                y = np.sin(np.deg2rad(ang))
                x = np.cos(np.deg2rad(ang))
                horizontalalignment = {-1: "right", 1: "left"}[int(np.sign(x))]
                connectionstyle = f"angle,angleA=0,angleB={ang}"
                kw["arrowprops"].update({"connectionstyle": connectionstyle})
                ax2.annotate(f"{df_pie['Category'].iloc[i]}\n{df_pie['CO2_kg'].iloc[i]:.1f} kg ({df_pie['Percent'].iloc[i]:.1f}%)",
                             xy=(x*0.8, y*0.8),
                             xytext=(1.2*np.sign(x), 1.2*y),
                             horizontalalignment=horizontalalignment,
                             **kw)
            
            # Draw center circle for donut effect
            centre_circle = plt.Circle((0,0), 0.6, fc='white')
            ax2.add_artist(centre_circle)
            
            # Add total in center
            ax2.text(0, 0, f"Total\n{total} kg", 
                     ha='center', va='center', 
                     fontsize=12, weight='bold')
            
            ax2.axis('equal')
            ax2.set_title("Contribution to Total Footprint", fontsize=14, pad=20)
            plt.tight_layout()
            st.pyplot(fig2)

        # Tips section
        st.subheader("✅ Tips to reduce your emissions:")
        tips = {
            "Electricity": "💡 Switch to renewables, unplug devices, use LED bulbs",
            "Natural Gas": "🔥 Improve insulation, reduce heating temperature",
            "Car Travel": "🚗 Use public transport, carpool, or go electric",
            "Flights": "✈️ Travel less by air or offset your trips",
            "Digital Devices": "💻 Power off when not in use, reduce screen time"
        }
        
        for category in df_sorted['Category']:
            st.write(f"**{category}:** {tips[category]}")
        
        # Offset programs
        st.subheader("🌱 Want to Offset Your Carbon?")
        st.markdown("""
        Consider these trusted programs:
        - [Gold Standard](https://www.goldstandard.org/)
        - [Cool Effect](https://www.cooleffect.org/)
        - [CarbonFund.org](https://carbonfund.org/)
        """)
    
    with tab2:
        st.subheader("How do you compare?")
        if percent_global < 100:
            st.success(f"👏 You're doing better than average! Your footprint is {percent_global}% of the global average.")
        elif percent_global == 100:
            st.info("You're right on track with the global average.")
        else:
            st.warning(f"⚠️ Your footprint is {percent_global}% of the global average. Consider making changes.")
    
    with tab3:
        st.subheader("Your Carbon Footprint History")
        if os.path.exists("footprint_log.csv"):
            history = pd.read_csv("footprint_log.csv")
            student_history = history[history['Name'] == student_name]
            
            if len(student_history) >= 2:
                student_history['Date'] = pd.to_datetime(student_history['Date'])
                fig3, ax3 = plt.subplots(figsize=(10, 5))
                ax3.plot(student_history['Date'], student_history['Total_CO2'], 
                        color='#2c6e49', linewidth=2, marker='o')
                ax3.axhline(y=goal, color='red', linestyle='--', label='Goal')
                ax3.set_title(f"CO₂ Emissions Over Time for {student_name}")
                ax3.set_xlabel("Date")
                ax3.set_ylabel("Total CO₂ (kg)")
                ax3.legend()
                ax3.grid(alpha=0.3)
                st.pyplot(fig3)
            else:
                st.info("Not enough data points to show progress chart.")
        else:
            st.info("No history data available yet.")
    
    with tab4:
        st.subheader("Latest Records by Student/Class")
        if os.path.exists("footprint_log.csv"):
            history = pd.read_csv("footprint_log.csv")
            latest = history.sort_values('Date').groupby('Name').last().reset_index()
            latest = latest.sort_values('Total_CO2')
            st.dataframe(latest[['Name', 'Date', 'Total_CO2', 'Goal']])
            
            class_avg = round(latest['Total_CO2'].mean(), 1)
            st.write(f"🌍 Class average CO₂ emissions: {class_avg} kg/month")
            
            # Download button
            csv = latest.to_csv(index=False)
            st.download_button(
                label="Download Class Log CSV",
                data=csv,
                file_name=f"class_footprint_log_{datetime.date.today()}.csv",
                mime='text/csv'
            )
        else:
            st.info("No class data available yet.")
    
    # Download buttons
    st.sidebar.download_button(
        label="Download Your Data (CSV)",
        data=df.to_csv(index=False),
        file_name=f"carbon_footprint_{student_name}_{datetime.date.today()}.csv",
        mime='text/csv'
    )

    # Log the calculation
    if not os.path.exists("footprint_log.csv"):
        log_df = pd.DataFrame(columns=['Name', 'Date', 'Total_CO2', 'Goal'])
    else:
        log_df = pd.read_csv("footprint_log.csv")
    
    new_entry = pd.DataFrame([{
        'Name': student_name,
        'Date': datetime.date.today(),
        'Total_CO2': total,
        'Goal': goal
    }])
    
    log_df = pd.concat([log_df, new_entry], ignore_index=True)
    log_df.to_csv("footprint_log.csv", index=False)
else:
    st.info("Enter your data in the sidebar and click 'Calculate Carbon Footprint' to see results.")