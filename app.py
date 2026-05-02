# 1. Importing extensions 
import streamlit as st 
import google.generativeai as ai

# 2. Creating app title
st.title('AI Studying Assistant✨')

# 3. Gemini setup   
gemini = 'gemini-3.1-flash-lite-preview'
api_key = "AIzaSyCMC4tXRKI-WV5lDMFHVAAbxW0JSdyLa3k"
ai.configure(api_key=api_key)
model = ai.GenerativeModel(model_name=gemini)

# 4. Making app tabs
questions_tab, quizzes_tab, planner_tab = st.tabs(
    ['Q&A ⁉️', 'Quizzes📃', 'Study Planner✅'])

# 5. Building the questions tab
with questions_tab:
    col1, col2 = st.columns(2)
    
    # Building column 1
    with col1:
        subject = st.selectbox(label='Choose a subject:',
            options=['Math', 'Programming', 'Physics', 'AI'])
        tone = st.selectbox(label='choose a tone:', 
            options=['Friendly', 'Professional'])
    
    # Building column 2
    with col2:
        details = st.selectbox(label='Choose level of details:',
            options=['Brief', 'Medium', 'Detailed'])
        edu_level = st.selectbox(label='Choose educational level:', 
            options=['School', 'University', 'Graduated'])
    
    st.divider()
    
    # Adding the chatting widget 
    question = st.chat_input('Enter your question:')
    
    # If the question is asked
    if question:
        # 1st chatting message
        with st.chat_message('human', avatar='😉'):
            st.write(question)
        
        # 2nd chatting message 
        with st.chat_message('ai', avatar='🤖'):
            prompt = f'''
            You are an expert AI Studying assistant
            that will answer me this question in {subject}: 
            {question}

            Customize your answer using this info:
            I am with {edu_level} education level and
            I need a {details} level of details with 
            explaining it in {tone} tone. 
            
            In case of the level of details is brief, 
            answer within 30 words
            '''
            with st.spinner('Generating...🧠'):
                answer = model.generate_content(prompt)
            st.write(answer.text)

# 6. Building the quizzes tab         
with quizzes_tab:

    # Creating a list of available quiz subjects
    subjects = [
        'Biology', 'Physics', 'Math', 'Chemistry',
        'Languages', 'Art', 'Social Science',
        'Computer Science', 'Entreprenuership'
    ]

    # Creating difficulty levels
    difficulty = ['Easy', 'Medium', 'Hard', 'Advanced']

    # Creating two columns for layout
    col1, col2 = st.columns(2)

    # Building column 1
    with col1:

        # Creating subject selector using pills UI
        sub_option = st.pills(
            "Choose subject:",
            options=subjects
        )

    # Building column 2
    with col2:

        # Dropdown for selecting quiz difficulty
        level = st.selectbox(
            "Choose difficulty",
            options=difficulty
        )

        # Input to select number of quiz questions
        questions_count = st.number_input(
            "Number of questions",
            min_value=1,
            max_value=20,
            value=5
        )

    # Text area to allow the user to specify the quiz topic
    topic = st.text_area("Enter quiz topic")

    # Button to generate quiz
    if st.button("Generate Quiz"):

        # Creating the prompt sent to Gemini
        prompt = f"""
        Create a quiz.

        Subject: {sub_option}
        Difficulty: {level}
        Number of Questions: {questions_count}

        Topic:
        {topic}

        Format:
        - Multiple choice
        - Provide correct answers
        """

        # Generating quiz using Gemini
        with st.spinner("Generating quiz...📃"):
            response = model.generate_content(prompt)

            # Displaying the generated quiz
            st.write(response.text)


# 7. Creating the planner tab
with planner_tab:

    # Creating the planner title
    st.title("📅 AI Study Planner")

    # Creating two columns for planner inputs
    col1, col2 = st.columns(2)

    # Building column 1
    with col1:

        # Creating a list of subjects for the study planner
        subjects = [
            'Biology', 'Physics', 'Math', 'Chemistry',
            'English', 'French', 'German',
            'Social Science', 'ICT', 'Entrepreneurship'
        ]

        # Allowing users to select multiple subjects
        selected_subjects = st.multiselect(
            "📚 Choose subjects",
            subjects,
            default=['Math', 'English']
        )

        # Selecting the time duration of each study session
        study_time = st.time_input(
            "⏱️ Time per study session"
        )

    # Building column 2
    with col2:

        # Input for number of subjects to study per day
        subjects_per_day = st.number_input(
            "📅 Subjects per day",
            min_value=1,
            max_value=len(subjects),
            value=3
        )

        # Control for selecting how many days per week to study
        study_days_per_week = st.segmented_control(
            "📆 Study days per week",
            options=list(range(1, 8)),
            width='stretch'
        )

    # Divider to separate inputs from output
    st.divider()

    # Button to generate study plan
    generate_plan = st.button("📝 Generate Study Plan")

    # Generate study plan when button is clicked
    if generate_plan and selected_subjects:

        # Displaying the user's study preferences
        preferences_text = f"""
        Subjects: {', '.join(selected_subjects)}
        Time per session: {study_time.strftime('%H:%M')}
        Subjects per day: {subjects_per_day}
        Study days per week: {study_days_per_week}
        """

        # Showing user preferences in chat format
        with st.chat_message("human"):
            st.write(preferences_text)

        # Creating prompt for Gemini to generate the study plan
        planner_prompt = f"""
        You are an expert study planner.

        Student Preferences:
        Subjects: {', '.join(selected_subjects)}
        Time per study session: {study_time.strftime('%H:%M')}
        Subjects per day: {subjects_per_day}
        Study days per week: {study_days_per_week}

        Instructions:
        - Output a study plan table.
        - Include study days and subjects.
        - Distribute subjects evenly.
        - Keep it simple and clear.
        """

        # Generating the study plan
        with st.chat_message("ai"):
            with st.spinner("Creating your study plan..."):

                response = model.generate_content(planner_prompt)

                # Saving the generated plan
                plan = response.text

                # Displaying the plan
                st.write(plan)