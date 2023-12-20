import streamlit as st
import os

csv_filename = 'registered_people.csv'
images_directory = 'images'

st.header("დარეგისტრირდით")

with st.form("input"):
    name = st.text_input(
        'სახელი',
        max_chars=30)
    surname = st.text_input(
        'გვარი',
        max_chars=50
    )

    allowed_types = ("jpg", "jpeg", "png")

    uploaded_image = st.file_uploader("აირჩიეთ ფოტო...", type=allowed_types)

    submit_button = st.form_submit_button(label="რეგისტრაცია")


def markAttendance(nam, surnam):
    with open('registered_people.csv', 'a') as file:
        file.writelines(f"{nam},{surnam}")


if submit_button:
    if name not in open(csv_filename, encoding='utf-8').read() and surname not in open(csv_filename, encoding='utf-8').read() or uploaded_image.name not in os.listdir(images_directory):
        markAttendance(name, surname)
        if uploaded_image is not None:
            st.image(uploaded_image, use_column_width=True)

            upload_dir = "images"
            os.makedirs(upload_dir, exist_ok=True)

            filename = os.path.join(upload_dir, f"{uploaded_image.name}")

            with open(filename, "wb") as f:
                f.write(uploaded_image.read())

            st.success(f"Image saved as {filename}")
        st.write("თქვენ წარმატებით დარეგისტრირდით")
    else:
        st.write("მომხმარებელი მოცემული მონაცემებით უკვე რეგისტრირებულია")
