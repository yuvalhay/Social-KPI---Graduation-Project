import streamlit as st
import streamlit_authenticator as stauth

def login():
    names = []
    usernames = []
    passwords = []
    hashed_passwords = stauth.Hasher(passwords).generate()

    authenticator = stauth.Authenticate(names,usernames,hashed_passwords,
                                      'some_cookie_name','some_signature_key',cookie_expiry_days=30)

    name, authentication_status, username = authenticator.login('Login','main')
    
    return name, authentication_status, authenticator
