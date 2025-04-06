import streamlit as st
import qrcode
import json
import base64
from io import BytesIO
from PIL import Image

# Set page configuration
st.set_page_config(page_title="FBO Contact QR Generator", page_icon="📇", layout="centered")

# Display logo and title
st.image("fbo-logo.png", width=200)
st.title("FBO Contact QR Generator")
st.markdown("Create your digital contact card and generate a QR code others can scan to view it.")

# Define the form using st.form
with st.form(key='contact_form'):
    full_name = st.text_input("Full Name")
    job_title = st.text_input("Job Title")
    company = st.text_input("Company")
    email = st.text_input("Email")
    phone = st.text_input("Phone Number")
    website = st.text_input("Website (Optional)")
    submit_button = st.form_submit_button(label='Generate QR Code')

# Process the form submission
if submit_button:
    # Validate required fields
    if not full_name or not job_title or not company or not email or not phone:
        st.error("Please fill in all required fields: Full Name, Job Title, Company, Email, and Phone Number.")
    else:
        # Collect contact information into a dictionary
        contact_info = {
            "full_name": full_name,
            "job_title": job_title,
            "company": company,
            "email": email,
            "phone": phone,
            "website": website
        }

        # Convert the dictionary to a JSON string
        contact_json = json.dumps(contact_info)

        # Encode the JSON string using base64
        encoded_data = base64.urlsafe_b64encode(contact_json.encode()).decode()

        # Construct the URL with the encoded data as a query parameter
        base_url = "https://fbo-qr-contact-app-6hbkk4qtfxdvo4g8duxgti.streamlit.app/"
        full_url = f"{base_url}?data={encoded_data}"

        # Generate the QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(full_url)
        qr.make(fit=True)
        qr_img = qr.make_image(fill_color="black", back_color="white")

        # Convert the PIL image to a byte array for display in Streamlit
        img_byte_arr = BytesIO()
        qr_img.save(img_byte_arr, format='PNG')
        img_byte_arr = img_byte_arr.getvalue()

        # Display the QR code image
        st.image(img_byte_arr, caption="Scan this QR code to view contact information", use_column_width=True)

        # Provide the full URL below the QR code
        st.markdown("**Shareable Link:**")
        st.write(full_url)

        # Optional: Provide a download link for the QR code image
        st.download_button(
            label="Download QR Code",
            data=img_byte_arr,
            file_name=f"{full_name.replace(' ', '_')}_QR.png",
            mime="image/png"
        )
