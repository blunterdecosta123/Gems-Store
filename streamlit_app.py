import requests
import streamlit as st
import os

API_BASE_URL = os.getenv("API_URL", "http://127.0.0.1:8000")
GEM_TYPES = ["DIAMOND", "RUBY", "EMERALD"]
CLARITIES = [1,2,3,4]
COLORS = ["D", "E", "F", "G", "H", "I"]


st.set_page_config(page_title="Gem Store", page_icon="💎", layout="wide")


def auth_headers():
    token = st.session_state.get("token")
    if not token:
        return {}
    return {"Authorization": f"Bearer {token}"}


def api_request(method, path, **kwargs):
    url = f"{API_BASE_URL}{path}"
    try:
        response = requests.request(method, url, timeout=10, **kwargs)
    except requests.RequestException as exc:
        st.error(f"Could not reach FastAPI server: {exc}")
        return None

    if response.status_code >= 400:
        st.error(f"{response.status_code}: {response.text}")
        return None

    if response.text:
        return response.json()
    return {}


st.title("Gem Store")
st.caption("Simple Demo Gem Store App")

with st.sidebar:
    st.header("API")
    api_url = st.text_input("FastAPI URL", value=API_BASE_URL)
    if api_url.endswith("/"):
        API_BASE_URL = api_url[:-1]
    else:
        API_BASE_URL = api_url

    st.divider()
    st.header("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login", use_container_width=True):
        data = api_request(
            "POST",
            "/login",
            json={"username": username, "password": password},
        )
        if data and data.get("token"):
            st.session_state["token"] = data["token"]
            st.success("Logged in")
        else:
            st.error("Invalid Username or Password")

    if st.session_state.get("token"):
        st.success("Token saved")
        if st.button("Logout", use_container_width=True):
            st.session_state.pop("token", None)
            st.rerun()

tab_gems, tab_create, tab_register,tab_gems_id,put_tab_gems_id,patch_tab_gmes_id,delete_tab_gem,gem_seller_tab,tab_current_user = st.tabs(["Browse Gems", "Create Gem", "Register User","Gem ID","Update Gem","Patch Gem","Delete Gem","Gem Seller","Current User"])

with tab_gems:
    st.subheader("Browse Gems")

    col1, col2, col3 = st.columns(3)
    with col1:
        lte = st.number_input("Max price", min_value=0, value=0, step=100)
    with col2:
        gte = st.number_input("Min price", min_value=0, value=0, step=100)
    with col3:
        selected_types = st.multiselect("Gem type", GEM_TYPES)

    params = {}
    if lte:
        params["lte"] = lte
    if gte:
        params["gte"] = gte
    if selected_types:
        params["type"] = selected_types

    if st.button("Load gems", type="primary"):
        data = api_request("GET", "/gems", params=params)
        if data:
            gems = data.get("gems", [])
            if not gems:
                st.info("No gems found")
            for item in gems:
                gem = item.get("gem", {})
                properties = item.get("properties", {})
                with st.container(border=True):
                    left, right = st.columns(2)
                    left.write("Gem")
                    left.json(gem)
                    right.write("Properties")
                    right.json(properties)

with tab_create:
    st.subheader("Create Gem")
    st.caption("This route requires a logged-in seller account.")

    col1, col2 = st.columns(2)
    with col1:
        gem_type = st.selectbox("Gem type", GEM_TYPES)
        availability = st.checkbox("Available", value=True)
    with col2:
        size = st.number_input("Size", min_value=0.1, value=1.0, step=0.1)
        clarity = st.selectbox("Clarity", CLARITIES)
        color = st.selectbox("Color", COLORS)

    if st.button("Create gem", type="primary"):
        data = api_request(
            "POST",
            "/gems",
            headers=auth_headers(),
            json={
                "gem_pr": {
                    "size": size,
                    "clarity": clarity,
                    "color": color,
                },
                "gem": {
                    "availability": availability,
                    "gem_type": gem_type,
                },
            },
        )
        if data:
            st.success("Gem created")
            st.json(data)

with tab_register:
    st.subheader("Register User")

    new_username = st.text_input("New username")
    new_email = st.text_input("Email")
    new_password = st.text_input("New password", type="password")
    new_password2 = st.text_input("Confirm password", type="password")
    is_seller = st.checkbox("Register as seller")

    if st.button("Register", type="primary"):
        data = api_request(
            "POST",
            "/registration",
            json={
                "username": new_username,
                "email": new_email,
                "password": new_password,
                "password2": new_password2,
                "is_seller": is_seller,
            },
        )
        if data:
            st.success(data.get("message", "Registered"))

with tab_gems_id:
    st.subheader("Gem ID")
    gem_id = st.text_input("Gem ID")
    if st.button("Get gem", type="primary"):
        data = api_request("GET", f"/gem/{gem_id}")
        if data:
            st.success("Gem found") 
            gem=data.get("gem",{})
            if gem:
                st.json(gem)
            else:
                st.error("Gem not found")
            
