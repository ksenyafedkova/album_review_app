import streamlit as st

def hide_sidebar_navigation():
    st.markdown("""
    <style>
        [data-testid="stSidebarNav"] {
            display: none;
        }
    </style>
    """, unsafe_allow_html=True)


def show_user_sidebar():
    if st.session_state.get("logged_in") is not True:
        st.switch_page("main.py")
    st.sidebar.success(f"Logged in as {st.session_state.get('username')}")
    if st.sidebar.button("🏠 Home"):
        st.switch_page("pages/home_page.py")
    if st.sidebar.button("🔎 Search"):
        st.switch_page("pages/search_page.py")
    # if st.session_state.get("username") == "ksenyafedkova":
    #     if st.sidebar.button("👑 Admin Panel"):
    #         st.switch_page("pages/admin_page.py")
    # if st.sidebar.button("🔑 Reset password"):
    #     st.switch_page("pages/reset_password.py")
    if st.sidebar.button("🚪 Logout"):
        st.session_state['logged_in'] = False
        st.session_state.pop('user_id', None)
        st.session_state.pop('username', None)
        st.switch_page("main.py")