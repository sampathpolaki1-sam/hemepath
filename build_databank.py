# build_databank.py - Generates comprehensive question bank, glossary, flashcards, and textbook presets
import json
import os

CONTENT_DIR = os.path.join(os.path.dirname(__file__), "content")

# 1. QUESTION BANK
questions = [
    # MCQs
    {
        "id": "q1",
        "lesson_id": 1,
        "type": "mcq",
        "stem": "Under physiological normoxic conditions, how is Hypoxia-Inducible Factor 1-alpha (HIF-1α) regulated in renal interstitial cells?",
        "options": [
            "Phosphorylated by JAK2 to stimulate EPO",
            "Hydroxylated by prolyl hydroxylases using O2 and Fe2+, targeting it for proteasomal degradation",
            "Bound to transferrin and stored in lysosomes",
            "Cleaved by hepcidin into an inactive fragment"
        ],
        "correct_answer": "Hydroxylated by prolyl hydroxylases using O2 and Fe2+, targeting it for proteasomal degradation",
        "correct_index": 1,
        "explanation": "In normoxia, oxygen-dependent prolyl hydroxylase domain (PHD) enzymes hydroxylate HIF-1α proline residues. This allows the von Hippel-Lindau (VHL) E3 ubiquitin ligase complex to recognize and polyubiquitinate HIF-1α for rapid proteasomal destruction.",
        "distractor_explanations": {
            "0": "JAK2 is involved in downstream EPO receptor signaling, not in HIF-1α normoxic degradation.",
            "2": "Transferrin transports ferric iron in plasma; it does not store HIF-1α.",
            "3": "Hepcidin targets ferroportin for degradation, not HIF-1α."
        },
        "difficulty": "Hard",
        "review_status": "Reviewed by Medical Educator",
        "source_id": "src-robbins-pathology"
    },
    {
        "id": "q2",
        "lesson_id": 1,
        "type": "mcq",
        "stem": "What is the primary intracellular energy-producing pathway in mature human erythrocytes?",
        "options": [
            "Mitochondrial oxidative phosphorylation",
            "Anaerobic glycolysis (Embden-Meyerhof pathway)",
            "Fatty acid beta-oxidation",
            "Citric acid cycle (Krebs cycle)"
        ],
        "correct_answer": "Anaerobic glycolysis (Embden-Meyerhof pathway)",
        "correct_index": 1,
        "explanation": "Mature erythrocytes lack mitochondria, nuclei, and ribosomes. Consequently, 100% of their ATP is generated through anaerobic glycolysis converting glucose to lactate.",
        "distractor_explanations": {
            "0": "Mitochondria are extruded during orthochromatic erythroblast and reticulocyte maturation.",
            "2": "Beta-oxidation occurs within mitochondria, which RBCs lack.",
            "3": "The Krebs cycle is localized in the mitochondrial matrix, absent in mature red cells."
        },
        "difficulty": "Easy",
        "review_status": "Reviewed by Medical Educator",
        "source_id": "src-robbins-pathology"
    },
    {
        "id": "q3",
        "lesson_id": 2,
        "type": "mcq",
        "stem": "Which formula correctly quantifies total arterial oxygen content (CaO2)?",
        "options": [
            "CaO2 = (Hb × 1.34 × SaO2) + (0.003 × PaO2)",
            "CaO2 = (Hb × 0.003 × SaO2) + (1.34 × PaO2)",
            "CaO2 = (Hematocrit ÷ 3) × PaO2",
            "CaO2 = Cardiac Output × Total Peripheral Resistance"
        ],
        "correct_answer": "CaO2 = (Hb × 1.34 × SaO2) + (0.003 × PaO2)",
        "correct_index": 0,
        "explanation": "Each gram of fully saturated hemoglobin carries approximately 1.34 mL of O2. Dissolved oxygen contributes 0.003 mL per 100 mL of blood per mmHg of PaO2.",
        "distractor_explanations": {
            "1": "The coefficients are transposed; 1.34 applies to Hb-bound oxygen, not dissolved O2.",
            "2": "Hct / 3 estimates Hb, not CaO2.",
            "3": "This is the hemodynamic equation for Mean Arterial Pressure."
        },
        "difficulty": "Medium",
        "review_status": "Reviewed by Medical Educator",
        "source_id": "src-statpearls-anemia"
    },
    {
        "id": "q4",
        "lesson_id": 3,
        "type": "mcq",
        "stem": "A 40-year-old female presents with sudden onset weakness. Labs reveal Hb 7.5 g/dL and an absolute reticulocyte count of 220,000/µL (uncorrected reticulocyte count 6.8%). Which category of anemia does this clinical picture indicate?",
        "options": [
            "Marrow hypoproliferation (production failure)",
            "Accelerated destruction (hemolysis) or acute bleeding with active marrow compensation",
            "Aplastic anemia",
            "Pure red cell aplasia"
        ],
        "correct_answer": "Accelerated destruction (hemolysis) or acute bleeding with active marrow compensation",
        "correct_index": 1,
        "explanation": "An absolute reticulocyte count > 100,000–120,000/µL or RPI > 2 demonstrates an appropriate, accelerated hyperproliferative marrow response, pointing toward hemolysis or acute blood loss.",
        "distractor_explanations": {
            "0": "Hypoproliferative states are characterized by low reticulocyte counts (<25,000/µL).",
            "2": "Aplastic anemia causes pancytopenia with near-zero reticulocytes.",
            "3": "Pure red cell aplasia features absence of erythroblasts and absent reticulocytes."
        },
        "difficulty": "Medium",
        "review_status": "Reviewed by Medical Educator",
        "source_id": "src-merck-anemia"
    },
    {
        "id": "q5",
        "lesson_id": 4,
        "type": "mcq",
        "stem": "Which mechanism most directly explains the microcytosis commonly seen in iron-deficiency anemia?",
        "options": [
            "Impaired DNA synthesis delaying cell division",
            "Reduced hemoglobin synthesis allowing extra erythroblast divisions before critical MCHC is reached",
            "Increased intravascular plasma volume diluting red cell volume",
            "Primary defect in cytoskeletal spectrin"
        ],
        "correct_answer": "Reduced hemoglobin synthesis allowing extra erythroblast divisions before critical MCHC is reached",
        "correct_index": 1,
        "explanation": "Erythroblasts divide until a critical internal hemoglobin concentration is reached. When heme/Hb synthesis is impaired by lack of iron, erythroblasts undergo one or more extra divisions, producing abnormally small (microcytic) cells.",
        "distractor_explanations": {
            "0": "Impaired DNA synthesis causes macrocytosis (megaloblastic anemia), not microcytosis.",
            "2": "Plasma expansion causes relative anemia/hemodilution, without changing red cell MCV.",
            "3": "Spectrin defects cause hereditary spherocytosis, which features high MCHC and normal/low MCV, not microcytic hypochromia."
        },
        "difficulty": "Medium",
        "review_status": "Reviewed by Medical Educator",
        "source_id": "src-robbins-pathology"
    },
    {
        "id": "q6",
        "lesson_id": 5,
        "type": "mcq",
        "stem": "Which finding on a peripheral blood smear is most characteristic of severe chronic iron deficiency?",
        "options": [
            "Hypersegmented neutrophils with macro-ovalocytes",
            "Microcytic, hypochromic cells with increased central pallor and pencil-shaped poikilocytes",
            "Schistocytes and helmet cells with thrombocytopenia",
            "Microspherocytes with polychromasia"
        ],
        "correct_answer": "Microcytic, hypochromic cells with increased central pallor and pencil-shaped poikilocytes",
        "correct_index": 1,
        "explanation": "Severe IDA exhibits marked central pallor (> 1/3 of cell diameter), microcytosis, anisocytosis (high RDW), and elongated pencil or cigar-shaped red cells.",
        "distractor_explanations": {
            "0": "This is characteristic of megaloblastic anemia (B12/folate deficiency).",
            "2": "This indicates Microangiopathic Hemolytic Anemia (TTP, HUS, DIC).",
            "3": "This is typical of Hereditary Spherocytosis or Autoimmune Hemolytic Anemia."
        },
        "difficulty": "Easy",
        "review_status": "Reviewed by Medical Educator",
        "source_id": "src-statpearls-anemia"
    },
    {
        "id": "q7",
        "lesson_id": 6,
        "type": "mcq",
        "stem": "Why does administration of high-dose folic acid to a patient with unrecognized Vitamin B12 deficiency represent a grave clinical danger?",
        "options": [
            "It induces acute hyperkalemia from rapid marrow turnover",
            "It corrects the anemia while permitting irreversible subacute combined degeneration of the spinal cord to progress",
            "It triggers immediate fulminant aplastic crisis",
            "It irreversibly blocks duodenal iron absorption"
        ],
        "correct_answer": "It corrects the anemia while permitting irreversible subacute combined degeneration of the spinal cord to progress",
        "correct_index": 1,
        "explanation": "Folate bypasses the 'folate trap', restoring thymidylate synthesis and normalizing hematological parameters. However, it does not correct the methylmalonyl-CoA mutase defect, masking the diagnosis while catastrophic neurological demyelination continues.",
        "distractor_explanations": {
            "0": "Hypokalemia (not hyperkalemia) may occur during initial B12 replacement due to potassium uptake by new cells.",
            "2": "Folate does not induce marrow aplasia.",
            "3": "Folate does not impair duodenal iron uptake."
        },
        "difficulty": "Hard",
        "review_status": "Reviewed by Medical Educator",
        "source_id": "src-robbins-pathology"
    },
    {
        "id": "q8",
        "lesson_id": 7,
        "type": "mcq",
        "stem": "Which of the following laboratory panels is diagnostic of acute intravascular hemolysis?",
        "options": [
            "High haptoglobin, normal LDH, negative urine hemosiderin",
            "Undetectable haptoglobin, markedly elevated LDH, positive urine hemoglobin, elevated indirect bilirubin",
            "High ferritin, high TIBC, normal haptoglobin",
            "Low indirect bilirubin, low direct bilirubin, normal reticulocytes"
        ],
        "correct_answer": "Undetectable haptoglobin, markedly elevated LDH, positive urine hemoglobin, elevated indirect bilirubin",
        "correct_index": 1,
        "explanation": "Free Hb scavenges haptoglobin (driving it to zero), massive intracellular LDH is released, filtered free Hb spills into urine (hemoglobinuria), and heme breakdown increases unconjugated bilirubin.",
        "distractor_explanations": {
            "0": "Haptoglobin is depleted in hemolysis, not elevated.",
            "2": "This represents an iron panel, not a hemolytic profile.",
            "3": "Bilirubin and reticulocytes are consistently elevated in active hemolysis."
        },
        "difficulty": "Medium",
        "review_status": "Reviewed by Medical Educator",
        "source_id": "src-robbins-pathology"
    },
    {
        "id": "q9",
        "lesson_id": 8,
        "type": "mcq",
        "stem": "What is the primary mechanism by which interleukin-6 (IL-6) induces Anemia of Chronic Disease / Inflammation?",
        "options": [
            "Directly cleaves the erythropoietin receptor on erythroblasts",
            "Stimulates hepatic synthesis of hepcidin, which degrades ferroportin and traps iron in storage cells",
            "Inhibits duodenal intrinsic factor synthesis",
            "Accelerates splenic macrophage sequestration of platelets"
        ],
        "correct_answer": "Stimulates hepatic synthesis of hepcidin, which degrades ferroportin and traps iron in storage cells",
        "correct_index": 1,
        "explanation": "IL-6 signals through STAT3 in hepatocytes, inducing rapid transcription of hepcidin. Circulating hepcidin binds ferroportin, causing its endocytosis and proteolysis, locking iron within macrophages and enterocytes.",
        "distractor_explanations": {
            "0": "IL-6 does not enzymatically cleave the EPO receptor.",
            "2": "Intrinsic factor is produced by gastric parietal cells, unaffected directly by IL-6.",
            "3": "This describes immune thrombocytopenia or hypersplenism, not IL-6 mediated anemia."
        },
        "difficulty": "Medium",
        "review_status": "Reviewed by Medical Educator",
        "source_id": "src-statpearls-anemia"
    },
    {
        "id": "q10",
        "lesson_id": 9,
        "type": "mcq",
        "stem": "How does the oxygen-hemoglobin dissociation curve adapt in chronic anemia, and what mediates this shift?",
        "options": [
            "Shifts to the left, mediated by decreased 2,3-BPG",
            "Shifts to the right, mediated by increased intracellular erythrocyte 2,3-BPG",
            "Remains completely unchanged due to homeostatic buffering",
            "Shifts to the left, mediated by systemic respiratory alkalosis"
        ],
        "correct_answer": "Shifts to the right, mediated by increased intracellular erythrocyte 2,3-BPG",
        "correct_index": 1,
        "explanation": "Tissue hypoxia increases 2,3-BPG production via the Rapoport-Luebering shunt. 2,3-BPG binds between beta chains of deoxyhemoglobin, stabilizing the low-affinity T-conformation and shifting the curve to the right, promoting oxygen delivery to tissues.",
        "distractor_explanations": {
            "0": "A left shift would increase O2 affinity, holding onto oxygen and worsening tissue hypoxia.",
            "2": "The curve is dynamic and adapts significantly in anemia.",
            "3": "Alkalosis shifts the curve left (Bohr effect), the opposite of the adaptive rightward compensation."
        },
        "difficulty": "Medium",
        "review_status": "Reviewed by Medical Educator",
        "source_id": "src-statpearls-anemia"
    },
    {
        "id": "q11",
        "lesson_id": 10,
        "type": "mcq",
        "stem": "A patient with severe diarrhea and dehydration has a hematocrit of 53%. Following 2 liters of IV isotonic saline, the hematocrit drops to 44%. What diagnosis explains this phenomenon?",
        "options": [
            "Polycythemia Vera",
            "Relative (spurious) erythrocytosis due to hemoconcentration",
            "Renal cell carcinoma secreting ectopic EPO",
            "Secondary hypoxia-induced erythrocytosis"
        ],
        "correct_index": 1,
        "correct_answer": "Relative (spurious) erythrocytosis due to hemoconcentration",
        "explanation": "Dehydration reduces plasma volume while red cell mass remains normal. This concentrates erythrocytes, yielding a transiently elevated hematocrit that normalizes upon fluid rehydration.",
        "distractor_explanations": {
            "0": "In PV, red cell mass is genuinely elevated and will not normalize with simple rehydration.",
            "2": "Ectopic EPO causes true absolute erythrocytosis.",
            "3": "Hypoxic erythrocytosis is an absolute increase in red cell mass."
        },
        "difficulty": "Easy",
        "review_status": "Reviewed by Medical Educator",
        "source_id": "src-accessmed-polycythemia"
    },
    {
        "id": "q12",
        "lesson_id": 11,
        "type": "mcq",
        "stem": "Which of the following is considered a MAJOR diagnostic criterion for Polycythemia Vera according to WHO guidelines?",
        "options": [
            "Subnormal serum erythropoietin (EPO) level",
            "Presence of JAK2 V617F or JAK2 exon 12 mutation",
            "Serum ferritin < 20 ng/mL",
            "Direct Antiglobulin Test (Coombs) positivity"
        ],
        "correct_answer": "Presence of JAK2 V617F or JAK2 exon 12 mutation",
        "correct_index": 1,
        "explanation": "WHO Major Criteria for PV: 1) Elevated Hb/Hct; 2) Trilineage hypercellularity (panmyelosis) on BM biopsy; 3) Presence of JAK2 V617F or exon 12 mutation. Subnormal serum EPO is the sole MINOR criterion.",
        "distractor_explanations": {
            "0": "Subnormal serum EPO is a MINOR criterion, not a major criterion.",
            "2": "Low ferritin may occur secondary to phlebotomy or iron consumption, but is not a WHO criterion.",
            "3": "Coombs test is used for autoimmune hemolytic anemia, irrelevant to MPN criteria."
        },
        "difficulty": "Hard",
        "review_status": "Reviewed by Medical Educator",
        "source_id": "src-who-hematology"
    },
    {
        "id": "q13",
        "lesson_id": 12,
        "type": "mcq",
        "stem": "Which of the following conditions represents physiologically APPROPRIATE secondary erythrocytosis?",
        "options": [
            "Cerebellar hemangioblastoma",
            "Chronic obstructive pulmonary disease (COPD) with resting PaO2 52 mmHg",
            "Hepatocellular carcinoma",
            "Uterine fibroid (leiomyoma)"
        ],
        "correct_answer": "Chronic obstructive pulmonary disease (COPD) with resting PaO2 52 mmHg",
        "correct_index": 1,
        "explanation": "COPD induces chronic arterial hypoxemia, which appropriately triggers renal HIF-1α stabilization and physiological EPO secretion to compensate for reduced oxygen saturation.",
        "distractor_explanations": {
            "0": "Hemangioblastoma secretes ectopic EPO in an inappropriate, non-physiological manner.",
            "2": "HCC is an inappropriate paraneoplastic EPO source.",
            "3": "Uterine leiomyomas can inappropriately produce EPO or compress ureters."
        },
        "difficulty": "Medium",
        "review_status": "Reviewed by Medical Educator",
        "source_id": "src-accessmed-polycythemia"
    },
    {
        "id": "q14",
        "lesson_id": 13,
        "type": "mcq",
        "stem": "A 54-year-old male with Polycythemia Vera complains of severe, burning, painful erythema in both feet that worsens with warmth and is dramatically relieved within 30 minutes of taking an aspirin. What is this clinical manifestation?",
        "options": [
            "Gouty podagra",
            "Erythromelalgia",
            "Raynaud phenomenon",
            "Deep vein thrombosis"
        ],
        "correct_answer": "Erythromelalgia",
        "correct_index": 1,
        "explanation": "Erythromelalgia is caused by microvascular platelet aggregation, arteriolar inflammation, and thrombosis in acral vessels. Because it is platelet-driven via cyclooxygenase-1, single-dose aspirin provides dramatic, pathognomonic relief.",
        "distractor_explanations": {
            "0": "Podagra involves the first MTP joint with severe swelling/urate crystals, not relieved instantly by aspirin.",
            "2": "Raynaud causes pallor/cyanosis provoked by cold, not burning erythema provoked by warmth.",
            "3": "DVT causes unilateral swelling, calf pain, and warmth, not bilateral burning foot pain relieved by aspirin."
        },
        "difficulty": "Medium",
        "review_status": "Reviewed by Medical Educator",
        "source_id": "src-accessmed-polycythemia"
    },
    {
        "id": "q15",
        "lesson_id": 14,
        "type": "mcq",
        "stem": "Why does whole blood viscosity rise in a non-linear, exponential fashion as hematocrit exceeds 50%?",
        "options": [
            "Platelets undergo spontaneous degranulation releasing ADP",
            "Crowded erythrocytes deform each other, increasing cellular contact friction and resistance to laminar shear flow",
            "Plasma albumin concentration doubles",
            "Fibrinogen polymerizes spontaneously in microcapillaries"
        ],
        "correct_answer": "Crowded erythrocytes deform each other, increasing cellular contact friction and resistance to laminar shear flow",
        "correct_index": 1,
        "explanation": "Blood is a non-Newtonian suspension. When the fraction of space occupied by deformable red cells (hematocrit) exceeds 50%, cell-cell crowding, collision frequency, and shear resistance escalate exponentially.",
        "distractor_explanations": {
            "0": "Platelet degranulation is secondary to shear stress, not the primary physical driver of whole-blood viscosity.",
            "2": "Plasma albumin does not change.",
            "3": "Fibrinogen does not spontaneously polymerize without thrombin activation."
        },
        "difficulty": "Hard",
        "review_status": "Reviewed by Medical Educator",
        "source_id": "src-accessmed-polycythemia"
    },

    # TRUE / FALSE QUESTIONS
    {
        "id": "q16",
        "lesson_id": 1,
        "type": "true_false",
        "stem": "True or False: Reticulocytes possess a complete, functioning nucleus when they enter peripheral blood.",
        "options": ["True", "False"],
        "correct_answer": "False",
        "correct_index": 1,
        "explanation": "False. The nucleus is actively condensed and extruded during the orthochromatic normoblast stage inside the bone marrow. Reticulocytes are enucleated, containing only residual ribosomal RNA network."
    },
    {
        "id": "q17",
        "lesson_id": 5,
        "type": "true_false",
        "stem": "True or False: Serum ferritin is an acute-phase reactant and may remain deceptively normal or elevated in a patient with concurrent iron deficiency and active rheumatoid arthritis.",
        "options": ["True", "False"],
        "correct_answer": "True",
        "correct_index": 0,
        "explanation": "True. Because ferritin is upregulated by inflammatory cytokines (like IL-6 and TNF-α), inflammatory states elevate serum ferritin, sometimes masking concurrent depleted iron stores."
    },
    {
        "id": "q18",
        "lesson_id": 7,
        "type": "true_false",
        "stem": "True or False: Hemoglobinuria is a classic diagnostic feature of pure extravascular hemolysis occurring in the spleen.",
        "options": ["True", "False"],
        "correct_answer": "False",
        "correct_index": 1,
        "explanation": "False. In extravascular hemolysis, red cells are degraded intracellularly within splenic macrophages; free hemoglobin is not released into plasma, so it never filters into urine. Hemoglobinuria occurs only in INTRAVASCULAR hemolysis."
    },
    {
        "id": "q19",
        "lesson_id": 11,
        "type": "true_false",
        "stem": "True or False: In Polycythemia Vera, serum erythropoietin (EPO) is characteristically elevated due to autonomous pituitary stimulation.",
        "options": ["True", "False"],
        "correct_answer": "False",
        "correct_index": 1,
        "explanation": "False. In Polycythemia Vera, serum EPO is characteristically SUPPRESSED (low or undetectable) because excessive autonomous marrow RBC production hyper-oxygenates the renal parenchyma, shutting down normal physiological EPO production."
    },
    {
        "id": "q20",
        "lesson_id": 13,
        "type": "true_false",
        "stem": "True or False: In Polycythemia Vera, maintaining a target hematocrit below 45% with therapeutic phlebotomy significantly decreases cardiovascular mortality and major thrombotic events.",
        "options": ["True", "False"],
        "correct_answer": "True",
        "correct_index": 0,
        "explanation": "True. The CYTO-PV trial proved conclusively that keeping Hct < 45% reduces thrombotic complications fourfold compared to less stringent control."
    },

    # MATCH MECHANISM TO FINDING
    {
        "id": "q21",
        "lesson_id": 4,
        "type": "matching",
        "stem": "Match each Anemia Classification Finding to its most accurate Clinical Association:",
        "pairs": [
            {"term": "Microcytic hypochromic with high RDW and low ferritin", "match": "Iron Deficiency Anemia"},
            {"term": "Macrocytic with hypersegmented neutrophils and high MMA", "match": "Vitamin B12 Deficiency"},
            {"term": "Normocytic with low EPO and burr cells (echinocytes)", "match": "Chronic Kidney Disease Anemia"},
            {"term": "High reticulocyte count with positive direct Coombs test", "match": "Autoimmune Hemolytic Anemia"}
        ],
        "explanation": "Iron deficiency causes microcytosis with wide RDW; B12 deficiency produces macro-ovalocytes and elevated MMA; CKD causes normocytic EPO-deficient anemia; warm or cold AIHA produces Coombs-positive hemolysis.",
        "difficulty": "Medium",
        "review_status": "Reviewed by Medical Educator",
        "source_id": "src-merck-anemia"
    },
    {
        "id": "q22",
        "lesson_id": 14,
        "type": "matching",
        "stem": "Match each Pathophysiological State to its Characteristic Laboratory Profile:",
        "pairs": [
            {"term": "Polycythemia Vera", "match": "High Hb/Hct, Low Serum EPO, JAK2 V617F Positive"},
            {"term": "Severe COPD / High Altitude", "match": "High Hb/Hct, High Serum EPO, Arterial Hypoxemia"},
            {"term": "Anemia of Chronic Disease", "match": "Low Hb, High/Normal Ferritin, Low TIBC, High Hepcidin"},
            {"term": "Intravascular Hemolysis", "match": "Low Hb, Absent Haptoglobin, Hemoglobinuria, High LDH"}
        ],
        "explanation": "PV has low EPO due to autonomous mutation; COPD hypoxia drives high EPO; ACD features hepcidin-mediated iron trapping; intravascular hemolysis depletes haptoglobin with free urinary hemoglobin.",
        "difficulty": "Hard",
        "review_status": "Reviewed by Medical Educator",
        "source_id": "src-robbins-pathology"
    },

    # ARRANGE MECHANISM STEPS
    {
        "id": "q23",
        "lesson_id": 5,
        "type": "ordering",
        "stem": "Arrange the pathophysiological steps of developing Iron Deficiency Anemia in chronological order from earliest to latest:",
        "steps": [
            "Negative iron balance exceeds daily 1-2 mg intestinal absorption",
            "Marrow hemosiderin and serum ferritin stores drop below 30 ng/mL",
            "Transferrin saturation falls below 16% with elevated TIBC",
            "Erythroblasts undergo extra divisions producing microcytic hypochromic red cells",
            "Overt anemia with low hemoglobin and elevated RDW appears on CBC"
        ],
        "correct_order": [0, 1, 2, 3, 4],
        "explanation": "Iron balance turns negative first -> storage pools (ferritin) deplete -> transport capacity becomes deficient (low transferrin sat) -> erythroblasts divide smaller -> overt microcytic anemia manifests.",
        "difficulty": "Medium",
        "review_status": "Reviewed by Medical Educator",
        "source_id": "src-statpearls-anemia"
    },
    {
        "id": "q24",
        "lesson_id": 1,
        "type": "ordering",
        "stem": "Arrange the chronological developmental stages of human erythropoiesis:",
        "steps": [
            "Multipotent Hematopoietic Stem Cell / CFU-Erythroid",
            "Proerythroblast (large nucleolated precursor)",
            "Polychromatic erythroblast (initial hemoglobinization)",
            "Orthochromatic normoblast (pyknotic nucleus extruded)",
            "Circulating Reticulocyte (residual ribosomal RNA meshwork)",
            "Mature biconcave erythrocyte"
        ],
        "correct_order": [0, 1, 2, 3, 4, 5],
        "explanation": "Erythropoiesis proceeds from stem cell/CFU-E -> Proerythroblast -> Basophilic -> Polychromatic -> Orthochromatic normoblast (enucleation) -> Reticulocyte -> Mature Erythrocyte.",
        "difficulty": "Medium",
        "review_status": "Reviewed by Medical Educator",
        "source_id": "src-robbins-pathology"
    },

    # CLINICAL VIGNETTES
    {
        "id": "q25",
        "lesson_id": 15,
        "type": "vignette",
        "stem": "A 28-year-old female presents with progressive fatigue, exertional dyspnea, and brittle nails for 8 months. She reports heavy menstrual periods lasting 7 days every month. Physical examination reveals conjunctival pallor and mild spooning of her fingernails (koilonychia). Laboratory evaluation demonstrates: Hb 7.9 g/dL, MCV 64 fL, RDW 19.2%, Serum Ferritin 6 ng/mL, TIBC 470 µg/dL. What is the fundamental cellular mechanism explaining her red blood cell morphology?",
        "options": [
            "Impairment of thymidine triphosphate synthesis halting DNA replication",
            "Inadequate iron availability restricting protoporphyrin heme assembly, causing delayed cytoplasmic hemoglobin accumulation and extra cellular divisions",
            "Hepcidin-mediated sequestration of iron within macrophage lysosomes",
            "Immune IgG opsonization triggering splenic red pulp phagocytosis"
        ],
        "correct_answer": "Inadequate iron availability restricting protoporphyrin heme assembly, causing delayed cytoplasmic hemoglobin accumulation and extra cellular divisions",
        "correct_index": 1,
        "explanation": "This patient exhibits classical Iron Deficiency Anemia secondary to menorrhagia. Without iron, heme synthesis is impaired. Erythroblasts delay reaching critical hemoglobin density, undergoing additional cell divisions that yield tiny, pale (microcytic, hypochromic) erythrocytes with wide size variance (high RDW).",
        "distractor_explanations": {
            "0": "This describes megaloblastic anemia from B12 or folate deficiency.",
            "2": "This describes Anemia of Chronic Disease, where ferritin would be high or normal.",
            "3": "This describes autoimmune hemolytic anemia, which typically features normocytic or spherocytic cells with positive Coombs."
        },
        "difficulty": "MBBS Exam Level",
        "review_status": "Reviewed by Medical Educator",
        "source_id": "src-robbins-pathology"
    },
    {
        "id": "q26",
        "lesson_id": 15,
        "type": "vignette",
        "stem": "A 62-year-old male presents with severe headache, dizziness, and intense generalized pruritus after taking warm showers. He denies smoking or lung disease. Physical exam shows a ruddy, plethoric face and a palpable spleen tip 4 cm below the left costal margin. Labs: Hb 19.8 g/dL, Hct 61%, Platelets 620,000/µL, WBC 15,400/µL. Serum EPO is undetectable (< 1 mIU/mL). Which molecular test will definitively confirm the diagnosis?",
        "options": [
            "BCR-ABL1 quantitative reverse transcriptase PCR",
            "JAK2 V617F somatic mutation assay",
            "Arterial carboxyhemoglobin level",
            "Urine hemosiderin Prussian blue stain"
        ],
        "correct_answer": "JAK2 V617F somatic mutation assay",
        "correct_index": 1,
        "explanation": "The clinical picture of panmyelosis (high RBCs, WBCs, platelets), splenomegaly, aquagenic pruritus, and suppressed EPO is diagnostic of Polycythemia Vera. Testing for the gain-of-function JAK2 V617F mutation (present in >95% of PV) definitively confirms the diagnosis.",
        "distractor_explanations": {
            "0": "BCR-ABL1 tests for Chronic Myeloid Leukemia (CML), which typically presents with extreme granulocytosis and low RBC mass.",
            "2": "Carboxyhemoglobin checks for smoker's polycythemia, where WBC and platelets are normal and EPO is elevated.",
            "3": "Urine hemosiderin evaluates intravascular hemolysis, irrelevant in MPN."
        },
        "difficulty": "MBBS Exam Level",
        "review_status": "Reviewed by Medical Educator",
        "source_id": "src-accessmed-polycythemia"
    }
]

