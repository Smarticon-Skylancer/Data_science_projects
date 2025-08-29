import streamlit as st
import pandas as pd
st.set_page_config(page_title="CGPA Calculator", layout="wide")
# Load courses dataset
@st.cache_data
def load_courses():
    df = pd.read_csv(r"C:\Users\hp\Desktop\cgpa_calculator_files\courses.csv" , encoding='latin1')
    return df

df_courses = load_courses()



# --- Custom CSS for Better UI ---
st.markdown("""
    <style>
        body {
            background: linear-gradient(120deg, #ff5f6d, #ffc371);
            color: #45367;
            font-family: 'Segoe UI', sans-serif;
        }
        .main-title {
            font-size: 36px;
            font-weight: bold;
            text-align: center;
            color: #ffffff;
        }
        .sub-title {
            font-size: 20px;
            text-align: center;
            color: #f7f7f7;
        }
        .stButton>button {
            background-color: #6a1b9a;
            color: white;
            font-weight: bold;
            border-radius: 12px;
            padding: 8px 20px;
        }
        .stButton>button:hover {
            background-color: #4a148c;
            color: #fff176;
        }
    </style>
""", unsafe_allow_html=True)

# --- Header ---
st.markdown("<div class='main-title'>🎓 CGPA Calculator</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-title'>Select your level, enter grades, and calculate your GPA easily.</div>", unsafe_allow_html=True)
st.write("---")

# --- Level Selection ---
level = st.selectbox("📌 Select Your Level:", df_courses["Level"].unique())

# Filter courses for selected level
level_courses = df_courses[df_courses["Level"] == level]["Course"].tolist()

num_courses = st.number_input(f"Enter number of courses you want to add (Max: {len(level_courses)}):", 
                              min_value=1, max_value=len(level_courses), step=1)

st.write("### 📚 Enter Your Course Details")

course_inputs = []
grade_points = {"A": 5, "B": 4, "C": 3, "D": 2, "E": 1, "F": 0}

for i in range(num_courses):
    st.write(f"#### Course {i+1}")
    
    course = st.selectbox(f"Select Course {i+1}", level_courses, key=f"course_{i}")
    credit_unit = st.number_input(f"Enter Credit Units for {course}", min_value=1, max_value=6, step=1, key=f"credit_{i}")
    grade = st.selectbox(f"Enter Grade for {course}", options=list(grade_points.keys()), key=f"grade_{i}")
    
    course_inputs.append({"Course": course, "CreditUnit": credit_unit, "Grade": grade})

# --- GPA Calculation ---
if st.button("🎯 Calculate GPA"):
    total_units = sum([c["CreditUnit"] for c in course_inputs])
    total_points = sum([c["CreditUnit"] * grade_points[c["Grade"]] for c in course_inputs])
    
    gpa = total_points / total_units if total_units > 0 else 0

    
    # Show breakdown table
    st.write("### 📊 Breakdown of Results")
    st.dataframe(pd.DataFrame(course_inputs))
    st.success(f"✅ Your GPA is: **{gpa:.2f}**")
    if gpa >= 4.5:
        st.write("Class of Degree : First Class")
    elif gpa >= 3.5:
        st.write('Class of Degree : Second Class Upper')
    elif gpa >= 2.5:
        st.write('Class of Degree : Second Class Lower')
    elif gpa >= 1.5:
        st.write('Class of Degree : Third Class')
    else:
        st.error('Class of Degree : Please check with the school for your class')