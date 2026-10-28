// upload.js - Textbook Photo Explainer, OCR Text Editor & 7-Part Output Renderer
(function() {
  window.HemeUpload = {
    selectedFile: null,
    currentResult: null,

    handleFileSelect: function(input) {
      if (!input.files || input.files.length === 0) return;
      const file = input.files[0];

      // File validation: Size (<10MB) and type
      const validTypes = ['image/jpeg', 'image/png', 'image/webp'];
      if (!validTypes.includes(file.type)) {
        alert('Unsupported format. Please upload a clear JPG, PNG, or WEBP image.');
        input.value = '';
        return;
      }
      if (file.size > 10 * 1024 * 1024) {
        alert('File size exceeds the 10 MB maximum limit.');
        input.value = '';
        return;
      }

      this.selectedFile = file;

      // Preview
      const previewImg = document.getElementById('image-preview');
      const previewContainer = document.getElementById('preview-container');
      const reader = new FileReader();
      reader.onload = function(e) {
        if (previewImg) previewImg.src = e.target.result;
        if (previewContainer) previewContainer.style.display = 'block';
      };
      reader.readAsDataURL(file);

      // Trigger automatic extraction
      this.extractFromImage();
    },

    loadPreset: function(presetText) {
      const textEditor = document.getElementById('extracted-text-editor');
      if (textEditor) {
        textEditor.value = presetText;
      }
      const previewContainer = document.getElementById('preview-container');
      if (previewContainer) previewContainer.style.display = 'none';

      HemeApp.showToast('📖 Textbook excerpt loaded into OCR editor!');
      this.processText();
    },

    extractFromImage: function() {
      if (!this.selectedFile) return;

      const formData = new FormData();
      formData.append('image', this.selectedFile);

      const statusElem = document.getElementById('ocr-status');
      if (statusElem) statusElem.textContent = 'Extracting textbook text and running OCR validation...';

      fetch('/api/explain-image', {
        method: 'POST',
        body: formData
      })
      .then(res => res.json())
      .then(data => {
        if (statusElem) statusElem.textContent = '';
        if (data.success) {
          const editor = document.getElementById('extracted-text-editor');
          if (editor) editor.value = data.extracted_text;
          this.currentResult = data.result;
          this.renderResult(data.result);
        } else {
          alert(data.error || 'Failed to process image.');
        }
      })
      .catch(() => {
        if (statusElem) statusElem.textContent = '';
        alert('Error communicating with explainer backend.');
      });
    },

    processText: function() {
      const editor = document.getElementById('extracted-text-editor');
      const text = editor ? editor.value.trim() : '';
      if (!text) {
        alert('Please enter or extract textbook text first.');
        return;
      }

      const statusElem = document.getElementById('ocr-status');
      if (statusElem) statusElem.textContent = 'Generating 7-part medical explanation...';

      fetch('/api/explain-image', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: text })
      })
      .then(res => res.json())
      .then(data => {
        if (statusElem) statusElem.textContent = '';
        if (data.success) {
          this.currentResult = data.result;
          this.renderResult(data.result);
        } else {
          alert(data.error || 'Failed to generate explanation.');
        }
      })
      .catch(() => {
        if (statusElem) statusElem.textContent = '';
        alert('Error processing textbook text.');
      });
    },

    renderResult: function(res) {
      const resultContainer = document.getElementById('explainer-result-container');
      if (!resultContainer) return;

      resultContainer.style.display = 'block';

      // 7 Mandatory Sections (Page 5 of Guide)
      let privacyWarningHtml = '';
      if (res.privacy_warning) {
        privacyWarningHtml = `
          <div class="card" style="border-left:4px solid var(--heme-primary); background:rgba(225,29,72,0.06); margin-bottom:12px;">
            <p style="font-size:12px; color:var(--heme-primary); font-weight:600;">${res.privacy_warning}</p>
          </div>
        `;
      }

      resultContainer.innerHTML = `
        ${privacyWarningHtml}

        <!-- 1. What the page is about -->
        <div class="card" style="margin-bottom:12px; border-top:3px solid var(--heme-primary);">
          <span class="badge badge-ruby" style="margin-bottom:6px;">1. Core Topic</span>
          <h3 style="font-size:16px; margin-bottom:4px;">${res.page_summary}</h3>
          <p style="font-size:13px; color:var(--text-secondary);">${res.simple_explanation}</p>
        </div>

        <!-- 2. Step-by-Step Mechanism -->
        <div class="card" style="margin-bottom:12px;">
          <span class="badge badge-indigo" style="margin-bottom:6px;">2. Step-by-Step Mechanism</span>
          <div style="margin-top:8px;">
            ${res.mechanism_steps.map((st, i) => `
              <div class="mechanism-step">
                <div class="step-num">${i+1}</div>
                <div class="step-content">
                  <p>${st}</p>
                </div>
              </div>
            `).join('')}
          </div>
        </div>

        <!-- 3. Text Flowchart -->
        <div class="card" style="margin-bottom:12px; background:var(--bg-subtle);">
          <span class="badge badge-amber" style="margin-bottom:6px;">3. Conceptual Flowchart</span>
          <pre style="font-family:var(--font-mono); font-size:11px; color:var(--heme-navy); white-space:pre-wrap; margin-top:6px;">${res.text_flowchart}</pre>
        </div>

        <!-- 4. Key Terms -->
        <div class="card" style="margin-bottom:12px;">
          <span class="badge badge-emerald" style="margin-bottom:6px;">4. Key Medical Terms</span>
          <div style="display:flex; flex-direction:column; gap:8px; margin-top:8px;">
            ${res.key_terms.map(t => `
              <div style="font-size:12px;">
                <strong style="color:var(--text-primary);">${t.term}</strong>: 
                <span style="color:var(--text-secondary);">${t.definition}</span>
              </div>
            `).join('')}
          </div>
        </div>

        <!-- 5. Exam Takeaway -->
        <div class="card" style="margin-bottom:12px; background:var(--heme-primary-light); border-color:rgba(225,29,72,0.3);">
          <div style="display:flex; align-items:center; gap:6px; margin-bottom:4px;">
            <span style="font-size:16px;">💡</span>
            <strong style="font-size:13px; color:var(--heme-primary);">5. High-Yield MBBS Exam Pearl</strong>
          </div>
          <p style="font-size:12px; color:var(--text-primary); font-weight:500;">${res.exam_takeaway}</p>
        </div>

        <!-- 6. Recall Questions -->
        <div class="card" style="margin-bottom:12px;">
          <span class="badge badge-indigo" style="margin-bottom:6px;">6. Active Recall Practice</span>
          <div style="display:flex; flex-direction:column; gap:10px; margin-top:8px;">
            ${res.recall_questions.map((rq, idx) => `
              <div style="background:var(--bg-subtle); padding:10px; border-radius:8px; font-size:12px;">
                <div style="font-weight:600; margin-bottom:4px;">Q${idx+1}: ${rq.question}</div>
                <div style="color:var(--accent-emerald); font-weight:500;">✓ Answer: ${rq.answer}</div>
              </div>
            `).join('')}
          </div>
        </div>

        <!-- 7. Uncertainty Notes -->
        <div class="card" style="margin-bottom:16px; border-left:3px solid var(--accent-amber);">
          <span class="badge badge-amber" style="margin-bottom:4px;">7. Optical Confidence & Scope Limits</span>
          <p style="font-size:11px; color:var(--text-muted);">${res.uncertainty_notes}</p>
        </div>

        <!-- Actions: Save to Notes or Delete -->
        <div style="display:flex; gap:10px; margin-top:14px;">
          <button class="btn btn-primary btn-block" onclick="HemeUpload.saveResultToNotes()">
            🔖 Save to Notes
          </button>
          <button class="btn btn-secondary" onclick="HemeUpload.clearResult()">
            🗑️ Delete
          </button>
        </div>
      `;

      resultContainer.scrollIntoView({ behavior: 'smooth' });
    },

    saveResultToNotes: function() {
      if (!this.currentResult) return;
      HemeApp.saveNote(
        'textbook_explainer_' + Date.now(),
        'textbook',
        this.currentResult.page_summary
      );
    },

    clearResult: function() {
      this.currentResult = null;
      this.selectedFile = null;
      const previewContainer = document.getElementById('preview-container');
      const editor = document.getElementById('extracted-text-editor');
      const resultContainer = document.getElementById('explainer-result-container');
      const fileInput = document.getElementById('textbook-file-input');

      if (previewContainer) previewContainer.style.display = 'none';
      if (editor) editor.value = '';
      if (resultContainer) {
        resultContainer.style.display = 'none';
        resultContainer.innerHTML = '';
      }
      if (fileInput) fileInput.value = '';

      HemeApp.showToast('Upload cleared.');
    }
  };
})();
