import streamlit as st
from datetime import date, timedelta


st.title("Streamlit Travel Planner")
st.divider()


# ================
# RESORT SELECTION
# ================


st.header("Resort Selection")

resort_type = st.radio(
    "Do you have a preference for a family-friendly resort or adults-only?",
    [
        "Family-Friendly", 
        "Adults Only", 
        "Either"
    ],
    index=None  # No default selected
)


if resort_type is not None:  # Runs once a resort type is selected

    amenity_options = [
        "Nature Activities",
        "Eco-Friendly",
        "Water Park",
        "Lighthouse",
        "Dolphin Pool"
    ]     
    
    amenities = st.multiselect(
        "Select your most preferred amenities or 'No preference'.", 
        amenity_options
    )

    no_preference = st.checkbox("No preference") 


    if no_preference and amenities:  # If a user selects an option from the dropdown AND the checkbox
        st.error("Please select either from the amenities list or 'No preference' (not both).")

    elif no_preference or amenities:           

        if resort_type == "Adults Only":

            resort = "Sandos Cancun"
            st.info(f"We recommend: {resort}")

            if amenities and not no_preference:  # Amenities are limited only to the family-friendly options
                st.warning("Note: While this resort does not offer the amenities above, it does provide a world-class adults-only experience.")


        elif resort_type in ["Family-Friendly", "Either"]:

            sandos_amenities = [
                "Nature Activities", 
                "Eco-Friendly", 
                "Water Park"
            ]

            hyatt_amenities = [
                "Lighthouse", 
                "Dolphin Pool"
            ]

            sandos_selected = any(a in sandos_amenities for a in amenities)
            hyatt_selected = any(a in hyatt_amenities for a in amenities)

            if sandos_selected and not hyatt_selected:
                resort = "Sandos Caracol"       

            elif hyatt_selected and not sandos_selected:
                resort = "Hyatt Ziva Cancun" 

            else:
                resort = "Hyatt Ziva Cancun"  # Default in the event that amenities from both resorts are selected

            st.info(f"We recommend: {resort}")  


        # =============
        # ROOM CATEGORY
        # =============


        st.divider()
        st.subheader("Room Category")  # Runs once the elements above have been determined and the resort recommendation displays

        room_rates = {
            "Standard": 200,
            "Ocean View": 300,
            "Junior Suite Tropical View": 400,
            "Club": 500
        }

        room_category = st.selectbox(
            "Please select a room category.",        
            list(room_rates.keys()),
            index=None,
            placeholder="Select..."
        )   

        if room_category is not None:
            rate = room_rates[room_category]
            st.caption(f"Estimated nightly rate: ${rate}/night")


            # ============
            # TRAVEL DATES
            # ============


            st.divider()
            st.header("Travel Dates")  # Runs once the elements above have been determined and the nightly rate displays

            today = date.today()  

            arrival_date = st.date_input(
                "Arrival:",
                value=None,
                format="MM/DD/YYYY",
                min_value=today  # Prevents booking in the past
            )

            if arrival_date is not None:
                
                departure_date = st.date_input(  # Runs once the elements above have been determined and an arrival date is selected
                    "Departure:",
                    value=None,
                    format="MM/DD/YYYY",
                    min_value=arrival_date + timedelta(days=1)  # Prevents booking for less than 1 night
                )

                if departure_date is not None:  # Runs once the elements above have been determined and the departure date is selected

                    num_nights = (departure_date - arrival_date).days                   
                    
                    st.write(f"Number of nights: {num_nights}")


                    # ===================
                    # CHECKBOX & ESTIMATE
                    # ===================


                    st.divider()
                    st.header("Estimated Cost")  # Runs once the elements above have been determined and the number of nights displays

                    checkbox = st.checkbox("I understand that this is only an estimate and is subject to change until confirmation.")

                    estimate_button = st.button("Calculate Trip Cost")

                    if estimate_button:  # Runs once the elements above have been determined and the estimate button is clicked

                        if not checkbox:  # Checkbox required for calculation
                            st.error("Please check the checkbox above in order to continue.")

                        else:  # Runs once the elements above have been determined and the checkbox is clicked

                            st.subheader("Your Trip Summary")

                            trip_cost = rate * num_nights
                            
                            summary = [
                                ["Recommended Resort", resort],
                                ["Room Category", room_category],
                                ["Arrival Date", arrival_date.strftime("%m/%d/%Y")],
                                ["Departure Date", departure_date.strftime("%m/%d/%Y")],
                                ["Number of Nights", num_nights],
                                ["Nightly Rate", f"${rate:,.2f}"]                                
                            ]

                            st.table(summary)
                            
                            st.metric(
                                label="Your Estimated Cost:",
                                value=f"${trip_cost:,.2f}"
                            )                          

                            st.warning("Note: This does not include airfare, luggage fees, transportation, etc.")