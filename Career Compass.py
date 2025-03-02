#imports for all the libraries used in the program
import os
from Aigeneration import gemini_run
import customtkinter as ctk
import pyttsx3
import sqlite3
import atexit
from auth_file import get_user_info  


# connecting the Database to the program
conn = sqlite3.connect('career_compass.db')
cursor = conn.cursor()

#to close the database connection
def close_db_connection():
    conn.close()

atexit.register(close_db_connection)

#creating the quiz screen class to display the quiz questions as a parents
class QuizScreen(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="#2c3e50")  # Set background for the frame

        #displaying an instruction to the user to complete quiz 
        label = ctk.CTkLabel(self, text="Complete the Quiz", font=("Arial", 16), text_color="white")
        label.pack(pady=10, padx=10)

        # Create a dictionary to store the user's career choices
        self.career = {
            "A": 0,
            "B": 0,
            "C": 0,
            "D": 0
        }

        # Fetch questions from the database
        self.questions = self.fetch_questions_from_db()

        # creates the variables to store the current question index, radio buttons, and selected option
        self.current_question_index = 0
        self.radio_buttons = []
        self.selected_option = ctk.StringVar()

        # Create the question frame
        self.question_frame = ctk.CTkFrame(self, fg_color="#2c3e50")
        self.question_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Create the question label
        self.question_label = ctk.CTkLabel(self.question_frame, text="", font=("Arial", 14), text_color="white", wraplength=400)
        self.question_label.pack(pady=10)

        #calls the load_question function to display the  question
        self.load_question()
        
        # Create the button frame
        self.button_frame = ctk.CTkFrame(self, fg_color="#2c3e50")
        self.button_frame.pack(fill="x", padx=10, pady=10)

        # Create the next button to go to the next question
        self.next_button = ctk.CTkButton(self.button_frame, text="Continue to the next question", command=self.next_question, fg_color="#f39c12", text_color="black")
        self.next_button.pack(side="left", padx=5)

        #text to speech function 
        self.tts_on_of = ctk.CTkButton(self.button_frame, text="Speak", command=self.text_to_speech, fg_color="#3498db", text_color="white")
        self.tts_on_of.pack(side="right", padx=5)

    def fetch_questions_from_db(self):
        cursor.execute("SELECT QuestionID, QuestionDescription FROM Quiz")
        

        questions = cursor.fetchall()
        question_list = []
        
        #for loop to iterate over the questions in the db 
        for question in questions:
            cursor.execute("SELECT OptionText FROM Options WHERE QuestionID = ?", (question[0],))
            options = cursor.fetchall()
            
            #appending the questions and options to the question list
            question_list.append({
                "question": question[1],
                "options": [option[0] for option in options]
            })

        #displaying the questions
        return question_list

    #function to load the questions
    def load_question(self):
        
        #fetching the question data from the questions list
        question_data = self.questions[self.current_question_index]
        
        #setting the question and options to the question data
        self.question = question_data["question"]
        self.options = question_data["options"]

        self.question_label.configure(text=self.question)

        #when the radio buttons are clicked, the selected option is stored and then cleared 
        for i in self.radio_buttons:
            i.destroy()
        self.radio_buttons.clear()

        #for loop to display each question
        for j in self.options:
            R1 = ctk.CTkRadioButton(self.question_frame, text=j, value=j, variable=self.selected_option, text_color="white", fg_color="#2c3e50", hover_color="#34495e")
            R1.pack(anchor='w')
            self.radio_buttons.append(R1)

    #function to convert the text to speech on the quiz screen
    def text_to_speech(self):
        engine = pyttsx3.init()
        engine.say(self.question)
        engine.say(self.options)
        engine.runAndWait()


    #function to go to the next question
    def next_question(self):
        #storing the selected option
        self.selected_career = self.selected_option.get()
        
        if self.selected_career:
            self.stripped_option = self.selected_career[0]

            if self.stripped_option in self.career:
                self.career[self.stripped_option] += 1

        self.current_question_index += 1

        if self.current_question_index < len(self.questions):
            self.load_question()
        else:
            self.show_results()
    
    #function to show the results of the quiz
    def show_results(self):
        #clearing the screen
        for widget in self.winfo_children():
            widget.pack_forget()

        #finding the best career fit from the results of the quiz
        self.best_career = max(self.career, key=self.career.get)

        #if statements to display the best career fit
        if self.best_career == 'A':
            self.result_label = ctk.CTkLabel(self, text="Best Career Fit: Technology", font=("Arial", 12, "bold"), text_color="white")
        elif self.best_career == 'B':
            self.result_label = ctk.CTkLabel(self, text="Best Career Fit: Healthcare", font=("Arial", 12, "bold"), text_color="white")
        elif self.best_career == 'C':
            self.result_label = ctk.CTkLabel(self, text="Best Career Fit: Creative Arts", font=("Arial", 12, "bold"), text_color="white")
        elif self.best_career == 'D':
            self.result_label = ctk.CTkLabel(self, text="Best Career Fit: Business", font=("Arial", 12, "bold"), text_color="white")
        self.result_label.pack(pady=20)

        #button to continue to the next screen
        learn_more = ctk.CTkButton(self, text=f"Learn more about your career", font=("Arial", 12, "bold"), fg_color="#e74c3c", text_color="white", command=self.change_more_info)
        learn_more.pack(pady=20)

    #function to change the screen to the MoreInformation class
    def change_more_info(self):
        for widget in self.winfo_children():
            widget.destroy()

        infoCareer = MoreInformation(self, self.best_career)
        infoCareer.pack(padx=10, pady=10)


