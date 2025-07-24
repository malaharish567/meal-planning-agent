import streamlit as st
from agents.meal_plan_agent import MealPlanningAgent
import os

# Page configuration
st.set_page_config(
    page_title="AI Meal Planning Agent",
    page_icon="🍳",
    layout="wide"
)

# Initialize the agent
@st.cache_resource
def load_agent():
    return MealPlanningAgent()

def main():
    st.title("🍳 AI Meal Planning Agent")
    st.markdown("Tell me what ingredients you have, and I'll suggest delicious recipes!")
    
    # Load agent
    try:
        agent = load_agent()
    except Exception as e:
        st.error("Failed to initialize the AI agent. Please check your API keys in the .env file.")
        st.stop()
    
    # Sidebar for user preferences
    with st.sidebar:
        st.header("Settings")
        dietary_restrictions = st.multiselect(
            "Dietary Restrictions",
            ["Vegetarian", "Vegan", "Gluten-Free", "Dairy-Free", "Nut-Free"]
        )
        
        cooking_skill = st.select_slider(
            "Cooking Skill Level",
            options=["Beginner", "Intermediate", "Advanced"],
            value="Intermediate"
        )
        
        prep_time = st.slider("Max Prep Time (minutes)", 10, 120, 30)
    
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Hi! I'm your AI meal planning assistant. What ingredients do you have available today?"}
        ]
    
    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Type your ingredients here..."):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Generate assistant response
        with st.chat_message("assistant"):
            with st.spinner("Finding recipes for you..."):
                try:
                    # Add context from sidebar
                    context = f"User preferences: Dietary restrictions: {', '.join(dietary_restrictions) if dietary_restrictions else 'None'}, "
                    context += f"Cooking skill: {cooking_skill}, Max prep time: {prep_time} minutes. "
                    
                    full_prompt = context + prompt
                    response = agent.chat(full_prompt)
                    st.markdown(response)
                    
                    # Add assistant response to chat history
                    st.session_state.messages.append({"role": "assistant", "content": response})
                    
                except Exception as e:
                    error_msg = "I'm having trouble right now. Please make sure your API keys are configured correctly."
                    st.error(error_msg)
                    st.session_state.messages.append({"role": "assistant", "content": error_msg})
    
    # Footer
    st.markdown("---")
    st.markdown("💡 **Tip**: List your ingredients like 'chicken, rice, onions, tomatoes' for best results!")

if __name__ == "__main__":
    main()