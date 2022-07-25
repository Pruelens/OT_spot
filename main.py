
import streamlit as st

from streamlit.components.v1 import iframe

st.set_page_config(layout="centered", page_icon="", page_title="Opentrons Spotting Protocol Generator")
st.title("Opentrons Protocol Generator")


number_samples=st.slider('Number of rows with samples in input plate:', 1,12,3)*8

values = [str(0),str(1),str(2),str(3),str(4),str(6)]
default_ix = values.index(str(1))
number_dilutions=int(st.selectbox('Number of 10-fold Dilutions to prepare',values,index=default_ix))

values=[]
for i in range(number_dilutions):
    values.append(str(i+1))
values.append(str(i+2))
default_ix = values.index(str(1))

range_tospot=st.slider('Select a range of 10-fold dilutions to spot:', 1, number_dilutions, (0, number_dilutions))

col1, col2 = st.columns(2)
with col1:
    st.write("Range that will be spotted:")
with col2:
    st.latex(r'''[10^{-'''+str(range_tospot[0])+'''}, 10^{-'''+str(range_tospot[1])+'''}]''')

tot_spot=number_samples*(range_tospot[1]-range_tospot[0]+1)
tot_dilwells=number_samples*number_dilutions
tot_spot_pl=int(tot_spot/96.0001)+1
tot_dilwells_pl=int(tot_dilwells/96.0001)+1
st.write(tot_dilwells_pl)
if tot_spot_pl+tot_dilwells_pl>5:
    st.write("Too few positions, consider splitting up experiment.")

else:
    col1, col2 = st.columns(2)
    with col1:
        st.write("Total spots:")
    with col2:
        st.latex(str(number_samples*(range_tospot[1]-range_tospot[0]+1)))


st.write("## Code")

st.write(
    "Contact: philip.ruelens(at)kuleuven.be")