#create the MoreInformation class to display the main screen
class MoreInformation(ctk.CTkFrame):
    def __init__(self, parent, career_type):
        super().__init__(parent, fg_color="#2c3e50")

        # Store and clean career type input
        self.career_type = str(career_type).strip()

        # Header Label
        header_text = {
            'A': "Information on Technology Career",
            'B': "Information on Healthcare Career",
            'C': "Information on Creative Arts Career",
            'D': "Information on Business Career"
        }.get(self.career_type, "Information on Career")

        # Display the career chosen
        label = ctk.CTkLabel(self, text=header_text, font=("Arial", 16, "bold"), text_color="white")
        label.pack(pady=10, padx=10)

        # Notebook (Tabbed UI)
        notebook = ctk.CTkTabview(self)
        notebook.pack(expand=True, fill="both", padx=10, pady=10)

        # Add Tabs
        notebook.add("Overview")
        notebook.add("University")
        notebook.add("Extracurriculars")
        notebook.add("AI Suggestions")
        notebook.add("GPA Checker")

        # Create Frames for Tabs
        overview_and_salary = ctk.CTkFrame(notebook.tab("Overview"), fg_color="#34495e")
        university_and_certifications = ctk.CTkFrame(notebook.tab("University"), fg_color="#34495e")
        extracurriculars_tab = ctk.CTkFrame(notebook.tab("Extracurriculars"), fg_color="#34495e")
        ai_suggestions_tab = ctk.CTkFrame(notebook.tab("AI Suggestions"), fg_color="#34495e")
        gpa_checker_tab = ctk.CTkFrame(notebook.tab("GPA Checker"), fg_color="#34495e")

        # Pack Frames Inside Tabs
        overview_and_salary.pack(expand=True, fill="both")
        university_and_certifications.pack(expand=True, fill="both")
        extracurriculars_tab.pack(expand=True, fill="both")
        ai_suggestions_tab.pack(expand=True, fill="both")
        gpa_checker_tab.pack(expand=True, fill="both")

        # Call the display_career_info method to populate the tabs with career information
        self.display_career_info(overview_and_salary, university_and_certifications, ai_suggestions_tab, extracurriculars_tab, gpa_checker_tab)

    # Function to display the career information
    def display_career_info(self, overview_tab, university_tab, ai_suggestions, extracurriculars_tab, gpa_checker_tab):
        
        # Displaying the career information based on the career type chosen
        if self.career_type == "A":
            overview_text = "Tech has careers in software engineering, AI, and cybersecurity."
            university_text = "Top universities: MIT, Stanford, Waterloo.\nDegrees: CS, Engineering."
            university_rates = "Acceptance: MIT - 4%, Stanford - 4.4%, Waterloo - 53%."
            
            # Calling the gemini_run function to generate the summary of the career
            summary_tech = gemini_run(
                """
                The user is interested in Technology. 
                Generate 2 bullet points for the pros and cons of the Technology field. 
                Generate 2 Future Career Trends. 
                Remove any * formatting from the output.
                """
            )

            # Displaying the extracurricular activities for the career
            extracurriculars = """
            - Coding Club / Hackathons – Develop programming skills, work on real projects, and participate in coding competitions.

            - Robotics Club – Gain hands-on experience with engineering, AI, and automation.

            - Math & Science Competitions – Strengthen problem-solving skills crucial 

            - Personal Tech Projects (Apps, Websites, AI Models) – Show initiative by building and publishing projects.

            - Internships / Tech Volunteering – Gain real-world experience through internships, Fiverr gigs, or helping local businesses.
            """

            # Displaying the high school courses needed for the career
            courses_needed_highschool = """
            - Computer Science – Take coding and IT-related courses.
            - Mathematics – Advanced Functions, Calculus, and Data Management.
            - Science (Physics & Chemistry) – Useful for logical problem-solving.
            - Business & Entrepreneurship – You want to start a tech-related business.
            """

            # Displaying the university courses needed for the career
            courses_needed_university = """
            - Computer Science – Programming, algorithms, and software development.
            - Software Engineering – Software design, testing, and project management.
            - IT & Cybersecurity – Networking, system administration, and security.
            - Data Science & AI – Machine learning, statistics, and big data.
            - Mathematics – Linear algebra, discrete math, and probability.
            - Web Development – AWS, SQL, and front-end/back-end development.
            """
            # Displaying the key responsibilities for the career
            key_responsibilities = """
            - Software Development – Writing, testing, and debugging code; maintaining applications
            - IT Support – Troubleshooting technical issues, managing networks, and assisting users
            - Cybersecurity – Protecting systems, preventing cyber threats, and responding to breaches
            - Data Science & AI – Analyzing data, building machine learning models, optimizing algorithms
            """

            # Displaying the famous people and quotes for the career
            famous_people_and_quotes = [
                "Steve Jobs (Apple Co-Founder) - 'Innovation distinguishes between a leader and a follower.'",
                "Bill Gates (Microsoft Co-Founder) - 'Your most unhappy customers are your greatest source of learning.'",
                "Alan Turing (Father of Computer Science) - 'Sometimes it is the people no one can imagine anything of, who do the things no one can imagine.'",
                "Elon Musk (Tesla, SpaceX, OpenAI) - 'When something is important enough, you do it even if the odds are not in your favor.'"
            ]
            # Displaying the challenges for the career
            challenges = [
                "Rapid Technological Changes – 'Keeping up with evolving technologies, tools, and programming languages.'",
                "Cybersecurity Threats – 'Constant risk of hacking, data breaches, and malware attacks.'",
                "High Workload & Deadlines – 'Tight project timelines and long working hours.'",
                "Complex Problem-Solving – 'Debugging, optimizing, and troubleshooting intricate technical issues.'",
                "Collaboration & Communication – 'Effectively working with teams across different disciplines.'"
            ]
        elif self.career_type == 'B':
            overview_text = "Healthcare includes medicine, nursing, and biomedical research."
            university_text = "Top universities: Harvard, Johns Hopkins.\nDegrees: Medicine, Pre-med."
            university_rates = "Acceptance: Harvard - 3.1%, Johns Hopkins - 7.3%."
            
            summary_tech = gemini_run(
                """
                The user is interested in Healthcare. 
                Generate 2 bullet points for the pros and cons of the Technology field. 
                Generate 2 Future Career Trends. 
                Remove any * formatting from the output.
                """
            )
            extracurriculars = """
            - Health Science Club / HOSA – Participate in healthcare-related competitions and leadership events.

            - Volunteering at Clinics – Gain firsthand experience in patient care and the medical environment.

            - Medical Research or Science Fairs – Conduct independent research on biology, medicine, or healthcare advancements.

            - First Aid & CPR Certification – Learn essential life-saving skills and gain certifications that look great on applications.
            
            - Shadowing Doctors  – Observe medical professionals and explore different healthcare careers.
            """
            courses_needed_highschool = """
            - Biology – A must-have for any healthcare-related field.
            - Chemistry – Needed for understanding medicine and bodily functions.
            - Physics – Required for medical technology.
            - Mathematics – Functions, calculus, and statistics for data analysis.
            - Social Sciences (Psychology, Sociology) – Helpful for understanding patient care.
            """
            courses_needed_university = """
            - Biology – Human anatomy, physiology, and microbiology.
            - Chemistry – General, organic, and biochemistry for medical applications.
            - Physics – Essential for medical imaging, biomechanics, and understanding body functions.
            - Mathematics – Statistics and calculus for medical research and data analysis.
            - Health Sciences – Covers healthcare systems, ethics, and medical technology.
            - Nursing or Pre-Med Courses – Pathophysiology, pharmacology, and clinical training.
            """
            key_responsibilities = """
            - Medical Research – Conducting experiments, collecting data, and analyzing results
            - Patient Care – Diagnosing, treating, and caring for patients
            - Healthcare Management – Managing healthcare facilities, staff, and resources
            - Public Health – Promoting health, preventing disease, and protecting populations
            """
            famous_people_and_quotes = [
                "Hippocrates (Father of Medicine) - 'Wherever the art of medicine is loved, there is also a love of humanity.'",
                "William Osler (Pioneer of Modern Medical Education) - 'The good physician treats the disease; the great physician treats the patient who has the disease.'",
                "Joans Salk (Developer of Polio Vaccine) - 'Hope lies in dreams, in imagination, and in the courage of those who dare to make dreams into reality.'"
            ]
            challenges = [
                "High-Stress Environment – 'Working in high-pressure situations, making life-or-death decisions.'",
                "Continuous Learning – 'Staying up-to-date with the latest medical research, technologies, and treatments.'",
                "Emotional Demands – 'Dealing with patients' suffering, death, and emotional trauma.'",
                "Long Hours – 'Working long shifts, including nights, weekends, and holidays.'",
                "Physical Demands – 'Standing for long periods, lifting patients, and working in a fast-paced environment.'"
            ]
        elif self.career_type == 'C':
            overview_text = "Creative Arts includes graphic design, film, and digital animation."
            university_text = "Top universities: RISD, CalArts.\nDegrees: Fine Arts, Digital Media."
            university_rates = "Acceptance: RISD - 17%, CalArts - 25%."
            summary_tech = gemini_run(
                """
                The user is interested in Creative Arts. 
                Generate 2 bullet points for the pros and cons of the Technology field. 
                Generate 2 Future Career Trends. 
                Remove any * formatting from the output.
                """
            )
            extracurriculars = """
            - Art Club / School Newspaper  – Develop skills in graphic design, photography, and visual storytelling.

            - Theater / Drama Club – Gain experience in acting, scriptwriting, stage design, and directing.

            - Film & Video Production Club / YouTube Channel – Learn filmmaking, editing, and content creation.

            - Fashion Design /  Music Production Projects – Build a portfolio with original work in creative arts

            - Freelancing or Selling Artwork Online (Fiverr, Etsy,) – Gain real-world experience by selling digital or physical creative work.
            """
            courses_needed_highschool = """
            - Visual Arts – Drawing, painting, sculpture, and digital art.
            - Media Arts – Photography, videography, and digital design.
            - Drama & Music – Performance-based courses for theater, acting, or music production.
            - English & Creative Writing – Develops storytelling and writing skills.
            - Business & Marketing – Helps with freelancing, branding, and selling artwork.
            - Technology (Graphic Design, Animation, Web Design) – Useful for digital art careers.
            """
            courses_needed_university = """
            - Fine Arts – Painting, drawing, sculpture, and mixed media.
            - Graphic Design – Digital art, branding, and visual communication.
            - Photography & Videography – Camera techniques and editing, 
            - Animation & Multimedia – 2D/3D animation and visual effects, 
            - Performing Arts – Acting, theater, dance, or music production.
            - Art History – Understanding artistic movements and influences.
            """
            key_responsibilities = """
            - Graphic Design – Creating visual elements, such as logos, graphics, and typography
            - Film Production – Producing, directing, and editing films, television shows, and commercials
            - Digital Animation – Creating 2D and 3D animations, special effects, and visual effects
            - Fine Arts – Creating paintings, sculptures, and other forms of visual art
            """
            famous_people_and_quotes = [
                "Pablo Picasso (Painter and Sculptor) - 'Every child is an artist. The problem is how to remain an artist once we grow up.'",
                "Leonardo Da Vinci (Renaissance Artist & Inventor) - 'Art is never finished, only abandoned.'",
                "Maya Angelou (Poet & Writer) - 'You can’t use up creativity. The more you use, the more you have.'",
                "Georgia O’Keeffe (Modernist Painter) - 'To create one’s world in any of the arts takes courage.'"
            ]
            challenges = [
                "High Competition – 'Standing out in the field, getting noticed by clients.'",
                "Continuous Learning – 'Staying up-to-date with latest design trends and technologies.'",
                "Time Management – 'Meeting deadlines, and managing multiple projects.'",
                "Criticism – 'Dealing with constructive criticism, rejection, and negative feedback.'",
                "Self-Motivation – 'Staying motivated, inspired, and creative in a fast-paced and often demanding field.'"
            ]
        elif self.career_type == 'D':
            overview_text = "Business includes finance, marketing, and entrepreneurship."
            university_text = "Top universities: Wharton, Harvard Business.\nDegrees: BBA, Economics."
            university_rates = "Acceptance: Wharton - 24.8%, Harvard Business - 11%."
            summary_tech = gemini_run(
                """
                The user is interested in Business. 
                Generate 2 bullet points for the pros and cons of the Technology field. 
                Generate 2 Future Career Trends. 
                Remove any * formatting from the output.
                """
            )
            extracurriculars = """
            - FBLA (Future Business Leaders of America)  – Compete in business-related events.

            - Student Government / Leadership Roles – Develop management, negotiation, and organizational skills.

            - Starting a Small Business / Freelancing – Sell products or services (e.g., dropshipping, tutoring, graphic design)

            - Investment or Finance Club – Learn about stock markets, budgeting, and financial management.

            - Entrepreneurship Competitions (Diamond Challenge) – Pitch business ideas and network with industry professionals.
            """
            courses_needed_highschool = """
            - Business Studies – Introduction to marketing, finance, and entrepreneurship.
            - Accounting – Basic financial management and bookkeeping.
            - Economics – Understanding markets, supply and demand, and global trade.
            - Mathematics – Functions, calculus, and data management for financial analysis.
            - English & Communication – Essential for business writing, presentations, and negotiations.
            """
            courses_needed_university = """
            - Business Administration – Covers management, leadership, and operations.
            - Accounting & Finance – Budgeting, financial statements, and investments.
            - Marketing – Branding, advertising, and consumer behavior.
            - Economics – Microeconomics, macroeconomics, and market trends.
            - Entrepreneurship – Business planning, innovation, and startup strategies.
            - Business Law & Ethics – Understanding contracts, regulations, and ethical decision-making.
            """
            key_responsibilities = """
            - Financial Analysis – Analyzing financial data, creating forecasts, and making investment decisions
            - Marketing Strategy – Developing marketing campaigns, managing social media, and analyzing market trends
            - Entrepreneurship – Starting and running a business, managing finances, and making strategic decisions
            - Management – Leading teams, managing operations, and making strategic decisions
            """
            famous_people_and_quotes = [
                "Warren Buffet (Investor & CEO of Berkshire Hathaway) - 'The best investment you can make is in yourself.'",
                "Indra Nooyi (Former CEO of PepsiCo) - 'Whatever you do, throw yourself into it. Throw your head, heart, and hands into it.'",
                "Jeff Bezos (Founder of Amazon) - 'If you double the number of experiments you do per year, you’re going to double your inventiveness.'",
                "Oprah Winfrey (Media Mogul & Entrepreneur) - 'The biggest adventure you can take is to live the life of your dreams.'"
            ]
            challenges = [
                "High-Stakes Decision Making – 'Making decisions that impact the company's bottom line, reputation, and future.'",
                "Fast-Paced Environment – 'Working in a fast-paced and often unpredictable business environment.'",
                "Continuous Learning – 'Staying up-to-date with the latest business trends, technologies, and best practices.'",
                "Leadership – 'Leading teams, managing conflicts, and making tough decisions.'",
                "Risk Management – 'Managing risk, mitigating threats, and capitalizing on opportunities.'"
            ]
        else:
            # If the career type is not recognized, display default messages
            overview_text = "No data available."
            university_text = "No data available."
            university_rates = "No data available."
            summary_tech = "No data available."
            extracurriculars = "No data available."
            courses_needed_highschool = "No data available."
            courses_needed_university = "No data available."
            key_responsibilities = "No data available."
            famous_people_and_quotes = []
            challenges = []
        

        # Dictionary to store all the information of the career
        info = {
            'overview': overview_text,
            'university': university_text,
            'acceptance': university_rates,
            'summary': summary_tech,
            'extracurriculars': extracurriculars,
            'highschool_courses': courses_needed_highschool,
            'university_courses': courses_needed_university,
            'responsibilities': key_responsibilities,
            'famous_people': famous_people_and_quotes,
            'challenges': challenges
        }

        # Wrap length and font settings for the text
        wrap_length = 400
        font_settings = ("Arial", 13)

        # Creating multiple labels to display the information of the career
        overview_label = ctk.CTkLabel(overview_tab, text=info.get("overview", ""), font=font_settings, text_color="white", wraplength=wrap_length)
        overview_label.pack(pady=5, padx=5)

        famous_people_and_quotes_menu = ctk.CTkOptionMenu(overview_tab, values=info.get("famous_people", []))
        famous_people_and_quotes_menu.pack(pady=5, padx=5)

        university_label = ctk.CTkLabel(university_tab, text=info.get("university", ""), font=font_settings, text_color="white", wraplength=wrap_length)
        university_label.pack(pady=5, padx=5)

        university_rates_label = ctk.CTkLabel(university_tab, text=info.get("acceptance", ""), font=font_settings, text_color="white", wraplength=wrap_length)
        university_rates_label.pack(pady=5, padx=5)

        key_responsibilities_label = ctk.CTkLabel(overview_tab, text=info.get("responsibilities", ""), font=font_settings, text_color="white", wraplength=wrap_length)
        key_responsibilities_label.pack(pady=5, padx=5)

        challenges_label = ctk.CTkLabel(overview_tab, text='\n'.join(info.get("challenges", [])), font=font_settings, text_color="white", wraplength=wrap_length)
        challenges_label.pack(pady=5, padx=5)

        highschool_label = ctk.CTkLabel(university_tab, text="High School Courses:", font=(font_settings), text_color="white")
        highschool_label.pack(pady=(10, 0), padx=5)

        highschool_courses = ctk.CTkLabel(university_tab, text=info.get("highschool_courses", ""), font=("Arial", 11), wraplength=500, text_color="white")
        highschool_courses.pack(pady=5, padx=5)

        university_label2 = ctk.CTkLabel(university_tab, text="University Courses:", font=(font_settings), text_color="white")
        university_label2.pack(pady=(10, 0), padx=5)

        university_courses = ctk.CTkLabel(university_tab, text=info.get("university_courses", ""), font=("Arial", 11), wraplength=500, text_color="white")
        university_courses.pack(pady=5, padx=5)

        summary_label = ctk.CTkLabel(ai_suggestions, text=info.get("summary", ""), wraplength=400, font=(font_settings), text_color="white")
        summary_label.pack(pady=5, padx=5)

        extracurriculars_label = ctk.CTkLabel(extracurriculars_tab, text=info.get("extracurriculars", ""), wraplength=400, font=(font_settings), text_color="white")
        extracurriculars_label.pack(pady=5, padx=5)

        # GPA Checker label to display instruction to user
        gpa_label = ctk.CTkLabel(gpa_checker_tab, text="Enter your GPA:", font=(font_settings), text_color="white")
        gpa_label.pack(pady=5, padx=5)

        #input box to get the GPA from the user
        gpa_entry = ctk.CTkEntry(gpa_checker_tab, font=("Arial", 10))
        gpa_entry.pack(pady=5, padx=5)


        #function to check the GPA of the user
        def check_gpa():
            #use try except block to check if the GPA is valid
            try:   
                #get the GPA from the user
                gpa = float(gpa_entry.get())

                #if statements to check the GPA and display the results
                if (gpa >= 3.5):
                    result_text = ("Your GPA is excellent! You have a good chance of getting into top universities such as:\n"
                                    "- Harvard University\n"
                                    "- Stanford University\n"
                                    "- Massachusetts Institute of Technology (MIT)\n"
                                    "- University of Toronto\n"
                                    "- University of California, Berkeley")
                elif (3.0 <= gpa < 3.5):
                    result_text = ("Your GPA is good. You have a fair chance of getting into good universities such as:\n"
                                    "- University of Washington\n"
                                    "- University of British Columbia\n"
                                    "- Purdue University\n"
                                    "- Pennsylvania State University")
                else:
                    result_text = ("Your GPA is below average. Consider improving it with these strategies:\n"
                                    "- Develop a study schedule and stay consistent.\n"
                                    "- Seek help from tutors, teachers, or study groups.\n"
                                    "- Focus on improving test-taking strategies and completing assignments on time.")
                    
           #if the GPA is not valid(e.g the user enters a string), display an error message
            except ValueError:
                result_text = "Please enter a valid GPA."

            #configure the results label to display the  GPA
            result_label.configure(text=result_text)

        #button to check the GPA
        check_button = ctk.CTkButton(gpa_checker_tab, text="Check GPA", command=check_gpa, font=("Arial", 10), fg_color="#f39c12", text_color="black")
        check_button.pack(pady=10)

        #label to display the result of the GPA
        result_label = ctk.CTkLabel(gpa_checker_tab, text="", font=("Arial", 10), wraplength=400, text_color="white")
        result_label.pack(pady=5, padx=5)



