# services/tutor_service.py - Topic-limited MBBS Hematology Tutor
import re
import os
import json

SAFETY_DISCLAIMER = "⚠️ Educational study aid for MBBS students only. Not a clinical diagnostic or treatment tool."

ALLOWED_KEYWORDS = [
    "anemia", "anaemia", "polycythemia", "erythrocytosis", "rbc", "erythrocyte", "erythropoiesis",
    "erythropoietin", "epo", "hemoglobin", "haemoglobin", "hematocrit", "haematocrit", "iron",
    "ferritin", "transferrin", "tibc", "hepcidin", "ferroportin", "b12", "folate", "megaloblastic",
    "cobalamin", "macrocytic", "microcytic", "normocytic", "mcv", "mch", "mchc", "rdw", "reticulocyte",
    "rpi", "hemolysis", "haemolysis", "haptoglobin", "bilirubin", "schistocyte", "spherocyte",
    "sickle", "thalassemia", "jak2", "polycythemia vera", "pv", "viscosity", "hypoxia", "hif",
    "g6pd", "hemosiderin", "pruritus", "erythromelalgia", "blood loss", "bone marrow", "budd-chiari"
]

PERSONAL_DIAGNOSIS_TRIGGERS = [
    "i have", "my blood test", "my report", "my hemoglobin is", "prescribe", "what should i take",
    "am i sick", "cure me", "my doctor said", "do i have cancer", "treat my", "my symptom"
]

def check_medical_safety(query_text):
    query_lower = query_text.lower()
    
    # Check for personal diagnosis/treatment request
    for trigger in PERSONAL_DIAGNOSIS_TRIGGERS:
        if trigger in query_lower:
            return {
                "safe": False,
                "reason": "personal_medical_request",
                "message": (
                    "⚠️ **Clinical Safety Warning**: HemePath is strictly an educational learning platform for MBBS students. "
                    "I cannot diagnose conditions, interpret personal medical laboratory reports, or advise on personal treatment. "
                    "If you or someone you know has health concerns or abnormal lab results, please consult a qualified physician or hematologist."
                )
            }
            
    # Check topic relevance
    has_relevant_kw = any(kw in query_lower for kw in ALLOWED_KEYWORDS)
    if not has_relevant_kw and len(query_text.split()) > 3:
        # Check if it's general greeting
        greetings = ["hi", "hello", "hey", "help", "who are you", "what can you do"]
        if any(g in query_lower for g in greetings):
            return {
                "safe": True,
                "is_greeting": True
            }
        return {
            "safe": False,
            "reason": "out_of_scope",
            "message": (
                "📚 **Topic Boundary**: I am specialized exclusively in **Anemia, Polycythemia / Erythrocytosis, and Red Blood Cell Pathophysiology** for MBBS learners. "
                "Please ask a question related to red cell disorders, diagnostic classifications (MCV/reticulocyte count), hemolytic mechanisms, or polycythemia vera."
            )
        }
        
    return {"safe": True}

