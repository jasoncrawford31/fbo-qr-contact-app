
import streamlit as st
import base64
import qrcode
import io
import smtplib
from email.mime.text import MIMEText
from PIL import Image
from datetime import datetime

# Branding colors
TEAL = "#00A3A6"
GOLD = "#E5B901"
GRAY = "#7E7E7E"

# Set up page config
st.set_page_config(page_title="FBO QR Contact Share", layout="centered")

# Load FBO logo
st.image("fbo-logo.png", width=250)

# Apply custom title style
st.markdown(f"<h2 style='color:{TEAL}; margin-top: 0;'>FBO Contact QR Generator</h2>", unsafe_allow_html=True)

# Check for ?data=... in URL to show viewer
query_data = st.query_params.get("data")

if query_data:
    try:
        decoded = base64.urlsafe_b64decode(query_data.encode()).decode("utf-8")
        st.markdown(f"<h3 style='color:{GOLD};'>📇 Contact Information</h3>", unsafe_allow_html=True)
        st.markdown(decoded, unsafe_allow_html=True)

        name_line = decoded.split("<h3>")[1].split("</h3>")[0]
        email_line = decoded.split("mailto:")[1].split("'")[0]

        if st.button("📥 Download Contact Card (.vcf)"):
            vcf = f"""BEGIN:VCARD\nVERSION:3.0\nFN:{name_line}\nEMAIL:{email_line}\nEND:VCARD"""
            st.download_button(
                label="Download .vcf file",
                data=vcf,
                file_name=f"{name_line.replace(' ', '_')}.vcf",
                mime="text/vcard"
            )

        st.markdown("#### Want to save this contact to your inbox?")

        user_email = st.text_input("Enter your email to receive this contact")
        st.caption("_Your email will be used only to send this contact and will not be stored._")

        if st.button("📧 Email me this contact"):
            if user_email:
                msg = MIMEText(f"Here is the contact info you scanned:\n\nName: {name_line}\nEmail: {email_line}")
                msg['Subject'] = f"Contact Info from FBO Conference: {name_line}"
                msg['From'] = "fboconnects@gmail.com"
                msg['To'] = user_email

                try:
                    with smtplib.SMTP('smtp.gmail.com', 587) as server:
                        server.starttls()
                        server.login('fboconnects@gmail.com', 'ftzbsxodskebfzyy')
                        server.send_message(msg)
                    st.success("✅ Contact info sent to your inbox!")
                except Exception as e:
                    st.error("Failed to send email. Please try again later.")
            else:
                st.warning("Please enter your email address to receive the contact.")
    except Exception as e:
        st.error("There was a problem decoding the contact data. The QR link might be broken or expired.")
    st.stop()

# Show the form if no data param
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
    st.image(buf, caption="Let attendees scan this QR to view your contact info.", use_container_width=False)

    b64_img = base64.b64encode(buf.getvalue()).decode()
    href = f'<a href="data:image/png;base64,{b64_img}" download="FBO_QR_{name}.png">📥 Download QR Code</a>'
    st.markdown(href, unsafe_allow_html=True)

    st.text_input("Shareable Contact Link", value=link)
    st.success("Done! You can now print or display this QR code at the event.")
else:
    st.info("Fill in your contact info and click 'Generate QR Code' to begin.")
