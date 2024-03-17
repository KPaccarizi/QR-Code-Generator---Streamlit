import streamlit as st
import qrcode
from qrcode.image.pil import PilImage
import io
import base64
from urllib.parse import urlparse

def get_image_as_base64(image):
    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    return image_base64

def get_url_filename(url):
    parsed_uri = urlparse(url)
    domain = '{uri.netloc}'.format(uri=parsed_uri)
    main_domain = domain.split('.')
    main_domain = main_domain[1] if main_domain[0] == 'www' else main_domain[0]
    path = parsed_uri.path.strip('/').replace('/', '_')
    return f"{main_domain}_{path}" if path else main_domain


st.title("✨ QR Code Generator ✨")

st.write("")  

st.write("Create custom QR codes for multiple URLs with this easy-to-use generator. \nSimply input your links, choose a color, and generate unique QR codes instantly! 🚀")

st.write("")  

content = st.text_area("Enter your URL(s) (one per line)", height=150)

colors = ['black', 'red', 'green', 'blue', 'orange', 'purple']

color_option = st.selectbox("Select QR code color", colors)

if st.button("Generate QR Code"):
    if content:
        urls = content.split("\n")

        for i, url in enumerate(urls):
            url = url.strip()
            if url and urlparse(url).scheme in ['http', 'https']: # Check if input is a valid URL
                # Generate QR code
                qr = qrcode.QRCode(
                    version=1,
                    error_correction=qrcode.constants.ERROR_CORRECT_H,
                    box_size=10,
                    border=4
                )
                qr.add_data(url)
                qr.make(fit=True)

                img = qr.make_image(fill_color=color_option, back_color="white", image_factory=PilImage)

                # PilImage to bytes-like object
                buffer = io.BytesIO()
                img.save(buffer, format="PNG")
                img_bytes = buffer.getvalue()

                img_base64 = get_image_as_base64(img)

                st.markdown(f"##### {url}")
                st.image(img_bytes, caption=f"QR code for {url}", use_column_width=True)
                file_name = get_url_filename(url)
                st.markdown(f'<a href="data:image/png;base64,{img_base64}" download="{file_name}.png" style="display:inline-block;background-color:#4CAF50;border:none;color:white;padding:8px 16px;text-align:center;text-decoration:none;font-size:16px;margin:4px 2px;cursor:pointer;">Download QR code</a>', unsafe_allow_html=True)
            elif url:
                st.error(f"'{url}' is not a valid URL.")
    else:
        st.error("Please enter URL(s) for the QR code.")

st.balloons()



