import sqlite3

# Connect to database
conn = sqlite3.connect('career_compass.db')
cursor = conn.cursor()

# Create Student Table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS  Student (
        ID INTEGER PRIMARY KEY,
        Name TEXT,
        School TEXT
    )
''')

cursor.execute('DELETE FROM Student')  # Clears all existing data


# Insert sample student data
cursor.executemany('INSERT INTO Student (ID, Name, School) VALUES (?, ?, ?)', [
    (1, 'John Doe 1', 'School 1'),
    (2, 'John Doe 2', 'School 2'),
    (3, 'John Doe 3', 'School 3')
])


# Create Quiz Table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Quiz (
        QuestionID INTEGER PRIMARY KEY AUTOINCREMENT,
        QuestionDescription TEXT NOT NULL
    )
''')

# Create Options Table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Options (
        OptionID INTEGER PRIMARY KEY AUTOINCREMENT,
        QuestionID INTEGER,
        OptionText TEXT NOT NULL,
        FOREIGN KEY (QuestionID) REFERENCES Quiz(QuestionID)
    )
''')

# Create Career Table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Career (
        CareerID INTEGER PRIMARY KEY AUTOINCREMENT,
        CareerName TEXT NOT NULL
    )
''')

# Create Courses Table (linked to Career)
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Courses (
        CourseID INTEGER PRIMARY KEY AUTOINCREMENT,
        CourseName TEXT NOT NULL,
        Level TEXT CHECK(Level IN ('High School', 'University')),
        CareerPath TEXT NOT NULL  -- Links to the career choice (A, B, C, or D)
    )
''')

# Create Extracurricular Table (linked to Career)
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Extracurricular (
        ActivityID INTEGER PRIMARY KEY AUTOINCREMENT,
        ActivityName TEXT NOT NULL,
        Category TEXT,
        CareerPath TEXT NOT NULL  -- Links to the career choice (A, B, C, or D)
    )
''')

# List of questions and options
questions = [
    ("What type of work do you enjoy the most?", [
        "A. Solving technical problems and developing software",
        "B. Caring for and assisting others in need",
        "C. Creating engaging visuals or digital content",
        "D. Analyzing data and making business decisions"
    ]),
    ("Which environment would you prefer to work in?", [
        "A. A tech-driven space where innovation is key",
        "B. A healthcare setting helping patients or clients",
        "C. A creative environment focused on design and branding",
        "D. A structured office handling finance or marketing"
    ]),
    ("What type of challenges do you like solving?", [
        "A. Debugging software and optimizing technology",
        "B. Diagnosing and treating health-related issues",
        "C. Designing eye-catching graphics or websites",
        "D. Understanding trends and making strategic decisions"
    ]),
    ("Which subjects interest you the most?", [
        "A. Computer Science or Engineering",
        "B. Biology or Health Sciences",
        "C. Art or Digital Design",
        "D. Business or Economics"
    ]),
    ("What type of tasks excite you?", [
        "A. Writing code and building applications",
        "B. Providing medical care or support",
        "C. Creating logos, websites, or digital content",
        "D. Managing financial strategies or marketing plans"
    ]),
    ("Which career field seems most appealing?", [
        "A. Software Development or Data Science",
        "B. Medicine or Nursing",
        "C. Graphic Design or Web Development",
        "D. Finance or Marketing"
    ])
]

# Insert Questions and Options into Database
for question_text, options in questions:
    cursor.execute('INSERT INTO Quiz (QuestionDescription) VALUES (?)', (question_text,))
    question_id = cursor.lastrowid  # Get the ID of the inserted question

    for option_text in options:
        cursor.execute('INSERT INTO Options (QuestionID, OptionText) VALUES (?, ?)', (question_id, option_text))

# Insert Sample Courses
cursor.executemany('''
    INSERT INTO Courses (CourseName, Level, CareerPath) VALUES (?, ?, ?)
''', [
    ("Computer Science", "University", "A"),
    ("Engineering Physics", "University", "A"),
    ("Biology", "University", "B"),
    ("Health Sciences", "University", "B"),
    ("Graphic Design", "University", "C"),
    ("Marketing", "University", "D"),
    ("Business Management", "University", "D")
])

# Insert Sample Extracurriculars
cursor.executemany('''
    INSERT INTO Extracurricular (ActivityName, Category, CareerPath) VALUES (?, ?, ?)
''', [
    ("Coding Club", "Clubs", "A"),
    ("Math Club", "Clubs", "A"),
    ("Volunteering at Hospital", "Volunteering", "B"),
    ("First Aid Training", "Workshops", "B"),
    ("Art Club", "Clubs", "C"),
    ("Social Media Marketing Club", "Clubs", "D"),
    ("Finance Club", "Clubs", "D")
])

# Commit and close
conn.commit()
conn.close()
print("Database setup complete.")
