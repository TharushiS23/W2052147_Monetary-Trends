import streamlit as st
import pandas as pd
import datetime
from PIL import Image
import plotly.graph_objects as go
import numpy as np
import plotly.express as px
from plotly.subplots import make_subplots

# Set page config FIRST before anything else
st.set_page_config(
    page_title="Monetary Trends Dashboard",
    page_icon="⌛",
    layout="wide"
)

# Initialize session state to manage navigation between loading page and dashboard
if 'current_page' not in st.session_state:
    st.session_state['current_page'] = 'loading'  # Default to loading page

# Game page content (Sudoku)
def show_loading_game():
    st.title("🧩 Play Sudoku")

    # Embed the external Sudoku game using HTML iframe
    st.components.v1.html(
        """
        <iframe src="http://www.free-sudoku.com/sudoku-webmaster.php" 
                width="100%" 
                height="600" 
                frameborder="0" 
                scrolling="no">
        </iframe>
        """,
        height=600,
    )

    if st.button("Launch Main App"):
        st.session_state['current_page'] = 'dashboard'
        st.rerun()

#defining the displaye header functions
def display_header():
            image = Image.open('MOF image.jpg')
            col1, col2 = st.columns([0.1, 0.9])
            with col1:
                st.image(image, width=100)
            with col2:
                st.markdown("""
            <style>
            .title-test {
                font-weight:bold;
                padding:5px;
                border-radius:6px;
            }
            </style>
            <center><h1 class="title-test">Monetary trends 1995-2025</h1></center>
        """, unsafe_allow_html=True)
col1, col2, col3 = st.columns([0.2, 0.8, 0.1])
with col3:
        date_str = datetime.datetime.now().strftime("%d %B %Y")
        st.write(f"Last updated by: Tharushi Seneviratne  \n {date_str}")

# Sidebar filters
def display_sidebar_filters(df):
    st.sidebar.header("Filter Data")
    df['Date'] = pd.to_datetime(df['Date'])
    df['Year'] = df['Date'].dt.year
    df['Month_Name'] = df['Date'].dt.month_name()
    df['Quarter'] = df['Date'].dt.quarter

    year_filter = st.sidebar.selectbox("Select Year", ['All'] + sorted(df['Year'].unique().tolist()))
    quarter_filter = st.sidebar.selectbox("Select Quarter", ['All', 'Q1', 'Q2', 'Q3', 'Q4'])
    month_filter = st.sidebar.selectbox("Select Month", ['All'] + list(df['Month_Name'].unique()))

    # Apply filters
    if year_filter != 'All':
        df = df[df['Year'] == year_filter]
    if quarter_filter != 'All':
        q_map = {'Q1': 1, 'Q2': 2, 'Q3': 3, 'Q4': 4}
        df = df[df['Quarter'] == q_map[quarter_filter]]
    if month_filter != 'All':
        df = df[df['Month_Name'] == month_filter]

    return df

@st.cache_data
def main():
        df = pd.read_csv("Monetary_stats_1995-2025.csv")
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce').dt.normalize()
        df['Year'] = df['Date'].dt.year
        df['Total'] = df["Broad Money (M2b) \n(d)            \n (3) + (4)"]
        return df

