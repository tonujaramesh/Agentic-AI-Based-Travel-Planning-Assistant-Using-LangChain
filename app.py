import streamlit as st
from agent.travel_agent import run_travel_agent
from output.final_output import generate_final_output

# -------------------------------------------------
# Page Configuration
# -------------------------------------------------
st.set_page_config(
    page_title="Agentic AI Travel Planner",
    page_icon="🌍",
    layout="centered",
    initial_sidebar_state="expanded"
)

# -------------------------------------------------
# Header Section
# -------------------------------------------------
st.markdown("## 🌍 Agentic AI Travel Planning Assistant")
st.markdown(
    "Plan personalized trips using **AI-driven reasoning**, "
    "real-time data, and intelligent decision making."
)

st.divider()

# -------------------------------------------------
# Sidebar — User Inputs
# -------------------------------------------------
st.sidebar.title("🧭 Trip Preferences")

source = st.sidebar.text_input("Departure City", "Bangalore")
destination = st.sidebar.text_input("Destination City", "Goa")

days = st.sidebar.slider(
    "Trip Duration (Days)",
    min_value=3,
    max_value=7,
    value=4
)

budget = st.sidebar.slider(
    "Maximum Hotel Price per Night (₹)",
    min_value=1000,
    max_value=6000,
    value=3000,
    step=500
)

st.sidebar.subheader("📍 Destination Coordinates")
latitude = st.sidebar.number_input(
    "Latitude", value=15.2993, format="%.4f"
)
longitude = st.sidebar.number_input(
    "Longitude", value=74.1240, format="%.4f"
)

generate_plan = st.sidebar.button("🚀 Generate Travel Plan")

# -------------------------------------------------
# Main Content — AI Execution
# -------------------------------------------------
if generate_plan:
    with st.spinner("AI is planning your trip..."):
        agent_result = run_travel_agent({
            "source": source,
            "destination": destination,
            "days": days,
            "budget": budget,
            "latitude": latitude,
            "longitude": longitude
        })

        final_output = generate_final_output(agent_result, days)

    st.success("Your personalized travel plan is ready!")

    # -------------------------------------------------
    # Trip Summary
    # -------------------------------------------------
    st.subheader("📌 Trip Summary")
    summary = final_output["Trip Summary"]

    st.markdown(
        f"""
        **From:** {summary['From']}  
        **To:** {summary['To']}  
        **Duration:** {summary['Duration']}  
        **Hotel Category:** {summary['Hotel Category']}
        """
    )

    # -------------------------------------------------
    # Flight Details
    # -------------------------------------------------
    st.subheader("✈️ Flight Selected")
    flight = final_output["Flight Option Selected"]

    st.markdown(
        f"""
        **Airline:** {flight['Airline']}  
        **Price:** ₹{flight['Price']}  
        **Departure:** {flight['Departure']}  
        **Arrival:** {flight['Arrival']}  
        **Duration:** {flight['Duration']} hours
        """
    )

    # -------------------------------------------------
    # Hotel Recommendation
    # -------------------------------------------------
    st.subheader("🏨 Hotel Recommendation")
    hotel = final_output["Hotel Recommendation"]

    st.markdown(
        f"""
        **Hotel Name:** {hotel['Hotel Name']}  
        **Star Rating:** {hotel['Stars']} ⭐  
        **Price per Night:** ₹{hotel['Price Per Night']}  
        **Amenities:** {", ".join(hotel['Amenities'])}
        """
    )

    # -------------------------------------------------
    # Itinerary Section
    # -------------------------------------------------
    st.subheader("🗺️ Day-wise Itinerary")
    for day, details in final_output["Day-wise Itinerary"].items():
        st.markdown(f"**{day}:** {details['Activity']}")

    # -------------------------------------------------
    # Weather Forecast
    # -------------------------------------------------
    st.subheader("🌦️ Weather Forecast")
    for day, info in final_output["Weather Forecast"].items():
        st.markdown(
            f"**{day}:** "
            f"Max {info['Max Temp']}°C | "
            f"Min {info['Min Temp']}°C | "
            f"Wind {info['Wind Speed']} km/h"
        )

    # -------------------------------------------------
    # Budget Breakdown
    # -------------------------------------------------
    st.subheader("💰 Budget Breakdown")
    budget_info = final_output["Budget Breakdown"]

    col1, col2, col3 = st.columns(3)
    col1.metric("✈️ Flight", f"₹{budget_info['Flight Cost']}")
    col2.metric("🏨 Hotel", f"₹{budget_info['Hotel Cost']}")
    col3.metric("🍽️ Local", f"₹{budget_info['Local Expenses']}")

    st.divider()
    st.metric("💵 Total Estimated Cost", f"₹{budget_info['Total Estimated Budget']}")