def generate_tutor_response(user_message, mode="mbbs_exam", context_text=None):
    # Safety Check
    safety = check_medical_safety(user_message)
    if not safety.get("safe"):
        return {
            "mode": mode,
            "reply": safety["message"],
            "disclaimer": SAFETY_DISCLAIMER,
            "citations": []
        }
        
    if safety.get("is_greeting"):
        return {
            "mode": mode,
            "reply": (
                "👋 **Welcome to your HemePath AI Tutor!**\n\n"
                "I am your dedicated study partner for MBBS-level pathophysiology of **Anemia** and **Polycythemia**.\n\n"
                "Select a mode above or ask questions like:\n"
                "- *'Explain the difference between iron deficiency and anemia of chronic disease.'*\n"
                "- *'Why does 2,3-BPG shift the oxygen curve in anemia?'*\n"
                "- *'Compare Polycythemia Vera with secondary erythrocytosis.'*\n"
                "- *'What causes hypersegmented neutrophils in megaloblastic anemia?'*"
            ),
            "disclaimer": SAFETY_DISCLAIMER,
            "citations": ["src-robbins-pathology", "src-statpearls-anemia"]
        }

    # 3. Call Live Gemini API with pedagogically tailored prompts per mode
    if os.environ.get("TESTING") != "true":
        try:
            from services.gemini_client import generate_medical_text
            
            mode_instructions = {
                "explain_simply": "Use intuitive real-world analogies, plain everyday language, and conceptual clarity before introducing medical terms.",
                "exam_mode": "Focus strictly on high-yield university MBBS board exam questions, diagnostic criteria, examiner traps, and must-know numerical cutoffs.",
                "compare": "Provide a clean comparative breakdown with contrasting mechanisms, differential tables, and key discriminating lab markers.",
                "socratic": "Act as a clinical mentor. Pose a guided clinical scenario with 1 thought-provoking question to help the student deduce the pathophysiology.",
                "diagram": "Describe cellular, molecular, and hormonal mechanisms step-by-step using clear directional flow (e.g. Stimulus ➔ Receptor ➔ Pathway ➔ Cell Change).",
                "from_page": "Ground your explanation directly in the student's textbook excerpt, defining any difficult terms and clarifying physiological mechanisms."
            }
            mode_instruction = mode_instructions.get(mode, "Provide a clear, high-yield MBBS pathophysiological explanation.")

            system_instruction = (
                "You are an expert hematologist and clinical educator tutoring MBBS students on the pathophysiology of Anemia and Polycythemia. "
                "Rules:\n"
                "1. Answer strictly on RBC physiology, pathophysiology of microcytic/normocytic/macrocytic anemias, and polycythemias (Polycythemia Vera vs secondary).\n"
                "2. Never diagnose personal medical symptoms or recommend individual clinical treatments (educational tutor only).\n"
                f"3. Active Tutor Mode: {mode.upper()}. Guideline: {mode_instruction}\n"
                "4. Format beautifully in Markdown with bold key terms, clear headers, and high-yield exam pearls.\n"
                "5. Cite gold-standard sources: Robbins Pathology (10th Ed), StatPearls NCBI, and WHO Guidelines."
            )

            prompt = f"Student Question: {user_message}"
            if context_text:
                prompt += f"\n\nStudent's Active Textbook Excerpt:\n{context_text}"

            ai_reply = generate_medical_text(prompt, system_instruction=system_instruction, max_tokens=1500)
            if ai_reply and len(ai_reply.strip()) > 30:
                return {
                    "mode": mode,
                    "reply": ai_reply,
                    "disclaimer": SAFETY_DISCLAIMER,
                    "citations": ["Robbins & Cotran Pathologic Basis of Disease (10th Ed)", "StatPearls Anemia", "WHO MPN Diagnostic Guidelines"],
                    "live_llm": True
                }
        except Exception:
            pass # Fall back seamlessly to local medical knowledge engine

    # Knowledge Engine fallback based on query & mode
    return synthesize_local_medical_response(user_message, mode, context_text)

