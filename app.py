
import streamlit as st
from utils.audit_parser import process_audits
import tempfile
import os

st.set_page_config(page_title="Audit Analyzer", layout="wide")
st.title("📊 Audit Analyzer")
st.markdown("Upload 2 or more PDF audit reports of **similar companies** to extract and compare key conclusions.")

uploaded_files = st.file_uploader("Upload PDF files", type=["pdf"], accept_multiple_files=True)

if uploaded_files:
    if len(uploaded_files) < 2:
        st.warning("Please upload at least 2 PDF files.")
    else:
        with st.spinner("Analyzing audit reports with AI..."):
            try:
                temp_paths = []
                for file in uploaded_files:
                    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
                    temp_file.write(file.read())
                    temp_paths.append(temp_file.name)

                table_data = process_audits(temp_paths)

                st.success("Analysis complete!")
                st.markdown("### 🧠 Key Messages Summary")
                for i, row in table_data.iterrows():
                    st.markdown(f"**{row.get('Company', f'Audit {i+1}')}**")
                    for key, value in row.items():
                        if key != "Company":
                            st.markdown(f"- **{key}:** {value}")
                    st.markdown("---")
                # Compare audits for similarities
                from collections import defaultdict

                field_groups = defaultdict(list)
                for _, row in table_data.iterrows():
                    for key, value in row.items():
                        if key != "Company":
                            field_groups[key].append(value.lower())

                st.markdown("### 📊 Audit Comparison Summary")
                for field, contents in field_groups.items():
                    unique = set(contents)
                    if len(unique) == 1:
                        st.success(f"All audits reported the same for **{field}**: *{list(unique)[0]}*")
                    elif len(unique) < len(contents):
                        st.warning(f"Some overlap in **{field}**, but not all audits agree.")
                    else:
                        st.info(f"Audits reported different insights for **{field}**.")


                # Export to CSV
                csv = table_data.to_csv(index=False).encode('utf-8')

                # Export to PDF
                        self.cell(0, 10, "Audit Analysis Summary", ln=True, align="C")
                        self.ln(10)

            except Exception as e:
                st.error(f"❌ An error occurred: {str(e)}")