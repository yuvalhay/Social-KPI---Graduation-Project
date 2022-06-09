import streamlit as st
import streamlit_authenticator as stauth

def login():
    names = ['Batel Yossef Ravid', 'Meirav Aharon - Gutman', 'Asaf Avrahami','Shai Zusman', 'Admin']
    usernames = ['BatelYR','MeiravAG', 'AsafA', 'ShaiZ', 'Admin']
    passwords = ['B!100yr','M@200ag', 'A#300a', 'S$400z', 'A%700g']
    hashed_passwords = stauth.Hasher(passwords).generate()

    authenticator = stauth.Authenticate(names,usernames,hashed_passwords,
                                      'some_cookie_name','some_signature_key',cookie_expiry_days=30)

    name, authentication_status, username = authenticator.login('Login','main')
    
    return name, authentication_status, user_id, authenticator
