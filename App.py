import os
import time
import json
import requests
import streamlit as st
from streamlit_pdf_viewer import pdf_viewer
from Converter import pdf_to_image
from Gemini_Text_fromatter import PDF_formatter, Image_formatter

local_api_url = "http://127.0.0.1:8000/convert"


def pdfProcess(filePath):
    with open(filePath, 'rb') as f:
        response = requests.post(local_api_url, files={'file': f})
    print("Docling Text : \n", response.text)
    doclingText = response.json()['text']
    imagePath = pdf_to_image(filePath)
    pdfText = PDF_formatter(doclingText, imagePath)
    os.remove(imagePath)
    return pdfText


def imageProcess(filePath):
    imageText = Image_formatter(filePath)
    print("ImageText:  \n", imageText)
    return imageText


def main():
    try:
        st.set_page_config(
            page_title="Document Processor",
            layout="wide",
            page_icon=":page_with_curl:"
        )
        st.title("Document Processor")
        st.markdown(
            """
                <style>
                %s
                </style>
                """ % open("style.css").read(),
            unsafe_allow_html=True
        )
        st.write("#### Process is for Single Page PDF")
        uploadedFile = st.file_uploader("Select a file to process", type=['png', 'jpg', 'jpeg', 'pdf'])
        # Create a placeholder for status updates
        status_placeholder = st.empty()
        # Check if a file has been uploaded
        if uploadedFile is not None:
            file_name = uploadedFile.name
            file_extension = file_name.split(".")[-1]
            filePath = os.path.join("temp", file_name)  # Updated folder path
            with open(filePath, "wb") as f:
                f.write(uploadedFile.getvalue())
            status_placeholder.write(":green[File uploaded successfully!..]")
            start_time = time.time()
            col1, col2 = st.columns(2)
            processedText = ""
            with col1:
                if file_extension == 'pdf':
                    pdf_viewer(filePath)
                elif file_extension in ['png', 'jpg', 'jpeg']:
                    st.image(filePath)

            with col2:
                if file_extension == 'pdf':
                    processedText += pdfProcess(filePath)

                elif file_extension in ['png', 'jpg', 'jpeg']:
                    processedText += imageProcess(filePath)

                with st.expander(label="PDF TEXT", expanded=True):
                    st.text(processedText)

                status_placeholder.write(f":green[Finished in..] : {round(time.time() - start_time, 2)} in sec "
                                         ":heavy_check_mark:")
        else:
            st.write("Please upload a file to process.")

    except Exception as exception:
        print(f"Error processing file: {exception}")
        st.error("Error processing file")


if __name__ == '__main__':
    main()
