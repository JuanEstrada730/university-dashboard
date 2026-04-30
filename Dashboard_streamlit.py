import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Student Dashboard", layout="wide")
st.title("University Student Data Dashboard")
st.write("Analysis of admissions, retention and student satisfaction")

# load data
df = pd.read_csv("university_student_data.csv")

# filters in the sidebar
st.sidebar.header("Filters")

año = st.sidebar.selectbox("Select the year", options=["All"] + sorted(df["Year"].unique().tolist()))
term = st.sidebar.selectbox("Select the term", options=["All", "Spring", "Fall"])
dept = st.sidebar.selectbox("Select the department", options=["All", "Engineering", "Business", "Arts", "Science"])

# apply filters
df_filtrado = df.copy()

if año != "All":
    df_filtrado = df_filtrado[df_filtrado["Year"] == int(año)]

if term != "All":
    df_filtrado = df_filtrado[df_filtrado["Term"] == term]

# KPI cards
st.subheader("General indicators")
col1, col2, col3 = st.columns(3)

col1.metric("Average Retention", f"{df_filtrado['Retention Rate (%)'].mean():.1f}%")
col2.metric("Average Satisfaction", f"{df_filtrado['Student Satisfaction (%)'].mean():.1f}%")
col3.metric("Total Enrolled", f"{int(df_filtrado['Enrolled'].sum())}")

st.divider()

# chart 1 - retention trend (line chart)
st.subheader("Retention Rate Trend")

retencion = df_filtrado.groupby("Year")["Retention Rate (%)"].mean().reset_index()

fig1, ax1 = plt.subplots(figsize=(10, 4))
sns.lineplot(data=retencion, x="Year", y="Retention Rate (%)", marker="o", ax=ax1, color="steelblue")
ax1.set_title("Student retention by year")
ax1.set_xlabel("Year")
ax1.set_ylabel("Retention (%)")
ax1.set_xticks(retencion["Year"])
plt.tight_layout()
st.pyplot(fig1)

st.divider()

# chart 2 - satisfaction by year (bar chart)
st.subheader("Student Satisfaction by Year")

satisfaccion = df_filtrado.groupby("Year")["Student Satisfaction (%)"].mean().reset_index()

fig2, ax2 = plt.subplots(figsize=(10, 4))
ax2.bar(satisfaccion["Year"], satisfaccion["Student Satisfaction (%)"], color="seagreen", width=0.5)
ax2.set_title("Student satisfaction by year")
ax2.set_xlabel("Year")
ax2.set_ylabel("Satisfaction (%)")
ax2.set_ylim(70, 95)
plt.tight_layout()
st.pyplot(fig2)

st.divider()

# chart 3 - spring vs fall comparison
st.subheader("Spring vs Fall Comparison")

# here we use the full df filtered by year only, not by term
df_term = df.copy()
if año != "All":
    df_term = df_term[df_term["Year"] == int(año)]

comp = df_term.groupby("Term")[["Enrolled", "Retention Rate (%)", "Student Satisfaction (%)"]].mean().reset_index()

fig3, ax3 = plt.subplots(figsize=(8, 4))
bars = ax3.bar(comp["Term"], comp["Enrolled"], color=["steelblue", "coral"], width=0.4)
ax3.set_title("Enrolled students by term")
ax3.set_xlabel("Term")
ax3.set_ylabel("Enrolled")
for bar in bars:
    h = bar.get_height()
    ax3.text(bar.get_x() + bar.get_width()/2, h + 1, f'{h:.0f}', ha='center', fontsize=10)
plt.tight_layout()
st.pyplot(fig3)

st.divider()

# chart 4 - department pie chart
st.subheader("Enrolled Students Distribution by Department")

cols_dept = {
    "Engineering": "Engineering Enrolled",
    "Business": "Business Enrolled",
    "Arts": "Arts Enrolled",
    "Science": "Science Enrolled"
}

totales = df_filtrado[list(cols_dept.values())].sum()
labels = list(cols_dept.keys())

fig4, ax4 = plt.subplots(figsize=(5, 5))
ax4.pie(totales, labels=labels, autopct="%1.1f%%", startangle=90)
ax4.set_title("Distribution by department")
col_izq, _ = st.columns([1, 1])
with col_izq:
    st.pyplot(fig4)

st.divider()

# table with filtered data
st.subheader("Filtered Data")
st.dataframe(df_filtrado.reset_index(drop=True), use_container_width=True)

st.caption("Activity I - Data Visualization and Dashboard Deployment | Data Mining")
