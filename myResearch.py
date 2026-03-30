import os
import tempfile
import streamlit as st
from pybedtools import BedTool
from main import main

# running from WSL -->
# conda activate research
# cd /mnt/c/Users/hnros/PycharmProjects/researchTest
# pip install streamlit
# FIXME: streamlit run myResearch.py
# C:\Users\hnros\PycharmProjects\researchTest

# TODO: pushing to git!
#  git add .
#  git commit -m "describe what you changed"
#  git pull origin main --allow-unrelated-histories
#  Then if Vim opens again, press Escape then type :wq and hit Enter.
#  git push

# FIXME: conda activate research

# TODO - printing details for files, and things selected probably,
#  before printing from comparison function
# Sidebar UI
st.markdown(
    """
    <style>
        [data-testid="stSidebar"] {
            background-color: #154734; 
        }
        [data-testid="stSidebar"] h1,
        [data-testid="stSidebar"] h2,
        [data-testid="stSidebar"] h3,
        [data-testid="stSidebar"] p,
        [data-testid="stSidebar"] div {
            color: #F8F8F2 !important;
        }
        [data-testid="stSidebar"] a.st-emotion-cache-1qg05tj {
            color: #F8F8F2 !important;      
            border-color: #F8F8F2 !important;  
            background-color: #F8F8F2 !important;
        }
        [data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] * {
            color: #31333F !important;
        }
        [data-testid="stSidebar"] button,
        [data-testid="stSidebar"] a {
            background-color: #2E7D57 !important;   /* light green */
            color: #F8F8F2 !important;              /* off‑white text */
            border: 1px solid #F8F8F2 !important;
            border-radius: 6px !important;
            padding: 0.5rem 1.2rem !important;      /* makes button wider */
            width: 100% !important;                 /* full-width buttons */
            text-align: center !important;
        }
        [data-testid="stSidebar"] button:hover,
        [data-testid="stSidebar"] a:hover {
            background-color: #246646 !important;   /* darker green */
            color: #F8F8F2 !important;
        }

    </style>
    """,
    unsafe_allow_html=True
)

st.write("Upload two gene coordinate files (BED format).")

# Create sidebar? - holding various options
with st.sidebar:
    st.title("Gene Coordinate Comparison Demo")
    st.header("Calculate enrichment between two gene coordinates.")

    # headers for each option
    pAnno = st.text_input("Percent Anno",
                               value = None,
                               placeholder="default: 1E -9")
    pAnno = pAnno if pAnno is not None else 1e-9

    pTest = st.text_input("Percent Test",
                                value = None,
                                placeholder="default: 1E-9")
    pTest = pTest if pTest is not None else 1e-9

    iterations = st.text_input("Iterations",
                               value = None,
                               placeholder="default: 100")
    iterations = iterations if iterations is not None else 100

    species = st.selectbox("Species", ('hg19', 'hg38', 'mm10', 'dm3', 'dm6', 'sacCer3'),
                            placeholder="default: hg19")
    species = species if species is not None else "hg19"

    blackListFile = st.text_input("Blacklist",
                                  value = "",
                                  placeholder="default: None")
    blackListFile = blackListFile if blackListFile is not None else ""

    threads = st.text_input("Number of Threads",
                            value = None,
                            placeholder="default: SLURM_CPUS_PER_TASK or 1")
    threads = threads if threads is not None else 0

    elementwise = st.checkbox("Elementwise", value=False)

    hapblock = st.checkbox("Haplotype Block", value=False)

    strand = st.checkbox("Strand-Specific", value=False)

    percent_overlap = 0
    # FIXME: change arguments to match the file
    # FIXME : ensure all the arguments are added

    # Details About Authors
    st.write(" ") # spacer?
    st.subheader("Created By: Dr. Mary Lauren Benton")
    st.link_button("Benton Biomedical Lab", "https://cs.baylor.edu/~benton/")
    st.subheader("Application Developer: Hannah Ross")

    st.write("Hannah Ross' Socials:")
    col1, col2 = st.columns(2)

    with col1:
        st.link_button("Github", "https://github.com/HannahRoss031")

    with col2:
        st.link_button("LinkedIn", "https://www.linkedin.com/in/hannah-ross-06247a272/")

# Upload files - BED
annotation = st.file_uploader("Upload Condition A", type=["bed"])
test = st.file_uploader("Upload Condition B", type=["bed"])

if annotation and test: # edit to make sure files are correct
    with tempfile.NamedTemporaryFile(delete=False, suffix=".bed") as tmp1:
        tmp1.write(annotation.read())
        annotation_path = tmp1.name

    with tempfile.NamedTemporaryFile(delete=False, suffix=".bed") as tmp2:
        tmp2.write(test.read())
        test_path = tmp2.name

    annotation_bed = BedTool(annotation_path)
    test_bed = BedTool(test_path)

# Embed the Function
if st.button("Run", key = "runButton"):
    st.write("RUNNING?...")
    main(annotation_path, test_path, pAnno, pTest,elementwise, hapblock, species, blackListFile, strand, threads, iterations)

    # cleanup temp files after
    os.unlink(annotation_path)
    os.unlink(test_path)
# FIXME: does not recognize the file types? formatting issue?
    # Output results into a readable table
    with st.spinner("Calculating enrichment..."):
        pass
        #result = subprocess.run(command, capture_output=True, text=True)
        #st.text(result.stdout)  # This shows whatever your other script printed
