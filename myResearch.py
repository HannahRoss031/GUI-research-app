import streamlit as st

#FIXME: streamlit run myResearch.py

#st.title("🧬 Gene Coordinate Comparison Demo")

st.write("Upload two gene coordinate files (BED format).")

# Create sidebar? - holding various options
with st.sidebar:
    st.title("🧬 Gene Coordinate Comparison Demo")

# Upload files - BED
#file1 = st.file_uploader("Upload Condition A", type=["csv"])
#file2 = st.file_uploader("Upload Condition B", type=["csv"])

# Files for the function

# Output results into a readable table