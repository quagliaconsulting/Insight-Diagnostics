import streamlit as st
import numpy as np
import plotly.graph_objects as go
import json
import os

# Define the grouped questions
grouped_questions = {
    'Psychiatric Symptoms': [
        'Do you have depression some days?',
        'Do you have significant anxiety?',
        'Do you have emotional liability (changes in your emotion frequently and quickly)?',
        'Do you have suicidal thoughts?'
    ],
    'Cognition': [
        'Do you have word finding difficulty worse than other people your age?',
        'Do you have changes in your memory?',
        'Do you have difficulty multitasking or slower mental processing speed?'
    ],
    'Vision': [
        'Do you have vision problems?',
        'Do you have double vision sometimes (seeing 2 objects instead of 1)?',
        'Do you have oscillopsia (see the world shaking)?',
        'Do you have trouble focusing on near objects (reading)?',
        'Do you have trouble focusing on far objects (seeing the TV)?',
        'Do you have difficulty moving your eyes or have eye lid spasms?'
    ],
    'Speech/Swallow': [
        'Do you have a quiet voice?',
        'Do you have slurred speech?',
        'Do you choke on food or drink?',
        'Do you have trouble swallowing?'
    ],
    'Balance': [
        'Do you lose your balance or fall?',
        'Do you have difficulty walking?',
        'Do you use a walker or wheelchair?'
    ],
    'Synucleinopathy Signs': [
        'Do you have a tremor?',
        'Do you have rigidity (stiffness in your arms or legs)?',
        'Do you have bradykinesia (slowness in moving your arms or legs)?',
        'Do you have dystonia (abnormal postures)?'
    ],
    'Autonomics': [
        'Do you have significant or frequent constipation?',
        'Do you act out your dreams?',
        'Do you get lightheaded or the feeling you will pass out if you stand up quickly from laying?',
        'Do you have erectile dysfunction?'
    ],
    'Fine Motor': [
        'Has your handwriting changed?',
        'Are your hands clumsy (knocking over things? Trouble buttoning shirt?)'
    ]
}

def main():
    # Initialize session state variables if they don't exist
    if 'responses' not in st.session_state:
        st.session_state.responses = {}

    if 'page' not in st.session_state:
        st.session_state.page = "questions"

    if st.session_state.page == "questions":
        display_questions()
    elif st.session_state.page == "user_details":
        display_user_details()
    elif st.session_state.page == "summary":
        display_summary()

def display_questions():
    st.title("Ataxia Questionaire")

    # Display the logos
    col1, col2 = st.columns(2)
    col1.image("logos/JH.png", use_column_width=True, caption="Ataxia Center for Excellence")
    col2.image("logos/ID.png", use_column_width=True, caption="Insight Diagnostics")

    # Collect responses
    for group, questions in grouped_questions.items():
        st.subheader(group)
        for q in questions:
            st.session_state.responses[q] = st.slider(q, 0, 5, 2)  # Default value set to 2 (Middle value)

    # Display plots and recommendations
    display_plots_and_recommendations()

    # Check if user has clicked the "Submit" button
    if st.button("Submit Responses"):
        st.session_state.page = "user_details"
        st.rerun()

def display_user_details():
    # Collect additional user details
    st.title("Please enter your details")
    st.session_state.name = st.text_input("Name:")
    st.session_state.birthday = st.text_input("Birthday:")
    st.session_state.mrn = st.text_input("JH MRN:")

    if st.button("Submit Details"):
        st.session_state.page = "summary"
        st.rerun()

def display_summary():
    st.subheader("Summary")
    st.write(f"Name: {st.session_state.name}")
    st.write(f"Birthday: {st.session_state.birthday}")
    st.write(f"JH MRN: {st.session_state.mrn}")

    # Display the stored recommendation
    st.subheader("Recommendation")
    st.write(f"Based on your responses, we recommend consulting an expert in **{st.session_state.recommended_group}**.")

    st.subheader("Responses")
    for question, response in st.session_state.responses.items():
        st.write(f"{question}: {response}")

    st.subheader("Database Upload")
    save_data_to_json()  # Save data to a JSON file
    upload_to_azure()    # Placeholder for Azure upload    

def save_data_to_json():
    # Organize data into a dictionary
    data = {
        'name': st.session_state.name,
        'birthday': st.session_state.birthday,
        'mrn': st.session_state.mrn,
        'responses': st.session_state.responses,
        'recommended_group': st.session_state.recommended_group
    }

    # Convert the dictionary to a JSON string
    json_str = json.dumps(data, indent=4)

    # Define the path where the JSON file will be saved
    save_path = os.path.join("C:", os.sep, "Users", "James", "Documents", "Insight Diagnostics", "responses", f"{st.session_state.mrn}.json")

    # Write the JSON string to a file
    with open(save_path, 'w') as json_file:
        json_file.write(json_str)

    st.write(f"Data has been saved to a JSON file at {save_path}.")        

def upload_to_azure():
    # Placeholder for Azure upload
    st.write("Uploading to Azure... (placeholder)")

# ... [your main function]        
   
def display_plots_and_recommendations():
    # Calculate group scores for recommendation
    group_scores = {}
    for group, questions in grouped_questions.items():
        valid_responses = [st.session_state.responses[q] for q in questions]
        group_scores[group] = np.mean(valid_responses)

    # Define distinct colors for each group
    colors = [
        '#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd',
        '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf'
    ]

    color_map = {group: colors[i] for i, group in enumerate(grouped_questions)}

    # Prepare data for Plotly clustered bar chart
    bars_data = []
    x_labels = []

    for group, questions in grouped_questions.items():
        # Flag to show legend only for the first question of each group
        show_legend = True
        for q in questions:
            x_labels.append(q)
            bars_data.append(
                go.Bar(
                    name=group,
                    x=[q],
                    y=[st.session_state.responses[q]],
                    width=[0.15],  # this controls the width of each bar
                    marker_color=color_map[group],  # set color based on group
                    legendgroup=group,  # group bars by their group in the legend
                    showlegend=show_legend  # show legend only for the first question of each group
                )
            )
            show_legend = False

    # Create the Plotly figure
    fig = go.Figure(data=bars_data)

    # Update layout for better visualization
    fig.update_layout(
        barmode='group',
        title="Survey Results",
        xaxis_title="Questions",
        xaxis={'tickvals': list(range(len(x_labels))), 'ticktext': x_labels, 'tickangle': -45},
        yaxis_title="Score",
        yaxis=dict(tickvals=list(range(6)), ticktext=[str(i) for i in range(6)]),
        legend_title="Groups",
        width=1200,  # Set the width of the graph
        height=800,   # Set the height of the graph
        margin=dict(l=0, r=50, b=150, t=50)  # Adjust left, right, bottom, and top margins as needed
    )

    # Provide recommendation
    st.session_state.recommended_group = max(group_scores, key=group_scores.get)
    st.subheader("Recommendation")
    st.write(f"Based on your responses, we recommend consulting an expert in **{st.session_state.recommended_group}**.")

    # Display the Plotly chart in Streamlit
    st.plotly_chart(fig)

if __name__ == "__main__":
    main()
