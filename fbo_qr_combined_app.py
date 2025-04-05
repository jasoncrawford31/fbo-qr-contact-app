
import streamlit as st
import base64
import qrcode
import io
from PIL import Image

# Check for ?data= in query string — if present, render viewer
query_data = st.query_params.get("data")

if query_data:
    try:
        decoded = base64.urlsafe_b64decode(query_data.encode()).decode("utf-8")
        st.set_page_config(page_title="FBO Contact Viewer", layout="centered")
        st.title("📇 Contact Information")
        st.markdown(decoded, unsafe_allow_html=True)

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
    except:
        st.error("Invalid or expired QR code.")
    st.stop()

# QR Generator Mode
st.set_page_config(page_title="FBO QR Contact Share", layout="centered")
st.title("FBO Contact QR Generator")
st.markdown("Create your digital contact card and generate a QR code others can scan to view it.")

with st.form("contact_form"):
    name = st.text_input("Full Name")
    title = st.text_input("Job Title")
    company = st.text_input("Company")
    email = st.text_input("Email")
    linkedin = st.text_input("LinkedIn Profile (optional)")
    submit = st.form_submit_button("Generate QR Code")

if submit and name and email:
    contact_page = f"""
    <h3>{name}</h3>
    <p><strong>{title}</strong><br>
    {company}<br>
    <a href='mailto:{email}'>{email}</a><br>
    <a href='{linkedin}'>{linkedin}</a></p>"""
    encoded_page = base64.urlsafe_b64encode(contact_page.encode()).decode()
    link = f"https://your-app-name.streamlit.app/?data={encoded_page}"

    qr = qrcode.make(link)
    buf = io.BytesIO()
    qr.save(buf, format="PNG")
    buf.seek(0)

    st.subheader("Here is your QR Code")
    st.image(buf, caption="Let attendees scan this QR to view your contact info.", use_column_width=True)

    b64_img = base64.b64encode(buf.getvalue()).decode()
    href = f'<a href="data:image/png;base64,{b64_img}" download="FBO_QR_{name}.png">📥 Download QR Code</a>'
    st.markdown(href, unsafe_allow_html=True)

    st.text_input("Shareable Contact Link", value=link)
    st.success("Done! You can now print or display this QR code at the event.")
else:
    st.info("Fill in your contact info and click 'Generate QR Code' to begin.")
