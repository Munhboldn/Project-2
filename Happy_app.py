import pandas as pd
import streamlit as st
import plotly.express as px
from io import BytesIO

# Load the data with caching for better performance
@st.cache_data
def load_data():
    data = pd.read_csv("World Happiness Report Data - Sheet1.csv")
    data['year'] = data['year'].astype(int)
    return data

data = load_data()

# Title and description
st.title("🌍 Happiness Score Analysis")
st.markdown(
    """
    Welcome to the Happiness Score Analysis app! Explore global happiness trends using data from the World Happiness Report.
    Use the sidebar to select a country or compare multiple countries, filter by year, and download data.
    """
)

# Sidebar for user inputs
st.sidebar.header("🛠 User Inputs")

# Multi-select for countries
selected_countries = st.sidebar.multiselect(
    "Select Countries:", data['Country name'].unique(), default=["Mongolia"]
)

# Year range slider
year_range = st.sidebar.slider(
    "Select Year Range:", int(data['year'].min()), int(data['year'].max()), (2010, 2023)
)

# Filter data based on user selections
filtered_data = data[
    (data['Country name'].isin(selected_countries)) &
    (data['year'] >= year_range[0]) &
    (data['year'] <= year_range[1])
]

# Key metrics
avg_score = filtered_data["Life Ladder"].mean()
min_score = filtered_data["Life Ladder"].min()
max_score = filtered_data["Life Ladder"].max()

st.write("### 🌟 Key Statistics")
col1, col2, col3 = st.columns(3)
col1.metric("Average Happiness", f"{avg_score:.2f}" if not filtered_data.empty else "N/A")
col2.metric("Lowest Score", f"{min_score:.2f}" if not filtered_data.empty else "N/A")
col3.metric("Highest Score", f"{max_score:.2f}" if not filtered_data.empty else "N/A")

# Tabs for organization
tab1, tab2, tab3, tab4, tab5 = st.tabs(["Insights", "Trends", "Global Map", "Detailed Metrics", "Comparisons"])

# Insights tab
with tab1:
    if len(selected_countries) == 1:
        country_data = data[data['Country name'] == selected_countries[0]]
        st.write(f"### Insights for {selected_countries[0]}:")
        if not country_data.empty:
            st.markdown(
                f"""
                **Key Indicators:**
                - Average Happiness Score: {country_data['Life Ladder'].mean():.2f}
                - Highest Happiness Score: {country_data['Life Ladder'].max():.2f} (Year: {country_data.loc[country_data['Life Ladder'].idxmax(), 'year']})
                - Lowest Happiness Score: {country_data['Life Ladder'].min():.2f} (Year: {country_data.loc[country_data['Life Ladder'].idxmin(), 'year']})
                - Average Social Support: {country_data['Social support'].mean():.2f}
                - Average Healthy Life Expectancy: {country_data['Healthy life expectancy at birth'].mean():.2f}
                - Average Log GDP per Capita: {country_data['Log GDP per capita'].mean():.2f}
                """
            )
        else:
            st.write("No data available for this country.")
    else:
        st.write("### Insights")
        st.write("Select a single country for detailed insights.")

# Trends tab
with tab2:
    if len(selected_countries) > 0:
        st.write("### Happiness Score Trends")
        trend_var = st.selectbox("Select a metric to display", ("Life Ladder", "Log GDP per capita", "Social support", "Healthy life expectancy at birth"))
        trend_chart = px.line(
            filtered_data,
            x="year",
            y=trend_var,
            color="Country name",
            title=f"{trend_var} Trends",
            markers=True
        )
        trend_chart.update_traces(
            hovertemplate=f"<b>%{{x}}</b><br>{trend_var}: %{{y:.2f}}<br>Country: %{{legendgroup}}"
        )
        st.plotly_chart(trend_chart, key=f"trend_chart_{trend_var}")

# Global Map tab
with tab3:
    st.write("### Global Happiness Map")
    global_data = data[data['year'] == year_range[1]]
    score_range = st.slider("Filter Happiness Scores", 0.0, 10.0, (0.0, 10.0))
    filtered_global_data = global_data[
        (global_data["Life Ladder"] >= score_range[0]) & (global_data["Life Ladder"] <= score_range[1])
    ]
    global_map = px.choropleth(
        filtered_global_data,
        locations="Country name",
        locationmode="country names",
        color="Life Ladder",
        title=f"Happiness Scores Worldwide ({year_range[1]})",
        color_continuous_scale="Viridis",
        labels={"Life Ladder": "Happiness Score"}
    )
    st.plotly_chart(global_map, key="global_map")

# Detailed Metrics tab
with tab4:
    st.write("### Detailed Metrics for Selected Countries")
    if len(selected_countries) > 0:
        st.dataframe(filtered_data)
    else:
        st.write("Select at least one country to view detailed metrics.")

# Comparisons tab
with tab5:
    st.write("### Side-by-Side Comparison of Selected Countries")
    if len(selected_countries) > 1:
        filtered_data["Country (Year)"] = filtered_data["Country name"] + " (" + filtered_data["year"].astype(str) + ")"
        comparison_chart = px.bar(
            filtered_data,
            x="Country (Year)",
            y=["Life Ladder", "Log GDP per capita", "Social support", "Healthy life expectancy at birth"],
            title="Comparison of Key Metrics Across Countries and Years",
            barmode="group",
            labels={"value": "Metric Value", "Country (Year)": "Country (Year)", "variable": "Metrics"},
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        st.plotly_chart(comparison_chart, use_container_width=True)
    else:
        st.write("Select more than one country to compare.")

# Download filtered data
csv = filtered_data.to_csv(index=False).encode('utf-8')
st.download_button(
    label="📂 Download Filtered Data as CSV",
    data=csv,
    file_name="filtered_happiness_data.csv",
    mime="text/csv",
    help="Download the data for further analysis."
)

# Footer
st.markdown("---")
st.markdown(
    "🔍 Data Source: [World Happiness Report](https://worldhappiness.report/) | Created by [Munkhbold Nyamdorj](https://github.com/Munhboldn)"
)



import random

# List of quotes
quotes = [
    "Happiness is not something ready-made. It comes from your own actions. - Dalai Lama",
    "The purpose of our lives is to be happy. - Dalai Lama",
    "Happiness depends upon ourselves. - Aristotle",
    "Success is not the key to happiness. Happiness is the key to success. - Albert Schweitzer",
    "Happiness is when what you think, what you say, and what you do are in harmony. - Mahatma Gandhi"
]

# List of facts
facts = [
    "Finland has ranked as the happiest country in the world for several years.",
    "Denmark, Switzerland, and Iceland are also consistently among the happiest countries.",
    "The World Happiness Report is published annually by the United Nations Sustainable Development Solutions Network.",
    "Happiness is strongly correlated with economic factors, such as GDP per capita and social support.",
    "Social trust and life expectancy are also major factors in determining a country's happiness score."
]

# Randomly select a quote and a fact
random_quote = random.choice(quotes)
random_fact = random.choice(facts)

# Display in the sidebar
st.sidebar.markdown("💬 **Quote of the Day:**")
st.sidebar.markdown(f"> *{random_quote}*")

st.sidebar.markdown("📚 **Fact of the Day:**")
st.sidebar.markdown(f"> *{random_fact}*")


