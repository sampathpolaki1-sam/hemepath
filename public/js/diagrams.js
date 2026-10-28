// diagrams.js - Hand-authored Medical SVG Diagrams with Interactive Node Explanations
(function() {
  window.HemeDiagrams = {
    render: function(containerId, diagramId, infoContainerId) {
      const container = document.getElementById(containerId);
      if (!container) return;

      const svgGenerator = this.registry[diagramId] || this.registry["diag_rbc_loop"];
      container.innerHTML = svgGenerator();

      // Attach interactivity
      if (infoContainerId) {
        const infoBox = document.getElementById(infoContainerId);
        const nodes = container.querySelectorAll('.svg-node');
        nodes.forEach(node => {
          node.addEventListener('click', function() {
            const title = this.getAttribute('data-title') || 'Educational Node';
            const detail = this.getAttribute('data-detail') || '';
            if (infoBox) {
              infoBox.innerHTML = `<strong>📌 ${title}</strong>: ${detail}`;
              infoBox.classList.add('active');
            }
          });
        });
      }
    },

    registry: {
      // 1. RBC Production Loop
      diag_rbc_loop: function() {
        return `
        <svg viewBox="0 0 500 280" class="diagram-svg" xmlns="http://www.w3.org/2000/svg">
          <defs>
            <marker id="arrow" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
              <path d="M 0 1 L 8 5 L 0 9 z" fill="#e11d48"/>
            </marker>
            <linearGradient id="gradRed" x1="0" y1="0" x2="1" y2="1">
              <stop offset="0%" stop-color="#e11d48"/>
              <stop offset="100%" stop-color="#9f1239"/>
            </linearGradient>
            <linearGradient id="gradBlue" x1="0" y1="0" x2="1" y2="1">
              <stop offset="0%" stop-color="#3b82f6"/>
              <stop offset="100%" stop-color="#1e40af"/>
            </linearGradient>
            <linearGradient id="gradPurple" x1="0" y1="0" x2="1" y2="1">
              <stop offset="0%" stop-color="#8b5cf6"/>
              <stop offset="100%" stop-color="#5b21b6"/>
            </linearGradient>
            <linearGradient id="gradGreen" x1="0" y1="0" x2="1" y2="1">
              <stop offset="0%" stop-color="#10b981"/>
              <stop offset="100%" stop-color="#047857"/>
            </linearGradient>
          </defs>

          <!-- Arrows -->
          <path d="M 120 70 L 210 70" stroke="#e11d48" stroke-width="2.5" marker-end="url(#arrow)" fill="none"/>
          <path d="M 320 70 L 380 120" stroke="#e11d48" stroke-width="2.5" marker-end="url(#arrow)" fill="none"/>
          <path d="M 380 170 L 290 220" stroke="#e11d48" stroke-width="2.5" marker-end="url(#arrow)" fill="none"/>
          <path d="M 190 220 L 80 170" stroke="#e11d48" stroke-width="2.5" marker-end="url(#arrow)" fill="none"/>
          <path d="M 70 120 L 70 85" stroke="#10b981" stroke-width="2" stroke-dasharray="4" marker-end="url(#arrow)" fill="none"/>

          <!-- Negative Feedback Label -->
          <text x="75" y="105" font-size="9" font-weight="700" fill="#10b981">Negative Feedback</text>

          <!-- Node 1: Tissue Oxygen Sensor -->
          <g class="svg-node" data-title="Renal Oxygen Sensor" data-detail="Renal interstitial fibroblasts sense low PaO2 via HIF-1alpha stabilization, triggering Erythropoietin (EPO) gene transcription.">
            <rect x="20" y="30" width="105" height="55" rx="8" fill="url(#gradBlue)" />
            <text x="72" y="52" fill="#fff" font-size="11" font-weight="bold" text-anchor="middle">Kidney Sensor</text>
            <text x="72" y="68" fill="#dbeafe" font-size="9" text-anchor="middle">HIF-1α Hypoxia</text>
          </g>

          <!-- Node 2: Erythropoietin Hormone -->
          <g class="svg-node" data-title="Erythropoietin (EPO)" data-detail="Glycoprotein hormone carried via bloodstream to bone marrow, binding homodimeric EPO receptors on erythroid progenitors.">
            <rect x="215" y="42" width="105" height="55" rx="8" fill="url(#gradPurple)" />
            <text x="267" y="64" fill="#fff" font-size="11" font-weight="bold" text-anchor="middle">EPO Secretion</text>
            <text x="267" y="80" fill="#ede9fe" font-size="9" text-anchor="middle">Blood Circulation</text>
          </g>

          <!-- Node 3: Bone Marrow Erythropoiesis -->
          <g class="svg-node" data-title="Bone Marrow CFU-E" data-detail="EPO stimulates proliferation and inhibits apoptosis of Colony-Forming Unit-Erythroid (CFU-E) and proerythroblasts via JAK2/STAT5.">
            <rect x="340" y="125" width="125" height="55" rx="8" fill="url(#gradRed)" />
            <text x="402" y="147" fill="#fff" font-size="11" font-weight="bold" text-anchor="middle">Bone Marrow</text>
            <text x="402" y="163" fill="#ffe4e6" font-size="9" text-anchor="middle">Erythropoiesis</text>
          </g>

          <!-- Node 4: Circulating Red Blood Cells -->
          <g class="svg-node" data-title="Mature RBC Circulation" data-detail="Enucleated, biconcave erythrocytes packed with hemoglobin circulate for 120 days, optimizing capillary gas exchange.">
            <rect x="195" y="195" width="115" height="55" rx="8" fill="url(#gradRed)" />
            <text x="252" y="217" fill="#fff" font-size="11" font-weight="bold" text-anchor="middle">Circulating RBCs</text>
            <text x="252" y="233" fill="#ffe4e6" font-size="9" text-anchor="middle">Reticulocytes Release</text>
          </g>

          <!-- Node 5: Tissue Oxygen Delivery -->
          <g class="svg-node" data-title="Tissue Oxygenation" data-detail="Increased RBC mass restores tissue PO2, enabling prolyl hydroxylases to degrade HIF-1alpha and downregulate further EPO release.">
            <rect x="20" y="135" width="105" height="55" rx="8" fill="url(#gradGreen)" />
            <text x="72" y="157" fill="#fff" font-size="11" font-weight="bold" text-anchor="middle">Tissue O2 Normal</text>
            <text x="72" y="173" fill="#d1fae5" font-size="9" text-anchor="middle">Hypoxia Cleared</text>
          </g>
        </svg>
        `;
      },

      // 2. Anemia Mechanism Map (Triad)
      diag_anemia_mechanisms: function() {
        return `
        <svg viewBox="0 0 500 280" class="diagram-svg" xmlns="http://www.w3.org/2000/svg">
          <defs>
            <marker id="arrow2" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
              <path d="M 0 1 L 8 5 L 0 9 z" fill="#4f46e5"/>
            </marker>
          </defs>

          <!-- Main Root -->
          <g class="svg-node" data-title="Anemia Pathophysiology" data-detail="All forms of anemia fundamentally originate from one or more of these three cardinal mechanisms.">
            <rect x="180" y="15" width="140" height="42" rx="8" fill="#e11d48"/>
            <text x="250" y="41" fill="#fff" font-size="13" font-weight="bold" text-anchor="middle">ANEMIA TRIAD</text>
          </g>

          <!-- Connectors -->
          <path d="M 220 57 L 90 105" stroke="#4f46e5" stroke-width="2" marker-end="url(#arrow2)" fill="none"/>
          <path d="M 250 57 L 250 105" stroke="#4f46e5" stroke-width="2" marker-end="url(#arrow2)" fill="none"/>
          <path d="M 280 57 L 410 105" stroke="#4f46e5" stroke-width="2" marker-end="url(#arrow2)" fill="none"/>

          <!-- Branch 1: Blood Loss -->
          <g class="svg-node" data-title="Mechanism 1: Blood Loss" data-detail="Acute (trauma, aneurysm) causes hypovolemia followed by reticulocyte surge. Chronic (GI ulcer, colon cancer, menorrhagia) causes iron depletion.">
            <rect x="20" y="110" width="135" height="145" rx="8" fill="#f8fafc" stroke="#3b82f6" stroke-width="1.5"/>
            <rect x="20" y="110" width="135" height="28" rx="8" fill="#3b82f6"/>
            <text x="87" y="129" fill="#fff" font-size="11" font-weight="bold" text-anchor="middle">1. Blood Loss</text>
            <text x="30" y="155" fill="#1e293b" font-size="10" font-weight="600">• Acute Hemorrhage</text>
            <text x="30" y="172" fill="#64748b" font-size="9">(Trauma, Rupture)</text>
            <text x="30" y="195" fill="#1e293b" font-size="10" font-weight="600">• Chronic Occult Bleed</text>
            <text x="30" y="212" fill="#64748b" font-size="9">(GI Polyp, Menorrhagia)</text>
            <text x="30" y="235" fill="#e11d48" font-size="9" font-weight="bold">→ Iron Depletion</text>
          </g>

          <!-- Branch 2: Production Defect -->
          <g class="svg-node" data-title="Mechanism 2: Decreased Production" data-detail="Marrow hypoproliferation due to lack of substrates (Iron, B12, Folate), lack of EPO (renal failure), or stem cell damage (aplastic anemia).">
            <rect x="180" y="110" width="140" height="145" rx="8" fill="#f8fafc" stroke="#8b5cf6" stroke-width="1.5"/>
            <rect x="180" y="110" width="140" height="28" rx="8" fill="#8b5cf6"/>
            <text x="250" y="129" fill="#fff" font-size="11" font-weight="bold" text-anchor="middle">2. Reduced Output</text>
            <text x="190" y="155" fill="#1e293b" font-size="10" font-weight="600">• Nutrient Deficiency</text>
            <text x="190" y="172" fill="#64748b" font-size="9">(Iron, B12, Folate)</text>
            <text x="190" y="195" fill="#1e293b" font-size="10" font-weight="600">• Hormonal Deficit</text>
            <text x="190" y="212" fill="#64748b" font-size="9">(EPO in CKD)</text>
            <text x="190" y="235" fill="#e11d48" font-size="9" font-weight="bold">→ RPI < 2.0 (Low Retic)</text>
          </g>

          <!-- Branch 3: Accelerated Destruction -->
          <g class="svg-node" data-title="Mechanism 3: Accelerated Hemolysis" data-detail="RBC survival shortened <120 days. Intravascular (mechanical, complement) or Extravascular (splenic macrophage phagocytosis).">
            <rect x="345" y="110" width="135" height="145" rx="8" fill="#f8fafc" stroke="#e11d48" stroke-width="1.5"/>
            <rect x="345" y="110" width="135" height="28" rx="8" fill="#e11d48"/>
            <text x="412" y="129" fill="#fff" font-size="11" font-weight="bold" text-anchor="middle">3. Destruction</text>
            <text x="355" y="155" fill="#1e293b" font-size="10" font-weight="600">• Intrinsic Defects</text>
            <text x="355" y="172" fill="#64748b" font-size="9">(Sickle, G6PD, Spherocyte)</text>
            <text x="355" y="195" fill="#1e293b" font-size="10" font-weight="600">• Extrinsic Hazards</text>
            <text x="355" y="212" fill="#64748b" font-size="9">(Autoimmune, TTP, DIC)</text>
            <text x="355" y="235" fill="#10b981" font-size="9" font-weight="bold">→ RPI > 2.0 (High Retic)</text>
          </g>
        </svg>
        `;
      },

      // 3. MCV Classification Flowchart
      diag_mcv_flowchart: function() {
        return `
        <svg viewBox="0 0 500 280" class="diagram-svg" xmlns="http://www.w3.org/2000/svg">
          <!-- Top Root -->
          <g class="svg-node" data-title="CBC Confirms Anemia" data-detail="Hemoglobin < 13.0 g/dL (men) or < 12.0 g/dL (women). Step 1: Examine Mean Corpuscular Volume (MCV).">
            <rect x="175" y="10" width="150" height="38" rx="8" fill="#0f172a"/>
            <text x="250" y="34" fill="#fff" font-size="12" font-weight="bold" text-anchor="middle">CONFIRMED ANEMIA</text>
          </g>

          <path d="M 210 48 L 80 85" stroke="#94a3b8" stroke-width="2" fill="none"/>
          <path d="M 250 48 L 250 85" stroke="#94a3b8" stroke-width="2" fill="none"/>
          <path d="M 290 48 L 420 85" stroke="#94a3b8" stroke-width="2" fill="none"/>

          <!-- Microcytic -->
          <g class="svg-node" data-title="Microcytic (< 80 fL)" data-detail="Defect in heme or globin synthesis. Mnemonic TAILS: Thalassemia, Anemia of Chronic Disease, Iron deficiency, Lead poisoning, Sideroblastic anemia.">
            <rect x="15" y="90" width="130" height="170" rx="8" fill="#f8fafc" stroke="#e11d48" stroke-width="1.5"/>
            <rect x="15" y="90" width="130" height="26" rx="8" fill="#e11d48"/>
            <text x="80" y="108" fill="#fff" font-size="11" font-weight="bold" text-anchor="middle">MICROCYTIC &lt; 80 fL</text>
            <text x="25" y="132" fill="#1e293b" font-size="10" font-weight="700">• Iron Deficiency (IDA)</text>
            <text x="25" y="146" fill="#64748b" font-size="9">Low Ferritin, High TIBC</text>
            <text x="25" y="166" fill="#1e293b" font-size="10" font-weight="700">• Thalassemia Trait</text>
            <text x="25" y="180" fill="#64748b" font-size="9">Mentzer &lt; 13, Normal Ferritin</text>
            <text x="25" y="200" fill="#1e293b" font-size="10" font-weight="700">• Anemia of Inflammation</text>
            <text x="25" y="214" fill="#64748b" font-size="9">Hepcidin block (mild)</text>
            <text x="25" y="234" fill="#1e293b" font-size="10" font-weight="700">• Sideroblastic / Lead</text>
          </g>

          <!-- Normocytic -->
          <g class="svg-node" data-title="Normocytic (80-100 fL)" data-detail="Check Reticulocyte Production Index (RPI). High RPI = Hemolysis/acute bleeding. Low RPI = Renal failure, marrow aplasia, early ACD.">
            <rect x="180" y="90" width="140" height="170" rx="8" fill="#f8fafc" stroke="#3b82f6" stroke-width="1.5"/>
            <rect x="180" y="90" width="140" height="26" rx="8" fill="#3b82f6"/>
            <text x="250" y="108" fill="#fff" font-size="11" font-weight="bold" text-anchor="middle">NORMOCYTIC 80-100</text>
            <text x="190" y="132" fill="#047857" font-size="10" font-weight="700">RPI &gt; 2.0 (High Retic):</text>
            <text x="190" y="146" fill="#64748b" font-size="9">• Acute Blood Loss</text>
            <text x="190" y="160" fill="#64748b" font-size="9">• Active Hemolysis</text>
            <text x="190" y="185" fill="#b91c1c" font-size="10" font-weight="700">RPI &lt; 2.0 (Low Retic):</text>
            <text x="190" y="200" fill="#64748b" font-size="9">• Chronic Kidney Disease</text>
            <text x="190" y="214" fill="#64748b" font-size="9">• Aplastic Anemia</text>
            <text x="190" y="228" fill="#64748b" font-size="9">• Bone Marrow Infiltration</text>
          </g>

          <!-- Macrocytic -->
          <g class="svg-node" data-title="Macrocytic (> 100 fL)" data-detail="Evaluate smear for hypersegmented neutrophils. Present = Megaloblastic (B12/Folate). Absent = Liver disease, alcohol, reticulocytosis.">
            <rect x="350" y="90" width="135" height="170" rx="8" fill="#f8fafc" stroke="#8b5cf6" stroke-width="1.5"/>
            <rect x="350" y="90" width="135" height="26" rx="8" fill="#8b5cf6"/>
            <text x="417" y="108" fill="#fff" font-size="11" font-weight="bold" text-anchor="middle">MACROCYTIC &gt; 100 fL</text>
            <text x="360" y="132" fill="#4338ca" font-size="10" font-weight="700">Megaloblastic (Hyperseg):</text>
            <text x="360" y="146" fill="#64748b" font-size="9">• Vitamin B12 Deficiency</text>
            <text x="360" y="160" fill="#64748b" font-size="9">• Folate Deficiency</text>
            <text x="360" y="174" fill="#64748b" font-size="9">• Methotrexate / Hydroxyurea</text>
            <text x="360" y="198" fill="#1e293b" font-size="10" font-weight="700">Non-Megaloblastic:</text>
            <text x="360" y="212" fill="#64748b" font-size="9">• Alcohol Use / Liver</text>
            <text x="360" y="226" fill="#64748b" font-size="9">• Marked Reticulocytosis</text>
          </g>
        </svg>
        `;
      },

      // 4. Polycythemia Classification
      diag_poly_class: function() {
        return `
        <svg viewBox="0 0 500 280" class="diagram-svg" xmlns="http://www.w3.org/2000/svg">
          <g class="svg-node" data-title="Elevated Hematocrit / Hb" data-detail="Hb > 16.5 g/dL (men) or > 16.0 g/dL (women). First step: rule out dehydration hemoconcentration.">
            <rect x="160" y="12" width="180" height="36" rx="8" fill="#be123c"/>
            <text x="250" y="35" fill="#fff" font-size="11" font-weight="bold" text-anchor="middle">ELEVATED HEMATOCRIT</text>
          </g>

          <path d="M 210 48 L 110 85" stroke="#94a3b8" stroke-width="2" fill="none"/>
          <path d="M 290 48 L 390 85" stroke="#94a3b8" stroke-width="2" fill="none"/>

          <!-- Relative -->
          <g class="svg-node" data-title="Relative Erythrocytosis" data-detail="Normal red cell mass. Reduced plasma volume caused by dehydration, diuretics, burns, or Gaisbock syndrome.">
            <rect x="25" y="90" width="170" height="150" rx="8" fill="#f8fafc" stroke="#3b82f6" stroke-width="1.5"/>
            <rect x="25" y="90" width="170" height="26" rx="8" fill="#3b82f6"/>
            <text x="110" y="108" fill="#fff" font-size="10" font-weight="bold" text-anchor="middle">RELATIVE (SPURIOUS)</text>
            <text x="35" y="132" fill="#1e293b" font-size="10" font-weight="600">• True RBC Mass: NORMAL</text>
            <text x="35" y="150" fill="#1e293b" font-size="10" font-weight="600">• Plasma Volume: LOW</text>
            <text x="35" y="175" fill="#64748b" font-size="9">Causes:</text>
            <text x="35" y="190" fill="#64748b" font-size="9">- Severe Dehydration / Cholera</text>
            <text x="35" y="205" fill="#64748b" font-size="9">- Diuretic Overuse / Burns</text>
            <text x="35" y="220" fill="#64748b" font-size="9">- Gaisböck Stress Polycythemia</text>
          </g>

          <!-- Absolute -->
          <g class="svg-node" data-title="Absolute Erythrocytosis" data-detail="True RBC mass elevated >25%. Measure serum EPO to separate Primary (autonomous JAK2) from Secondary (EPO-driven).">
            <rect x="300" y="90" width="180" height="150" rx="8" fill="#f8fafc" stroke="#e11d48" stroke-width="1.5"/>
            <rect x="300" y="90" width="180" height="26" rx="8" fill="#e11d48"/>
            <text x="390" y="108" fill="#fff" font-size="10" font-weight="bold" text-anchor="middle">ABSOLUTE (TRUE MASS ↑)</text>
            <text x="310" y="132" fill="#991b1b" font-size="10" font-weight="700">LOW SERUM EPO:</text>
            <text x="310" y="146" fill="#1e293b" font-size="9">• Polycythemia Vera (JAK2 V617F)</text>
            <text x="310" y="160" fill="#64748b" font-size="8">Panmyelosis, Splenomegaly, Pruritus</text>
            <text x="310" y="185" fill="#047857" font-size="10" font-weight="700">HIGH / NORMAL EPO:</text>
            <text x="310" y="200" fill="#1e293b" font-size="9">• Hypoxia: COPD, Altitude, OSA</text>
            <text x="310" y="214" fill="#1e293b" font-size="9">• Ectopic Tumors: RCC, HCC, Hemangio</text>
          </g>
        </svg>
        `;
      },

      // 5. Viscosity Curve
      diag_viscosity_curve: function() {
        return `
        <svg viewBox="0 0 500 280" class="diagram-svg" xmlns="http://www.w3.org/2000/svg">
          <!-- Graph Axes -->
          <line x1="60" y1="230" x2="450" y2="230" stroke="#94a3b8" stroke-width="2"/>
          <line x1="60" y1="230" x2="60" y2="30" stroke="#94a3b8" stroke-width="2"/>
          
          <text x="250" y="260" fill="#64748b" font-size="11" font-weight="600" text-anchor="middle">Hematocrit (%)</text>
          <text x="20" y="130" fill="#64748b" font-size="11" font-weight="600" transform="rotate(-90 20 130)" text-anchor="middle">Viscosity & O2 Delivery</text>

          <!-- Ticks -->
          <text x="120" y="245" fill="#94a3b8" font-size="9" text-anchor="middle">20%</text>
          <text x="180" y="245" fill="#94a3b8" font-size="9" text-anchor="middle">30%</text>
          <text x="250" y="245" fill="#047857" font-size="10" font-weight="bold" text-anchor="middle">45% (Optimum)</text>
          <text x="320" y="245" fill="#b91c1c" font-size="10" font-weight="bold" text-anchor="middle">55% (Danger)</text>
          <text x="400" y="245" fill="#94a3b8" font-size="9" text-anchor="middle">70%</text>

          <!-- Safe Zone -->
          <rect x="220" y="30" width="60" height="200" fill="rgba(16, 185, 129, 0.08)"/>

          <!-- Exponential Viscosity Curve (Red) -->
          <path d="M 60 215 Q 240 205 320 130 T 430 40" fill="none" stroke="#e11d48" stroke-width="3.5"/>
          <text x="410" y="35" fill="#e11d48" font-size="11" font-weight="bold">Blood Viscosity</text>

          <!-- Oxygen Transport Delivery Curve (Blue bell) -->
          <path d="M 60 210 Q 150 120 250 80 T 430 215" fill="none" stroke="#3b82f6" stroke-width="3" stroke-dasharray="6"/>
          <text x="220" y="70" fill="#3b82f6" font-size="11" font-weight="bold">Net Tissue O2 Transport</text>

          <!-- Hotspots -->
          <g class="svg-node" data-title="Optimal Oxygen Delivery" data-detail="At Hct 40-45%, oxygen carrying capacity and blood flow velocity are optimally balanced for peak tissue oxygen delivery.">
            <circle cx="250" cy="80" r="6" fill="#10b981"/>
          </g>

          <g class="svg-node" data-title="Viscosity Exponential Rise" data-detail="When Hct exceeds 50-55%, non-Newtonian erythrocyte crowding escalates viscosity exponentially, causing vascular stasis and thrombosis.">
            <circle cx="320" cy="130" r="6" fill="#e11d48"/>
          </g>
        </svg>
        `;
      }
    }
  };

  // Auto-init diagrams if on page
  document.addEventListener('DOMContentLoaded', function() {
    const diagElem = document.querySelector('[data-diagram-id]');
    if (diagElem) {
      const dId = diagElem.getAttribute('data-diagram-id');
      window.HemeDiagrams.render(diagElem.id, dId, 'diagram-info-box');
    }
  });
})();
