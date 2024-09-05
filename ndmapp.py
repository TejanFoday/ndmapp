import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Load the data
@st.cache_data
def load_data():
    df = pd.read_csv('051022NDMADATABASE_tej.csv', encoding='unicode_escape', parse_dates=['Date of Occurance'])
    df['year'] = df['Date of Occurance'].dt.year
    df['month'] = df['Date of Occurance'].dt.month
    df['Type of Incident'] = df['Type of Incident'].replace({
        'fire': 'Fire', 
        'Flash Flood': 'Flooding', 
        'Bolder Roll': 'Boulder Roll'
    })
    return df

# Data preprocessing
@st.cache_data
def process_data(df):
    dfs = df.groupby(['year', 'Region', 'District', 'Type of Incident']).size().reset_index(name='Frequency')
    dfs['percent'] = (dfs['Frequency'] / dfs['Frequency'].sum() * 100).round(2)
    dfs['percentage'] = dfs['percent'].astype(str) + '%'
    return dfs

# Main function to run the Streamlit app
def main():
    st.set_page_config(page_title="NDMA Interactive Data App", page_icon="🇸🇱", layout="wide")
    st.title("NDMA INTERACTIVE DATA APP")
    st.markdown("---")

    try:
        df = load_data()
        dfs = process_data(df)
    except Exception as e:
        st.error(f"Error loading or processing data: {e}")
        return

    # Year selection
    year_chosen = st.selectbox("Choose year of interest:", sorted(df["year"].unique(), reverse=True))

    # Filter data
    dff = df[df["year"] == year_chosen]
    dfy = dfs[dfs["year"] == year_chosen]
    incident_types = ["Fire", "Windstorm", "Flooding", "Building Collapse", "Mudslide", "Road Accident"]
    dff = dff[dff['Type of Incident'].isin(incident_types)]

    # Map visualization
    st.header("Incident Locations and Key Metrics")
    fig_map = px.scatter_mapbox(
        dff, 
        lat="Latitude", 
        lon="Longitude", 
        hover_name="District", 
        hover_data={
            "Latitude": True,
            "Longitude": True,
            "Type of Incident": True,
            "Population Size": True,
            "Death Cases": True,
            "Injured cases": True
        },
        color="Type of Incident", 
        zoom=6, 
        height=500,
        title="Incident Locations within Sierra Leone"
    )
    fig_map.update_layout(mapbox_style="open-street-map")
    st.plotly_chart(fig_map, use_container_width=True)

    # Other visualizations
    col1, col2 = st.columns(2)

    with col1:
        fig_01 = px.histogram(dfy, x='Region', y='Frequency', color='Type of Incident', 
                              title='Incidents By Region', 
                              labels={'Frequency': 'Number of Incidents'},
                              hover_data=['percentage'], text_auto=True)
        fig_01.update_layout(barmode='stack', xaxis={'categoryorder': 'total descending'})
        st.plotly_chart(fig_01, use_container_width=True)

        fig_03 = px.histogram(dff, x='Region', y='Death Cases', 
                              title='Death Cases by Region', text_auto=True)
        fig_03.update_layout(xaxis={'categoryorder': 'total descending'})
        st.plotly_chart(fig_03, use_container_width=True)

        fig_05 = px.line(dff, x='Date of Occurance', y='Type of Incident', color='Type of Incident', 
                         title='Incident Occurrence During The Year')
        st.plotly_chart(fig_05, use_container_width=True)

    with col2:
        fig_02 = px.histogram(dff, x='Region', y='Population Size', color='Type of Incident', 
                              title='Affected Population by Incident Type and Region', 
                              labels={'Population Size': 'Number of People Affected'},
                              hover_name='Population Size', text_auto=True)
        fig_02.update_layout(barmode='stack', xaxis={'categoryorder': 'total descending'})
        st.plotly_chart(fig_02, use_container_width=True)

        fig_04 = px.histogram(dff, x='Region', y='Injured cases', 
                              title='Injured Cases by Region', text_auto=True)
        fig_04.update_layout(xaxis={'categoryorder': 'total descending'})
        st.plotly_chart(fig_04, use_container_width=True)

        fig_06 = px.histogram(dff, x='Region', y=['School Going Boys', 'School Going Girls'], 
                              title='Affected School-Going Children', text_auto=True)
        fig_06.update_layout(barmode='stack', xaxis={'categoryorder': 'total descending'})
        st.plotly_chart(fig_06, use_container_width=True)

    st.header("Analysis By District")
    fig_08 = px.histogram(dfy, x='District', y='Frequency', color='Type of Incident', 
                          title='Incidents By District', 
                          labels={'Frequency': 'Number of Incidents'},
                          hover_data=['percentage'], text_auto=True)
    fig_08.update_layout(barmode='stack', xaxis={'categoryorder': 'total descending'})
    st.plotly_chart(fig_08, use_container_width=True)

    col3, col4 = st.columns(2)

    with col3:
        fig_09 = px.histogram(dff, x='District', y='Population Size', color='Type of Incident', 
                              title='Affected Population by Incident Type and District', 
                              labels={'Population Size': 'Number of People Affected'},
                              hover_name='Population Size')
        fig_09.update_layout(barmode='stack', xaxis={'categoryorder': 'total descending'})
        st.plotly_chart(fig_09, use_container_width=True)

        fig_11 = px.histogram(dff, x='District', y='Injured cases', 
                              title='Injured Cases by District', text_auto=True)
        fig_11.update_layout(xaxis={'categoryorder': 'total descending'})
        st.plotly_chart(fig_11, use_container_width=True)

    with col4:
        fig_10 = px.histogram(dff, x='District', y='Death Cases', 
                              title='Death Cases by District', text_auto=True)
        fig_10.update_layout(xaxis={'categoryorder': 'total descending'})
        st.plotly_chart(fig_10, use_container_width=True)

        fig_12 = px.histogram(dff, x='District', y=['School Going Boys', 'School Going Girls'], 
                              title='Affected School-Going Children By District', text_auto=True)
        fig_12.update_layout(barmode='stack', xaxis={'categoryorder': 'total descending'})
        st.plotly_chart(fig_12, use_container_width=True)

    st.markdown("---")
    st.caption("Data source: National Disaster Management Agency (NDMA) of Sierra Leone")

if __name__ == "__main__":
    main()