import streamlit as st
import os
import json

# Define the directory path where the .json files are located
DIRECTORY_PATH = 'C:/Users/James/Documents/Insight Diagnostics/responses'

def list_json_files(directory):
    """Return a list of .json files in the specified directory."""
    return [f for f in os.listdir(directory) if f.endswith('.json')]

def load_json_file(file_path):
    """Load the content of a JSON file."""
    with open(file_path, 'r') as f:
        return json.load(f)

def save_json_file(file_path, content):
    """Save the content to a JSON file."""
    with open(file_path, 'w') as f:
        json.dump(content, f, indent=4)

# Main Streamlit app
def main():
    st.title('Ataxia Questionaire Editor')

    # Display the logos
    col1, col2 = st.columns(2)
    col1.image("logos/JH.png", use_column_width=True, caption="Ataxia Center for Excellence")
    col2.image("logos/ID.png", use_column_width=True, caption="Insight Diagnostics")
    
    # List all .json files in the directory
    json_files = list_json_files(DIRECTORY_PATH)
    selected_file = st.selectbox('Select a submission file:', json_files)
    
    # Load the content of the selected file
    file_content = load_json_file(os.path.join(DIRECTORY_PATH, selected_file))
    
    # Display the JSON content in a text area with increased height
    edited_content = st.text_area('Edit submission content:', value=json.dumps(file_content, indent=4), height=1000)
    
    # Provide a button to save changes
    if st.button('Save Changes'):
        try:
            # Parse the edited content to ensure it's valid JSON
            parsed_content = json.loads(edited_content)
            
            # Save the parsed content to the file
            save_json_file(os.path.join(DIRECTORY_PATH, selected_file), parsed_content)
            st.success('Changes saved successfully!')
        except json.JSONDecodeError:
            st.error('Invalid JSON content. Please correct it before saving.')

if __name__ == '__main__':
    main()
