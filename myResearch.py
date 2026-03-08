import streamlit as st

#FIXME: streamlit run myResearch.py
# C:\Users\hnros\PycharmProjects\researchTest

# TODO: pushing to git!
#  git add .
#  git commit -m "describe what you changed"
#  git push


st.write("Upload two gene coordinate files (BED format).")

# Create sidebar? - holding various options
with st.sidebar:
    st.title("Gene Coordinate Comparison Demo")
    st.header("Calculate enrichment between two gene coordinates.")

    # headers for each option
    st.text_input("Percent Anno", placeholder="default: 1E -9")
    st.text_input("Percent Test", placeholder="default: 1E-9")
    st.text_input("Iterations", placeholder="default: 100")
    st.selectbox("Species", ('hg19', 'hg38', 'mm10', 'dm3', 'dm6', 'sacCer3'),
                 placeholder="default: hg19")
    st.text_input("Blacklist", placeholder="default: None")
    st.text_input("Number of Threads", placeholder="default: SLURM_CPUS_PER_TASK or 1")

    # Details About Authors
    st.text_input(" ") # spacer?
    st.subheader("Created By: Dr. Mary Lauren Benton")
    st.write("Under the Benton Biomedical Lab: __(add link)__")
    st.subheader("Application Developer: Hannah Ross")
    st.write("Hannah Ross' Socials:")
    st.link_button("Github","https://github.com/HannahRoss031")
    st.link_button("LinkedIn", "https://www.linkedin.com/in/hannah-ross-06247a272/")

# TODO: Add run button?

# Upload files - BED
file1 = st.file_uploader("Upload Condition A", type=["bed"])
file2 = st.file_uploader("Upload Condition B", type=["bed"])

# Files for the function

# Output results into a readable table