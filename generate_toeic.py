import json
import random

subjects = ["The manager", "The CEO", "Mr. Smith", "Ms. Davis", "The board of directors", "The HR department", "Our team", "The client"]
objects = ["the report", "the proposal", "the contract", "the budget", "the new policy", "the presentation", "the design"]
times = ["tomorrow", "next week", "before Friday", "by the end of the month", "soon", "immediately"]

def generate_grammar():
    questions = []
    
    # Template 1: ask someone to do something
    for i in range(20):
        sub = random.choice(subjects)
        obj = random.choice(objects)
        time_word = random.choice(times)
        verbs = [("submit", "submits", "submitting", "submitted"),
                 ("review", "reviews", "reviewing", "reviewed"),
                 ("sign", "signs", "signing", "signed"),
                 ("approve", "approves", "approving", "approved")]
        verb_set = random.choice(verbs)
        q = f"{sub} asked us to ___ {obj} {time_word}."
        questions.append({
            "type": "grammar",
            "q": q,
            "a": list(verb_set),
            "correct": 0,
            "whyVi": "Cấu trúc 'ask someone to DO something' yêu cầu động từ nguyên thể."
        })

    # Template 2: Modals (must/should/will) + base verb
    for i in range(20):
        sub = random.choice(["All employees", "Staff members", "Visitors", "Candidates", "Managers"])
        modal = random.choice(["must", "should", "will", "can", "could"])
        verbs = [("follow", "follows", "following", "followed"),
                 ("attend", "attends", "attending", "attended"),
                 ("complete", "completes", "completing", "completed")]
        verb_set = random.choice(verbs)
        q = f"{sub} {modal} ___ the training session."
        questions.append({
            "type": "grammar",
            "q": q,
            "a": list(verb_set),
            "correct": 0,
            "whyVi": f"Sau động từ khiếm khuyết '{modal}', động từ luôn ở dạng nguyên thể không 'to'."
        })

    # Template 3: Passive voice (is/are/was/were + V3)
    for i in range(20):
        obj = random.choice(objects).capitalize()
        be = random.choice(["is", "was", "will be", "has been"])
        verbs = [("approved", "approve", "approves", "approving"),
                 ("rejected", "reject", "rejects", "rejecting"),
                 ("discussed", "discuss", "discusses", "discussing")]
        verb_set = random.choice(verbs)
        q = f"{obj} {be} ___ by {random.choice(subjects).lower()}."
        questions.append({
            "type": "grammar",
            "q": q,
            "a": list(verb_set),
            "correct": 0,
            "whyVi": f"Câu bị động yêu cầu động từ ở dạng Phân từ II (Past Participle - V3/ed)."
        })
        
    return questions

def generate_tenses():
    questions = []
    
    # Template 1: Present Perfect (since/for)
    for i in range(15):
        sub = random.choice(subjects)
        time_phrase = random.choice(["since 2019", "since last year", "for 5 years", "for a long time"])
        verbs = [("has worked", "worked", "is working", "works"),
                 ("has managed", "managed", "is managing", "manages"),
                 ("has developed", "developed", "is developing", "develops")]
        verb_set = random.choice(verbs)
        q = f"{sub} ___ in this field {time_phrase}."
        questions.append({
            "type": "tenses",
            "q": q,
            "a": list(verb_set),
            "correct": 0,
            "whyVi": f"Dấu hiệu '{time_phrase}' chỉ thì Hiện tại hoàn thành."
        })
        
    # Template 2: Future (next, tomorrow)
    for i in range(15):
        sub = random.choice(subjects)
        time_phrase = random.choice(["tomorrow", "next week", "next month"])
        verbs = [("will announce", "announced", "announces", "has announced"),
                 ("will visit", "visited", "visits", "has visited")]
        verb_set = random.choice(verbs)
        q = f"{sub} ___ the decision {time_phrase}."
        questions.append({
            "type": "tenses",
            "q": q,
            "a": list(verb_set),
            "correct": 0,
            "whyVi": f"Dấu hiệu '{time_phrase}' chỉ thì Tương lai đơn."
        })
    return questions

