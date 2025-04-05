
import streamlit as st
import base64
import urllib.parse

# --- Setup ---
st.set_page_config(page_title="FBO Contact Viewer", layout="centered")
st.title("📇 Contact Information")

# --- Read encoded data from URL ---
data_param = st.query_params.get("data")

if data_param:
    try:
        decoded = base64.urlsafe_b64decode(data_param.encode()).decode("utf-8")
        st.markdown("### Here's the contact info:")
        st.markdown(decoded, unsafe_allow_html=True)

        # Download VCF option
        if st.button("📥 Download Contact Card (.vcf)"):
            name_line = decoded.split("<h3>")[1].split("</h3>")[0]
            email_line = decoded.split("mailto:")[1].split("'")[0]
            vcf = f"""BEGIN:VCARD
VERSION:3.0
FN:{name_line}
EMAIL:{email_line}
END:VCARD"""
            st.download_button(
                label="Download .vcf file",
                data=vcf,
                file_name=f"{name_line.replace(' ', '_')}.vcf",
                mime="text/vcard"
            )
    except Exception as e:
        st.error("There was a problem decoding the contact data. The QR link might be broken or expired.")
else:
    st.info("Scan a valid FBO QR code to view contact details here.")
