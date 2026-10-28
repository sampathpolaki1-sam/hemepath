# 🩸 HemePath — Anemia & Polycythemia Tutor
> **A focused MBBS learning application built following the Google Antigravity Project Blueprint.**

---

## 🎯 Educational Purpose & Scope Boundary
**HemePath** teaches **ONLY** the pathophysiology of **Anemia** and **Polycythemia / Erythrocytosis** for MBBS students and medical learners.
- **Educational study aid only**: It is **not** a clinical diagnostic or treatment product.
- **Privacy First**: Designed with strict guidelines prohibiting entry or retention of identifiable patient health records.

---

## 📱 Device Scale: Phone Mode & Laptop Mode
The user requested: *"complete the project and make sure it is only for phone use only so accordingly make the scale and make for laptop also"*.

To fulfill this dual requirement with extreme precision and polish:
1. **Phone Mode (Default)**:
   - Encapsulated in an authentic smartphone hardware shell (with curved bezels, camera dot notch, and simulated hardware home bar).
   - Features a **Status Bar** with live real-time clock, battery icon, and cellular status.
   - Includes **Scale Controls** right on the screen: **75%**, **85%**, **90%**, **100%**, and **110%**, enabling students on laptops to zoom and scale the phone frame to match their preferred display size!
   - On genuine mobile phones, the viewport auto-detects small screens (`<= 600px`) and automatically expands to full native edge-to-edge mobile app mode!
2. **Laptop Mode**:
   - A single click on the **💻 Laptop Mode** switcher seamlessly stretches the application into a full-width desktop layout with multi-column views, expanded cards, and dual-pane reader navigation!

---

## 🚀 Key Features

### 1. 15-Lesson Ordered Syllabus
Comprehensive MBBS hematology curriculum covering:
1. **Normal Red Blood Cells and Erythropoiesis** (HIF-1α, EPO, CFU-E, reticulocytes)
2. **What is Anemia?** (WHO criteria, CaO2 equation, tissue hypoxia)
3. **Core Pathophysiology of Anemia** (Blood loss, decreased production, increased destruction)
4. **Classifying Anemia** (MCV categories: microcytic, normocytic, macrocytic, RPI)
5. **Iron-Deficiency Anemia** (Duodenal ferroportin, ferritin, TIBC, microcytic hypochromia)
6. **Megaloblastic Anemia** (B12 vs Folate, folate trap, MMA, hypersegmented PMNs)
7. **Hemolytic Anemia** (Intravascular vs extravascular, haptoglobin, LDH, schistocytes)
8. **Anemia of Inflammation & Renal Disease** (Hepcidin-ferroportin block, CKD EPO deficit)
9. **Clinical Effects & Compensatory Responses** (Hyperdynamic state, 2,3-BPG right shift)
10. **What is Polycythemia / Erythrocytosis?** (WHO thresholds, relative vs absolute)
11. **Primary Polycythemia: Polycythemia Vera** (JAK2 V617F, panmyelosis, low EPO, phlebotomy <45%)
12. **Secondary Erythrocytosis** (Hypoxia-driven COPD/altitude vs EPO-secreting tumors)
13. **Consequences of Polycythemia** (Exponential blood viscosity, thrombosis, erythromelalgia)
14. **Anemia vs Polycythemia Comparison** (Comprehensive side-by-side matrix)
15. **Integrated Clinical Cases & Revision** (5 real-world MBBS clinical vignettes)

### 2. Hand-Authored Interactive SVG Diagrams
- **Renal-Erythroid Negative Feedback Loop**
- **Three Cardinal Mechanisms of Anemia**
- **MCV Algorithmic Classification Flowchart**
- **Iron Absorption & Ferroportin Axis**
- **Relative vs Absolute Polycythemia Tree**
- **Blood Viscosity Exponential Curve vs Tissue Oxygen Transport**
- Clickable nodes with instant pop-up clinical pearls!

### 3. Topic-Limited AI Medical Tutor
- Strict safety guardrails: strictly answers anemia, polycythemia, and RBC physiology; politely declines personal diagnosis or treatment requests.
- **6 Dedicated Modes**:
  1. *Explain Simply* (ELI5 + plain analogy)
  2. *MBBS Exam Mode* (Mechanism, morphology/lab clues, clinical significance)
  3. *Compare Concepts* (Side-by-side comparison tables)
  4. *Ask Me Questions* (Socratic drill)
  5. *Diagram Mode* (Algorithmic flowchart)
  6. *From My Page* (Analyzes uploaded textbook excerpts)

### 4. Textbook Photo Explainer (OCR + 7-Part Output)
- Validates file type (JPG/PNG/WEBP) and size (<10MB).
- Text inspection editor allows student to review and correct any OCR words before generating.
- Includes **1-Click High-Yield Presets** (Robbins Iron Deficiency, Robbins Megaloblastic, Robbins Polycythemia Vera, Merck Hemolysis).
- Formats explanation into the 7 mandatory sections:
  1. What the page is about
  2. 3–6 line plain explanation
  3. Step-by-step mechanism
  4. Conceptual text flowchart
  5. Key medical terms
  6. High-yield MBBS exam pearl
  7. 3 active recall questions
  8. Optical confidence notes & privacy alerts