# 2. GLOSSARY (40+ terms)
glossary = [
    {"term": "2,3-BPG", "category": "Physiology", "definition": "2,3-Bisphosphoglycerate; erythrocyte glycolytic metabolite that binds deoxyhemoglobin to shift the O2 dissociation curve rightward, facilitating tissue oxygen release."},
    {"term": "Absolute Erythrocytosis", "category": "Polycythemia", "definition": "True increase in total circulating red blood cell mass (>25% above normal), subdivided into primary and secondary causes."},
    {"term": "Anisocytosis", "category": "Morphology", "definition": "Abnormal variation in the size of red blood cells, quantified by the Red Cell Distribution Width (RDW)."},
    {"term": "Aquagenic Pruritus", "category": "Polycythemia", "definition": "Intractable burning itching without cutaneous lesions provoked by warm water contact; pathognomonic clinical feature of Polycythemia Vera."},
    {"term": "Basophilic Stippling", "category": "Morphology", "definition": "Precipitated ribosomal RNA distributed throughout the erythrocyte, seen in lead poisoning, thalassemia, and sideroblastic anemia."},
    {"term": "Bite Cells (Degmacytes)", "category": "Hemolysis", "definition": "Erythrocytes with semicircular peripheral defect created when splenic macrophages pluck out Heinz bodies in G6PD deficiency."},
    {"term": "Budd-Chiari Syndrome", "category": "Complications", "definition": "Occlusion of hepatic venous outflow causing hepatomegaly, ascites, and abdominal pain; frequently caused by latent Polycythemia Vera."},
    {"term": "Burr Cells (Echinocytes)", "category": "Morphology", "definition": "Erythrocytes with regularly spaced, blunt spicules across the membrane; classically seen in uremia, renal failure, and liver dysfunction."},
    {"term": "Carboxyhemoglobin", "category": "Physiology", "definition": "Hemoglobin complexed with carbon monoxide; unable to bind oxygen and shifts remaining tetramers left, causing smoker's polycythemia."},
    {"term": "CFU-E", "category": "Physiology", "definition": "Colony-Forming Unit-Erythroid; late erythroid bone marrow progenitor possessing high densities of functional erythropoietin receptors."},
    {"term": "Coombs Test (DAT)", "category": "Diagnostic", "definition": "Direct Antiglobulin Test; detects antibodies (IgG) or complement (C3d) bound directly to the patient's red blood cell membrane."},
    {"term": "Erythropoietin (EPO)", "category": "Physiology", "definition": "Glycoprotein hormone synthesized by renal cortical interstitial fibroblasts in response to low PO2, driving erythroid survival and proliferation."},
    {"term": "Erythromelalgia", "category": "Polycythemia", "definition": "Episodic burning pain, warmth, and erythema of the hands/feet due to platelet microthrombosis in polycythemia vera; dramatically relieved by aspirin."},
    {"term": "Extravascular Hemolysis", "category": "Hemolysis", "definition": "Destruction of abnormal or antibody-coated red blood cells by macrophages within the splenic red pulp cords and hepatic Kupffer cells."},
    {"term": "Ferritin", "category": "Iron Metabolism", "definition": "Major intracellular iron storage protein complex; serum ferritin is the most sensitive non-invasive indicator of total body iron stores."},
    {"term": "Ferroportin", "category": "Iron Metabolism", "definition": "The only identified cellular iron export channel in enterocytes and macrophages; targeted for degradation by hepcidin."},
    {"term": "Gaisböck Syndrome", "category": "Polycythemia", "definition": "Relative or stress erythrocytosis characterized by elevated hematocrit due to reduced plasma volume in hypertensive, obese males."},
    {"term": "Haptoglobin", "category": "Hemolysis", "definition": "Serum alpha-2 glycoprotein that binds free hemoglobin dimers with high affinity; levels drop to near zero during intravascular hemolysis."},
    {"term": "Heinz Bodies", "category": "Hemolysis", "definition": "Insoluble clumps of oxidized, denatured hemoglobin visualized on supravital stains in G6PD deficiency and unstable hemoglobinopathies."},
    {"term": "Hematocrit (Hct)", "category": "Diagnostic", "definition": "Volume percentage of whole blood composed of packed red blood cells; normal is ~40-52% in adult males and ~36-48% in adult females."},
    {"term": "Hemosiderin", "category": "Iron Metabolism", "definition": "Insoluble granular iron storage complex visualized with Prussian blue stain; shed into urine during intravascular hemolysis."},
    {"term": "Hepcidin", "category": "Iron Metabolism", "definition": "Hepatic peptide hormone induced by IL-6 that binds and internalizes ferroportin, causing systemic iron trapping in Anemia of Chronic Disease."},
    {"term": "HIF-1α", "category": "Physiology", "definition": "Hypoxia-Inducible Factor 1-alpha; master transcription factor degraded in normoxia by prolyl hydroxylases but stabilized in hypoxia to drive EPO gene transcription."},
    {"term": "Hypersegmented Neutrophils", "category": "Morphology", "definition": "Neutrophils exhibiting 6 or more nuclear lobes (or >5% with 5 lobes); pathognomonic peripheral blood finding of megaloblastic anemia."},
    {"term": "Hypochromia", "category": "Morphology", "definition": "Decreased hemoglobin content inside erythrocytes, causing an expanded central pale area (>1/3 of diameter) and reduced MCHC."},
    {"term": "Intravascular Hemolysis", "category": "Hemolysis", "definition": "Lysis of red blood cells within the circulation, releasing free hemoglobin into plasma, depleting haptoglobin, and causing hemoglobinuria."},
    {"term": "JAK2 V617F", "category": "Polycythemia", "definition": "Somatic gain-of-function valine-to-phenylalanine mutation at codon 617 of Janus Kinase 2, present in >95% of Polycythemia Vera cases."},
    {"term": "Koilonychia", "category": "Clinical", "definition": "Concave, spoon-shaped malformation of fingernails classically seen in longstanding, severe iron deficiency anemia."},
    {"term": "Macrocytosis", "category": "Morphology", "definition": "Abnormally enlarged red blood cells with Mean Corpuscular Volume (MCV) exceeding 100 fL."},
    {"term": "Mean Corpuscular Volume (MCV)", "category": "Diagnostic", "definition": "Average volume of a single erythrocyte in femtoliters (fL). Normal reference range: 80 to 100 fL."},
    {"term": "Megaloblast", "category": "Morphology", "definition": "Giant, abnormal erythroid precursor in bone marrow demonstrating nuclear-cytoplasmic dyssynchrony caused by defective DNA synthesis."},
    {"term": "Mentzer Index", "category": "Diagnostic", "definition": "Ratio of MCV to RBC count (millions). Value < 13 suggests Thalassemia trait; > 13 suggests Iron Deficiency Anemia."},
    {"term": "Microcytosis", "category": "Morphology", "definition": "Abnormally small erythrocytes with Mean Corpuscular Volume (MCV) below 80 fL."},
    {"term": "Panmyelosis", "category": "Polycythemia", "definition": "Simultaneous hypercellular proliferation of all three hematopoietic bone marrow lineages: erythroid, granulocytic, and megakaryocytic."},
    {"term": "Pernicious Anemia", "category": "Anemia", "definition": "Autoimmune gastritis with destruction of gastric parietal cells, causing intrinsic factor deficiency and severe Vitamin B12 malabsorption."},
    {"term": "Plethora", "category": "Clinical", "definition": "Ruddy, dusky reddish-purple skin and mucous membrane discoloration caused by engorgement of capillaries with packed red cells."},
    {"term": "Poikilocytosis", "category": "Morphology", "definition": "Presence of abnormally shaped red blood cells (e.g., target cells, sickle cells, spherocytes, schistocytes) on blood smear."},
    {"term": "Polycythemia Vera (PV)", "category": "Polycythemia", "definition": "Clonal myeloproliferative neoplasm characterized by autonomous trilineage marrow proliferation driven by JAK2 mutation and suppressed EPO."},
    {"term": "Relative Erythrocytosis", "category": "Polycythemia", "definition": "Apparent elevation in hematocrit and Hb caused by reduced intravascular plasma volume with normal true total red cell mass."},
    {"term": "Reticulocyte", "category": "Physiology", "definition": "Young, non-nucleated erythrocyte containing residual ribosomal RNA; serves as the primary clinical gauge of marrow erythropoietic response."},
    {"term": "RPI (Reticulocyte Production Index)", "category": "Diagnostic", "definition": "Calculated value correcting reticulocyte percentage for both anemia severity and premature marrow shift; RPI > 2 indicates adequate marrow response."},
    {"term": "Schistocyte", "category": "Morphology", "definition": "Fragmented red blood cell (helmet cell) formed by mechanical shearing against intravascular fibrin strands in microangiopathic hemolytic anemias."},
    {"term": "Sideroblast", "category": "Morphology", "definition": "Erythroblast containing iron granules in cytoplasm; ringed sideroblasts feature iron accumulation in perinuclear mitochondria."},
    {"term": "Subacute Combined Degeneration", "category": "Clinical", "definition": "Demyelination of spinal cord dorsal and lateral columns caused by B12 deficiency; presents with sensory ataxia and spastic weakness."},
    {"term": "Target Cells (Codocytes)", "category": "Morphology", "definition": "Erythrocytes with central hemoglobin collection surrounded by clear ring and outer rim; seen in thalassemia, hemoglobin C, and liver disease."},
    {"term": "TIBC (Total Iron-Binding Capacity)", "category": "Iron Metabolism", "definition": "Laboratory measure of maximum iron that transferrin can bind; elevated in iron deficiency, decreased in anemia of chronic disease."}
]