with put_tab_gems_id:
    st.subheader("Update Gem")
    gem_id1 = st.text_input("Gem ID to update")
    update_gem_type = st.selectbox("Gem type", GEM_TYPES,key="update_gem_type")
    update_availability = st.checkbox("Available", value=True,key="update_gem_availability")
    update_size = st.number_input("Size", min_value=0.1, value=1.0, step=0.1,key="update_gem_size")
    update_clarity = st.selectbox("Clarity", CLARITIES,key="update_gem_clarity")
    update_color = st.selectbox("Color", COLORS,key="update_gem_color")

    if st.button("Update gem", type="primary"):
        data = api_request(
            "PUT",
            f"/gems/{gem_id1}",
            headers=auth_headers(),
            json={
                "gem_pr": {
                    "size": update_size,
                    "clarity": update_clarity,
                    "color": update_color,
                },
                "gem": {
                    "availability": update_availability,
                    "gem_type": update_gem_type,
                },
            },
        )
        if data:
            st.success("Gem updated")
            st.json(data)
        else:
            st.error("Invalid Data or Authorization")

with patch_tab_gmes_id:
    st.subheader("Patch Gem")
    gem_id2 = st.text_input("Gem ID to patch")
    old_response=None
    if not gem_id2:
        st.info("Please enter a valid gem id")
    else:
        old_response=api_request("GET", f"/gem/{gem_id2}")
    
    if old_response:
        old_gem=old_response.get("gem",{})
        properties=old_response.get("properties",{})
        if old_gem and properties:
            st.session_state["gem_type"]=old_gem.get("gem_type")
            st.session_state["availability"]=old_gem.get("availability")
            st.session_state["size"]=properties.get("size")
            st.session_state["clarity"]=properties.get("clarity")    
            st.session_state["color"]=properties.get("color")
        else:   
            st.session_state["gem_type"]=None
            st.session_state["availability"]=None
            st.session_state["size"]=None
            st.session_state["clarity"]=None    
            st.session_state["color"]=None
            
    gem_type_value = st.session_state.get("gem_type")
    gem_type_index = GEM_TYPES.index(gem_type_value) if gem_type_value in GEM_TYPES else 0
    gem_clarity_value = st.session_state.get("clarity")
    gem_clarity_index = CLARITIES.index(gem_clarity_value) if gem_clarity_value in CLARITIES else 0
    gem_color_value = st.session_state.get("color") 
    gem_color_index = COLORS.index(gem_color_value) if gem_color_value in COLORS else 0
    patch_gem_type = st.selectbox("Gem type(Optional)", GEM_TYPES,key="patch_gem_type",index=gem_type_index)
    patch_availability = st.checkbox("Available(Optional)", key="patch_gem_availability",value=st.session_state.get("availability",True))
    patch_size = st.number_input("Size(Optional)", min_value=0.1,step=0.1,key="patch_gem_size",value=st.session_state.get("size",1.0))
    patch_clarity = st.selectbox("Clarity(Optional)", CLARITIES,key="patch_gem_clarity",index=gem_clarity_index)
    patch_color = st.selectbox("Color(Optional)", COLORS,key="patch_gem_color",index=gem_color_index)
    st.session_state.pop("patch_gem_type",None)
    st.session_state.pop("patch_gem_availability",None)
    st.session_state.pop("patch_gem_size",None)
    st.session_state.pop("patch_gem_clarity",None)
    st.session_state.pop("patch_gem_color",None)    
    if st.button("Patch gem", type="primary"):
        data = api_request(
            "PATCH",
            f"/gems/{gem_id2}",
            headers=auth_headers(),
            json={
                "gem_pr": {
                    "size": patch_size,
                    "clarity": patch_clarity,
                    "color": patch_color,
                },
                "gem": {
                    "availability": patch_availability,
                    "gem_type": patch_gem_type,
                },
            },
        )
        if data:
            st.success("Gem patched")
            st.json(data)
        else:
            st.error("Invalid Data or Authorization")
            
with delete_tab_gem:
    st.subheader("Delete Gem")
    gem_id3 = st.text_input("Gem ID to delete")
    if st.button("Delete gem", type="primary"):
        data = api_request(
            "DELETE",
            f"/gems/{gem_id3}",
            headers=auth_headers(),
        )
        if data:
            st.success("Gem deleted")
            st.json(data)
        else:
            st.error("Invalid Data or Authorization")
            
with gem_seller_tab:
    st.subheader("Gem Seller")
    if st.button("Get gems", type="primary"):
        data = api_request("GET", f"/gems/seller/me",headers=auth_headers())
        if data:
            st.success("Gems found") 
            for item in data:
                gem = item.get("gem", {})
                properties = item.get("properties", {})
                with st.container(border=True):
                    left, right = st.columns(2)
                    left.write("Gem")
                    left.json(gem)
                    right.write("Properties")
                    right.json(properties)
        else:
            st.error("Invalid Gem ID or Authorization")
            
with tab_current_user:
    st.subheader("Current User")
    if st.button("Get current user", type="primary"):
        data = api_request("GET", f"/users/me",headers=auth_headers())
        if data:
            st.success("User found") 
            st.json({"username":data})
        else:
            st.error("Invalid User ID or Authorization")
