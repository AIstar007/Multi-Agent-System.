st.markdown(f"**🚀 Launch:** {result['launch']['name']}")
st.markdown(f"**🕒 Launch Time:** {result['launch']['launch_time']}")
st.markdown(f"**📊 Weather:** {result['weather']['weather'][0]['description']}")

try:
    st.markdown(f"**💡 Assessment:** {result['assessment']}")
except KeyError:
    st.warning("⚠️ Assessment not available. Please check weather or delay agents.")