# 3. FLASHCARDS (30 cards)
flashcards = [
    {
        "id": "fc1",
        "category": "Physiology",
        "front": "What cell type produces ~90% of human erythropoietin, and what molecular factor triggers its transcription?",
        "back": "Renal interstitial peritubular fibroblasts (capillary plexus). Transcription is triggered by stabilization of Hypoxia-Inducible Factor 1-alpha (HIF-1α) under low tissue PO2."
    },
    {
        "id": "fc2",
        "category": "Physiology",
        "front": "What is the normal lifespan of a circulating erythrocyte, and why must it produce 100% of its ATP via anaerobic glycolysis?",
        "back": "Lifespan is 120 ± 20 days. Mature RBCs lack mitochondria, so they rely exclusively on the Embden-Meyerhof anaerobic pathway to generate ATP."
    },
    {
        "id": "fc3",
        "category": "Classification",
        "front": "What is the normal reference range for Mean Corpuscular Volume (MCV), and what defines microcytic vs macrocytic?",
        "back": "Normal MCV = 80 to 100 fL. Microcytic = MCV < 80 fL (heme/globin synthesis defect). Macrocytic = MCV > 100 fL (DNA synthesis or lipid defect)."
    },
    {
        "id": "fc4",
        "category": "Classification",
        "front": "How do you calculate and interpret the Reticulocyte Production Index (RPI)?",
        "back": "RPI = [Observed Retic % × (Patient Hct / 45)] ÷ Shift Factor (1.0 to 2.5). RPI > 2.0 = adequate/hyperproliferative response (hemolysis/bleeding). RPI < 2.0 = hypoproliferative (production failure)."
    },
    {
        "id": "fc5",
        "category": "Iron Deficiency",
        "front": "What is the classic laboratory profile of Iron Deficiency Anemia (Ferritin, Serum Iron, TIBC, Transferrin Saturation)?",
        "back": "Serum Ferritin: Low (< 30 ng/mL, most specific)\nSerum Iron: Low\nTIBC: High (compensatory transferrin increase)\nTransferrin Saturation: Low (< 16%)"
    },
    {
        "id": "fc6",
        "category": "Iron Deficiency",
        "front": "What is the Mentzer Index and how does it differentiate Iron Deficiency from Thalassemia Minor?",
        "back": "Mentzer Index = MCV / RBC count (millions).\n> 13 indicates Iron Deficiency Anemia (low RBC count with low MCV).\n< 13 indicates Thalassemia Trait (high RBC count despite low MCV)."
    },
    {
        "id": "fc7",
        "category": "Megaloblastic",
        "front": "What pathognomonic peripheral smear finding characterizes megaloblastic anemia, and what causes nuclear-cytoplasmic asynchrony?",
        "back": "Hypersegmented neutrophils (≥ 6 lobes, or ≥ 5% with 5 lobes). Nuclear maturation lags behind hemoglobinized cytoplasm due to impaired thymidine (dTTP) DNA synthesis."
    },
    {
        "id": "fc8",
        "category": "Megaloblastic",
        "front": "Which metabolite is elevated ONLY in Vitamin B12 deficiency and normal in Folate deficiency?",
        "back": "Methylmalonic Acid (MMA) is elevated only in B12 deficiency (due to methylmalonyl-CoA mutase failure). Homocysteine is elevated in both B12 and folate deficiency."
    },
    {
        "id": "fc9",
        "category": "Megaloblastic",
        "front": "Why is it dangerous to treat an unknown macrocytic anemia with folic acid alone?",
        "back": "Folic acid corrects the anemia and smear abnormalities, but does NOT prevent irreversible demyelination of spinal cord dorsal and lateral columns (Subacute Combined Degeneration)."
    },
    {
        "id": "fc10",
        "category": "Hemolysis",
        "front": "Differentiate the sites and clinical consequences of Intravascular vs Extravascular Hemolysis.",
        "back": "Extravascular: Spleen/liver macrophages engulf RBCs -> Jaundice, elevated unconjugated bilirubin, splenomegaly, gallstones.\nIntravascular: Lysis inside blood vessels -> Depleted haptoglobin, hemoglobinemia, hemoglobinuria, hemosiderinuria."
    },
    {
        "id": "fc11",
        "category": "Hemolysis",
        "front": "What is haptoglobin and why does its serum concentration plummet in hemolytic anemia?",
        "back": "Haptoglobin is an acute-phase protein that binds free hemoglobin dimers forming a stable 1:1 complex, which is rapidly cleared and degraded by hepatic CD163 macrophages."
    },
    {
        "id": "fc12",
        "category": "Inflammation & Renal",
        "front": "Explain the role of Hepcidin in Anemia of Chronic Disease (ACD).",
        "back": "IL-6 triggers hepatic hepcidin secretion. Hepcidin binds and degrades ferroportin on enterocytes and macrophages, trapping iron inside storage cells -> Low serum iron, High/Normal ferritin, Low TIBC."
    },
    {
        "id": "fc13",
        "category": "Inflammation & Renal",
        "front": "What is the primary mechanism of anemia in Chronic Kidney Disease (CKD)?",
        "back": "Tubulointerstitial fibrosis destroys renal peritubular interstitial fibroblasts, causing profound deficiency in Erythropoietin (EPO) synthesis -> Normocytic hypoproliferative anemia."
    },
    {
        "id": "fc14",
        "category": "Physiology",
        "front": "How does 2,3-Bisphosphoglycerate (2,3-BPG) facilitate tissue oxygenation in anemic patients?",
        "back": "2,3-BPG binds between beta-globin chains, stabilizing the deoxygenated T-conformation of hemoglobin and shifting the oxygen dissociation curve to the right, enhancing tissue oxygen unloading."
    },
    {
        "id": "fc15",
        "category": "Polycythemia",
        "front": "What is the difference between Relative (spurious) and Absolute Erythrocytosis?",
        "back": "Relative: Total RBC mass is NORMAL, but plasma volume is reduced (dehydration, burns, diuretics, Gaisböck syndrome).\nAbsolute: True expansion of total circulating RBC mass (>25% above normal)."
    },
    {
        "id": "fc16",
        "category": "Polycythemia",
        "front": "What is the molecular hallmark of Polycythemia Vera (PV)?",
        "back": "Somatic gain-of-function mutation in Janus Kinase 2: JAK2 V617F (present in >95% of cases) or JAK2 exon 12, causing constitutive downstream STAT5/AKT signaling without EPO binding."
    },
    {
        "id": "fc17",
        "category": "Polycythemia",
        "front": "Why is serum Erythropoietin (EPO) low/undetectable in Polycythemia Vera?",
        "back": "Autonomous, unregulated marrow RBC production creates massive red cell mass and high renal oxygen delivery, suppressing normal renal EPO transcription via negative feedback."
    },
    {
        "id": "fc18",
        "category": "Polycythemia",
        "front": "What are the WHO 2016/2022 Major Criteria for diagnosing Polycythemia Vera?",
        "back": "1. Hb > 16.5 g/dL (men) / > 16.0 g/dL (women) or Hct > 49% (men) / > 48% (women)\n2. Bone marrow biopsy showing trilineage hypercellularity (panmyelosis)\n3. Presence of JAK2 V617F or JAK2 exon 12 mutation"
    },
    {
        "id": "fc19",
        "category": "Polycythemia",
        "front": "What is the target hematocrit during therapeutic phlebotomy in Polycythemia Vera, and why?",
        "back": "Target Hct < 45% in both men and women. The CYTO-PV trial proved this threshold reduces cardiovascular death and major arterial/venous thrombotic events fourfold."
    },
    {
        "id": "fc20",
        "category": "Polycythemia",
        "front": "Name 4 tumors that can cause paraneoplastic inappropriate secondary erythrocytosis by secreting EPO.",
        "back": "Potentially Really High Hematocrit:\n1. Pheochromocytoma\n2. Renal cell carcinoma (RCC)\n3. Hepatocellular carcinoma (HCC)\n4. Hemangioblastoma (cerebellar)"
    },
    {
        "id": "fc21",
        "category": "Complications",
        "front": "Why does blood viscosity increase exponentially when hematocrit exceeds 50%?",
        "back": "Whole blood is non-Newtonian. When the volume fraction of deformable erythrocytes exceeds 50%, cell-cell collision frequency and shear friction between packed RBCs escalate exponentially."
    },
    {
        "id": "fc22",
        "category": "Complications",
        "front": "What is Erythromelalgia and what medication provides pathognomonic relief?",
        "back": "Episodic burning pain, erythema, and warmth in hands and feet caused by microvascular platelet aggregation and thrombosis in polycythemia vera. Aspirin provides prompt relief."
    },
    {
        "id": "fc23",
        "category": "Comparison",
        "front": "Contrast blood viscosity and cardiac output in severe anemia versus severe polycythemia.",
        "back": "Anemia: Low viscosity, decreased peripheral resistance, high cardiac output (hyperdynamic circulation, flow murmurs).\nPolycythemia: Markedly high viscosity, sluggish microcirculatory flow, high vascular resistance, thrombosis risk."
    },
    {
        "id": "fc24",
        "category": "Morphology",
        "front": "What are Schistocytes and in which hematological conditions are they characteristically observed?",
        "back": "Fragmented red blood cells (helmet cells) created by mechanical shearing on fibrin strands. Seen in Microangiopathic Hemolytic Anemia (TTP, HUS, DIC) and mechanical heart valves."
    },
    {
        "id": "fc25",
        "category": "Clinical",
        "front": "What is Budd-Chiari syndrome and how does it relate to Polycythemia Vera?",
        "back": "Thrombosis of hepatic veins causing hepatomegaly, ascites, and abdominal pain. PV is the leading underlying cause; any patient presenting with Budd-Chiari should be tested for JAK2 V617F."
    }
]

