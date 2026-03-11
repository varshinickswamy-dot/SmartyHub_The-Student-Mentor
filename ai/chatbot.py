import random

def reply(msg):

    msg = msg.lower().strip()

    # ============================================
    # MEDICAL FIELD
    # ============================================

    if "medical" in msg or "doctor" in msg or "mbbs" in msg:
        return (
            "Medical field is suitable if:\n"
            "• You enjoy Biology\n"
            "• You want to save lives\n"
            "• You can handle long study years\n\n"
            "Path: NEET → MBBS → Internship → Specialization\n"
            "Top Careers: Doctor, Surgeon, Dentist, Pharmacist"
        )

    if "neet" in msg:
        return (
            "NEET Exam Info:\n"
            "• Subjects: Physics, Chemistry, Biology\n"
            "• Very competitive exam\n"
            "• Needs daily practice + revision\n\n"
            "Tip: Solve MCQs daily + mock tests"
        )

    # ============================================
    # ENGINEERING FIELD
    # ============================================

    if "engineering" in msg or "engineer" in msg:
        return (
            "Engineering is good if:\n"
            "• You like problem solving\n"
            "• You enjoy Maths & Technology\n\n"
            "Popular Branches:\n"
            "• Computer Science\n"
            "• AI & Data Science\n"
            "• Mechanical\n\n"
            "Path: JEE → B.Tech → Job / Higher Studies"
        )

    if "jee" in msg:
        return (
            "JEE Exam Info:\n"
            "• Subjects: Maths, Physics, Chemistry\n"
            "• Requires deep concept understanding\n"
            "• Daily practice needed\n\n"
            "Tip: Focus on NCERT + mock tests"
        )

    # ============================================
    # BUSINESS / COMMERCE
    # ============================================

    if "commerce" in msg or "business" in msg or "mba" in msg or "bba" in msg:
        return (
            "Business field suits you if:\n"
            "• You like management\n"
            "• You enjoy finance & marketing\n\n"
            "Courses:\n"
            "• BBA\n"
            "• B.Com\n"
            "• MBA\n\n"
            "Careers: Manager, Analyst, Accountant"
        )

    # ============================================
    # ARTS / DESIGN
    # ============================================

    if "arts" in msg or "design" in msg or "media" in msg:
        return (
            "Arts/Design field suits you if:\n"
            "• You are creative\n"
            "• You enjoy drawing/designing\n\n"
            "Careers:\n"
            "• Graphic Designer\n"
            "• UI/UX Designer\n"
            "• Animator"
        )

    # ============================================
    # STUDY PLAN
    # ============================================

    if "study plan" in msg or "how to study" in msg:
        return (
            "Simple Daily Study Plan:\n"
            "• 2 hrs concept learning\n"
            "• 2 hrs practice\n"
            "• 1 hr revision\n"
            "• 1 hr mock test\n\n"
            "Follow daily for best results."
        )

    # ============================================
    # STRESS / MOTIVATION
    # ============================================

    if "stress" in msg or "pressure" in msg or "depressed" in msg:
        return (
            "Don't worry, you are not alone ❤️\n\n"
            "• Take short breaks\n"
            "• Avoid comparison\n"
            "• Believe in yourself\n\n"
            "Small progress daily = Big success."
        )

    if "motivate" in msg or "motivation" in msg:
        return (
            "Believe in yourself 💪\n"
            "Consistency beats talent.\n"
            "Never give up.\n\n"
            "You can do it!"
        )

    # ============================================
    # GREETING
    # ============================================

    if "hi" in msg or "hello" in msg:
        return "Hello! I am your AI Counselor 🤖 Ask me about careers, exams or studies."

    # ============================================
    # FUNNY FALLBACK RESPONSES
    # ============================================

    funny_responses = [
        "Hmm... my brain.exe stopped working 🤯😂",
        "I am still a student bot, learning slowly 😅",
        "That question went over my head 🤪",
        "Ask me about careers or studies, not about aliens 👽😂",
        "Oops! I need more coffee to answer that ☕😆",
        "Interesting question... but I am not that smart yet 😜"
    ]

    return random.choice(funny_responses)