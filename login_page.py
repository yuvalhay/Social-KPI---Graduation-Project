import streamlit as st
import streamlit_authenticator as stauth

def loginn():
    names = st.secrets["DB_USERNAME"]
    usernames = st.secrets["DB_USERNAME"]
    passwords = st.secrets["DB_TOKEN"]
    hashed_passwords = stauth.Hasher(passwords).generate()

    authenticator = stauth.Authenticate(names,usernames,hashed_passwords,
                                      'some_cookie_name','some_signature_key',cookie_expiry_days=30)

    name, authentication_status, username = authenticator.login('Login','main')
    
    return name, authentication_status, username, authenticator
