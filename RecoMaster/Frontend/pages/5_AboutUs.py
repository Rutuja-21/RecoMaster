import streamlit as st

# Background image styling (optional)
page_bg_img = '''
<style>
body {
background-image: url("https://your-background-image-link.jpg");
background-size: cover;
background-position: top left;
background-repeat: no-repeat;
background-attachment: fixed;
}
</style>
'''

st.markdown(page_bg_img, unsafe_allow_html=True)

# Page Title and Subtitle
st.title("About Us")
st.subheader("Empowering Healthy Eating with Personalized Diet Recommendations")

# Introduction
st.write("""
Welcome to our Diet Recommendation System! Our mission is to make healthy eating simple, personalized, 
and accessible. We understand that every individual is unique, and so are their dietary needs. Whether you're managing 
a health condition like diabetes or simply striving for better nutrition, our platform is here to guide you with tailored meal suggestions.
""")

# About the Project
st.subheader("What We Do")
st.write("""
We use advanced algorithms to analyze user inputs, including dietary preferences and health conditions, to provide customized meal recommendations. 
  
By offering meals that fit your health needs, we aim to help you achieve your wellness goals efficiently.
""")

# How It Works
st.subheader("How It Works")
st.write("""
Our recommendation system processes the following:
- **Diet Preferences:** Vegetarian, Non-Vegetarian, Vegan
- **Health Conditions:** Suggests meals optimized for managing specific conditions
- **Nutritional Balance:** Ensures your meals are balanced with the right nutrients

With this information, we generate meal plans that are not only nutritious but also delicious, making it easier to stick to a healthy eating routine.
""")

# Call to Action
st.markdown("""
**Ready to Start Your Journey to Healthier Eating?**  
[Sign Up Now](#) to get personalized meal recommendations today!
""")

# Footer
st.write("---")
st.write("**© 2024 Diet Recommendation System**")
