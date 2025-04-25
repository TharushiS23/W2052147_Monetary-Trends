import streamlit as st
import pandas as pd
import datetime
from PIL import Image
import plotly.graph_objects as go
import numpy as np
from plotly.subplots import make_subplots

# Load the dataset
@st.cache_data
def load_data():
    df = pd.read_csv("Monetary_stats_1995-2025.csv")
    # Ensure that the 'Date' column is in datetime format and remove the time part
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce').dt.normalize()
    # Extract year and use it for the filter
    df['Year'] = df['Date'].dt.year
    # Calculate the total for M1, M2, and M2b by adding the three columns
    df['Total'] = df["Narrow Money (M1) \n(c)    \n (1) + (2)"] + df["Broad Money (M2) (b)"] + df["Broad Money (M2b) \n(d)            \n (3) + (4)"]
    return df

# Set Streamlit page config and styling
st.set_page_config(layout="wide")
st.markdown('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)

# Load data
df = load_data()

# Common header for all dashboards
def display_header():
    image = Image.open('MOF image.jpg')
    col1, col2 = st.columns([0.1, 0.9])
    with col1:
        st.image(image, width=100)
    
    html_title = """
        <style>
        .title-test {
        font-weight:bold;
        padding:5px;
        border-radius:6px;
        }
        </style>
        <center><h1 class="title-test">Monetary trends 1995-2025</h1></center>"""
    with col2:
        st.markdown(html_title, unsafe_allow_html=True)
    
    col3, _, _ = st.columns([0.1, 0.45, 0.45])
    with col3:
        # Display last updated date
        box_date = str(datetime.datetime.now().strftime("%d %B %Y"))
        st.write(f"Last updated by:  \n {box_date}")

# Common sidebar filters for all dashboards
def display_sidebar_filters(df):
    st.sidebar.header("Filter Data")

    # Add date-related columns
    df['Year'] = df['Date'].dt.year
    df['Month_Name'] = df['Date'].dt.month_name()
    df['Quarter'] = df['Date'].dt.quarter

    # Sidebar filters
    year_filter = st.sidebar.selectbox("Select Year", sorted(df['Year'].unique()))
    quarter_filter = st.sidebar.selectbox("Select Quarter", ['All', 'Q1', 'Q2', 'Q3', 'Q4'])
    month_filter = st.sidebar.selectbox("Select Month", ['All'] + list(df['Month_Name'].unique()))

    # Apply year filter
    filtered_df = df[df['Year'] == year_filter]

    # Apply quarter filter
    if quarter_filter != 'All':
        q_map = {'Q1': 1, 'Q2': 2, 'Q3': 3, 'Q4': 4}
        filtered_df = filtered_df[filtered_df['Quarter'] == q_map[quarter_filter]]

    # Apply month filter
    if month_filter != 'All':
        filtered_df = filtered_df[filtered_df['Month_Name'] == month_filter]

    return filtered_df

# Call the function with your DataFrame
filtered_df = display_sidebar_filters(df)

# Create main tabs for different dashboards
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Money Supply Overview", 
    "Credit Availability Trends", 
    "Economic Liquidity Indicators", 
    "Relationship Explorer", 
    "Key Insights & Highlights"
])
# DASHBOARD 1: MONEY SUPPLY OVERVIEW
with tab1:
    display_header()
    st.header("Overview of Money Supply Components")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Line chart: M0, M1, M2, M3 over time
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=filtered_df["Date"], y=filtered_df["Reserve Money (M0)  (a)"], mode='lines', name='M0'))
        fig.add_trace(go.Scatter(x=filtered_df["Date"], y=filtered_df["Narrow Money (M1) \n(c)    \n (1) + (2)"], mode='lines', name='M1'))
        fig.add_trace(go.Scatter(x=filtered_df["Date"], y=filtered_df["Broad Money (M2) (b)"], mode='lines', name='M2'))
        fig.add_trace(go.Scatter(x=filtered_df["Date"], y=filtered_df["Broad Money (M2b) \n(d)            \n (3) + (4)"], mode='lines', name='M2b'))
        
        fig.update_layout(
            title='Money Supply Measures Over Time',
            xaxis_title='Date',
            yaxis_title='Rs. Mn',
            legend_title='Money Supply Types'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Bar chart or stacked area: Year-wise composition of money supply
        fig2 = go.Figure()
        fig2.add_trace(go.Bar(x=filtered_df["Date"],y=filtered_df["Reserve Money (M0)  (a)"], name='M0'))
        fig2.add_trace(go.Bar(x=filtered_df["Date"], y=filtered_df["Narrow Money (M1) \n(c)    \n (1) + (2)"], name='M1'))
        fig2.add_trace(go.Bar(x=filtered_df["Date"], y=filtered_df["Broad Money (M2) (b)"], name='M2'))
        fig2.add_trace(go.Bar(x=filtered_df["Date"], y=filtered_df["Broad Money (M2b) \n(d)            \n (3) + (4)"], name='M2b'))
        
        fig2.update_layout(
            title='Distribution of Money Supply Components',
            xaxis_title='Date',
            yaxis_title='Rs. Mn',
            barmode='stack',
            legend_title='Money Supply Types'
        )
        st.plotly_chart(fig2, use_container_width=True)
    
    # Growth rate line chart: YoY % change in M1, M2, M3
    st.subheader("Year-over-Year Growth Rates")
    
    # Calculating YoY growth rates
    df_temp = filtered_df.copy()
    df_temp['M0_Growth'] = df_temp["Reserve Money (M0)  (a)"].pct_change(periods=12) * 100
    df_temp['M1_Growth'] = df_temp["Narrow Money (M1) \n(c)    \n (1) + (2)"].pct_change(periods=12) * 100
    df_temp['M2_Growth'] = df_temp["Broad Money (M2) (b)"].pct_change(periods=12) * 100
    df_temp['M2b_Growth'] = df_temp["Broad Money (M2b) \n(d)            \n (3) + (4)"].pct_change(periods=12) * 100
    
    fig3 = go.Figure()
    fig3.add_trace(go.Scatter(x=df_temp["Date"], y=df_temp["M0_Growth"], mode='lines', name='M0 Growth %'))
    fig3.add_trace(go.Scatter(x=df_temp["Date"], y=df_temp["M1_Growth"], mode='lines', name='M1 Growth %'))
    fig3.add_trace(go.Scatter(x=df_temp["Date"], y=df_temp["M2_Growth"], mode='lines', name='M2 Growth %'))
    fig3.add_trace(go.Scatter(x=df_temp["Date"], y=df_temp["M2b_Growth"], mode='lines', name='M2b Growth %'))
    
    fig3.update_layout(
        title='YoY % Change in Money Supply Components',
        xaxis_title='Date',
        yaxis_title='Growth Rate (%)',
        legend_title='Money Supply Types'
    )
    st.plotly_chart(fig3, use_container_width=True)
    
    # Add a pie chart to the dashboard
    st.subheader("Distribution of Money Supply Components (Pie Chart)")
    
    # Summing up the latest available data for the components
    latest_data = filtered_df.iloc[-1]  # Get the latest row of data
    money_supply = [
        latest_data["Narrow Money (M1) \n(c)    \n (1) + (2)"],
        latest_data["Broad Money (M2) (b)"],
        latest_data["Broad Money (M2b) \n(d)            \n (3) + (4)"]
    ]
    
    labels = ['M1', 'M2', 'M2b']
    
    fig4 = go.Figure(data=[go.Pie(labels=labels, values=money_supply, hole=0.3)])
    
    fig4.update_layout(
        title='Pie Chart of Money Supply Components',
        legend_title='Money Supply Types'
    )
    
    st.plotly_chart(fig4, use_container_width=True)
    
    # Add an expander for the raw data
    with st.expander("View Raw Data"):
        st.write(filtered_df[["Date", "Narrow Money (M1) \n(c)    \n (1) + (2)", "Broad Money (M2) (b)", "Broad Money (M2b) \n(d)            \n (3) + (4)"]])
        st.download_button("Download Data", filtered_df.to_csv().encode("utf-8"), "money_supply_data.csv", "text/csv")

# DASHBOARD 2: CREDIT AVAILABILITY TRENDS
with tab2:
    display_header()
    st.header("Credit Availability Trends")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Line chart: Private sector credit, total domestic credit over time
        # Replace with actual column names from your dataset
        credit_columns = ["Broad Money (M2) (b)", "Broad Money (M2b) \n(d)            \n (3) + (4)"]  # Replace with actual credit columns
        
        fig4 = go.Figure()
        for col in credit_columns:
            fig4.add_trace(go.Scatter(x=filtered_df["Date"], y=filtered_df[col], mode='lines', name=col))
        
        fig4.update_layout(
            title='Credit Growth Over Time',
            xaxis_title='Date',
            yaxis_title='Credit Amount (Rs. Mn)',
            legend_title='Credit Types'
        )
        st.plotly_chart(fig4, use_container_width=True)
    
    with col2:
        # Dual-axis chart: M2 vs Private Sector Credit
        fig5 = make_subplots(specs=[[{"secondary_y": True}]])
        
        fig5.add_trace(
            go.Scatter(x=filtered_df["Date"], y=filtered_df["Broad Money (M2) (b)"], name="M2"),
            secondary_y=False,
        )
        
        # Replace with actual private sector credit column
        fig5.add_trace(
            go.Scatter(x=filtered_df["Date"], y=filtered_df["Broad Money (M2b) \n(d)            \n (3) + (4)"], name="Private Sector Credit"),
            secondary_y=True,
        )
        
        fig5.update_layout(
            title_text="M2 vs Private Sector Credit",
            xaxis_title="Date"
        )
        
        fig5.update_yaxes(title_text="M2 (Rs. Mn)", secondary_y=False)
        fig5.update_yaxes(title_text="Private Sector Credit (Rs. Mn)", secondary_y=True)
        
        st.plotly_chart(fig5, use_container_width=True)
    
    # Correlation matrix using heatmap without px
    st.subheader("Correlation Matrix: Credit Variables vs Money Supply")
    
    # For demonstration we'll create a correlation matrix with available columns
    # Replace with actual credit-related columns
    corr_columns = ["Narrow Money (M1) \n(c)    \n (1) + (2)", "Broad Money (M2) (b)", "Broad Money (M2b) \n(d)            \n (3) + (4)"]
    corr_df = filtered_df[corr_columns].corr()
    
    # Create a heatmap using go.Heatmap instead of px.imshow
    corr_z = corr_df.values
    
    fig6 = go.Figure(data=go.Heatmap(
        z=corr_z,
        x=corr_df.columns,
        y=corr_df.columns,
        colorscale='RdBu_r',
        zmin=-1, zmax=1
    ))
    
    # Add annotations (correlation values)
    for i, row in enumerate(corr_z):
        for j, val in enumerate(row):
            fig6.add_annotation(
                x=corr_df.columns[j],
                y=corr_df.columns[i],
                text=f"{val:.2f}",
                showarrow=False,
                font=dict(color="white" if abs(val) > 0.5 else "black")
            )
    
    fig6.update_layout(
        title="Correlation Between Money Supply and Credit Variables"
    )
    
    st.plotly_chart(fig6, use_container_width=True)

# DASHBOARD 3: ECONOMIC LIQUIDITY INDICATORS
with tab3:
    display_header()
    st.header("Economic Liquidity Indicators")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Line chart: Interest rates, reserve money, inflation
        # Replace with actual column names from your dataset
        # For demonstration, we'll create random data
        filtered_df['Interest_Rate'] = np.random.uniform(5, 15, size=len(filtered_df))
        filtered_df['Reserve_Money'] = filtered_df["Narrow Money (M1) \n(c)    \n (1) + (2)"] * 0.3  # Just for demo
        filtered_df['Inflation'] = np.random.uniform(2, 10, size=len(filtered_df))
        
        fig7 = go.Figure()
        fig7.add_trace(go.Scatter(x=filtered_df["Date"], y=filtered_df["Interest_Rate"], mode='lines', name='Interest Rate (%)'))
        fig7.add_trace(go.Scatter(x=filtered_df["Date"], y=filtered_df["Reserve_Money"], mode='lines', name='Reserve Money (Rs. Mn)'))
        fig7.add_trace(go.Scatter(x=filtered_df["Date"], y=filtered_df["Inflation"], mode='lines', name='Inflation (%)'))
        
        fig7.update_layout(
            title='Key Liquidity Indicators',
            xaxis_title='Date',
            yaxis_title='Value',
            legend_title='Indicators'
        )
        st.plotly_chart(fig7, use_container_width=True)
    
    with col2:
        # Dual-axis: Reserve money vs Inflation or Interest Rate
        fig8 = make_subplots(specs=[[{"secondary_y": True}]])
        
        fig8.add_trace(
            go.Scatter(x=filtered_df["Date"], y=filtered_df["Reserve_Money"], name="Reserve Money"),
            secondary_y=False,
        )
        
        fig8.add_trace(
            go.Scatter(x=filtered_df["Date"], y=filtered_df["Inflation"], name="Inflation Rate"),
            secondary_y=True,
        )
        
        fig8.update_layout(
            title_text="Reserve Money vs Inflation",
            xaxis_title="Date"
        )
        
        fig8.update_yaxes(title_text="Reserve Money (Rs. Mn)", secondary_y=False)
        fig8.update_yaxes(title_text="Inflation Rate (%)", secondary_y=True)
        
        st.plotly_chart(fig8, use_container_width=True)
    
    # YoY % change plots: For liquidity-related variables
    st.subheader("Year-over-Year Changes in Liquidity Indicators")
    
    # Calculate YoY changes (placeholder calculations)
    filtered_df['Reserve_Money_Growth'] = filtered_df["Reserve_Money"].pct_change(periods=12) * 100
    
    fig9 = go.Figure()
    fig9.add_trace(go.Scatter(x=filtered_df["Date"], y=filtered_df["Reserve_Money_Growth"], mode='lines', name='Reserve Money Growth (%)'))
    fig9.add_trace(go.Scatter(x=filtered_df["Date"], y=filtered_df["Inflation"], mode='lines', name='Inflation Rate (%)'))
    
    fig9.update_layout(
        title='YoY % Change in Liquidity Indicators',
        xaxis_title='Date',
        yaxis_title='Growth Rate (%)',
        legend_title='Indicators'
    )
    st.plotly_chart(fig9, use_container_width=True)

# DASHBOARD 4: RELATIONSHIP EXPLORER
with tab4:
    display_header()
    st.header("Relationship Explorer")
    
    # Variables for selection
    available_variables = [
        "Narrow Money (M1) \n(c)    \n (1) + (2)", 
        "Broad Money (M2) (b)", 
        "Broad Money (M2b) \n(d)            \n (3) + (4)",
        "Interest_Rate",
        "Reserve_Money",
        "Inflation"
    ]
    
    col1, col2 = st.columns(2)
    
    with col1:
        x_variable = st.selectbox("Select X-Axis Variable:", available_variables, index=0)
    
    with col2:
        y_variable = st.selectbox("Select Y-Axis Variable:", available_variables, index=1)
    
    # Generate scatter plot without trendline (to avoid statsmodels dependency)
    fig10 = go.Figure()
    
    fig10.add_trace(go.Scatter(
        x=filtered_df[x_variable],
        y=filtered_df[y_variable],
        mode='markers',
        marker=dict(
            size=8,
            color='blue',
            opacity=0.7
        ),
        name='Data Points'
    ))
    
    # Manual calculation of best-fit line using numpy
    if len(filtered_df) > 1:  # Only calculate if we have enough data points
        x_values = filtered_df[x_variable].values
        y_values = filtered_df[y_variable].values
        
        # Filter out NaN values
        mask = ~np.isnan(x_values) & ~np.isnan(y_values)
        x_filtered = x_values[mask]
        y_filtered = y_values[mask]
        
        if len(x_filtered) > 1:  # Ensure we still have enough points after filtering
            # Calculate best fit line
            slope, intercept = np.polyfit(x_filtered, y_filtered, 1)
            
            # Create x points for the line
            x_line = np.array([min(x_filtered), max(x_filtered)])
            y_line = slope * x_line + intercept
            
            # Add the trendline to plot
            fig10.add_trace(go.Scatter(
                x=x_line,
                y=y_line,
                mode='lines',
                line=dict(color='red', dash='dash'),
                name=f'Trend Line (y = {slope:.4f}x + {intercept:.4f})'
            ))
    
    fig10.update_layout(
        title=f"Relationship Between {x_variable} and {y_variable}",
        xaxis_title=x_variable,
        yaxis_title=y_variable
    )
    
    st.plotly_chart(fig10, use_container_width=True)
    
    # Calculate correlation
    correlation = filtered_df[x_variable].corr(filtered_df[y_variable])
    
    st.metric(
        label="Correlation Coefficient", 
        value=f"{correlation:.4f}",
        delta=None
    )
    
    # Interpretation of correlation
    st.write("### Interpretation")
    if correlation > 0.7:
        st.write("There is a strong positive correlation between the selected variables.")
    elif correlation > 0.3:
        st.write("There is a moderate positive correlation between the selected variables.")
    elif correlation > -0.3:
        st.write("There is a weak or no correlation between the selected variables.")
    elif correlation > -0.7:
        st.write("There is a moderate negative correlation between the selected variables.")
    else:
        st.write("There is a strong negative correlation between the selected variables.")

# DASHBOARD 5: KEY INSIGHTS & HIGHLIGHTS
with tab5:
    display_header()
    st.header("Key Insights & Highlights")
    
    # KPI cards
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Peak M2 growth
        max_m2_growth = df_temp['M2_Growth'].max()
        # Handle potential NaN values
        if pd.isna(max_m2_growth):
            max_m2_growth = 0
            max_m2_growth_date = "N/A"
        else:
            max_m2_growth_date = df_temp.loc[df_temp['M2_Growth'].idxmax(), 'Date'].strftime('%b %Y') if not pd.isna(df_temp['M2_Growth'].idxmax()) else "N/A"
        
        st.metric(
            label="Peak M2 Growth", 
            value=f"{max_m2_growth:.2f}%",
            delta=f"in {max_m2_growth_date}"
        )
    
    with col2:
        # Max M1 value
        max_m1 = df["Narrow Money (M1) \n(c)    \n (1) + (2)"].max()
        max_m1_date = df.loc[df["Narrow Money (M1) \n(c)    \n (1) + (2)"].idxmax(), 'Date'].strftime('%b %Y') if not pd.isna(df["Narrow Money (M1) \n(c)    \n (1) + (2)"].idxmax()) else "N/A"
        
        st.metric(
            label="Maximum M1 Value", 
            value=f"{max_m1/1000:.1f}B",
            delta=f"in {max_m1_date}"
        )
    
    with col3:
        # Average inflation (using our placeholder data)
        avg_inflation = filtered_df['Inflation'].mean()
        
        st.metric(
            label="Average Inflation", 
            value=f"{avg_inflation:.2f}%",
            delta=None
        )
    
    st.subheader("Summary Points")
    
    # Key points (replace with actual insights based on your data)
    st.markdown("""
    ### Key Observations:
    - M2 money supply has grown at an average rate of X% per year over the past decade
    - During economic crisis periods (2008, 2019), money supply growth accelerated
    - Private sector credit and M2 show a strong positive correlation (r = 0.8)
    - Reserve money fluctuations tend to precede inflation changes by approximately 6 months
    
    ### Major Economic Events:
    - **2008 Global Financial Crisis**: Sharp decline in credit growth but increased money supply
    - **2019 Economic Downturn**: Record levels of reserve money injection
    - **2020-2022 COVID-19 Response**: Unprecedented expansion in M1 and M2
    """)
    
    # Key trend visualization
    st.subheader("Long-Term Money Supply Trend")
    
    # Create a simple visualization for the summary
    fig11 = go.Figure()
    
    # Use annual averages for cleaner visualization
    annual_avg = df.groupby('Year')[["Narrow Money (M1) \n(c)    \n (1) + (2)", "Broad Money (M2) (b)", "Broad Money (M2b) \n(d)            \n (3) + (4)"]].mean().reset_index()
    
    fig11.add_trace(go.Scatter(x=annual_avg["Year"], y=annual_avg["Narrow Money (M1) \n(c)    \n (1) + (2)"], mode='lines+markers', name='M1'))
    fig11.add_trace(go.Scatter(x=annual_avg["Year"], y=annual_avg["Broad Money (M2) (b)"], mode='lines+markers', name='M2'))
    fig11.add_trace(go.Scatter(x=annual_avg["Year"], y=annual_avg["Broad Money (M2b) \n(d)            \n (3) + (4)"], mode='lines+markers', name='M2b'))
    
    # Add annotations for major events (replace with actual years/events)
    # Check if years exist in the data before adding annotations
    if 2008 in annual_avg['Year'].values:
        fig11.add_annotation(
            x=2008, 
            y=annual_avg.loc[annual_avg['Year'] == 2008, "Broad Money (M2) (b)"].values[0],
            text="2008 Crisis",
            showarrow=True,
            arrowhead=1
        )
    
    if 2019 in annual_avg['Year'].values:
        fig11.add_annotation(
            x=2019, 
            y=annual_avg.loc[annual_avg['Year'] == 2019, "Broad Money (M2) (b)"].values[0],
            text="2019 Crisis",
            showarrow=True,
            arrowhead=1
        )
    
    fig11.update_layout(
        title='Long-Term Money Supply Trends (Annual Averages)',
        xaxis_title='Year',
        yaxis_title='Money Supply (Rs. Mn)',
        legend_title='Money Supply Measures'
    )
    
    st.plotly_chart(fig11, use_container_width=True)