import streamlit as st
from PIL import Image
import streamlit.components.v1 as components
import codecs

f=codecs.open("./src/output/global/copd.html", 'r')
copd = f.read()

components.html(copd,height=600,scrolling=True)