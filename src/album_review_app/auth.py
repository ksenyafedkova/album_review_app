import streamlit as st
from db_request import make_request, execute_request, check_user, create_user
import bcrypt
from logger import logger

def register_user():
    with (st.form(key='Register form', enter_to_submit=False)):
        username = st.text_input("Username")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        repeat_password = st.text_input("Repeat password", type="password")

        submitted = st.form_submit_button('Create an account')

        if submitted:
            if not username or not email or not password or not repeat_password:
                st.info('Please fill in all fields.')
            elif password != repeat_password:
                st.info('Passwords do not match.')

            else:
                try:
                    username_exists = check_user(username)
                    email_exists = check_user(email)
                except Exception as e:
                    logger.error(
                        f'Registration database check failed for username '
                        f'{username}: {e}'
                    )
                    st.error('Something went wrong. Please try again later.')
                    st.stop()
                if username_exists:
                    st.info('Username is taken.')
                elif email_exists:
                    st.info('An account with this email already exists.')
                else:
                    password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
                    password_hash = password_hash.decode('utf-8')

                    try:
                        create_user(
                            username,
                            email,
                            password_hash
                        )

                        st.success('Account created successfully!')
                    except Exception as e:
                        logger.error(
                            f'Failed to create account for username {username}: {e}'
                        )
                        st.error('Something went wrong while creating your account.')

def login_user():
    with (st.form(key='Login form', enter_to_submit=False)):
        username_or_email = st.text_input("Username or email")
        password = st.text_input("Password", type="password")

        submitted = st.form_submit_button('Log in')

        if submitted:
            if not username_or_email or not password:
                st.info('Please fill in all fields.')
            else:
                try:
                    user = check_user(username_or_email)
                except Exception as e:
                    logger.error(
                        f'Login database request failed for '
                        f'{username_or_email}: {e}'
                    )
                    st.error('Something went wrong. Please try again later.')
                    st.stop()
                if not user:
                    st.info('There is no such user.')
                else:
                    try:
                        password_hash = user[0]['password_hash']
                        password_correct = bcrypt.checkpw(
                            password.encode('utf-8'),
                            password_hash.encode('utf-8')
                        )
                    except Exception as e:
                        logger.error(
                            f'Password verification failed for user '
                            f'{user[0]["username"]}: {e}'
                        )
                        st.error('Something went wrong. Please try again later.')
                        st.stop()

                    if password_correct:
                        st.session_state['logged_in'] = True
                        st.session_state['user_id'] = user[0]['id']
                        st.session_state['username'] = user[0]['username']
                        st.success('Login successful!')
                    else:
                        st.info('Incorrect password.')