import streamlit as st
import face_recognition_live_mode as fc


with st.spinner(text='მიმდინარეობს მონაცემთა ანალიზი…'):
    with open('registered_people.csv', 'r', encoding='utf-8') as file:
        first = file.readlines()
        if not first[0].strip():
            st.write("არავინაა რეგისტრირებული")
        else:
            result = fc.aut()
            if not result[0]:
                st.write("არავინაა რეგისტრირებული")
            else:
                name, surname = result[3].split(',')
                st.write(f"მოგესალმებით {name}")