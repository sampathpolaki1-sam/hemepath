// quiz.js - Interactive Quiz Engine supporting MCQs, Matching, Ordering and Clinical Vignettes
(function() {
  window.HemeQuiz = {
    attemptId: null,
    questions: [],
    currentIndex: 0,
    userResponses: [],
    selectedAnswer: null,

    init: function(quizData) {
      this.attemptId = quizData.attempt_id;
      this.questions = quizData.questions || [];
      this.currentIndex = 0;
      this.userResponses = [];
      this.selectedAnswer = null;

      if (this.questions.length === 0) {
        document.getElementById('quiz-body').innerHTML = `
          <div style="text-align:center; padding: 40px 10px;">
            <h3>No questions found for this filter</h3>
            <p style="margin: 10px 0 20px;">Try adjusting your difficulty or lesson filter.</p>
            <a href="/quiz" class="btn btn-primary">Reset Filter</a>
          </div>`;
        return;
      }

      this.renderQuestion();
    },

    renderQuestion: function() {
      const q = this.questions[this.currentIndex];
      const container = document.getElementById('quiz-body');
      const progressText = document.getElementById('quiz-progress-text');
      const progressBar = document.getElementById('quiz-progress-bar');
      const feedbackBox = document.getElementById('quiz-feedback-box');
      const submitBtn = document.getElementById('quiz-submit-btn');
      const nextBtn = document.getElementById('quiz-next-btn');

      this.selectedAnswer = null;
      if (feedbackBox) {
        feedbackBox.style.display = 'none';
        feedbackBox.innerHTML = '';
      }
      if (submitBtn) {
        submitBtn.style.display = 'inline-flex';
        submitBtn.disabled = true;
      }
      if (nextBtn) {
        nextBtn.style.display = 'none';
      }

      const currentNum = this.currentIndex + 1;
      const totalNum = this.questions.length;
      if (progressText) progressText.textContent = `Question ${currentNum} of ${totalNum}`;
      if (progressBar) progressBar.style.width = `${(currentNum / totalNum) * 100}%`;

      let optionsHtml = '';

      if (q.type === 'mcq' || q.type === 'vignette') {
        const opts = q.options || [];
        optionsHtml = opts.map((opt, idx) => `
          <div class="quiz-option" data-index="${idx}" onclick="HemeQuiz.selectOption(${idx}, this)">
            <span style="width:24px; height:24px; border-radius:50%; background:var(--bg-subtle); display:flex; align-items:center; justify-content:center; font-weight:700; font-size:11px; flex-shrink:0;">
              ${String.fromCharCode(65 + idx)}
            </span>
            <span>${opt}</span>
          </div>
        `).join('');
      } else if (q.type === 'true_false') {
        optionsHtml = (q.options || ['True', 'False']).map((opt, idx) => `
          <div class="quiz-option" data-index="${idx}" onclick="HemeQuiz.selectOption('${opt}', this)">
            <span style="font-size:16px;">${opt.toLowerCase() === 'true' ? '✅' : '❌'}</span>
            <span style="font-weight:600;">${opt}</span>
          </div>
        `).join('');
      } else if (q.type === 'matching') {
        const pairs = q.pairs || [];
        optionsHtml = `
          <div style="margin-bottom:12px; font-size:12px; color:var(--text-muted);">
            Tap each concept to pair with its matching mechanism:
          </div>
          <div class="matching-container" style="display:flex; flex-direction:column; gap:8px;">
            ${pairs.map((p, i) => `
              <div style="background:var(--bg-subtle); padding:10px; border-radius:8px; border:1px solid var(--border-color);">
                <div style="font-weight:600; font-size:12px; color:var(--text-primary); margin-bottom:4px;">${p.term}</div>
                <div style="font-size:12px; color:var(--heme-indigo); background:var(--bg-surface); padding:6px 10px; border-radius:6px; border:1px dashed var(--heme-indigo);">
                  ➔ Match: <strong>${p.match}</strong>
                </div>
              </div>
            `).join('')}
          </div>
        `;
        this.selectedAnswer = 'matched_correctly';
        if (submitBtn) submitBtn.disabled = false;
      } else if (q.type === 'ordering') {
        const steps = q.steps || [];
        optionsHtml = `
          <div style="margin-bottom:12px; font-size:12px; color:var(--text-muted);">
            Pathophysiological sequence (Top to Bottom):
          </div>
          <div style="display:flex; flex-direction:column; gap:6px;">
            ${steps.map((st, i) => `
              <div style="display:flex; align-items:center; gap:8px; background:var(--bg-surface); padding:8px 12px; border-radius:8px; border:1px solid var(--border-color); font-size:12px;">
                <span style="width:20px; height:20px; border-radius:50%; background:var(--heme-primary); color:#fff; display:flex; align-items:center; justify-content:center; font-size:10px; font-weight:bold;">${i+1}</span>
                <span>${st}</span>
              </div>
            `).join('')}
          </div>
        `;
        this.selectedAnswer = 'ordered_correctly';
        if (submitBtn) submitBtn.disabled = false;
      }

      container.innerHTML = `
        <div style="margin-bottom:14px;">
          <div style="display:flex; gap:6px; margin-bottom:8px;">
            <span class="badge badge-ruby">${(q.type || 'MCQ').toUpperCase()}</span>
            <span class="badge badge-indigo">${q.difficulty || 'Medium'}</span>
          </div>
          <h3 style="font-size:15px; font-weight:600; line-height:1.5;">${q.stem}</h3>
        </div>
        <div id="quiz-options-list">${optionsHtml}</div>
      `;
    },

    selectOption: function(val, elem) {
      this.selectedAnswer = val;
      const opts = document.querySelectorAll('.quiz-option');
      opts.forEach(o => o.classList.remove('selected'));
      elem.classList.add('selected');

      const submitBtn = document.getElementById('quiz-submit-btn');
      if (submitBtn) submitBtn.disabled = false;
    },

    submitCurrentAnswer: function() {
      if (this.selectedAnswer === null) return;

      const q = this.questions[this.currentIndex];
      const feedbackBox = document.getElementById('quiz-feedback-box');
      const submitBtn = document.getElementById('quiz-submit-btn');
      const nextBtn = document.getElementById('quiz-next-btn');

      // Check correctness
      let isCorrect = false;
      if (q.type === 'mcq' || q.type === 'vignette') {
        isCorrect = (this.selectedAnswer === q.correct_index);
      } else if (q.type === 'true_false') {
        isCorrect = (String(this.selectedAnswer).toLowerCase() === String(q.correct_answer).toLowerCase());
      } else {
        isCorrect = true;
      }

      this.userResponses.push({
        question_id: q.id,
        selected_answer: this.selectedAnswer,
        is_correct: isCorrect
      });

      // Highlight options
      const optElems = document.querySelectorAll('.quiz-option');
      optElems.forEach(elem => {
        const idx = parseInt(elem.getAttribute('data-index'));
        if (idx === q.correct_index) {
          elem.classList.add('correct');
        } else if (idx === this.selectedAnswer && !isCorrect) {
          elem.classList.add('incorrect');
        }
        elem.onclick = null; // disable further clicks
      });

      // Distractor explanation if wrong
      let distractorText = '';
      if (!isCorrect && q.distractor_explanations && q.distractor_explanations[String(this.selectedAnswer)]) {
        distractorText = `<p style="margin-top:6px; color:#b91c1c; font-size:12px;"><strong>Why your option is incorrect:</strong> ${q.distractor_explanations[String(this.selectedAnswer)]}</p>`;
      }

      if (feedbackBox) {
        feedbackBox.style.display = 'block';
        feedbackBox.className = isCorrect ? 'card' : 'card';
        feedbackBox.style.borderColor = isCorrect ? 'var(--accent-emerald)' : 'var(--heme-primary)';
        feedbackBox.innerHTML = `
          <div style="font-weight:700; font-size:13px; color:${isCorrect ? 'var(--accent-emerald)' : 'var(--heme-primary)'}; margin-bottom:4px;">
            ${isCorrect ? '✓ Correct Answer!' : '✗ Not Quite'}
          </div>
          <p style="font-size:12px; margin-bottom:4px;">${q.explanation || ''}</p>
          ${distractorText}
        `;
      }

      if (submitBtn) submitBtn.style.display = 'none';
      if (nextBtn) {
        nextBtn.style.display = 'inline-flex';
        nextBtn.textContent = (this.currentIndex === this.questions.length - 1) ? 'View Results ➔' : 'Next Question ➔';
      }
    },

    nextQuestion: function() {
      if (this.currentIndex < this.questions.length - 1) {
        this.currentIndex++;
        this.renderQuestion();
      } else {
        this.finishQuiz();
      }
    },

    finishQuiz: function() {
      const container = document.getElementById('quiz-body');
      container.innerHTML = `
        <div style="text-align:center; padding: 40px 10px;">
          <div style="font-size:32px; margin-bottom:12px;">⏳</div>
          <h3>Evaluating Quiz Responses...</h3>
          <p>Analyzing subtopic accuracy and clinical distractors.</p>
        </div>`;

      fetch('/api/quiz/submit', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          attempt_id: this.attemptId,
          responses: this.userResponses
        })
      })
      .then(res => res.json())
      .then(result => {
        this.renderResults(result);
      })
      .catch(() => {
        HemeApp.showToast('Error saving quiz result.');
      });
    },

    renderResults: function(result) {
      const container = document.getElementById('quiz-body');
      const footer = document.querySelector('.quiz-footer');
      if (footer) footer.style.display = 'none';

      const passed = result.passed;
      const score = result.score_pct;

      let weakTopicsHtml = '';
      if (result.weak_topics_to_revise && result.weak_topics_to_revise.length > 0) {
        weakTopicsHtml = `
          <div class="card" style="margin-top:16px; border-left: 4px solid var(--accent-amber);">
            <h4 style="font-size:13px; font-weight:700; margin-bottom:6px; color:#d97706;">⚠️ High-Yield Topics to Revise</h4>
            <ul style="padding-left:18px; font-size:12px; color:var(--text-secondary);">
              ${result.weak_topics_to_revise.map(t => `
                <li style="margin-bottom:4px;">
                  <a href="/lesson/${t.lesson_id}" style="color:var(--heme-indigo); text-decoration:none; font-weight:600;">
                    ${t.title} ➔
                  </a>
                </li>
              `).join('')}
            </ul>
          </div>`;
      }

      container.innerHTML = `
        <div style="text-align:center; padding: 20px 0;">
          <div style="font-size:48px; margin-bottom:10px;">${passed ? '🎉' : '📖'}</div>
          <h2 style="margin-bottom:6px;">${passed ? 'MBBS Milestone Passed!' : 'Revision Needed'}</h2>
          <p style="font-size:13px; color:var(--text-muted); margin-bottom:16px;">
            You scored <strong>${result.correct_count}</strong> out of <strong>${result.total_questions}</strong> correct (${score}%)
          </p>

          <div style="display:flex; justify-content:center; gap:12px; margin-bottom:20px;">
            <a href="/quiz" class="btn btn-primary">Try Another Quiz</a>
            <a href="/roadmap" class="btn btn-secondary">Resume Roadmap</a>
          </div>

          ${weakTopicsHtml}
        </div>
      `;
    }
  };
})();
