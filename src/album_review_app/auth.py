import streamlit as st
from album_review_app.backend.v1.api_script import check_user, create_user
from album_review_app.backend.schemes.schemes import UserCreate
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
                        user_data = UserCreate(
                            username=username,
                            email=email,
                            password_hash=password_hash
                        )

                        create_user(user_data)

                        st.success('Account created successfully!')
                    except Exception as e:
                        logger.error(
                            f'Failed to create account for username {username}: {e}'
                        )
                        st.error('Something went wrong while creating your account.')





def _check_user_in_db(username_or_email):
    try:
        users = check_user(username_or_email)
        return users[0] if users else None

    except Exception as e:
        logger.error(
            f'Database request failed while checking user '
            f'{username_or_email}: {e}'
        )
        st.error('Something went wrong. Please try again later.')
        st.stop()

def _verify_password(password, password_hash, username):
    try:
        return bcrypt.checkpw(
            password.encode('utf-8'),
            password_hash.encode('utf-8')
        )

    # except Exception as e:
    #     logger.error(
    #         f'Password verification failed for user {username}: {e}'
    #     )
    #     st.error('Something went wrong. Please try again later.')
    #     st.stop()

    except Exception as e:
        print(f'Password verification failed: {e!r}')
        raise

def _set_logged_in_user(user):
    st.session_state['logged_in'] = True
    st.session_state['user_id'] = user['id']
    st.session_state['username'] = user['username']

def _process_login(username_or_email, password):
    if not username_or_email or not password:
        st.info('Please fill in all fields.')
        return

    user = _check_user_in_db(username_or_email)

    if not user:
        st.info('There is no such user.')
        return

    password_correct = _verify_password(
        password,
        user['password_hash'],
        user['username']
    )

    if password_correct:
        _set_logged_in_user(user)
        st.success('Login successful!')
    else:
        st.info('Incorrect password.')


def login_user():
    with (st.form(key='Login form', enter_to_submit=False)):
        username_or_email = st.text_input("Username or email")
        password = st.text_input("Password", type="password")

        submitted = st.form_submit_button('Log in')

        if submitted:
            _process_login(username_or_email, password)