import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# --- PAGE CONFIGURATION & STYLING ---
st.set_page_config(
    page_title="Personal Net Worth Dashboard",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Premium UI Styling
st.markdown("""
<style>
    /* Styling Metrics & Cards */
    div[data-testid="metric-container"] {
        background-color: rgba(28, 115, 237, 0.08);
        border: 1px solid rgba(28, 115, 237, 0.2);
        padding: 15px 20px;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
    }
    div[data-testid="metric-container"]:hover {
        background-color: rgba(28, 115, 237, 0.12);
        border-color: rgba(28, 115, 237, 0.4);
    }
    /* Dynamic Color indicators for Positive Net Worth */
    .net-worth-highlight {
        font-size: 2.2rem;
        font-weight: 700;
        color: #2ecc71;
        background: rgba(46, 204, 113, 0.1);
        padding: 10px 20px;
        border-radius: 8px;
        display: inline-block;
        border: 1px solid rgba(46, 204, 113, 0.2);
    }
    .main-header {
        font-family: 'Inter', sans-serif;
        font-weight: 800;
        color: #1e293b;
    }
</style>
""", unsafe_allow_html=True)

# --- MONTHS CONFIGURATION ---
months = [
    "START (2023)", "JANUARY", "FEBRUARY", "MARCH", "APRIL", 
    "MAY", "JUNE", "JULY", "AUGUST", "SEPTEMBER", "OCTOBER", "NOVEMBER", "DECEMBER"
]

# --- REPLICATE EXACT USER SPREADSHEET DATA ---
# This matches the user's specific items and values perfectly from the provided spreadsheet image!
default_data = {
    # Assets: Cash & Bank
    "Cash & Bank Accounts (Generic)": [2896.01, 966.69, 966.69, 966.69, 966.69, 457.14, 34.24, 442.16, 0.0, 0.0, 0.0, 0.0, 0.0],
    "Cash & Emergency Fund (RHB 1)": [10.02, 119.24, 119.24, 119.24, 119.24, 2.67, 2.67, 2.67, 0.0, 0.0, 0.0, 0.0, 0.0],
    "Cash & Emergency Fund (RHB 2)": [2800.00, 820.05, 820.05, 820.05, 820.05, 434.25, 17.71, 259.32, 0.0, 0.0, 0.0, 0.0, 0.0],
    "Cash & Emergency Fund (MB)": [75.99, 17.40, 17.40, 17.40, 17.40, 10.22, 3.86, 170.17, 0.0, 0.0, 0.0, 0.0, 0.0],
    "Cash & Emergency Fund (CIMB)": [10.00, 10.00, 10.00, 10.00, 10.00, 10.00, 10.00, 10.00, 0.0, 0.0, 0.0, 0.0, 0.0],
    
    # Assets: Investments
    "Luno": [807.42, 1577.00, 1577.00, 1577.00, 1577.00, 1328.00, 1079.00, 1577.00, 0.0, 0.0, 0.0, 0.0, 0.0],
    "Stashaway": [14889.62, 40400.16, 40400.16, 40400.16, 40400.16, 41914.18, 42735.55, 44267.88, 0.0, 0.0, 0.0, 0.0, 0.0],
    "Moomoo": [4000.00, 5115.59, 5115.59, 5115.59, 5115.59, 6081.33, 6055.82, 8354.45, 0.0, 0.0, 0.0, 0.0, 0.0],
    "Wahed": [2280.15, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    "Principal CIMB": [11135.16, 13734.59, 13734.59, 13734.59, 13734.59, 15642.31, 16275.17, 16740.91, 0.0, 0.0, 0.0, 0.0, 0.0],
    "ASB Financing (Asset)": [100000.00, 131156.63, 131156.63, 131156.63, 131156.63, 131156.63, 131156.63, 131156.63, 0.0, 0.0, 0.0, 0.0, 0.0],
    "Quantum Gold": [11.03, 23.40, 23.40, 23.40, 23.40, 22.22, 20.82, 20.69, 0.0, 0.0, 0.0, 0.0, 0.0],
    "TnG": [2196.47, 3043.16, 3043.16, 3043.16, 3043.16, 992.68, 4188.74, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    "Rakuten": [95.48, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    "Versa": [462.24, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    "Shopee Money+": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 2645.10, 0.0, 0.0, 0.0, 0.0, 0.0],
    "EPF": [42218.75, 53110.29, 53110.29, 53110.29, 53110.29, 60136.74, 60136.74, 60928.74, 0.0, 0.0, 0.0, 0.0, 0.0],
    "Properties": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    "Other Assets": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],

    # Liabilities: Short-Term Debts
    "Short-Term Debts (Generic)": [595.00, 303.45, 303.45, 303.45, 303.45, 294.15, 294.15, 357.15, 0.0, 0.0, 0.0, 0.0, 0.0],
    "Insurance": [155.00, 170.45, 170.45, 170.45, 170.45, 189.15, 189.15, 189.15, 0.0, 0.0, 0.0, 0.0, 0.0],
    "Tommy (Internet/Starlink)": [130.00, 90.00, 90.00, 90.00, 90.00, 62.00, 62.00, 125.00, 0.0, 0.0, 0.0, 0.0, 0.0],
    "House Rent": [150.00, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    "Parking": [90.00, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    "Starlink": [70.00, 43.00, 43.00, 43.00, 43.00, 43.00, 43.00, 43.00, 0.0, 0.0, 0.0, 0.0, 0.0],
    
    # Liabilities: Long-Term Debts
    "Car Loan (AXIA)": [40917.00, 19591.57, 19591.57, 19591.57, 19591.57, 17643.57, 17156.57, 17156.57, 0.0, 0.0, 0.0, 0.0, 0.0],
    "ASB Financing (Loan)": [103038.00, 99627.06, 99627.06, 99627.06, 99627.06, 99217.52, 99114.29, 99114.29, 0.0, 0.0, 0.0, 0.0, 0.0],
    "PTPTN": [13220.00, 4807.11, 4807.11, 4807.11, 4807.11, 4851.19, 4862.21, 4862.21, 0.0, 0.0, 0.0, 0.0, 0.0],
    "Other Liabilities": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
}

# Maintain classification categorizations
default_item_types = {
    # Assets
    "Cash & Bank Accounts (Generic)": "Cash",
    "Cash & Emergency Fund (RHB 1)": "Cash",
    "Cash & Emergency Fund (RHB 2)": "Cash",
    "Cash & Emergency Fund (MB)": "Cash",
    "Cash & Emergency Fund (CIMB)": "Cash",
    "Luno": "Investments",
    "Stashaway": "Investments",
    "Moomoo": "Investments",
    "Wahed": "Investments",
    "Principal CIMB": "Investments",
    "ASB Financing (Asset)": "Investments",
    "Quantum Gold": "Investments",
    "TnG": "Investments",
    "Rakuten": "Investments",
    "Versa": "Investments",
    "Shopee Money+": "Investments",
    "EPF": "Retirement/EPF",
    "Properties": "Properties",
    "Other Assets": "Other Assets",
    
    # Liabilities
    "Short-Term Debts (Generic)": "Short-Term Debts",
    "Insurance": "Short-Term Debts",
    "Tommy (Internet/Starlink)": "Short-Term Debts",
    "House Rent": "Short-Term Debts",
    "Parking": "Short-Term Debts",
    "Starlink": "Short-Term Debts",
    "Car Loan (AXIA)": "Long-Term Debts",
    "ASB Financing (Loan)": "Long-Term Debts",
    "PTPTN": "Long-Term Debts",
    "Other Liabilities": "Other Liabilities"
}

# --- STATE INITIALIZATION ---
if "financial_data" not in st.session_state:
    st.session_state.financial_data = pd.DataFrame(default_data, index=months).T
if "item_types" not in st.session_state:
    st.session_state.item_types = default_item_types.copy()

# Prepare variables for quick access
df = st.session_state.financial_data

# --- SIDEBAR CONTROLS & MASTER NAVIGATION ---
st.sidebar.title("💰 Tracker Navigation")

# Persistent Navigation Option inside the Sidebar!
# Consolidated Category Manager directly into monthly edit tab to reduce navigation clutter
selected_tab = st.sidebar.radio(
    "Choose Active View:",
    [
        "🏆 Interactive Dashboard", 
        "✏️ Update Monthly Figures", 
        "📋 Spreadsheet Database"
    ],
    index=0,
    key="sidebar_navigation_menu"
)

st.sidebar.divider()
st.sidebar.subheader("⚙️ Dashboard Settings")
currency = st.sidebar.selectbox("Currency Unit", ["RM", "$", "€", "£"], index=0)

if st.sidebar.button("🔄 Reset to Default Template Data"):
    st.session_state.financial_data = pd.DataFrame(default_data, index=months).T
    st.session_state.item_types = default_item_types.copy()
    st.rerun()

# --- CALCULATING TOTALS & GROWTH ---
# Dynamically separate assets vs liabilities based on user-managed categories
assets_keys = [k for k, t in st.session_state.item_types.items() if t in ["Cash", "Investments", "Retirement/EPF", "Properties", "Other Assets"]]
liabilities_keys = [k for k, t in st.session_state.item_types.items() if t in ["Short-Term Debts", "Long-Term Debts", "Other Liabilities"]]

# Calculate sums for every month
total_assets_series = df.loc[assets_keys].sum() if assets_keys else pd.Series(0.0, index=months)
total_liabs_series = df.loc[liabilities_keys].sum() if liabilities_keys else pd.Series(0.0, index=months)
net_worth_series = total_assets_series - total_liabs_series

# Locate current active month (latest month with inputs / non-zero values)
active_month_index = 0
for i, m in enumerate(months):
    if total_assets_series[m] > 0:
        active_month_index = i

current_month = months[active_month_index]
current_net_worth = net_worth_series[current_month]
current_assets = total_assets_series[current_month]
current_liabs = total_liabs_series[current_month]

# Start reference calculations
start_month = months[0]
start_net_worth = net_worth_series[start_month]

# Absolute and Percentage Growth
net_worth_growth_abs = current_net_worth - start_net_worth
net_worth_growth_pct = (net_worth_growth_abs / start_net_worth) * 100 if start_net_worth != 0 else 0


# ==========================================
# PAGE VIEW 1: INTERACTIVE DASHBOARD VIEW
# ==========================================
if selected_tab == "🏆 Interactive Dashboard":
    st.markdown("### Financial Overview Tracker")
    
    # Custom Premium Highlight Card Layout
    h_col1, h_col2, h_col3 = st.columns(3)
    
    with h_col1:
        st.markdown(f"""
        <div style="background-color: #0f172a; padding: 20px; border-radius: 12px; border: 1px solid #1e293b; color: white;">
            <p style="margin: 0; font-size: 0.9rem; text-transform: uppercase; letter-spacing: 0.05em; color: #94a3b8;">Current Active Net Worth ({current_month})</p>
            <h1 style="margin: 5px 0; font-size: 2.3rem; font-weight: 800; color: #2ecc71;">{currency} {current_net_worth:,.2f}</h1>
            <p style="margin: 0; font-size: 0.85rem; color: #64748b;">Assets: {currency}{current_assets:,.2f} | Debt: {currency}{current_liabs:,.2f}</p>
        </div>
        """, unsafe_allow_html=True)
        
    with h_col2:
        st.markdown(f"""
        <div style="background-color: #0f172a; padding: 20px; border-radius: 12px; border: 1px solid #1e293b; color: white;">
            <p style="margin: 0; font-size: 0.9rem; text-transform: uppercase; letter-spacing: 0.05em; color: #94a3b8;">Your Annual Growth (Since START)</p>
            <h1 style="margin: 5px 0; font-size: 2.3rem; font-weight: 800; color: #3498db;">+{currency} {net_worth_growth_abs:,.2f}</h1>
            <p style="margin: 0; font-size: 0.85rem; color: #64748b;">A positive progression of your financial timeline.</p>
        </div>
        """, unsafe_allow_html=True)
        
    with h_col3:
        st.markdown(f"""
        <div style="background-color: #0f172a; padding: 20px; border-radius: 12px; border: 1px solid #1e293b; color: white;">
            <p style="margin: 0; font-size: 0.9rem; text-transform: uppercase; letter-spacing: 0.05em; color: #94a3b8;">Growth Percentage</p>
            <h1 style="margin: 5px 0; font-size: 2.3rem; font-weight: 800; color: #f1c40f;">{net_worth_growth_pct:,.2f}%</h1>
            <p style="margin: 0; font-size: 0.85rem; color: #64748b;">Assets to Debt Ratio: {((current_assets / current_liabs) if current_liabs > 0 else 0):,.2f}x</p>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    # Graphical Charts Row 1
    g_col1, g_col2 = st.columns(2)
    
    with g_col1:
        st.markdown("#### 📈 Net Worth Progress Timeline")
        # Build DataFrame for bar-chart plotting
        nw_df = pd.DataFrame({
            "Month": months,
            "Net Worth": net_worth_series.values
        })
        fig_nw = px.bar(
            nw_df, x="Month", y="Net Worth",
            text="Net Worth",
            color_discrete_sequence=["#16a34a"],
            height=380
        )
        fig_nw.update_traces(texttemplate=f'{currency}%{{y:,.0f}}', textposition='outside')
        fig_nw.update_layout(
            margin=dict(l=10, r=10, t=10, b=10),
            yaxis_title=None, xaxis_title=None,
            plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)"
        )
        st.plotly_chart(fig_nw, use_container_width=True)
        
    with g_col2:
        st.markdown("#### ⚖️ Assets vs Liabilities Progression")
        fig_trend = go.Figure()
        fig_trend.add_trace(go.Scatter(
            x=months, y=total_assets_series.values,
            mode='lines+markers', name='Total Assets',
            line=dict(color='#2ecc71', width=3),
            fill='tozeroy', fillcolor='rgba(46, 204, 113, 0.1)'
        ))
        fig_trend.add_trace(go.Scatter(
            x=months, y=total_liabs_series.values,
            mode='lines+markers', name='Total Liabilities',
            line=dict(color='#e74c3c', width=3),
            fill='tozeroy', fillcolor='rgba(231, 76, 60, 0.05)'
        ))
        fig_trend.update_layout(
            margin=dict(l=10, r=10, t=10, b=10),
            yaxis_title=None, xaxis_title=None,
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
            height=380
        )
        st.plotly_chart(fig_trend, use_container_width=True)

    st.divider()

    # Graphical Charts Row 2 (Breakdown Analysis)
    c_col1, c_col2 = st.columns(2)
    
    with c_col1:
        st.markdown(f"#### 🍩 Asset Distribution Breakdown ({current_month})")
        
        # User selection to toggle detailed account vs macro class views!
        view_mode_assets = st.radio("Asset Chart View:", ["By Macro Category Class", "By Individual Accounts"], horizontal=True, key="asset_chart_toggle")
        
        if view_mode_assets == "By Macro Category Class":
            # Grouping dynamically by active groups
            group_sums = {}
            for key in assets_keys:
                grp = st.session_state.item_types.get(key, "Other Assets")
                val = df.at[key, current_month]
                if val > 0:
                    group_sums[grp] = group_sums.get(grp, 0.0) + val
            
            if group_sums:
                df_pie = pd.DataFrame(list(group_sums.items()), columns=["Category Class", "Amount"])
                fig_pie = px.pie(
                    df_pie, values="Amount", names="Category Class",
                    hole=0.45, color_discrete_sequence=px.colors.qualitative.Pastel
                )
                fig_pie.update_layout(margin=dict(l=10, r=10, t=10, b=10), height=320)
                st.plotly_chart(fig_pie, use_container_width=True)
            else:
                st.info("No active Asset values to display.")
        else:
            asset_distribution = {k: df.at[k, current_month] for k in assets_keys if df.at[k, current_month] > 0}
            if asset_distribution:
                df_pie = pd.DataFrame(list(asset_distribution.items()), columns=["Account", "Amount"])
                fig_pie = px.pie(
                    df_pie, values="Amount", names="Account",
                    hole=0.45, color_discrete_sequence=px.colors.qualitative.Pastel
                )
                fig_pie.update_layout(margin=dict(l=10, r=10, t=10, b=10), height=320)
                st.plotly_chart(fig_pie, use_container_width=True)
            else:
                st.info("No active Asset values to display.")

    with c_col2:
        st.markdown(f"#### 🧾 Liabilities Class Breakdown ({current_month})")
        
        view_mode_liabs = st.radio("Liability Chart View:", ["By Macro Category Class", "By Individual Accounts"], horizontal=True, key="liab_chart_toggle")
        
        if view_mode_liabs == "By Macro Category Class":
            group_sums = {}
            for key in liabilities_keys:
                grp = st.session_state.item_types.get(key, "Other Liabilities")
                val = df.at[key, current_month]
                if val > 0:
                    group_sums[grp] = group_sums.get(grp, 0.0) + val
            
            if group_sums:
                df_liab_pie = pd.DataFrame(list(group_sums.items()), columns=["Category Class", "Amount"])
                fig_liab_pie = px.pie(
                    df_liab_pie, values="Amount", names="Category Class",
                    hole=0.45, color_discrete_sequence=px.colors.qualitative.Safe
                )
                fig_liab_pie.update_layout(margin=dict(l=10, r=10, t=10, b=10), height=320)
                st.plotly_chart(fig_liab_pie, use_container_width=True)
            else:
                st.info("No active Liability values to display.")
        else:
            liab_distribution = {k: df.at[k, current_month] for k in liabilities_keys if df.at[k, current_month] > 0}
            if liab_distribution:
                df_liab_pie = pd.DataFrame(list(liab_distribution.items()), columns=["Account", "Amount"])
                fig_liab_pie = px.pie(
                    df_liab_pie, values="Amount", names="Account",
                    hole=0.45, color_discrete_sequence=px.colors.qualitative.Safe
                )
                fig_liab_pie.update_layout(margin=dict(l=10, r=10, t=10, b=10), height=320)
                st.plotly_chart(fig_liab_pie, use_container_width=True)
            else:
                st.info("No active Liability values to display.")

# ==========================================
# PAGE VIEW 2: MONTH-BY-MONTH DATA EDITOR (WITH INTEGRATED CATEGORY MANAGER)
# ==========================================
elif selected_tab == "✏️ Update Monthly Figures":
    st.markdown("### ✏️ Update Financial Entry Logs")
    st.markdown("Your categories are grouped below. Select a month and expand any classification drawer to adjust figures.")
    
    # -------------------------------------------------------------
    # INTEGRATED ACCOUNT & CATEGORY MANAGER (IN COLLAPSIBLE DRAWER)
    # -------------------------------------------------------------
    with st.expander("⚙️ Manage Accounts & Categories (Add or Delete Items)", expanded=False):
        st.markdown("Easily add new cash accounts, cards, and investments, or remove them from your active balance sheet instantly.")
        col_add, col_remove = st.columns(2)
        
        with col_add:
            st.markdown("##### ➕ Add New Account/Category")
            new_name = st.text_input("Name of Account/Asset/Debt (e.g., 'Bitcoin Wallet', 'My Home'):", key="add_cat_input")
            new_group = st.selectbox(
                "Account Classification Group:",
                ["Cash", "Investments", "Retirement/EPF", "Properties", "Other Assets", "Short-Term Debts", "Long-Term Debts", "Other Liabilities"],
                key="add_cat_select"
            )
            
            if st.button("🚀 Add New Category", use_container_width=True, key="add_cat_btn"):
                cleaned_name = new_name.strip()
                if not cleaned_name:
                    st.error("Please enter a valid category name!")
                elif cleaned_name in st.session_state.financial_data.index:
                    st.error("An account with this name already exists in your table.")
                else:
                    # 1. Create a row of zero inputs mapping across all months
                    new_row = pd.Series([0.0] * len(months), index=months, name=cleaned_name)
                    # 2. Add it directly into our persistent DataFrame
                    st.session_state.financial_data = pd.concat([st.session_state.financial_data, pd.DataFrame([new_row])])
                    # 3. Add classification
                    st.session_state.item_types[cleaned_name] = new_group
                    st.success(f"Successfully added '{cleaned_name}' to your dashboard as a {new_group}!")
                    st.rerun()
                    
        with col_remove:
            st.markdown("##### 🗑️ Remove Existing Account/Category")
            # Display list of user's active custom keys
            available_categories = list(st.session_state.item_types.keys())
            category_to_delete = st.selectbox("Select Account/Category to Delete:", available_categories, key="del_cat_select")
            
            st.warning("⚠️ Warning: Deleting an item will permanently remove it from the sheet and wipe out any of its recorded history!")
            
            if st.button("🔥 Permanently Delete Category", use_container_width=True, key="del_cat_btn"):
                if category_to_delete:
                    # 1. Remove the key from item classifications
                    st.session_state.item_types.pop(category_to_delete)
                    # 2. Drop the row from the data table
                    st.session_state.financial_data = st.session_state.financial_data.drop(category_to_delete)
                    st.success(f"Successfully deleted '{category_to_delete}' from your tracker.")
                    st.rerun()
                    
    st.divider()
    
    # Month Picker
    selected_month = st.selectbox("Select Target Month to Edit:", months)
    
    st.divider()
    
    # Split layout for asset categories & liability categories inside the form editor
    with st.form(key=f"editor_form_{selected_month}"):
        form_col1, form_col2 = st.columns(2)
        
        updated_assets = {}
        updated_liabs = {}
        
        with form_col1:
            st.markdown("#### 🏦 Cash & Asset Inputs (By Category)")
            
            # Group A: Cash
            cash_items = [k for k in assets_keys if st.session_state.item_types.get(k) == "Cash"]
            if cash_items:
                with st.expander("💵 Cash & Liquid Accounts", expanded=True):
                    for item in cash_items:
                        current_val = float(df.at[item, selected_month]) if item in df.index else 0.0
                        updated_assets[item] = st.number_input(
                            f"{item} ({currency})", value=current_val, step=100.0, key=f"edit_asset_{item}"
                        )
            
            # Group B: Investments
            inv_items = [k for k in assets_keys if st.session_state.item_types.get(k) == "Investments"]
            if inv_items:
                with st.expander("📈 Long-Term Investments", expanded=True):
                    for item in inv_items:
                        current_val = float(df.at[item, selected_month]) if item in df.index else 0.0
                        updated_assets[item] = st.number_input(
                            f"{item} ({currency})", value=current_val, step=100.0, key=f"edit_asset_{item}"
                        )
            
            # Group C: Retirement
            ret_items = [k for k in assets_keys if st.session_state.item_types.get(k) == "Retirement/EPF"]
            if ret_items:
                with st.expander("👴 Retirement Savings (EPF)", expanded=True):
                    for item in ret_items:
                        current_val = float(df.at[item, selected_month]) if item in df.index else 0.0
                        updated_assets[item] = st.number_input(
                            f"{item} ({currency})", value=current_val, step=100.0, key=f"edit_asset_{item}"
                        )
            
            # Group D: Properties & Others
            other_ast_items = [k for k in assets_keys if st.session_state.item_types.get(k) in ["Properties", "Other Assets"]]
            if other_ast_items:
                with st.expander("🏡 Real Estate & Tangible Assets", expanded=False):
                    for item in other_ast_items:
                        current_val = float(df.at[item, selected_month]) if item in df.index else 0.0
                        updated_assets[item] = st.number_input(
                            f"{item} ({currency})", value=current_val, step=100.0, key=f"edit_asset_{item}"
                        )
                        
        with form_col2:
            st.markdown("#### 💳 Outstanding Liabilities (By Category)")
            
            # Group A: Short-Term Debts
            st_debt_items = [k for k in liabilities_keys if st.session_state.item_types.get(k) == "Short-Term Debts"]
            if st_debt_items:
                with st.expander("📱 Short-Term Liabilities & Bills", expanded=True):
                    for item in st_debt_items:
                        current_val = float(df.at[item, selected_month]) if item in df.index else 0.0
                        updated_liabs[item] = st.number_input(
                            f"{item} ({currency})", value=current_val, step=100.0, key=f"edit_liab_{item}"
                        )
            
            # Group B: Long-Term Debts
            lt_debt_items = [k for k in liabilities_keys if st.session_state.item_types.get(k) == "Long-Term Debts"]
            if lt_debt_items:
                with st.expander("🏠 Long-Term Structured Debts", expanded=True):
                    for item in lt_debt_items:
                        current_val = float(df.at[item, selected_month]) if item in df.index else 0.0
                        updated_liabs[item] = st.number_input(
                            f"{item} ({currency})", value=current_val, step=100.0, key=f"edit_liab_{item}"
                        )
            
            # Group C: Other Liabilities
            other_liab_items = [k for k in liabilities_keys if st.session_state.item_types.get(k) == "Other Liabilities"]
            if other_liab_items:
                with st.expander("🛑 Other Miscellaneous Debts", expanded=False):
                    for item in other_liab_items:
                        current_val = float(df.at[item, selected_month]) if item in df.index else 0.0
                        updated_liabs[item] = st.number_input(
                            f"{item} ({currency})", value=current_val, step=100.0, key=f"edit_liab_{item}"
                        )
                
        # Submit updates
        submit_btn = st.form_submit_button(label="💾 Save Values and Rerun Calculations")
        
        if submit_btn:
            # Inject form values back into active state dataframe
            for k, v in updated_assets.items():
                st.session_state.financial_data.at[k, selected_month] = v
            for k, v in updated_liabs.items():
                st.session_state.financial_data.at[k, selected_month] = v
            
            st.success(f"Successfully recorded all financial logging adjustments for {selected_month}!")
            st.rerun()

# ==========================================
# PAGE VIEW 3: COMPLETE SPREADSHEET MATRIX VIEW (SORTED BY CATEGORY)
# ==========================================
elif selected_tab == "📋 Spreadsheet Database":
    st.markdown("### 📋 Full Financial Ledger Spreadsheet Matrix")
    st.markdown("Your entire asset portfolio and liabilities organized beautifully by dynamic classes.")
    
    # Render interactive DataFrame matching the structures of your spreadsheet
    display_df = df.copy()
    
    # Inject temporary sorting class column
    display_df['Class'] = display_df.index.map(st.session_state.item_types)
    
    # Establish dynamic sorting list order
    group_order = [
        "Cash", "Investments", "Retirement/EPF", "Properties", "Other Assets", 
        "Short-Term Debts", "Long-Term Debts", "Other Liabilities"
    ]
    display_df['Class'] = pd.Categorical(display_df['Class'], categories=group_order, ordered=True)
    display_df = display_df.sort_values('Class')
    
    # Pull Class column to the front visually
    cols = ['Class'] + [col for col in display_df.columns if col != 'Class']
    display_df = display_df[cols]
    
    # Append calculated Net Worth, Total Assets, Total Liabilities summaries dynamically
    summary_rows = pd.DataFrame({
        "Total Assets": total_assets_series,
        "Total Liabilities": total_liabs_series,
        "Calculated Net Worth": net_worth_series
    }).T
    summary_rows['Class'] = "📊 Summary Header"
    summary_rows = summary_rows[cols]
    
    ledger_matrix = pd.concat([summary_rows, display_df])
    
    # Style and format cell numerical data for professional visualization
    # We must skip formatting the string 'Class' column in our lambda statement
    formatted_matrix = ledger_matrix.style.format(lambda val: f"{val:,.2f}" if isinstance(val, (int, float)) else str(val))
    
    # Display the grid on the screen
    st.dataframe(formatted_matrix, use_container_width=True, height=600)
    
    # Export options
    csv_data = ledger_matrix.to_csv().encode('utf-8')
    st.download_button(
        label="📥 Download Full Financial Matrix as CSV",
        data=csv_data,
        file_name="My_Personal_Net_Worth_Tracker.csv",
        mime="text/csv"
    )