def synthesize_local_medical_response(query, mode, context_text=None):
    q = query.lower()
    
    # 1. Iron Deficiency vs Anemia of Chronic Disease
    if ("iron" in q and "chronic" in q) or ("ferritin" in q and "tibc" in q) or ("hepcidin" in q and "ferroportin" in q):
        if mode == "explain_simply":
            text = (
                "### 💡 Simple Explanation: Iron Deficiency vs Chronic Inflammation\n\n"
                "Think of iron as money. In **Iron Deficiency Anemia (IDA)**, you are genuinely broke—there is simply no money in the bank or in your wallet.\n\n"
                "In **Anemia of Chronic Disease (ACD)**, you have plenty of money in your safe (storage ferritin), but the immune system has placed a padlock (**hepcidin**) on the safe door. The body locks the iron away to starve bacteria during inflammation, leaving your bone marrow broke despite a full bank!"
            )
        elif mode == "compare":
            text = (
                "### ⚖️ Side-by-Side Comparison: IDA vs ACD\n\n"
                "| Diagnostic Parameter | Iron Deficiency Anemia (IDA) | Anemia of Chronic Disease (ACD) |\n"
                "| :--- | :--- | :--- |\n"
                "| **Primary Mechanism** | True body iron deficit (blood loss / poor intake) | Hepcidin-mediated iron trapping in macrophages |\n"
                "| **Serum Iron** | Decreased (< 30 µg/dL) | Decreased (< 50 µg/dL) |\n"
                "| **Serum Ferritin** | **Markedly Low (< 30 ng/mL)** | **Normal or High (> 100 ng/mL)** (Acute phase reactant) |\n"
                "| **TIBC / Transferrin** | **Elevated (> 360 µg/dL)** (Liver makes more) | **Low or Normal (< 240 µg/dL)** |\n"
                "| **Transferrin Saturation** | Severely reduced (< 16%) | Normal or mildly decreased (15–25%) |\n"
                "| **Soluble Transferrin Receptor** | Elevated | Normal |\n"
                "| **Marrow Prussian Blue** | Absent hemosiderin (no iron) | Abundant hemosiderin trapped in macrophages |"
            )
        elif mode == "diagram":
            text = (
                "### 📊 Flowchart: The Hepcidin-Ferroportin Block in ACD\n\n"
                "```text\n"
                "Chronic Infection / Autoimmunity / Malignancy\n"
                "                   ↓\n"
                "  T-cells & Macrophages release Interleukin-6 (IL-6)\n"
                "                   ↓\n"
                "  Hepatocytes synthesize and secrete HEPCIDIN\n"
                "                   ↓\n"
                "  Hepcidin binds FERROPORTIN on macrophages & enterocytes\n"
                "                   ↓\n"
                "  Ferroportin is internalized and degraded in lysosomes\n"
                "                   ↓\n"
                "  Iron is trapped in storage (High Ferritin, Low Serum Iron)\n"
                "                   ↓\n"
                "  Erythroid marrow lacks iron → Normocytic/Microcytic Anemia\n"
                "```"
            )
        elif mode == "quiz_me":
            text = (
                "### 🎯 Socratic Quiz Challenge\n\n"
                "**Clinical Question**: A 65-year-old patient with active Rheumatoid Arthritis presents with Hb 9.2 g/dL and MCV 78 fL. Serum ferritin is 180 ng/mL, and serum iron is 25 µg/dL.\n\n"
                "**Question**: Which additional lab test would be elevated in Iron Deficiency Anemia but remains completely normal in Anemia of Chronic Disease?\n\n"
                "*(Think about the receptor shed by erythroblasts when they are starving for iron! Reply with your answer.)*"
            )
        else: # mbbs_exam
            text = (
                "### 🎓 MBBS Exam Analysis: Iron Deficiency vs Chronic Inflammation\n\n"
                "#### 1. Pathophysiological Mechanism\n"
                "- **Iron Deficiency Anemia**: Depleted total body iron stores impair protoporphyrin heme ring synthesis. Erythroblasts undergo extra divisions waiting for hemoglobin density, producing microcytic hypochromic cells with wide RDW.\n"
                "- **Anemia of Chronic Disease**: Mediated by inflammatory cytokines (IL-6, TNF-α, IFN-γ). IL-6 upregulates hepatic **hepcidin**, which binds and degrades **ferroportin**, trapping iron inside macrophage storage vaults.\n\n"
                "#### 2. Classic Laboratory Profile\n"
                "- **Ferritin**: < 30 ng/mL in IDA (diagnostic); normal to markedly elevated in ACD.\n"
                "- **TIBC**: Elevated in IDA (hepatic compensation); reduced in ACD.\n"
                "- **Bone Marrow Aspirate**: Prussian blue stain reveals absence of storage iron in IDA, versus prominent macrophage hemosiderin in ACD.\n\n"
                "#### 3. High-Yield Exam Pearls\n"
                "- In an elderly male or postmenopausal female, IDA is **colorectal malignancy** until proven otherwise by colonoscopy.\n"
                "- If ferritin is between 30 and 100 ng/mL in a patient with active inflammation, check **soluble transferrin receptor (sTfR)**; elevated sTfR confirms concurrent iron deficiency."
            )
        return {
            "mode": mode,
            "reply": text,
            "disclaimer": SAFETY_DISCLAIMER,
            "citations": ["src-statpearls-anemia", "src-robbins-pathology"]
        }

    # 2. Polycythemia Vera vs Secondary Erythrocytosis
    if "polycythemia" in q or "jak2" in q or "erythrocytosis" in q or "viscosity" in q:
        if mode == "explain_simply":
            text = (
                "### 💡 Simple Explanation: Polycythemia Vera vs Secondary Polycythemia\n\n"
                "Imagine a factory that makes red blood cells.\n\n"
                "- In **Secondary Erythrocytosis**, the factory manager is working overtime because they received urgent high-priority orders from headquarters (high **EPO** caused by low oxygen from COPD, high altitude, or an EPO-secreting kidney tumor).\n"
                "- In **Polycythemia Vera**, the workers have rebelled! The conveyor belt is running wild due to a broken switch (**JAK2 mutation**). Headquarters keeps shouting 'STOP!' (serum EPO is zero), but the machines won't turn off."
            )
        elif mode == "compare":
            text = (
                "### ⚖️ Comparison: Polycythemia Vera vs Secondary Erythrocytosis\n\n"
                "| Clinical Feature | Polycythemia Vera (Primary) | Secondary Erythrocytosis |\n"
                "| :--- | :--- | :--- |\n"
                "| **Underlying Defect** | Somatic **JAK2 V617F** mutation in hematopoietic stem cells | Hypoxia or ectopic EPO secretion |\n"
                "| **Serum Erythropoietin (EPO)** | **Suppressed (Low or undetectable)** | **Elevated or inappropriately normal** |\n"
                "| **Lineages Involved** | **Panmyelosis** (Elevated RBCs, WBCs, and Platelets) | **Isolated Erythrocytosis** (WBC and Platelets normal) |\n"
                "| **Splenomegaly** | Present in > 70% of cases | Absent (unless underlying disease causes it) |\n"
                "| **Aquagenic Pruritus** | Frequent (histamine from basophils) | Extremely rare |\n"
                "| **Thrombotic Risk** | High (arterial and venous: Budd-Chiari, stroke) | Moderate (viscosity related) |\n"
                "| **Target Hematocrit** | Strictly < 45% via phlebotomy | Treat underlying cause (e.g., oxygen, tumor resection) |"
            )
        elif mode == "diagram":
            text = (
                "### 📊 Algorithmic Approach to Polycythemia / Erythrocytosis\n\n"
                "```text\n"
                "Elevated Hemoglobin (>16.5 M / >16.0 F) or Hct (>49% M / >48% F)\n"
                "                   ↓\n"
                "  Rule out Relative Polycythemia (Dehydration / Hemoconcentration)\n"
                "                   ↓\n"
                "  Measure Serum Erythropoietin (EPO)\n"
                "          /               \\\n"
                "     LOW EPO             HIGH / NORMAL EPO\n"
                "        ↓                        ↓\n"
                "  Polycythemia Vera      Secondary Erythrocytosis\n"
                "  Check JAK2 V617F       Check SaO2 / Nocturnal O2 / CT Abdomen\n"
                "  Marrow Biopsy:          - Hypoxia (COPD, cyanotic heart)\n"
                "  Panmyelosis             - Tumors (RCC, HCC, Hemangioblastoma)\n"
                "```"
            )
        else: # mbbs_exam
            text = (
                "### 🎓 MBBS Exam Analysis: Polycythemia Vera\n\n"
                "#### 1. Molecular Genetics\n"
                "- Driven by a gain-of-function somatic point mutation in **Janus Kinase 2 (JAK2 V617F)** on chromosome 9p in >95% of cases (exon 12 mutations in remaining 2-3%).\n"
                "- This mutation disrupts the autoinhibitory JH2 pseudokinase domain, leading to constitutive kinase signaling through STAT5, AKT, and MAPK independent of EPO.\n\n"
                "#### 2. WHO Diagnostic Criteria (2016/2022)\n"
                "- **Major 1**: Hb > 16.5 g/dL (men) / > 16.0 g/dL (women), or Hct > 49% (men) / > 48% (women).\n"
                "- **Major 2**: Bone marrow biopsy showing hypercellularity with prominent erythroid, granulocytic, and megakaryocytic proliferation (**panmyelosis**).\n"
                "- **Major 3**: Presence of JAK2 V617F or JAK2 exon 12 mutation.\n"
                "- **Minor**: Subnormal serum erythropoietin (EPO) level.\n"
                "*(Diagnosis requires all 3 major, OR first 2 major + minor criterion)*.\n\n"
                "#### 3. Critical Morbidities and Treatment\n"
                "- **Hyperviscosity & Thrombosis**: Whole-blood viscosity rises exponentially above Hct 50%. Major cause of death is arterial (stroke, MI) and unusual venous thrombosis (**Budd-Chiari syndrome**).\n"
                "- **Erythromelalgia**: Burning, painful redness in hands/feet due to platelet microthrombi, relieved by aspirin.\n"
                "- **Management**: Therapeutic phlebotomy to maintain **Hct < 45%**, low-dose aspirin, and cytoreduction (hydroxyurea) for high-risk patients."
            )
        return {
            "mode": mode,
            "reply": text,
            "disclaimer": SAFETY_DISCLAIMER,
            "citations": ["src-who-hematology", "src-accessmed-polycythemia"]
        }

    # 3. Megaloblastic Anemia & B12 vs Folate
    if "megaloblastic" in q or "b12" in q or "folate" in q or "macrocytic" in q or "hypersegmented" in q:
        if mode == "explain_simply":
            text = (
                "### 💡 Simple Explanation: Megaloblastic Anemia\n\n"
                "To divide, a cell must copy its DNA blueprint using Vitamin B12 and Folate. When either vitamin is missing, DNA copying stalls. The nucleus remains immature and stuck. However, protein building in the rest of the cell keeps going full steam! The cell expands into a gigantic, floppy monster called a **megaloblast** that gets destroyed inside the marrow before it can even leave."
            )
        elif mode == "compare":
            text = (
                "### ⚖️ Vitamin B12 (Cobalamin) vs Folate (Vitamin B9) Deficiency\n\n"
                "| Feature | Vitamin B12 Deficiency | Folate Deficiency |\n"
                "| :--- | :--- | :--- |\n"
                "| **Body Storage** | Large (3–5 years in liver) | Small (3–4 months in liver) |\n"
                "| **Primary Etiology** | Pernicious anemia (anti-IF), veganism, terminal ileal resection | Poor diet, alcoholism, pregnancy, methotrexate |\n"
                "| **Neurological Symptoms** | **Present**: Subacute Combined Degeneration (ataxia, paresthesias) | **ABSENT** |\n"
                "| **Methylmalonic Acid (MMA)** | **Markedly Elevated** | **Normal** |\n"
                "| **Homocysteine** | Elevated | Elevated |\n"
                "| **Peripheral Smear** | Macro-ovalocytes + Hypersegmented neutrophils | Macro-ovalocytes + Hypersegmented neutrophils |"
            )
        else:
            text = (
                "### 🎓 MBBS Exam Analysis: Megaloblastic Anemia & Pathophysiology\n\n"
                "#### 1. Biochemical Cascade (The Folate Trap)\n"
                "- Vitamin B12 is the essential cofactor for **methionine synthase**, transferring a methyl group from N5-methyl tetrahydrofolate (THF) to homocysteine, generating methionine and active THF.\n"
                "- In B12 deficiency, folate is trapped as N5-methyl THF, halting production of methylene THF required by thymidylate synthase for **dTMP (thymidine) synthesis**.\n\n"
                "#### 2. Morphological Hallmarks\n"
                "- **Nuclear-Cytoplasmic Asynchrony**: Immature, lace-like nuclear chromatin alongside mature, fully hemoglobinized pink cytoplasm.\n"
                "- **Peripheral Smear**: Oval macrocytes (MCV > 110 fL) and **hypersegmented neutrophils** (≥ 6 nuclear lobes, or ≥ 5% with 5 lobes).\n\n"
                "#### 3. Neurological Sequelae (B12 Specific)\n"
                "- B12 is also required for **methylmalonyl-CoA mutase**. Deficiency causes accumulation of **methylmalonic acid (MMA)** and abnormal branched fatty acids in myelin.\n"
                "- Manifests as **Subacute Combined Degeneration (SCD)** of the dorsal (loss of vibration/proprioception) and lateral (spastic paresis) spinal tracts.\n"
                "- ⚠️ **High-Yield Board Trap**: Giving folic acid alone to a B12-deficient patient corrects the anemia but allows catastrophic neurological demyelination to progress!"
            )
        return {
            "mode": mode,
            "reply": text,
            "disclaimer": SAFETY_DISCLAIMER,
            "citations": ["src-robbins-pathology", "src-statpearls-anemia"]
        }

    # 4. Hemolysis (Intravascular vs Extravascular)
    if "hemolysis" in q or "haemolysis" in q or "haptoglobin" in q or "bilirubin" in q or "schistocyte" in q or "coombs" in q:
        text = (
            "### 🎓 MBBS Exam Analysis: Hemolytic Anemias\n\n"
            "#### 1. Intravascular vs Extravascular Destruction\n"
            "- **Extravascular Hemolysis** (Most common): Abnormal RBCs (spherocytes, sickle cells, IgG-opsonized cells) are destroyed by macrophages in the splenic cords of Billroth. Features **splenomegaly, unconjugated hyperbilirubinemia (jaundice), and pigment gallstones** without hemoglobinuria.\n"
            "- **Intravascular Hemolysis**: RBCs rupture inside circulation (microangiopathic shear in TTP/DIC, complement in PNH, prosthetic valves). Free hemoglobin is released into plasma.\n\n"
            "#### 2. Key Diagnostic Signatures of Intravascular Lysis\n"
            "1. **Serum Haptoglobin**: Drops to near zero because free Hb binds haptoglobin forming a 1:1 complex cleared by hepatic CD163 receptors.\n"
            "2. **Serum LDH**: Markedly elevated from ruptured RBC contents.\n"
            "3. **Hemoglobinuria & Hemosiderinuria**: Saturated haptoglobin allows free Hb dimers to filter through glomeruli, causing dark red/black urine and shed renal hemosiderin.\n\n"
            "#### 3. Peripheral Smear Clues\n"
            "- **Schistocytes (Helmet cells)**: Fibrin strand shearing in TTP/HUS/DIC.\n"
            "- **Spherocytes**: Extravascular macrophage membrane clipping in Hereditary Spherocytosis or Warm AIHA."
        )
        return {
            "mode": mode,
            "reply": text,
            "disclaimer": SAFETY_DISCLAIMER,
            "citations": ["src-robbins-pathology", "src-merck-anemia"]
        }

    # General Fallback for other hematology questions
    text = (
        f"### 🩺 HemePath Medical Tutor ({mode.replace('_', ' ').title()})\n\n"
        f"Regarding **'{query.strip()}'** in red cell pathophysiology:\n\n"
        "1. **Core Mechanism**: Erythrocyte homeostasis balances renal hypoxia sensing (HIF-1α → EPO) with bone marrow precursor maturation and peripheral clearance at ~120 days.\n"
        "2. **Diagnostic Bifurcation**: Start with the **MCV** (microcytic <80 fL, normocytic 80-100 fL, macrocytic >100 fL) combined with the **Reticulocyte Production Index (RPI)** to separate hypoproliferation from hemolysis/bleeding.\n"
        "3. **Clinical Integration**: Always evaluate red cell mass alongside plasma volume changes (e.g., hemoconcentration in relative polycythemia or hemodilution in pregnancy).\n\n"
        "💡 *Tip: Try switching to **Compare Concepts**, **Diagram Mode**, or **MBBS Exam Mode** to explore this topic from multiple angles!*"
    )
    return {
        "mode": mode,
        "reply": text,
        "disclaimer": SAFETY_DISCLAIMER,
        "citations": ["src-robbins-pathology", "src-statpearls-anemia"]
    }