#creating a master class GoogleAuthentication to display the user information
class GoogleAuthentication(ctk.CTkFrame):

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.geometry("500x600")


        # Get user info from authentication functionin auth_file.py
        name, user_id, email = get_user_info()

        # Header Label to display if authentication is good 
        label = ctk.CTkLabel(self, text="Google Authentication Succseful!", font=("Lemon", 16, "bold"), text_color="white")
        label.pack(pady=10)

        # Display user information  name, ID, email
        name_label = ctk.CTkLabel(self, text=f"Welcome, {name}!", font=("Lemon", 14))
        name_label.pack(pady=10)

        id_label = ctk.CTkLabel(self, text=f"User ID: {user_id}", font=("Lemon", 12))
        id_label.pack(pady=10)

        email_label = ctk.CTkLabel(self, text=f"User Email: {email}", font=("Lemon", 12))
        email_label.pack(pady=10)


        # Button to continue to the main screen
        continue_button = ctk.CTkButton(self, text="Continue to Program", command=self.go_to_main_screen)
        continue_button.pack(pady=20)

    #function to go to the Mainscreen class
    def go_to_main_screen(self):

        self.pack_forget()  # Hide authentication screen
        main_screen = MainScreen(self.master)
        main_screen.pack(fill="both", expand=True)