st.markdown('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)


if __name__ == "__main__":
    # Check which page to display based on session state
    if st.session_state['current_page'] == 'loading':
        # Show loading game (Sudoku)
        show_loading_game()
else:
        df = main()
        df['Date'] = df['Date'].dt.date

        #display header
        display_header()

        # Tabs (rendered correctly)
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "Money Supply Overview", 
        "Credit Availability Trends", 
        "Economic Liquidity Indicators", 
        "Relationship Explorer", 
        "Key Insights & Highlights"
        ])

        filtered_df = display_sidebar_filters(df)

        # DASHBOARD 1: MONEY SUPPLY OVERVIEW
        with tab1:
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

            # Add a pie chart to the dashboard
            st.subheader("Distribution of Money Supply Components (%)")

            # Summing up the latest available data for the components
            latest_data = filtered_df.iloc[-1]  
            money_supply = [
                latest_data["Reserve Money (M0)  (a)"],
                latest_data["Narrow Money (M1) \n(c)    \n (1) + (2)"],
                latest_data["Broad Money (M2) (b)"],
                latest_data["Broad Money (M2b) \n(d)            \n (3) + (4)"]
            ]

            labels = ['M0','M1', 'M2', 'M2b']

            fig4 = go.Figure(data=[go.Pie(labels=labels, values=money_supply, hole=0.3)])

            fig4.update_layout(
                title='Pie Chart of Money Supply Components',
                legend_title='Money Supply Types'
            )
            st.plotly_chart(fig4, use_container_width=True)

            st.subheader("Yearly Summary of Money Supply Components")

            # Group data by year and calculate the total sum for each component
            yearly_summary = filtered_df.groupby(filtered_df['Date'].dt.year).agg({
                "Reserve Money (M0)  (a)": "sum",
                "Narrow Money (M1) \n(c)    \n (1) + (2)": "sum",
                "Broad Money (M2) (b)": "sum",
                "Broad Money (M2b) \n(d)            \n (3) + (4)": "sum"
            }).reset_index()
            yearly_summary.rename(columns={
                "Date": "Year",
                "Reserve Money (M0)  (a)": "M0",
                "Narrow Money (M1) \n(c)    \n (1) + (2)": "M1",
                "Broad Money (M2) (b)": "M2",
                "Broad Money (M2b) \n(d)            \n (3) + (4)": "M2b"
            }, inplace=True)
            st.dataframe(yearly_summary, use_container_width=True)

            st.subheader("View filterd data")
            with st.expander("View Raw Data"):
                st.write(filtered_df[["Date", "Narrow Money (M1) \n(c)    \n (1) + (2)", "Broad Money (M2) (b)", "Broad Money (M2b) \n(d)            \n (3) + (4)"]])
                st.download_button("Download Data", filtered_df.to_csv().encode("utf-8"), "money_supply_data.csv", "text/csv")
                
        # DASHBOARD 2: CREDIT AVAILABILITY TRENDS
        with tab2:
            st.header("Credit Availability Trends")

            col1, col2 = st.columns(2)
            with col1:
                # Dual-axis chart: M2 vs Private Sector Credit
                fig5 = make_subplots(specs=[[{"secondary_y": True}]])

                fig5.add_trace(
                    go.Scatter(x=filtered_df["Date"], y=filtered_df["Broad Money (M2) (b)"], name="M2"),
                    secondary_y=False,
                )

                fig5.add_trace(
                    go.Scatter(x=filtered_df["Date"], y=filtered_df["Credit granted to the Private Sector by Commercial Banks"], name="Private Sector Credit"),
                    secondary_y=True,
                )

                fig5.update_layout(
                    title_text="M2 vs Private Sector Credit",
                    xaxis_title="Date"
                )

                fig5.update_yaxes(title_text="M2 (Rs. Mn)", secondary_y=False)
                fig5.update_yaxes(title_text="Private Sector Credit (Rs. Mn)", secondary_y=True)

                st.plotly_chart(fig5, use_container_width=True)

            with col2:
                # Line chart:credit columns
                credit_columns = {
                    "Net Credit granted to the Government by Central Bank": "Govt Credit by Central Bank",
                    "Net Credit granted to the Government by Commercial Banks": "Govt Credit by Commercial Banks",
                    "Net Credit granted to the Government (NCG)\n(8) + (9)": "Total Govt Credit (NCG)",
                    "Credit granted to Public Corporations by Commercial Banks": "Credit to Public Corporations",
                    "Credit granted to the Private Sector by Commercial Banks": "Credit to Private Sector",
                    "Domestic Credit \n(10) + (11) + (12)": "Total Domestic Credit"
                }
                fig4 = go.Figure()
                for old_col, new_col in credit_columns.items():
                    fig4.add_trace(go.Scatter(x=filtered_df["Date"], y=filtered_df[old_col], mode='lines', name=new_col))
                fig4.update_layout(
                    title='Credit Growth Over Time',
                    xaxis_title='Date',
                    yaxis_title='Credit Amount (Rs. Mn)',
                    legend_title='Credit Types'
                )
                st.plotly_chart(fig4, use_container_width=True)

            # Define the credit-related columns and money supply columns with short names
            credit_columns = {
                "Net Credit granted to the Government by Central Bank": "Govt Credit by Central Bank",
                "Net Credit granted to the Government by Commercial Banks": "Govt Credit by Commercial Banks",
                "Net Credit granted to the Government (NCG)\n(8) + (9)": "Total Govt Credit (NCG)",
                "Credit granted to Public Corporations by Commercial Banks": "Credit to Public Corporations",
                "Credit granted to the Private Sector by Commercial Banks": "Credit to Private Sector",
                "Domestic Credit \n(10) + (11) + (12)": "Total Domestic Credit"
            }
            money_supply_columns = {
                "Narrow Money (M1) \n(c)    \n (1) + (2)": "Narrow Money (M1)",
                "Broad Money (M2) (b)": "Broad Money (M2)",
                "Broad Money (M2b) \n(d)            \n (3) + (4)": "Broad Money (M2b)"
            }
            # Merge both dictionaries
            all_columns = {**credit_columns, **money_supply_columns}
            # Select only the original columns (keys)
            selected_df = filtered_df[list(all_columns.keys())]
            # Rename the selected columns to their short names (values)
            selected_df = selected_df.rename(columns=all_columns)
            # Now calculate the correlation matrix
            corr_df = selected_df.corr()
            # Create a heatmap using go.Heatmap
            corr_z = corr_df.values
            fig6 = go.Figure(data=go.Heatmap(
                z=corr_z,
                x=corr_df.columns,
                y=corr_df.columns,
                colorscale='RdBu_r',
                zmin=-1,
                zmax=1
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
            # Update layout with title
            fig6.update_layout(
                title="Correlation Between Credit and Money Supply Variables"
            )
            # Display in Streamlit
            st.subheader("Correlation Matrix: Credit Variables vs Money Supply")
            st.plotly_chart(fig6, use_container_width=True)
            
        # DASHBOARD 3: ECONOMIC LIQUIDITY INDICATORS
        with tab3:
            st.header("Economic Liquidity Indicators")
            
            # Bubble Chart: Liquidity Measures vs Foreign Assets
            filtered_df['Month'] = pd.to_datetime(filtered_df['Date']).dt.strftime('%B')
            
            fig7 = px.scatter(
                filtered_df,
                x="Broad Money (M2b) \n(d)            \n (3) + (4)",  
                y="Net Foreign Assets of Monetary Authorities (e)",
                size="Net Credit granted to the Government by Central Bank",
                color="Month",  # color by Year instead of Date
                title="Liquidity Measures and Foreign Assets",
                labels={
                    "Broad Money (M2b) \n(d)            \n (3) + (4)": "Broad Money (M2b) (Rs. Mn)",
                    "Net Foreign Assets of Monetary Authorities (e)": "Net Foreign Assets (Rs. Mn)",
                    "Net Credit granted to the Government by Central Bank": "Credit to Government (Rs. Mn)",
                    "Month": "Month"
                }
            )
            fig7.update_layout(
                xaxis_title="Broad Money (M2b) (Rs. Mn)",
                yaxis_title="Net Foreign Assets of Monetary Authorities (Rs. Mn)"
            )
            st.plotly_chart(fig7, use_container_width=True)

            # Area Chart: Liquidity Ratios Over Time
            liquidity_df = filtered_df.copy()

            # Calculate Liquidity Ratios
            liquidity_df["Currency Ratio"] = liquidity_df["Currency held by the Public"] / liquidity_df["Narrow Money (M1) \n(c)    \n (1) + (2)"]
            liquidity_df["Reserve Money Ratio"] = liquidity_df["Reserve Money (M0)  (a)"] / liquidity_df["Broad Money (M2) (b)"]
            liquidity_df["Money Multiplier"] = liquidity_df["Broad Money (M2) (b)"] / liquidity_df["Reserve Money (M0)  (a)"]
            liquidity_df["Deposit Ratio"] = liquidity_df["Demand Deposits held by the Public"] / liquidity_df["Narrow Money (M1) \n(c)    \n (1) + (2)"]

            # Melt the ratios into long format
            liquidity_melted = liquidity_df.melt(
                id_vars=["Date"],
                value_vars=["Currency Ratio", "Reserve Money Ratio", "Money Multiplier", "Deposit Ratio"],
                var_name="Liquidity Ratio",
                value_name="Value"
            )

            # Plot Area Chart
            fig8 = px.area(
                liquidity_melted,
                x="Date",
                y="Value",
                color="Liquidity Ratio",
                title="Liquidity Ratios Over Time"
            )

            # Display the chart
            st.plotly_chart(fig8, use_container_width=True)

            # Sunburst Chart: Breakdown of Domestic and Foreign Liquidity
            liquidity_df = filtered_df.copy()

            # Step 1: Categorize data into Domestic and Foreign liquidity
            liquidity_df['Liquidity Type'] = 'Domestic'
            liquidity_df.loc[liquidity_df['Net Foreign Assets of Monetary Authorities (e)'] > 0, 'Liquidity Type'] = 'Foreign'

            # Step 2: Create new columns for the liquidity components
            liquidity_df['Domestic Credit'] = liquidity_df["Net Credit granted to the Government by Central Bank"] + liquidity_df["Net Credit granted to the Government by Commercial Banks"] + liquidity_df["Credit granted to Public Corporations by Commercial Banks"] + liquidity_df["Credit granted to the Private Sector by Commercial Banks"]
            liquidity_df['Foreign Assets'] = liquidity_df["Net Foreign Assets of Monetary Authorities (e)"] + liquidity_df["Net Foreign Assets of Commercial Banks "]

            # Step 3: Create a Sunburst chart structure
            sunburst_df = liquidity_df[['Liquidity Type', 'Domestic Credit', 'Foreign Assets']]

            # Reshape the DataFrame for Sunburst chart
            sunburst_df_melted = sunburst_df.melt(id_vars=['Liquidity Type'], value_vars=['Domestic Credit', 'Foreign Assets'], var_name='Liquidity Component', value_name='Amount')

            # Step 4: Plot the Sunburst chart
            fig = px.sunburst(
                sunburst_df_melted, 
                path=['Liquidity Type', 'Liquidity Component'],  # Hierarchy: Domestic/Foreign -> Credit/Assets
                values='Amount',  # Values to visualize (amounts)
                title="Breakdown of Domestic and Foreign Liquidity"
            )

            # Display the Sunburst chart
            st.plotly_chart(fig, use_container_width=True)

        # DASHBOARD 4: RELATIONSHIP EXPLORER
        with tab4:
            st.header("Relationship Explorer")
            
            # Variables for selection
            available_variables = [
                "Reserve Money (M0)  (a)", 
                "Broad Money (M2) (b)", 
                "Currency held by the Public",
                "Demand Deposits held by the Public",
                "Narrow Money (M1) \n(c)    \n (1) + (2)",
                "Time and Savings Deposits held by the Public",
                "Broad Money (M2b) \n(d)            \n (3) + (4)",
                "Net Foreign Assets of Monetary Authorities (e)",
                "Net Foreign Assets of Commercial Banks ",
                "Net Foreign Assets (NFA) \n(5) + (6)",
                "Net Credit granted to the Government by Central Bank",
                "Net Credit granted to the Government by Commercial Banks",
                "Net Credit granted to the Government (NCG)\n(8) + (9)",
                "Credit granted to Public Corporations by Commercial Banks",
                "Credit granted to the Private Sector by Commercial Banks",
                "Domestic Credit \n(10) + (11) + (12)",
                "Net Domestic Assets  (NDA)       \n (13) + (14)",
                "Broad Money (M2b)\n (7) + (15)"
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
            st.header("Key Insights & Highlights")

            # KPI cards
            col1, col2, col3 = st.columns(3)

            with col1:
                # Check if 'M2_Growth' exists, otherwise calculate it
                if 'M2_Growth' not in filtered_df.columns:
                    # Assuming 'M2_Growth' is the growth rate from previous year, calculate it
                    filtered_df['M2_Growth'] = filtered_df['Broad Money (M2) (b)'].pct_change() * 100

                # Peak M2 growth
                max_m2_growth = filtered_df['M2_Growth'].max()
                # Handle potential NaN values
                if pd.isna(max_m2_growth):
                    max_m2_growth = 0
                    max_m2_growth_date = "N/A"
                else:
                    max_m2_growth_date = filtered_df.loc[filtered_df['M2_Growth'].idxmax(), 'Date'].strftime('%b %Y') if not pd.isna(filtered_df['M2_Growth'].idxmax()) else "N/A"

                st.metric(
                    label="Peak M2 Growth", 
                    value=f"{max_m2_growth:.3f}%",
                    delta=f"in {max_m2_growth_date}"
                )

            with col2:
                # Max M1 value
                max_m1 = filtered_df["Narrow Money (M1) \n(c)    \n (1) + (2)"].max()
                max_m1_date = filtered_df.loc[filtered_df["Narrow Money (M1) \n(c)    \n (1) + (2)"].idxmax(), 'Date'].strftime('%b %Y') if not pd.isna(filtered_df["Narrow Money (M1) \n(c)    \n (1) + (2)"].idxmax()) else "N/A"

                st.metric(
                    label="Maximum M1 Value", 
                    value=f"{max_m1/1000:.1f}B",  
                    delta=f"in {max_m1_date}"
                )

            with col3:
                # Max Reserve Money (M0) value
                max_m0 = filtered_df["Reserve Money (M0)  (a)"].max()
                max_m0_date = filtered_df.loc[filtered_df["Reserve Money (M0)  (a)"].idxmax(), 'Date'].strftime('%b %Y') if not pd.isna(filtered_df["Reserve Money (M0)  (a)"].idxmax()) else "N/A"

                st.metric(
                    label="Maximum M0 Value", 
                    value=f"{max_m0/1000:.1f}B",  
                    delta=f"in {max_m0_date}"
                )

            st.subheader("Summary Points")

            # Key points 
            st.markdown(""" 
            ### Key Observations:
            - The M2 money supply has grown significantly over the past decade, particularly during periods of economic instability.
            - M1 and M2 show a positive correlation, reflecting the relationship between narrow and broad money supply.
            - Reserve money fluctuations tend to precede broader monetary supply trends.

            ### Major Economic Events:
            - **2008 Global Financial Crisis**: A significant impact on the money supply and reserve money.
            - **2019 Economic Downturn**: Increased central bank intervention and reserve money injections.
            - **COVID-19 Pandemic (2020-2022)**: Massive increase in money supply to stimulate the economy.
            """)

            # Key trend visualization
            st.subheader("Long-Term Money Supply Trend")

            # Create a simple visualization for the summary
            fig11 = go.Figure()

            # Use annual averages for cleaner visualization
            filtered_df['Year'] = filtered_df['Date'].dt.year  # Ensure Year is available for grouping
            annual_avg = filtered_df.groupby('Year')[["Narrow Money (M1) \n(c)    \n (1) + (2)", "Broad Money (M2) (b)", "Broad Money (M2b) \n(d)            \n (3) + (4)"]].mean().reset_index()

            fig11.add_trace(go.Scatter(x=annual_avg["Year"], y=annual_avg["Narrow Money (M1) \n(c)    \n (1) + (2)"], mode='lines+markers', name='M1'))
            fig11.add_trace(go.Scatter(x=annual_avg["Year"], y=annual_avg["Broad Money (M2) (b)"], mode='lines+markers', name='M2'))
            fig11.add_trace(go.Scatter(x=annual_avg["Year"], y=annual_avg["Broad Money (M2b) \n(d)            \n (3) + (4)"], mode='lines+markers', name='M2b'))

            # Add annotations for major events (replace with actual years/events)
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

if __name__ == "__main__":
    main()
