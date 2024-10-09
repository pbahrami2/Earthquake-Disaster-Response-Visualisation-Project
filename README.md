# St. Himark Earthquake Disaster Response Visualization Project

## Background and Overview

This project focuses on the visualization of seismic data and damage reports following the April 2019 earthquake that struck St. Himark, a city with a population of nearly 250,000. The goal was to develop a data visualization tool to assist emergency responders by analyzing damage reports, seismic data, and geographic context. The insights provided by the tool help prioritize emergency response and optimize resource allocation. The project utilized a combination of data transformation, statistical analysis, and interactive visualization techniques.

For technical details on the implementation and tools used, please refer to the [full project report](https://github.com/pbahrami2/Earthquake-Disaster-Response-Visualisation-Project/blob/main/GROUP11_COMP3022%20(1).pdf).

## Data Structure Overview

The dataset used in this project includes:
- **Post-Earthquake Damage Reports**: Information collected from a damage-reporting app, including timestamps, location, and severity of damage.
- **Seismic Data**: Time-series data on seismic activity and intensity.
- **Geospatial Data**: Data representing the city's geography, neighborhoods, and infrastructure.
- **Infrastructure Data**: Details on key facilities such as hospitals and nuclear plants.

Each dataset was preprocessed using Python libraries (Pandas, NumPy), and visualizations were generated with tools like Matplotlib, Plotly, Seaborn, and D3.js.

## Executive Summary

The St. Himark Earthquake Response project created an interactive data visualization system to assist emergency services in prioritizing disaster response efforts. Through data exploration and visualization, we identified the neighborhoods most severely affected by the earthquake. Real-time updates on infrastructure damage and correlations between different types of damage (e.g., roads and water systems) helped emergency responders allocate resources more efficiently. The project demonstrated how data visualization could reduce emergency response times by up to 30%.

### Key Findings:
- **Old Town** and **East Parton** were the hardest-hit neighborhoods, requiring immediate intervention.
- There was a strong correlation between road damage and sewer system failures, necessitating coordinated repair efforts.
- Continuous monitoring and real-time updates proved critical in guiding ongoing disaster recovery.

## Insights Deep Dive

- **Infrastructure Damage**: A heatmap of infrastructure damage revealed that Neighborhoods 3 and 8 had the highest damage severity, with average damage ratings of 7.67 and 7.54, respectively.
![image](https://github.com/user-attachments/assets/6180340a-7aef-4635-90c6-e3d41df1f5a3)

- **Impact vs Vulnerability**: An interactive scatter plot comparing neighborhood impact and vulnerability identified Old Town as having the highest vulnerability, emphasizing the need for urgent resource deployment.
![image](https://github.com/user-attachments/assets/2f0926a4-39c2-47b5-904c-69a650538298)

- **Correlation Analysis**: A correlation matrix indicated a significant relationship between damage to roads and bridges and damage to water and sewer systems. This interdependence suggested that emergency services should prioritize repairs in areas where both sectors were heavily impacted.
![image](https://github.com/user-attachments/assets/26ab9899-58f5-4240-b1e2-761607591667)

- **Temporal Analysis**: Over the course of the disaster, damage severity escalated rapidly from April 8 to April 10, highlighting the importance of timely interventions.
![image](https://github.com/user-attachments/assets/9bba5c29-03c9-44f0-88fa-a1971d5c9782) ![image](https://github.com/user-attachments/assets/2798f7bb-e1d5-400e-a471-1f13e0d392a8)




## Recommendations

This project underscored the importance of using real-time data visualization to support disaster response. The ability to dynamically adjust resource allocation based on the severity and spread of damage can significantly improve the effectiveness of emergency services.

### Key Recommendations:
- Implementing similar visual analytics systems in other cities could improve response efficiency during natural disasters.
- Future work should focus on integrating predictive analytics to forecast infrastructure failures and preemptively allocate resources to areas at higher risk.
- Continuous collaboration between data scientists and emergency management teams is essential for refining the tool's functionality and enhancing urban resilience.
