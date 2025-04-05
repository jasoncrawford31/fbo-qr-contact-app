
import streamlit as st
import qrcode
from PIL import Image
import base64
import json
from io import BytesIO
import smtplib
from email.message import EmailMessage

st.set_page_config(page_title="FBO Contact QR Generator", page_icon="📇", layout="centered")

st.image("fbo-logo.png", width=200)
st.title("FBO Contact QR Generator")
st.markdown("Create your digital contact card and generate a QR code others can scan to view it.")

# Form for input
with st.form("contact_form"):
    full_name = st.text_input("Full Name")
    job_title = st.text_input("Job Title")
    company = st.text_input("Company")
    email = st.text_input("Email")
    phone = st.text_input("Phone Number")
    website = st.text_input("Website (Optional)")
    submit = st.form_submit_button("Generate QR Code")

if submit:
    # Encode contact data
    contact_data = {
        "full_name": full_name,
        "job_title": job_title,
        "company": company,
        "email": email,
        "phone": phone,
        "website": website,
    }
    encoded_page = base64.urlsafe_b64encode(json.dumps(contact_data).encode()).decode()
    link = f"https://fbo-qr-contact-app-bkrgokecpkqgkf2pwicxwj.streamlit.app/?data={encoded_page}"

    # Generate QR code
    qr = qrcode.make(link)
    qr_buffer = BytesIO()
    qr.save(qr_buffer, format="PNG")
    qr_image = qr_buffer.getvalue()
    st.subheader("Here is your QR Code")
    st.image(qr_image, use_container_width=True)

    # Download
    href = f'<a href="data:image/png;base64,{base64.b64encode(qr_image).decode()}" download="fbo_qr_code.png">📥 Download QR Code</a>'
    st.markdown(href, unsafe_allow_html=True)

# Page view section
query_params = st.query_params
if "data" in query_params:
    try:
        contact_info = json.loads(base64.urlsafe_b64decode(query_params["data"]).decode())
        st.subheader("📇 Contact Details")
        st.write(f"**Name:** {contact_info['full_name']}")
        st.write(f"**Title:** {contact_info['job_title']}")
        st.write(f"**Company:** {contact_info['company']}")
        st.write(f"**Email:** {contact_info['email']}")
        st.write(f"**Phone:** {contact_info['phone']}")
        if contact_info.get("website"):
            st.write(f"**Website:** {contact_info['website']}")

        st.markdown("---")
        st.subheader("📧 Want to save this contact?")
        user_email = st.text_input("Enter your email to receive this contact:")
        if st.button("Email me this contact"):
            msg = EmailMessage()
            msg["Subject"] = f"Contact info for {contact_info['full_name']}"
            msg["From"] = "fboconnects@gmail.com"
            msg["To"] = user_email
            body = "\n".join([f"{k.title().replace('_', ' ')}: {v}" for k, v in contact_info.items()])
            msg.set_content(f"Here is the contact info you scanned:\n\n{body}")

            try:
                with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
                    smtp.login("fboconnects@gmail.com", "ftzb sxod skeb fzyy")
                    smtp.send_message(msg)
                st.success("Contact sent to your inbox!")
            except Exception as e:
                st.error(f"Failed to send email: {e}")
    except Exception:
        st.error("There was a problem decoding the contact data. The QR link might be broken or expired.")
