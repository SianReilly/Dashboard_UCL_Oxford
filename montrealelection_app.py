import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Set the page title
st.set_page_config(page_title="2013 Montreal Election Analysis", layout="wide")

# Remove whitespace and Streamlit branding
st.markdown("""
<style>
header.stAppHeader {
    background-color: transparent;
}
section.stMain .block-container {
    padding-top: 0rem;
    z-index: 1;
}
</style>""", unsafe_allow_html=True)

hide_streamlit_style = """
                <style>
                div[data-testid="stToolbar"] {
                visibility: hidden;
                height: 0%;
                position: fixed;
                }
                div[data-testid="stDecoration"] {
                visibility: hidden;
                height: 0%;
                position: fixed;
                }
                div[data-testid="stStatusWidget"] {
                visibility: hidden;
                height: 0%;
                position: fixed;
                }
                #MainMenu {
                visibility: hidden;
                height: 0%;
                }
                header {
                visibility: hidden;
                height: 0%;
                }
                footer {
                visibility: hidden;
                height: 0%;
                }
                </style>
                """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# Custom CSS for Dark Green Background and White Text
st.markdown(
    """
    <style>
        .stApp {
            background-color: #013220;
            color: white;
        }
        div.stMultiSelect label, div.stSelectbox label {
            color: white !important;
        }
        div[data-baseweb="tag"] {
            background-color: green !important;
            color: yellow !important;
        }
        /* Make plot backgrounds transparent to match theme */
        .js-plotly-plot {
            background-color: transparent !important;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Load election data
election = px.data.election()

# Calculate metrics
winner_counts = election['winner'].value_counts()
total_votes = {
    'Coderre': election['Coderre'].sum(),
    'Bergeron': election['Bergeron'].sum(),
    'Joly': election['Joly'].sum()
}
total_all_votes = sum(total_votes.values())

# Consistent color scheme
colors = {'Coderre': '#6366F1', 'Bergeron': '#EF4444', 'Joly': '#10B981'}
candidates_order = ['Coderre', 'Bergeron', 'Joly']

# Title
st.markdown("<h1 style='text-align: center; color: white;'>2013 Montreal Mayoral Election</h1>", unsafe_allow_html=True)

st.markdown(
    """
    <p style='text-align: center; color: white; font-size: 24px;'>
    by Siân Reilly
    </p>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <p style='text-align: center; color: white; font-size: 18px; max-width: 900px; margin: 0 auto; line-height: 1.6;'>
    An analysis of how Denis Coderre won the 2013 Montreal mayoral election despite receiving only 38% of the popular vote. 
    This dashboard explores the electoral dynamics across 58 districts, revealing how vote splitting between Richard Bergeron 
    and Mélanie Joly enabled Coderre's victory—a classic example of the spoiler effect in plurality voting systems.
    </p>
    """,
    unsafe_allow_html=True
)

st.markdown("<br>", unsafe_allow_html=True)

# Interactive Filters
col1, col2 = st.columns([1, 1])
with col1:
    winner_filter = st.multiselect(
        "Filter by Winner", 
        options=candidates_order, 
        default=candidates_order,
        key="winner_filter"
    )
    
with col2:
    result_filter = st.multiselect(
        "Filter by Result Type",
        options=['majority', 'plurality'],
        default=['majority', 'plurality'],
        key="result_filter"
    )

# Filter data
filtered_election = election[
    (election['winner'].isin(winner_filter)) & 
    (election['result'].isin(result_filter))
]

# Recalculate metrics for filtered data
filtered_winner_counts = filtered_election['winner'].value_counts()
filtered_total_votes = {
    'Coderre': filtered_election['Coderre'].sum(),
    'Bergeron': filtered_election['Bergeron'].sum(),
    'Joly': filtered_election['Joly'].sum()
}

st.markdown("<br>", unsafe_allow_html=True)

# ============ CHART 1: Districts Won vs Popular Vote (Your existing chart) ============
fig1 = make_subplots(
    rows=2, cols=2,
    specs=[[{"type": "pie"}, {"type": "pie"}],
           [{"type": "bar", "colspan": 2}, None]],
    subplot_titles=("<b style='color:white;'>Districts Won</b> (of 58)", 
                    "<b style='color:white;'>Popular Vote Share</b>",
                    "<b style='color:white;'>Comparison: Districts Won vs Popular Vote</b>"),
    vertical_spacing=0.15,
    horizontal_spacing=0.12
)

# Districts Won Pie Chart
fig1.add_trace(go.Pie(
    labels=[c for c in candidates_order if c in winner_filter],
    values=[filtered_winner_counts.get(c, 0) for c in candidates_order if c in winner_filter],
    hole=0.4,
    marker=dict(colors=[colors[c] for c in candidates_order if c in winner_filter]),
    texttemplate='<b>%{label}</b><br>%{value}<br>(%{percent})',
    textfont=dict(size=12, family='Arial, sans-serif', color='white'),
    hovertemplate='<b>%{label}</b><br>Districts: %{value}<br>%{percent}<extra></extra>',
    showlegend=False
), row=1, col=1)

# Popular Vote Pie Chart
fig1.add_trace(go.Pie(
    labels=[c for c in candidates_order if c in winner_filter],
    values=[filtered_total_votes[c] for c in candidates_order if c in winner_filter],
    hole=0.4,
    marker=dict(colors=[colors[c] for c in candidates_order if c in winner_filter]),
    texttemplate='<b>%{label}</b><br>%{value:,}<br>(%{percent})',
    textfont=dict(size=12, family='Arial, sans-serif', color='white'),
    hovertemplate='<b>%{label}</b><br>Votes: %{value:,}<br>%{percent}<extra></extra>',
    showlegend=False
), row=1, col=2)

# Bar chart
for candidate in [c for c in candidates_order if c in winner_filter]:
    # Districts
    fig1.add_trace(go.Bar(
        name=candidate,
        x=['Districts Won'],
        y=[filtered_winner_counts.get(candidate, 0)],
        marker_color=colors[candidate],
        text=[f"<b>{filtered_winner_counts.get(candidate, 0)}</b>"],
        textposition='outside',
        textfont=dict(size=13, color='white'),
        showlegend=True,
        legendgroup=candidate
    ), row=2, col=1)
    
    # Popular Vote
    fig1.add_trace(go.Bar(
        name=candidate,
        x=['Popular Vote (thousands)'],
        y=[filtered_total_votes[candidate]/1000],
        marker_color=colors[candidate],
        text=[f"<b>{filtered_total_votes[candidate]:,}</b>"],
        textposition='outside',
        textfont=dict(size=13, color='white'),
        showlegend=False,
        legendgroup=candidate
    ), row=2, col=1)

fig1.update_layout(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font=dict(color='white', family='Arial'),
    height=650,
    showlegend=True,
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.15,
        xanchor="center",
        x=0.5,
        font=dict(color='white', size=12)
    ),
    margin=dict(l=40, r=40, t=80, b=80)
)

fig1.update_yaxes(
    gridcolor='rgba(255,255,255,0.1)',
    title_font=dict(color='white'),
    tickfont=dict(color='white'),
    row=2, col=1
)

fig1.update_xaxes(
    title_font=dict(color='white'),
    tickfont=dict(color='white'),
    row=2, col=1
)

for annotation in fig1['layout']['annotations']:
    annotation['font'] = dict(size=14, color='white')

# ============ CHART 2: Sankey Diagram ============
result_winner_counts = filtered_election.groupby(['result', 'winner']).size().reset_index(name='count')

result_labels = [
    '<b>Plurality</b><br>(< 50% votes)',
    '<b>Majority</b><br>(> 50% votes)'
]
winner_labels = [f'<b>{c}</b>' for c in candidates_order if c in winner_filter]
all_labels = result_labels + winner_labels

result_mapping = {'plurality': 0, 'majority': 1}
winner_mapping = {c: i + 2 for i, c in enumerate([c for c in candidates_order if c in winner_filter])}

source = [result_mapping[row['result']] for _, row in result_winner_counts.iterrows()]
target = [winner_mapping[row['winner']] for _, row in result_winner_counts.iterrows()]
value = result_winner_counts['count'].tolist()

colors_sankey = {
    'Coderre': 'rgba(99, 102, 241, 0.4)',
    'Bergeron': 'rgba(239, 68, 68, 0.4)',
    'Joly': 'rgba(16, 185, 129, 0.4)'
}

link_colors = [colors_sankey[result_winner_counts.iloc[i]['winner']] for i in range(len(source))]

fig2 = go.Figure(data=[go.Sankey(
    node=dict(
        pad=20,
        thickness=25,
        line=dict(color="white", width=0.5),
        label=all_labels,
        color=['#94A3B8', '#94A3B8'] + [colors[c] for c in candidates_order if c in winner_filter],
    ),
    link=dict(
        source=source,
        target=target,
        value=value,
        color=link_colors
    )
)])

fig2.update_layout(
    title={
        'text': "<b>How Candidates Won: Majority vs Plurality</b>",
        'x': 0.5,
        'xanchor': 'center',
        'font': {'size': 18, 'color': 'white'}
    },
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font=dict(color='white', size=12),
    height=500,
    margin=dict(l=20, r=20, t=60, b=40)
)

# ============ CHART 3: Vote Margin Analysis ============
election_margins = filtered_election.copy()
vote_cols = ['Coderre', 'Bergeron', 'Joly']
election_margins['first_place'] = election_margins[vote_cols].max(axis=1)
election_margins['second_place'] = election_margins[vote_cols].apply(
    lambda row: sorted(row, reverse=True)[1], axis=1
)
election_margins['margin'] = election_margins['first_place'] - election_margins['second_place']
election_margins['margin_pct'] = (election_margins['margin'] / election_margins['total']) * 100

fig3 = px.scatter(
    election_margins,
    x='total',
    y='margin_pct',
    color='winner',
    color_discrete_map=colors,
    size='margin',
    hover_data=['district', 'result'],
    title='<b>Victory Margins Across Districts</b>',
    labels={'total': 'Total Votes in District', 'margin_pct': 'Victory Margin (%)'}
)

fig3.update_layout(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font=dict(color='white'),
    height=450,
    title_x=0.5,
    title_font=dict(size=18),
    xaxis=dict(
        gridcolor='rgba(255,255,255,0.1)',
        title_font=dict(color='white'),
        tickfont=dict(color='white')
    ),
    yaxis=dict(
        gridcolor='rgba(255,255,255,0.1)',
        title_font=dict(color='white'),
        tickfont=dict(color='white')
    ),
    legend=dict(font=dict(color='white'))
)

# ============ CHART 4: District Performance Breakdown ============
performance_data = []
for candidate in candidates_order:
    if candidate in winner_filter:
        wins = filtered_election[filtered_election['winner'] == candidate]
        performance_data.append({
            'Candidate': candidate,
            'Districts Won': len(wins),
            'Avg Votes': wins[candidate].mean(),
            'Total Votes': wins[candidate].sum(),
            'Avg Margin': wins.apply(lambda row: row[candidate] - sorted([row['Coderre'], row['Bergeron'], row['Joly']], reverse=True)[1], axis=1).mean()
        })

perf_df = pd.DataFrame(performance_data)

fig4 = go.Figure()
for i, candidate in enumerate(perf_df['Candidate']):
    fig4.add_trace(go.Bar(
        name=candidate,
        x=['Districts Won', 'Avg Votes per District', 'Avg Victory Margin'],
        y=[
            perf_df.loc[i, 'Districts Won'],
            perf_df.loc[i, 'Avg Votes'] / 100,  # Scale down for visibility
            perf_df.loc[i, 'Avg Margin'] / 100   # Scale down for visibility
        ],
        marker_color=colors[candidate],
        text=[
            f"{perf_df.loc[i, 'Districts Won']:.0f}",
            f"{perf_df.loc[i, 'Avg Votes']:.0f}",
            f"{perf_df.loc[i, 'Avg Margin']:.0f}"
        ],
        textposition='outside',
        textfont=dict(color='white', size=12),
        hovertemplate=f'<b>{candidate}</b><br>%{{x}}: %{{text}}<extra></extra>'
    ))

fig4.update_layout(
    title={
        'text': '<b>Candidate Performance Metrics</b>',
        'x': 0.5,
        'font': {'size': 18, 'color': 'white'}
    },
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font=dict(color='white'),
    height=450,
    xaxis=dict(
        tickfont=dict(color='white'),
        showgrid=False
    ),
    yaxis=dict(
        title='Scaled Values (÷100 for visibility)',
        gridcolor='rgba(255,255,255,0.1)',
        tickfont=dict(color='white'),
        title_font=dict(color='white')
    ),
    legend=dict(font=dict(color='white')),
    barmode='group'
)

# ============ Display Charts in 2x2 Grid ============
col1, col2 = st.columns(2)

with col1:
    st.plotly_chart(fig1, use_container_width=True)
    st.markdown("""
        <p style='color: white; font-size: 14px; line-height: 1.6;'>
        <b>The Electoral Paradox:</b> Coderre won 50% of districts but only 38% of the popular vote. 
        This visualization reveals the stark difference between district victories and overall voter support—
        demonstrating how Canada's first-past-the-post system can produce winners without majority backing.
        </p>
    """, unsafe_allow_html=True)
    
    st.plotly_chart(fig3, use_container_width=True)
    st.markdown("""
        <p style='color: white; font-size: 14px; line-height: 1.6;'>
        <b>Competitive Races:</b> Larger bubbles indicate bigger victory margins. Many of Coderre's wins 
        (blue points) cluster at lower margins, showing he often won by slim pluralities. Bergeron's wins 
        tend to be more decisive, appearing higher on the margin scale.
        </p>
    """, unsafe_allow_html=True)

with col2:
    st.plotly_chart(fig2, use_container_width=True)
    st.markdown("""
        <p style='color: white; font-size: 14px; line-height: 1.6;'>
        <b>The Split Vote Effect:</b> This flow diagram shows that Coderre won most districts by plurality 
        (less than 50% support), while Bergeron achieved more majority victories. The opposition vote split 
        between Bergeron and Joly was crucial to Coderre's success—a textbook spoiler effect scenario.
        </p>
    """, unsafe_allow_html=True)
    
    st.plotly_chart(fig4, use_container_width=True)
    st.markdown("""
        <p style='color: white; font-size: 14px; line-height: 1.6;'>
        <b>Performance Comparison:</b> While Coderre won the most districts, Bergeron averaged more votes 
        per district won and had larger average victory margins—indicating stronger support intensity in 
        his winning districts compared to Coderre's broader but shallower appeal.
        </p>
    """, unsafe_allow_html=True)

# Summary Statistics
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: white;'>Key Electoral Statistics</h3>", unsafe_allow_html=True)

stat_col1, stat_col2, stat_col3 = st.columns(3)

with stat_col1:
    st.markdown(f"""
        <div style='text-align: center; padding: 20px; background-color: rgba(99, 102, 241, 0.2); border-radius: 10px;'>
            <h2 style='color: #6366F1; margin: 0;'>{winner_counts.get('Coderre', 0)}</h2>
            <p style='color: white; margin: 5px 0;'>Districts Won by Coderre</p>
            <p style='color: white; font-size: 12px;'>{total_votes['Coderre']:,} total votes (38.2%)</p>
        </div>
    """, unsafe_allow_html=True)

with stat_col2:
    st.markdown(f"""
        <div style='text-align: center; padding: 20px; background-color: rgba(239, 68, 68, 0.2); border-radius: 10px;'>
            <h2 style='color: #EF4444; margin: 0;'>{winner_counts.get('Bergeron', 0)}</h2>
            <p style='color: white; margin: 5px 0;'>Districts Won by Bergeron</p>
            <p style='color: white; font-size: 12px;'>{total_votes['Bergeron']:,} total votes (30.3%)</p>
        </div>
    """, unsafe_allow_html=True)

with stat_col3:
    st.markdown(f"""
        <div style='text-align: center; padding: 20px; background-color: rgba(16, 185, 129, 0.2); border-radius: 10px;'>
            <h2 style='color: #10B981; margin: 0;'>{winner_counts.get('Joly', 0)}</h2>
            <p style='color: white; margin: 5px 0;'>Districts Won by Joly</p>
            <p style='color: white; font-size: 12px;'>{total_votes['Joly']:,} total votes (31.5%)</p>
        </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown(
    """
    <style>
        .footer {
            position: static;
            bottom: 0;
            left: 0;
            width: 100%;
            text-align: center;
            font-size: 14px;
            color: rgba(255, 255, 255, 0.4);
            background-color: #013220;
            padding: 20px 0;
            margin-top: 40px;
            z-index: 1000;
        }
    </style>
    <div class="footer">
        © 2025 Montreal Election Analysis Dashboard | Data Source: Plotly Express<br>
        Analysis following Edward Tufte's principles of data visualization
    </div>
    """,
    unsafe_allow_html=True
)