def generate_prepositions():
    questions = []
    
    # Template: time prepositions
    for i in range(15):
        day = random.choice(["Monday", "Tuesday", "Wednesday"])
        q = f"The meeting is scheduled ___ 3 p.m. on {day}."
        questions.append({
            "type": "prepositions",
            "q": q,
            "a": ["at", "in", "on", "for"],
            "correct": 0,
            "whyVi": "Dùng 'at' trước giờ cụ thể (at 3 p.m.)."
        })
        
    for i in range(15):
        month = random.choice(["January", "February", "March", "April"])
        q = f"Our new branch will open ___ {month}."
        questions.append({
            "type": "prepositions",
            "q": q,
            "a": ["in", "on", "at", "to"],
            "correct": 0,
            "whyVi": "Dùng 'in' trước tháng."
        })
        
    return questions

def generate_reading():
    questions = []
    # Mocking 5 distinct reading passages
    for i in range(1, 6):
        passage = f"""To: All Employees
From: Management
Date: October {i}
Subject: Policy Update

Please note that starting next month, the reimbursement policy will change. All receipts must be submitted within {i*5} days of the expense. Late submissions will not be processed. If you need clarification, reach out to the accounting department at extension 10{i}."""
        
        questions.append({
            "type": "reading",
            "passageText": passage,
            "questions": [
                {
                    "q": "What is the main topic of the email?",
                    "a": ["A policy update", "A new employee", "A holiday party", "An office relocation"],
                    "correct": 0,
                    "whyVi": "Tiêu đề (Subject) ghi rõ là 'Policy Update' (Cập nhật chính sách)."
                },
                {
                    "q": "How many days do employees have to submit receipts?",
                    "a": [f"{i*5} days", f"{i*10} days", "30 days", "immediately"],
                    "correct": 0,
                    "whyVi": f"Đoạn văn nêu rõ: 'within {i*5} days of the expense'."
                }
            ]
        })
    return questions

if __name__ == "__main__":
    toeic_data = {
        "grammar": generate_grammar(),
        "tenses": generate_tenses(),
        "prepositions": generate_prepositions(),
        "comparisons": [
            { "type": "comparisons", "q": "Of the three proposals, hers is the ___.", "a": ["most practical", "more practical", "practical", "practically"], "correct": 0, "whyVi": "So sánh nhất trong 3 đối tượng → the most practical." },
            { "type": "comparisons", "q": "This year's sales are ___ than last year's.", "a": ["higher", "highest", "high", "highly"], "correct": 0, "whyVi": "Có từ 'than' nên dùng so sánh hơn (higher)." }
        ] * 10,  # Duplicate for volume
        "cloze": [
            { "type": "cloze", "q": "If the client agrees, we will ___ the contract tomorrow.", "a": ["sign", "signs", "signing", "signed"], "correct": 0, "whyVi": "Sau 'will' dùng động từ nguyên mẫu: sign." },
            { "type": "cloze", "q": "Please make sure that all files are ___ backed up.", "a": ["properly", "proper", "property", "properties"], "correct": 0, "whyVi": "Cần trạng từ bổ nghĩa cho động từ 'backed up'." }
        ] * 10,
        "reading": generate_reading()
    }
    
    # Shuffle options and correct index
    for category in toeic_data:
        if category == 'reading':
            continue
        for q in toeic_data[category]:
            correct_ans = q['a'][q['correct']]
            random.shuffle(q['a'])
            q['correct'] = q['a'].index(correct_ans)

    with open('toeic_exams.json', 'w', encoding='utf-8') as f:
        json.dump(toeic_data, f, ensure_ascii=False, indent=2)
    
    print("Generated toeic_exams.json successfully with over 150 questions.")