### 5. Objective Question Bank & Practice
- Single-best-answer MCQs, True/False, Match Mechanism to Finding, Arrange Mechanism Steps, and Case Vignettes.
- Distractor rationales (explains why incorrect options are wrong).
- Instant feedback, scoring, and weak-topic remediation recommendations.

### 6. Active Recall Flashcards & Searchable Glossary
- 3D flip card deck with 25+ high-yield cards (Mastered vs Revision).
- 46-term searchable hematology dictionary.

---

## 🛠️ Project Folder Structure
```text
hemepath/
├── app.py                      # Flask backend routes & REST API endpoints
├── requirements.txt            # Python dependencies
├── .env.example                # Environment variables template
├── README.md                   # Complete documentation & QA guide
├── build_lessons.py            # Generates lessons.json content
├── build_databank.py           # Generates questions, glossary, flashcards
├── content/
│   ├── lessons.json            # 15 detailed lessons with syllabus metadata
│   ├── questions_seed.json     # 26+ questions (MCQs, matching, vignettes)
│   ├── glossary.json           # 46 medical definitions
│   ├── flashcards.json         # 25 active recall flashcards
│   ├── sample_textbooks.json   # 4 high-yield textbook presets
│   └── sources.json            # Medical references (StatPearls, Robbins, etc.)
├── database/
│   ├── schema.sql              # SQLite database schema
│   ├── db.py                   # SQLite connection and helper functions
│   └── hemepath.db             # Local SQLite database file
├── services/
│   ├── tutor_service.py        # 6-mode tutor chatbot & safety guardrails
│   ├── image_explainer.py      # Photo processor & 7-part structured engine
│   └── quiz_service.py         # Quiz generator, scoring & distractor analysis
├── templates/
│   ├── base.html               # Phone frame, scale bar, status bar, navigation
│   ├── index.html              # Dashboard, progress bar, quick actions
│   ├── roadmap.html            # 15 ordered lessons with search filter
│   ├── lesson.html             # Lesson tabs (Core, Diagram, Go Deeper, Recall)
│   ├── upload_explainer.html   # Textbook photo upload & OCR editor
│   ├── chat.html               # AI Tutor chatbot with mode selector
│   ├── quiz.html               # Interactive quiz engine
│   ├── results.html            # Quiz performance & remediation
│   ├── flashcards.html         # 3D interactive flashcards
│   ├── glossary.html           # Searchable medical dictionary
│   ├── bookmarks.html          # Saved notes & bookmarks
│   └── sources.html            # Reference sources & quality controls
├── static/
│   ├── css/
│   │   ├── style.css           # Design system (Outfit & Inter fonts, dark mode)
│   │   └── diagrams.css        # SVG diagram styling and nodes
│   └── js/
│       ├── device_scale.js     # Phone scale (75%-110%) & laptop switcher
│       ├── main.js             # Toasts, bookmarks, progress update, TTS
│       ├── diagrams.js         # Hand-crafted interactive SVG schematics
│       ├── quiz.js             # Quiz runner, instant feedback, scoring
│       ├── chat.js             # Tutor AI frontend logic
│       └── upload.js           # Photo upload and 7-part explainer renderer
└── tests/
    ├── test_routes.py          # Route handler tests
    ├── test_quiz.py            # Quiz generation & scoring tests
    ├── test_upload_validation.py # Image validation & OCR tests
    └── test_tutor.py           # Safety guardrails & tutor modes tests
```

---

## 💻 Quick Start & Running Locally

### 1. Prerequisites
- Python 3.10+ installed.

### 2. Clone or Enter Project
```powershell
cd C:\Users\sampa\.gemini\antigravity-ide\scratch\hemepath
```

### 3. Install Dependencies
```powershell
pip install -r requirements.txt
```

### 4. Run the Application
```powershell
python app.py
```
Open your browser and navigate to: **`http://127.0.0.1:5000`**

### 5. Running the Automated Test Suite
```powershell
python -m unittest discover tests
```
*All 16 tests will execute and pass.*

---

## 📋 Quality Assurance & Manual QA Checklist
| Verification Item | Test Steps | Expected Result |
| :--- | :--- | :--- |
| **Phone Scale Mode** | Tap `75%`, `90%`, `100%`, `110%` in top bar | Phone frame scales smoothly without breaking UI |
| **Laptop Mode** | Tap `💻 Laptop Mode` button | Screen expands to full width multi-column desktop layout |
| **Lesson Progression** | Click *Mark Complete* on Lesson 1 | Status changes to *Completed ✓*, progress bar increases |
| **Interactive Diagram** | Tap nodes on the RBC Production Loop | Pop-up box reveals specific cellular/signaling details |
| **Tutor Safety Check** | Ask *"What medicine should I take for my anemia?"* | Polite refusal + referral to licensed physician |
| **Textbook Explainer** | Tap *Robbins Pathology (Iron Deficiency)* preset | Generates full 7-part structured MBBS breakdown |
| **Quiz Feedback** | Answer question incorrectly | Displays why option is wrong and which lesson to revise |

---

## 🔒 Medical Reference Attribution
- **Robbins and Cotran Pathologic Basis of Disease (10th Ed)**
- **StatPearls, NCBI Bookshelf — Anemia Mechanisms and Evaluation**
- **Merck Manual Professional Edition — Etiology of Anemia**
- **WHO Classification of Tumours of Haematopoietic and Lymphoid Tissues (MPN Criteria)**