#creating the MainScreen class to display the starting information 
class MainScreen(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.master.title("Career Compass")
        self.master.geometry("500x600")

        # Set the background color
        self.master.configure(bg="#4750a1")

        # Create label for the name of the app
        self.initial_label = ctk.CTkLabel(self, text="Career Compass!", text_color="white", font=("Lemon ", 20))
        self.initial_label.place(relx=0.5, rely=0.3, anchor='center')

        # Button to start the journey
        self.continueButton = ctk.CTkButton(self, text="Start Your Journey", fg_color="#f39c12", font=("Lemon", 15),
                                            command=self.changeWindow)
        self.continueButton.pack(pady=20)

        # Show the main screen
        self.configure(fg_color="#4750a1")
        self.pack(fill="both", expand=True)

    def changeWindow(self):
        # Destroy the current screen and show the quiz screen
        for widget in self.winfo_children():
            widget.destroy()

        quiz_screen = QuizScreen(self)
        quiz_screen.pack(padx=10, pady=10)


#main function to run the program
if __name__ == "__main__":
    root = ctk.CTk()
    #make sure GoogleAuthentication is the first screen to appear
    auth_screen = GoogleAuthentication(master=root)
    auth_screen.pack(fill="both", expand=True)  # Ensure it appears in the window
    root.mainloop()