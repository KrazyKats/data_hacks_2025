import streamlit as st
import plotly.graph_objects as go
from PIL import Image
import similar_princess

princess_personality = {
    "anna": {
        "openness": 4,
        "conscientiousness": 3,
        "extraversion": 5,
        "agreeableness": 5,
        "neuroticism": 3
    },
    "ariel": {
        "openness": 5,
        "conscientiousness": 2,
        "extraversion": 5,
        "agreeableness": 4,
        "neuroticism": 4
    },
    "aurora": {
        "openness": 3,
        "conscientiousness": 4,
        "extraversion": 2,
        "agreeableness": 5,
        "neuroticism": 2
    },
    "belle": {
        "openness": 5,
        "conscientiousness": 5,
        "extraversion": 3,
        "agreeableness": 4,
        "neuroticism": 2
    },
    "cinderella": {
        "openness": 4,
        "conscientiousness": 5,
        "extraversion": 3,
        "agreeableness": 5,
        "neuroticism": 2
    },
    "elsa": {
        "openness": 4,
        "conscientiousness": 5,
        "extraversion": 2,
        "agreeableness": 4,
        "neuroticism": 5
    },
    "jasmine": {
        "openness": 4,
        "conscientiousness": 3,
        "extraversion": 4,
        "agreeableness": 3,
        "neuroticism": 3
    },
    "merida": {
        "openness": 5,
        "conscientiousness": 3,
        "extraversion": 4,
        "agreeableness": 2,
        "neuroticism": 3
    },
    "rapunzel": {
        "openness": 5,
        "conscientiousness": 4,
        "extraversion": 5,
        "agreeableness": 5,
        "neuroticism": 3
    },
    "snow white": {
        "openness": 3,
        "conscientiousness": 4,
        "extraversion": 3,
        "agreeableness": 5,
        "neuroticism": 2
    },
    "tiana": {
        "openness": 4,
        "conscientiousness": 5,
        "extraversion": 3,
        "agreeableness": 4,
        "neuroticism": 2
    }
}

# Dummy user input for now
user_personality = {
    "openness": 4,
    "conscientiousness": 4,
    "extraversion": 3,
    "agreeableness": 5,
    "neuroticism": 2
}

# App layout
st.set_page_config(page_title="Disney Princess Look-a-Like", layout="wide")
st.title("Disney Princess Look-a-Like")

# Top section: Insert image and match result
top_left, top_right = st.columns(2)

with top_left:
    st.subheader("Insert Image")
    uploaded_file = st.file_uploader("Upload your image", type=["jpg", "jpeg", "png"])

    if uploaded_file:
        st.image(uploaded_file, caption="Your Uploaded Image", use_container_width=True)

with top_right:
    st.subheader("Matched Princess")
    matched_princess = "belle"  # Placeholder match result
    st.markdown(f"You look most like **{matched_princess.title()}**!")

    # Show image if available
    try:
        princess_image = Image.open(f"princess_images/{matched_princess}.jpg") 
        st.image(princess_image, caption=f"{matched_princess.title()}", use_container_width=True)
    except:
        st.warning("Princess image not found.")

st.markdown("<br><br>", unsafe_allow_html=True)
st.divider()
st.markdown("<br><br>", unsafe_allow_html=True)

# Middle: Text-based input
bottom_left, bottom_right = st.columns(2)

with bottom_left:
    st.subheader("Enter personality text")
    user_text = st.text_area("Describe yourself or paste some dialogue to analyze personality")
    
    if user_text:
        st.markdown("*(Pretend we're analyzing the text...)*")
        # plug in a model here later
        st.info("Using default user personality scores for demo")

    # Display Personality-Based Matched Princess
    st.subheader("Your Personality Matches Best With:")

    personality_princess = "elsa"  # Replace this with actual personality-matching logic

    st.markdown(f"Based on your personality, you're most like **{personality_princess.title()}**!")

    # Try to show personality princess image
    try:
        personality_img = Image.open(f"princess_images/{personality_princess}.jpg")
        st.image(personality_img, caption=f"{personality_princess.title()}", use_container_width=True)
    except:
        st.warning("Personality princess image not found.")


with bottom_right:
    st.subheader("Personality Radar Plot")

    with st.expander("🧠 What do the Big Five traits mean?"):
        st.markdown("""
        - **Openness**: Creativity, imagination, curiosity  
        - **Conscientiousness**: Organization, responsibility, self-discipline  
        - **Extraversion**: Sociability, energy, talkativeness  
        - **Agreeableness**: Compassion, cooperativeness, kindness  
        - **Neuroticism**: Tendency to experience anxiety, fear, or emotional instability
        """)

    def radar_chart(user, princess, label):
        categories = list(user.keys())
        fig = go.Figure()

        fig.add_trace(go.Scatterpolar(
            r=list(user.values()),
            theta=categories,
            fill='toself',
            name="You"
        ))

        fig.add_trace(go.Scatterpolar(
            r=list(princess.values()),
            theta=categories,
            fill='toself',
            name=label
        ))

        fig.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[1, 5])),
            showlegend=True
        )
        return fig

    princess_traits = princess_personality.get(matched_princess, None)
    if princess_traits:
        fig = radar_chart(user_personality, princess_traits, matched_princess.title())
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("No personality data available for this princess.")
