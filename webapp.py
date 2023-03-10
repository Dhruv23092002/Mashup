import os
import glob

# Get a list of all files in the folder
folder = os.getcwd()
files = glob.glob(folder + "/*")

# Count the number of MP3 and MP4 files in the list
mp3_files = [f for f in files if f.endswith(".mp3")]
mp4_files = [f for f in files if f.endswith(".mp4")]

if(len(mp3_files)>0):
    folder=os.getcwd()
    for file in glob.glob(os.path.join(folder, '*.mp3')):
        os.remove(file)
    
if(len(mp4_files)>0):
    folder=os.getcwd()
    for file in glob.glob(os.path.join(folder, '*.mp4')):
        os.remove(file)
import streamlit as st
from pytube import YouTube
import os
import smtplib
from youtube_search import YoutubeSearch
from moviepy.editor import *
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

def send_email_with_attachment(email, password, to, subject, body, file_path):
    msg = MIMEMultipart()
    msg['From'] = email
    msg['To'] = to
    msg['Subject'] = subject

    msg.attach(MIMEText(body))

    with open(file_path, "rb") as f:
        attachment = MIMEBase("application", "octet-stream")
        attachment.set_payload(f.read())
    encoders.encode_base64(attachment)
    attachment.add_header('Content-Disposition', "attachment; filename= %s" % file_path)
    msg.attach(attachment)

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(email, password)
    server.sendmail(email, to, msg.as_string())
    server.quit()

def createmash(Singer,num,dur):
    filedir=os.getcwd()
    files=os.listdir(filedir)

    print(files)
    mp3_files = [file for file in files if file.endswith('.mp3')]

    for i in mp3_files:
        os.remove(i)

    results = YoutubeSearch(Singer, max_results=int(num)).to_dict()

    for i in results:
        video = YouTube('http://youtube.com/watch?v='+i['id']).streams.filter(only_audio=True).first().download()
        base, ext = os.path.splitext(video)
        new_file = base + '.mp3'
        os.rename(video, new_file)

    filedir=os.getcwd()
    files=os.listdir(filedir)

    print(files)
    mp3_files = [file for file in files if file.endswith('.mp3')]

    ad = AudioFileClip(mp3_files[0])
    merged_audio=ad.subclip(0,0)

    time=int(dur)
    for i in range(0,len(mp3_files)):
        audio = AudioFileClip(mp3_files[i])
        trimmed_audio = audio.subclip(10, time+10)
        merged_audio = concatenate_audioclips([merged_audio, trimmed_audio])

    merged_audio.write_audiofile("output.mp3")
    return os.getcwd()+"/output.mp3"


st.set_page_config(page_title="MASHUP")
st.subheader("MASHUP CREATOR:notes:")
st.write('Made by Dhruv Singla')

st.write("Enter details: ")

with st.form("my_form"):
   Singer = st.text_input("Singer Name")
   num = st.text_input("Number of songs")
   dur = st.text_input("Audio duration")
   rec_email = st.text_input("Enter Email")
   # Every form must have a submit button.
   submitted = st.form_submit_button("Submit")
   if submitted:
       output=createmash(Singer,num,dur)
       email = "dsingla_be20@thapar.edu"
       password = 'rcyrtbqqbtdhxbpy'
       to = rec_email
       subject = "MASHUP By Dhruv Singla"
       body = "Enjoy Your Mashup"
       file_path = os.getcwd()+"/output.mp3"
       send_email_with_attachment(email, password, to, subject, body, file_path)
       st.subheader("MAIL sent")