# 4. SAMPLE TEXTBOOK PRESETS (For 1-click textbook explainer testing)
sample_textbooks = [
    {
        "id": "tb-ida",
        "title": "Robbins Pathology — Iron Deficiency Anemia (Excerpt)",
        "chapter": "Chapter 14: Red Blood Cell Disorders",
        "text": "Iron deficiency is the most common nutritional disorder in the world. It results in a microcytic, hypochromic anemia. In well-nourished individuals, iron balance is maintained by tight regulation of duodenal mucosal absorption of dietary iron, since there is no regulated physiological pathway for iron excretion. Most iron loss occurs through shedding of mucosal and skin epithelial cells (approx 1 mg/day). In adult men and postmenopausal women, gastrointestinal blood loss must be considered the cause of iron deficiency until proven otherwise. The stages of iron deficiency begin with depletion of storage iron, reflected by a decline in serum ferritin. This is followed by a fall in serum iron and an increase in total iron-binding capacity (TIBC), driving transferrin saturation below 16%. In the final stage, microcytic and hypochromic red cells appear on peripheral smear with high RDW and low hemoglobin."
    },
    {
        "id": "tb-megalo",
        "title": "Robbins Pathology — Megaloblastic Anemias (Excerpt)",
        "chapter": "Chapter 14: Megaloblastic Anemias",
        "text": "The megaloblastic anemias are a group of disorders characterized by common morphologic findings: the presence of erythroblasts in the bone marrow that are abnormally large (megaloblasts) and have a distinctive nuclear-cytoplasmic asynchrony. The fundamental biochemical lesion is an impairment of DNA synthesis, caused most commonly by deficiencies of vitamin B12 (cobalamin) or folic acid. RNA and protein synthesis proceed at a relatively normal pace, explaining why the cytoplasm enlarges and matures with hemoglobinization while the nucleus remains immature and finely stippled. In peripheral blood, red cells are macro-ovalocytes with mean corpuscular volume (MCV) exceeding 100 to 110 fL. A hallmark finding on peripheral smear is the presence of hypersegmented neutrophils, defined as neutrophils with five or more nuclear lobes. Unlike folate deficiency, vitamin B12 deficiency leads to progressive demyelination of the posterior and lateral columns of the spinal cord (subacute combined degeneration)."
    },
    {
        "id": "tb-pv",
        "title": "Robbins Pathology — Polycythemia Vera (Excerpt)",
        "chapter": "Chapter 14: Myeloproliferative Neoplasms",
        "text": "Polycythemia vera (PV) is a chronic myeloproliferative neoplasm characterized by autonomous production of red blood cells, granulocytes, and platelets (panmyelosis). It is strongly associated with activating point mutations in the tyrosine kinase JAK2, most commonly JAK2 V617F, found in over 95% of patients. This somatic mutation renders hematopoietic stem cells independent of erythropoietin (EPO) and other growth factors for survival and proliferation. Consequently, serum EPO levels are characteristically low or undetectable due to negative feedback inhibition from the expanded red cell mass. The clinical morbidities of PV stem from increased whole-blood viscosity and vascular stasis. Major complications include arterial and venous thrombosis, including deep vein thrombosis, pulmonary embolism, stroke, and hepatic vein thrombosis (Budd-Chiari syndrome). Patients characteristically report aquagenic pruritus (severe itching after warm baths) and erythromelalgia."
    },
    {
        "id": "tb-hemolysis",
        "title": "Merck Manual — Extravascular vs Intravascular Hemolysis (Excerpt)",
        "chapter": "Hematology: Approach to Hemolytic Anemia",
        "text": "Hemolytic anemias are defined by premature destruction of circulating erythrocytes, reducing red cell lifespan to less than 120 days. Extravascular hemolysis takes place when damaged or antibody-coated red blood cells are identified and cleared by macrophages of the reticuloendothelial system, particularly in the spleen and liver. Extravascular hemolysis characteristically manifests with splenomegaly, unconjugated hyperbilirubinemia, and increased fecal/urinary urobilinogen, but absent hemoglobinuria. In contrast, intravascular hemolysis occurs when erythrocytes rupture directly within the circulation as a result of complement fixation, mechanical shear trauma, or exogenous toxins. Free hemoglobin is liberated into plasma, where it binds irreversibly to serum haptoglobin. When haptoglobin is exhausted, free hemoglobin dimers are filtered by the glomeruli, causing gross hemoglobinuria and dark brown urine. Renal tubular epithelial cells reabsorb iron from hemoglobin, sloughing off days later as detectable urine hemosiderin."
    }
]

# Write all databank files
with open(os.path.join(CONTENT_DIR, "questions_seed.json"), "w", encoding="utf-8") as f:
    json.dump(questions, f, indent=2)
print(f"Created questions_seed.json with {len(questions)} high-yield medical questions.")

with open(os.path.join(CONTENT_DIR, "glossary.json"), "w", encoding="utf-8") as f:
    json.dump(glossary, f, indent=2)
print(f"Created glossary.json with {len(glossary)} hematology terms.")

with open(os.path.join(CONTENT_DIR, "flashcards.json"), "w", encoding="utf-8") as f:
    json.dump(flashcards, f, indent=2)
print(f"Created flashcards.json with {len(flashcards)} active recall flashcards.")

with open(os.path.join(CONTENT_DIR, "sample_textbooks.json"), "w", encoding="utf-8") as f:
    json.dump(sample_textbooks, f, indent=2)
print(f"Created sample_textbooks.json with {len(sample_textbooks)} textbook presets.")
