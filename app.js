/**
 * =========================================================================
 * VOCAB FLOW - CORE APPLICATION LOGIC (ES6+ Module Pattern)
 * =========================================================================
 */

// --- UTILITIES ---
const $ = id => document.getElementById(id);
const toast = (msg) => {
    const el = $('toast');
    el.textContent = msg;
    el.classList.add('show');
    setTimeout(() => el.classList.remove('show'), 2000);
};
const escapeHtml = (unsafe) => {
    return (unsafe || '').toString()
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
};

// --- DYNAMIC DATA ---
let GLOBAL_TOPICS = [];
let GLOBAL_TOEIC_DATA = {};
let EXTERNAL_VOCAB = [];
const REVIEW_LABELS = { all: 'Mixed practice', vocabulary: 'Vocabulary', grammar: 'Grammar', tenses: 'Common tenses', prepositions: 'Prepositions', comparisons: 'Comparisons', cloze: 'Fill in the blank', reading: 'Reading (Part 6/7)' };

async function fetchAppData() {
    try {
        const [appRes, vocabRes, examRes] = await Promise.all([
            fetch('data.json'),
            fetch('toeic_vocab.json'), // Mocking external reliable source
            fetch('toeic_exams.json')  // Large TOEIC dataset
        ]);
        const appData = await appRes.json();
        GLOBAL_TOPICS = appData.topics || [];
        GLOBAL_TOEIC_DATA = await examRes.json();
        EXTERNAL_VOCAB = await vocabRes.json();
    } catch (e) {
        console.error("Failed to load application data", e);
        toast("Lỗi tải dữ liệu. Ứng dụng có thể không hoạt động đúng.");
    }
}

/**
 * 1. STORAGE & STREAK MANAGER
 */
class StorageManager {
    constructor() {
        this.personalWords = [];
        this.stats = { learned: 0, reviews: 0 };
        this.streak = 1;
        this.lastLogin = Date.now();
        this.wordProgress = {};
        this.loadData();
        this.updateStreak();
    }

    loadData() {
        try {
            this.personalWords = JSON.parse(localStorage.getItem('vf-personal') || '[]');
        } catch (e) {
            console.error("LocalStorage data corrupted. Resetting personal words.", e);
            this.personalWords = [];
        }
        this.stats.learned = Number(localStorage.getItem('vf-learned') || 0);
        this.stats.reviews = Number(localStorage.getItem('vf-reviews') || 0);
        this.streak = Number(localStorage.getItem('vf-streak') || 1);
        this.lastLogin = Number(localStorage.getItem('vf-last-login') || Date.now());
        this.weakQuestions = JSON.parse(localStorage.getItem('vf-weak-questions') || '[]');
        this.wordProgress = JSON.parse(localStorage.getItem('vf-word-progress') || '{}');
    }

    saveData() {
        localStorage.setItem('vf-personal', JSON.stringify(this.personalWords));
        localStorage.setItem('vf-learned', this.stats.learned);
        localStorage.setItem('vf-reviews', this.stats.reviews);
        localStorage.setItem('vf-streak', this.streak);
        localStorage.setItem('vf-last-login', Date.now());
        localStorage.setItem('vf-weak-questions', JSON.stringify(this.weakQuestions));
        localStorage.setItem('vf-word-progress', JSON.stringify(this.wordProgress));
    }

    importVocabulary(jsonArray) {
        if (!Array.isArray(jsonArray)) return false;
        let added = 0;
        jsonArray.forEach(w => {
            if (w.word && w.meaning && !this.personalWords.some(p => p.word === w.word)) {
                this.personalWords.unshift({
                    word: w.word,
                    meaning: w.meaning,
                    example: w.example || '',
                    phonetic: w.phonetic || '',
                    topic: w.topic || 'Imported',
                    nextReview: 0
                });
                added++;
            }
        });
        if (added > 0) this.saveData();
        return added;
    }

    updateStreak() {
        const now = Date.now();
        const diffDays = (now - this.lastLogin) / (1000 * 60 * 60 * 24);

        if (diffDays >= 1 && diffDays < 2) {
            this.streak++;
        } else if (diffDays >= 2) {
            this.streak = 1;
        }
        this.lastLogin = now;
        this.saveData();
    }

    getAllWords() {
        let allBuiltIn = [];
        GLOBAL_TOPICS.forEach(t => {
            if (t.words) allBuiltIn = allBuiltIn.concat(t.words);
        });
        return [...allBuiltIn, ...this.personalWords];
    }

    getDueWords() {
        const now = Date.now();
        return this.getAllWords().filter(w => !w.nextReview || w.nextReview <= now);
    }
}

/**
 * 2. AUTH GUARD (Route Protection)
 */
class AuthGuard {
    static checkAuth() {
        const userStr = localStorage.getItem('vf-user');
        if (!userStr) {
            window.location.href = 'register.html';
            return null;
        }
        try {
            return JSON.parse(userStr);
        } catch {
            window.location.href = 'register.html';
            return null;
        }
    }
}

/**
 * 3. ROUTER & UI STATE
 */
class Router {
    constructor(app) {
        this.app = app;
        this.init();
    }

    init() {
        document.querySelectorAll('nav .nav-item').forEach(item => {
            item.addEventListener('click', (e) => {
                e.preventDefault();
                this.navigate(item.dataset.page);
            });
        });
    }

    navigate(pageId, data = null) {
        document.querySelectorAll('.page-content').forEach(el => el.classList.remove('active'));
        document.querySelectorAll('nav .nav-item').forEach(el => el.classList.remove('active'));

        const targetSection = $(pageId);
        const targetNav = document.querySelector(`nav .nav-item[data-page="${pageId}"]`);

        if (targetSection) targetSection.classList.add('active');
        if (targetNav) targetNav.classList.add('active');

        // Dispatch page lifecycle events
        if (pageId === 'home') this.app.renderHome();
        if (pageId === 'vocabulary') this.app.renderMyWords();
        if (pageId === 'progress') this.app.renderProgress();
        if (pageId === 'learn') this.app.flashcardApp.initSession(data);
        if (pageId === 'review') {
            this.app.quizApp.initSession();
        } else {
            this.app.quizApp.stopTimer(); // Stop exam timer if navigating away
        }
    }
}

/**
 * 4. FLASHCARD & SPACED REPETITION (Learn)
 */
class FlashcardApp {
    constructor(storage) {
        this.storage = storage;
        this.dueWords = [];
        this.currentIndex = 0;
        this.currentWord = null;
        this.currentTopicId = null;
    }

    initSession(topicId) {
        this.currentTopicId = topicId || this.currentTopicId || 'business';

        let topicWords = [];
        if (this.currentTopicId === 'personal') {
            topicWords = this.storage.personalWords;
        } else {
            const topic = GLOBAL_TOPICS.find(t => t.id === this.currentTopicId);
            if (topic && topic.words) topicWords = topic.words;
            else topicWords = this.storage.getAllWords();
        }

        const now = Date.now();
        let unseen = [];
        let learning = [];
        let masteredDue = [];

        topicWords.forEach(w => {
            const progress = this.storage.wordProgress[w.word] || { state: 'unseen', nextReview: 0, streak: 0 };

            if (progress.state === 'unseen') unseen.push(w);
            else if (progress.state === 'learning') learning.push(w);
            else if (progress.state === 'mastered' && progress.nextReview <= now) masteredDue.push(w);
        });

        // Smart Logic: prioritize Unseen & Learning over Mastered
        this.dueWords = [...learning, ...unseen, ...masteredDue];

        this.currentIndex = 0;
        if (this.dueWords.length === 0) {
            this.dueWords = topicWords; // fallback if no due words but user clicked
        }

        // Take a batch for the current session (max 30)
        this.dueWords = this.dueWords.slice(0, 30).sort(() => Math.random() - 0.5);
        this.renderCard();
    }

    renderCard() {
        const cardEl = $('flashcard-el');
        if (!cardEl) return;
        cardEl.classList.remove('flipped');

        // Ngăn chặn "Bóng ma" (xoá trắng data cũ trước khi flip)
        if ($('word')) $('word').innerText = "";
        if ($('phonetic')) $('phonetic').innerText = "";
        if ($('options')) $('options').innerHTML = "";
        if ($('meaning')) $('meaning').innerText = "";
        if ($('example')) $('example').innerText = "";
        if ($('exampleVi')) $('exampleVi').innerText = "";
        if ($('wordImage')) {
            $('wordImage').removeAttribute('src');
            $('wordImage').style.display = 'none';
        }

        if (this.dueWords.length === 0) {
            $('word').textContent = 'Oops';
            $('meaning').textContent = 'Chưa có từ vựng nào!';
            return;
        }

        if (this.currentIndex >= this.dueWords.length) this.currentIndex = 0;
        this.currentWord = this.dueWords[this.currentIndex];

        // Cập nhật mặt trước ngay lập tức
        $('word').textContent = this.currentWord.word;
        $('phonetic').textContent = this.currentWord.phonetic || '';
        $('modeLabel').textContent = `Learn • ${this.currentWord.topic || 'Personal'}`;
        $('studyCount').textContent = `${this.currentIndex + 1} / ${this.dueWords.length}`;
        if ($('bar')) $('bar').style.width = `${((this.currentIndex + 1) / this.dueWords.length) * 100}%`;
        
        this.generateQuizOptions(); // Render nút Quiz ở mặt trước ngay lập tức

        // Cập nhật mặt sau (không bị block bởi API ảnh)
        $('meaning').textContent = `Nghĩa: ${this.currentWord.meaning}`;
        $('example').textContent = this.currentWord.example || 'Thêm ví dụ để nhớ lâu hơn.';
        const exampleVi = $('exampleVi');
        if (exampleVi) {
            exampleVi.textContent = this.currentWord.example_vi || '';
            exampleVi.style.display = this.currentWord.example_vi ? 'block' : 'none';
        }

        const wordImg = $('wordImage');
        if (wordImg) {
            wordImg.removeAttribute('src');
            wordImg.classList.remove('loaded');
            wordImg.style.display = 'none';

            let finalImageUrl = this.currentWord.image_url;

            // Xử lý fetch ảnh background
            (async () => {
                if (!finalImageUrl || finalImageUrl.includes('placehold.co')) {
                    finalImageUrl = await ApiManager.fetchImageForWord(this.currentWord.word);
                    this.currentWord.image_url = finalImageUrl;
                }

                if (finalImageUrl) {
                    wordImg.style.display = 'block';
                    wordImg.onload = () => {
                        wordImg.classList.add('loaded');
                    };
                    wordImg.src = finalImageUrl;
                }
            })();
        }
    }


    generateQuizOptions() {
        const all = this.storage.getAllWords();
        const distractors = all
            .filter(w => w.meaning !== this.currentWord.meaning)
            .sort(() => Math.random() - 0.5)
            .slice(0, 3)
            .map(w => w.meaning);

        const choices = [this.currentWord.meaning, ...distractors].sort(() => Math.random() - 0.5);

        const optionsEl = $('options');
        optionsEl.innerHTML = choices.map(c =>
            `<div class="quiz-option" data-answer="${escapeHtml(c)}" onclick="App.flashcardApp.answerQuiz(event, this, this.dataset.answer)">${escapeHtml(c)}</div>`
        ).join('');

        $('learnPrompt').classList.remove('hide');
        optionsEl.classList.remove('hide');
        $('rating').classList.add('hide');
    }

    answerQuiz(event, btn, selected) {
        if (event) event.stopPropagation();
        
        const optionsEl = $('options');
        [...optionsEl.children].forEach(b => b.style.pointerEvents = 'none');

        const isCorrect = selected === this.currentWord.meaning;
        btn.classList.add(isCorrect ? 'correct' : 'wrong');

        if (!isCorrect) {
            [...optionsEl.children].forEach(child => {
                if (child.dataset.answer === this.currentWord.meaning) child.classList.add('correct');
            });
        }

        setTimeout(() => {
            $('flashcard-el').classList.add('flipped');
            $('rating').classList.remove('hide');
        }, 600);
    }

    processSrsRating(daysMultiplier) {
        const wordStr = this.currentWord.word;
        const progress = this.storage.wordProgress[wordStr] || { state: 'unseen', nextReview: 0, streak: 0 };

        if (daysMultiplier === 1 || daysMultiplier === 2) { // Again or Hard
            progress.state = 'learning';
            progress.streak = 0;
            progress.nextReview = Date.now() + (10 * 60 * 1000); // 10 mins
        } else { // Good
            progress.streak++;
            if (progress.streak >= 2) {
                progress.state = 'mastered';
                const days = progress.streak === 2 ? 1 : (progress.streak === 3 ? 3 : 7);
                progress.nextReview = Date.now() + (days * 24 * 60 * 60 * 1000);
            } else {
                progress.state = 'learning';
                progress.nextReview = Date.now() + (12 * 60 * 60 * 1000); // 12 hours
            }
        }

        this.storage.wordProgress[wordStr] = progress;

        this.storage.stats.reviews++;
        if (progress.state === 'mastered' && progress.streak === 2) {
            this.storage.stats.learned++;
        }

        this.storage.saveData();
        this.currentIndex++;

        toast(daysMultiplier >= 4 ? `Tuyệt vời! Đã ghi nhớ.` : `Đã ghi nhận, sẽ ôn lại sớm.`);
        this.renderCard();
        App.renderHome();
    }
}

/**
 * 5. TOEIC QUIZ MANAGER (Review)
 */
class QuizApp {
    constructor(storage) {
        this.storage = storage;
        this.pool = [];
        this.currentIndex = 0;
        this.currentQuestion = null;
        this.isExamMode = false;
        this.timer = null;
        this.timeLeft = 0;
        this.examResults = [];
        this.userAnswers = [];

        this.bindEvents();
    }

    bindEvents() {
        const select = $('reviewType');
        if (select) select.addEventListener('change', () => this.initSession());

        const modeToggle = $('examModeToggle');
        if (modeToggle) modeToggle.addEventListener('change', (e) => {
            this.isExamMode = e.target.checked;
            this.initSession();
        });
    }

    generateVocabQuestions(count = 10) {
        const allVocab = [...EXTERNAL_VOCAB, ...this.storage.personalWords];
        if (allVocab.length < 4) return [];

        let questions = [];
        // Shuffle vocab
        const shuffled = [...allVocab].sort(() => Math.random() - 0.5);
        const toGenerate = Math.min(count, shuffled.length);

        for (let i = 0; i < toGenerate; i++) {
            const target = shuffled[i];
            const distractors = allVocab
                .filter(w => w.meaning !== target.meaning)
                .sort(() => Math.random() - 0.5)
                .slice(0, 3)
                .map(w => w.meaning);

            const options = [target.meaning, ...distractors].sort(() => Math.random() - 0.5);
            const correctIndex = options.indexOf(target.meaning);

            questions.push({
                type: 'vocabulary',
                q: `What is the meaning of "${target.word}"?`,
                a: options,
                correct: correctIndex,
                why: `The word "${target.word}" means "${target.meaning}".`,
                whyVi: `Từ "${target.word}" có nghĩa là "${target.meaning}".`
            });
        }
        return questions;
    }

    initSession() {
        this.stopTimer();
        this.hideBottomSheet();
        $('reportBoard').classList.add('hide');
        $('quizArea').classList.remove('hide');

        const type = $('reviewType').value;
        let combinedPool = [];

        if (type === 'all') {
            Object.values(GLOBAL_TOEIC_DATA).forEach(arr => {
                if (Array.isArray(arr)) combinedPool = combinedPool.concat(arr);
            });
            combinedPool = combinedPool.concat(this.generateVocabQuestions(5));
        } else if (type === 'vocabulary') {
            combinedPool = this.generateVocabQuestions(15);
        } else {
            combinedPool = GLOBAL_TOEIC_DATA[type] || [];
        }

        this.pool = [...combinedPool].sort(() => Math.random() - 0.5);
        this.currentIndex = 0;
        this.examResults = [];
        this.userAnswers = new Array(this.pool.length).fill(null);

        if (this.pool.length === 0) {
            $('examTimerContainer').classList.add('hide');
        } else if (this.isExamMode) {
            $('examTimerContainer').classList.remove('hide');
            this.timeLeft = this.pool.length * 60; // 1 minute per question
            this.startTimer();
        } else {
            $('examTimerContainer').classList.add('hide');
        }

        this.renderQuestion();
    }

    startTimer() {
        this.updateTimerDisplay();
        this.timer = setInterval(() => {
            if (this.timeLeft > 0) {
                this.timeLeft--;
            }
            this.updateTimerDisplay();
            if (this.timeLeft <= 0) {
                this.stopTimer();
                this.submitExam();
            }
        }, 1000);
    }

    stopTimer() {
        if (this.timer) clearInterval(this.timer);
    }

    updateTimerDisplay() {
        const mins = Math.floor(this.timeLeft / 60).toString().padStart(2, '0');
        const secs = (this.timeLeft % 60).toString().padStart(2, '0');
        $('examTimer').textContent = `${mins}:${secs}`;
    }

    renderQuestion() {
        this.hideBottomSheet();
        if (this.pool.length === 0) {
            $('quizArea').innerHTML = '<div style="padding:24px; text-align:center;">Chưa có dữ liệu cho phần này.</div>';
            return;
        }
        if (this.currentIndex >= this.pool.length) {
            if (this.isExamMode) this.submitExam();
            else this.initSession();
            return;
        }

        this.currentQuestion = this.pool[this.currentIndex];

        const type = $('reviewType').value;
        $('reviewCategory').textContent = REVIEW_LABELS[type] || REVIEW_LABELS.all;
        $('reviewCount').textContent = `Question ${this.currentIndex + 1} / ${this.pool.length}`;

        const quizArea = $('quizArea');

        if (this.currentQuestion.type === 'reading') {
            // Split layout for reading
            quizArea.innerHTML = `
                <div class="reading-split-layout">
                    <div class="reading-passage">
                        ${escapeHtml(this.currentQuestion.passageText).replace(/\\n/g, '<br>')}
                    </div>
                    <div class="reading-questions">
                        <div class="quiz-question">${escapeHtml(this.currentQuestion.questions[0].q)}</div>
                        <div class="quiz-options">
                            ${this.currentQuestion.questions[0].a.map((ans, idx) =>
                `<div class="quiz-option" onclick="App.quizApp.answerQuestion(this, ${idx}, true)">${escapeHtml(ans)}</div>`
            ).join('')}
                        </div>
                    </div>
                </div>
            `;
            // Simplified handling for reading: assuming 1 question rendered at a time for simplicity, 
            // but saving sub-question context. We extract the first question for now to fit the architecture.
            this.currentQuestion.correct = this.currentQuestion.questions[0].correct;
            this.currentQuestion.why = this.currentQuestion.questions[0].why;
            this.currentQuestion.whyVi = this.currentQuestion.questions[0].whyVi;
        } else {
            // Standard layout
            quizArea.innerHTML = `
                <div class="quiz-card">
                    <div class="quiz-question">${escapeHtml(this.currentQuestion.q)}</div>
                    <div class="quiz-options">
                        ${this.currentQuestion.a.map((ans, idx) =>
                `<div class="quiz-option" onclick="App.quizApp.answerQuestion(this, ${idx}, false)">${escapeHtml(ans)}</div>`
            ).join('')}
                    </div>
                </div>
            `;
        }

        $('nextQuestion').classList.remove('hide');

        if (this.isExamMode) {
            if (this.currentIndex === 0) {
                $('prevQuestion').classList.add('hide');
            } else {
                $('prevQuestion').classList.remove('hide');
            }
            $('nextQuestion').querySelector('.btn-text').textContent = (this.currentIndex === this.pool.length - 1) ? 'Nộp bài' : 'Câu tiếp theo';

            if (this.userAnswers[this.currentIndex] !== null) {
                const selectedIdx = this.userAnswers[this.currentIndex];
                const optionsEl = $('quizArea').querySelector('.quiz-options');
                if (optionsEl && optionsEl.children[selectedIdx]) {
                    optionsEl.children[selectedIdx].classList.add('selected');
                }
            }
        } else {
            const prevBtn = document.getElementById('prevQuestion');
            if (prevBtn) prevBtn.classList.add('hide');
            $('nextQuestion').classList.add('hide');
            $('nextQuestion').querySelector('.btn-text').textContent = 'Câu tiếp theo';
        }
    }

    answerQuestion(btn, idx, isReading) {
        const optionsEl = btn.parentElement;

        if (this.isExamMode) {
            [...optionsEl.children].forEach(b => {
                b.classList.remove('selected');
            });
            btn.classList.add('selected');
            this.userAnswers[this.currentIndex] = idx;
        } else {
            [...optionsEl.children].forEach(b => {
                b.style.pointerEvents = 'none';
                b.classList.remove('selected');
            });

            const isCorrect = idx === this.currentQuestion.correct;
            btn.classList.add(isCorrect ? 'correct' : 'wrong');
            if (!isCorrect) {
                optionsEl.children[this.currentQuestion.correct].classList.add('correct');
            }
            this.showBottomSheet(isCorrect);
            $('nextQuestion').classList.remove('hide');

            this.storage.stats.reviews++;
            this.storage.saveData();
        }
    }

    prevAction() {
        if (this.isExamMode && this.currentIndex > 0) {
            this.currentIndex--;
            this.renderQuestion();
        }
    }

    nextAction() {
        if (this.isExamMode && this.currentIndex === this.pool.length - 1) {
            this.submitExam();
            return;
        }
        this.currentIndex++;
        this.renderQuestion();
    }

    submitExam() {
        this.stopTimer();
        $('quizArea').classList.add('hide');
        $('nextQuestion').classList.add('hide');
        const prevBtn = document.getElementById('prevQuestion');
        if (prevBtn) prevBtn.classList.add('hide');
        $('reportBoard').classList.remove('hide');
        $('mistakesArea').classList.add('hide');
        $('mistakesArea').innerHTML = '';

        this.examResults = [];
        let correctCount = 0;

        this.pool.forEach((q, i) => {
            const chosenIdx = this.userAnswers[i];
            const isCorrect = chosenIdx === q.correct;
            this.examResults.push({ q, isCorrect, chosenIdx });
            if (isCorrect) {
                correctCount++;
            } else {
                if (!this.storage.weakQuestions.some(wq => wq.q === q.q)) {
                    this.storage.weakQuestions.push(q);
                }
            }
        });
        this.storage.saveData();

        const total = this.pool.length;
        const percentage = total > 0 ? Math.round((correctCount / total) * 100) : 0;

        $('reportScore').textContent = `${correctCount} / ${total}`;
        $('reportPercent').textContent = `${percentage}%`;

        const timeUsed = (total * 60) - this.timeLeft;
        const mins = Math.floor(timeUsed / 60);
        const secs = timeUsed % 60;
        $('reportTime').textContent = `${mins}m ${secs}s`;
    }

    renderMistakes() {
        try {
            const mistakesArea = $('mistakesArea');
            mistakesArea.classList.remove('hide');

            const mistakes = this.examResults.filter(r => !r.isCorrect);

            if (mistakes.length === 0) {
                mistakesArea.innerHTML = '<div style="text-align:center; padding: 24px; color: var(--success); font-weight: bold;">Hoàn hảo! Bạn không sai câu nào.</div>';
                return;
            }

            mistakesArea.innerHTML = mistakes.map((m, index) => {
                const q = m.q || {};

                let passageHtml = '';
                if (q.type === 'reading') {
                    passageHtml = `<div class="reading-passage" style="margin-bottom: 12px; max-height: 150px;">${escapeHtml(q.passageText).replace(/\\n/g, '<br>')}</div>`;
                }

                let optionsHtml = (q.a || []).map((ans, idx) => {
                    let classNames = 'quiz-option';
                    let icon = '';
                    if (idx === q.correct) {
                        classNames += ' correct';
                        icon = '<span style="float:right;">✅</span>';
                    } else if (idx === m.chosenIdx) {
                        classNames += ' wrong';
                        icon = '<span style="float:right;">❌</span>';
                    }
                    return `<div class="${classNames}" style="pointer-events: none; margin-bottom: 8px;">${escapeHtml(ans)} ${icon}</div>`;
                }).join('');

                return `
                    <div class="quiz-card" style="margin-bottom: 0;">
                        <div style="font-weight: bold; color: var(--text-muted); margin-bottom: 8px;">Câu hỏi sai #${index + 1}</div>
                        ${passageHtml}
                        <div class="quiz-question">${escapeHtml(q.q || 'Câu hỏi trống')}</div>
                        <div class="quiz-options">
                            ${optionsHtml}
                        </div>
                        <div style="margin-top: 16px; padding: 12px; background: var(--bg-color); border-left: 4px solid var(--primary); border-radius: 4px; font-size: 14px;">
                            <strong>Giải thích:</strong> ${escapeHtml(q.whyVi || q.why || 'Không có giải thích chi tiết.')}
                        </div>
                    </div>
                `;
            }).join('');
            mistakesArea.scrollIntoView({ behavior: 'smooth' });
        } catch (e) {
            console.error("renderMistakes Error: ", e);
            toast("Lỗi hiển thị chi tiết: " + e.message);
        }
    }

    showBottomSheet(isCorrect) {
        if (this.isExamMode) return; // Never show in exam mode
        $('sheet-status').textContent = isCorrect ? 'Chính xác!' : 'Chưa đúng!';
        $('sheet-status').className = 'exp-status ' + (isCorrect ? 'success' : 'error');
        $('sheet-en').textContent = this.currentQuestion.why;
        $('sheet-vi').textContent = this.currentQuestion.whyVi;

        document.querySelector('.bottom-sheet-overlay').classList.add('active');
        document.querySelector('.bottom-sheet').classList.add('active');
    }

    hideBottomSheet() {
        const sheet = document.querySelector('.bottom-sheet');
        const overlay = document.querySelector('.bottom-sheet-overlay');
        if (sheet) sheet.classList.remove('active');
        if (overlay) overlay.classList.remove('active');
    }
}

/**
 * 6. API MANAGER (My Words)
 */
class ApiManager {
    static async translate(word) {
        try {
            const res = await fetch(`https://api.mymemory.translated.net/get?q=${encodeURIComponent(word)}&langpair=en|vi`);
            const data = await res.json();
            return data.responseData?.translatedText || null;
        } catch (e) {
            console.error('Translation error', e);
            return null;
        }
    }

    static async fetchImageForWord(word) {
        const PEXELS_API_KEY = "";

        try {
            if (PEXELS_API_KEY) {
                const pexelsRes = await fetch(`https://api.pexels.com/v1/search?query=${word}&per_page=1`, {
                    headers: { Authorization: PEXELS_API_KEY }
                });
                const pexelsData = await pexelsRes.json();
                if (pexelsData.photos && pexelsData.photos.length > 0) {
                    console.log(`✅ [SUCCESS] Đã tải ảnh thành công cho từ: ${word} - Nguồn: Pexels API`);
                    return pexelsData.photos[0].src.medium;
                }
            }
            throw new Error("Pexels failed or empty");
        } catch (error) {
            console.error("❌ [ERROR] Lỗi fetch ảnh từ Pexels: ", error);
            console.warn(`⚠️ [NO IMAGE] Không tìm thấy ảnh cho từ: ${word}`);
            // Không dùng placeholder nữa, trả về rỗng
            return "";
        }
    }

    static async checkGrammar(sentence) {
        const API_KEY = "YOUR_GEMINI_API_KEY";
        try {
            const url = `https://generativelanguage.googleapis.com/v1beta/models/gemini-3.6-flash:generateContent?key=${API_KEY}`;

            const prompt = `Bạn là giáo viên tiếng Anh. Hãy sửa lỗi ngữ pháp hoặc viết lại câu sau cho tự nhiên hơn. Giải thích ngắn gọn bằng tiếng Việt lý do sửa. Bắt buộc trả về đúng định dạng JSON (không có markdown block): { "suggested_sentence": "...", "explanation": "..." }. Câu cần sửa: "${sentence}"`;

            const res = await fetch(url, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    contents: [{ parts: [{ text: prompt }] }]
                })
            });
            const data = await res.json();

            if (data.error) throw new Error(data.error.message);
            if (!data.candidates || data.candidates.length === 0) throw new Error("No response from AI");

            const textResponse = data.candidates[0].content.parts[0].text;

            // Xử lý text thừa (markdown backticks) trước khi parse
            const jsonStr = textResponse.replace(/```json/g, '').replace(/```/g, '').trim();
            const result = JSON.parse(jsonStr);

            return result;
        } catch (e) {
            console.error('Grammar check error:', e);
            throw e;
        }
    }
}

/**
 * MAIN APPLICATION BOOTSTRAP
 */
class VocabFlowApplication {
    constructor() {
        this.user = AuthGuard.checkAuth();
        if (!this.user) return; // Stop init if redirecting

        this.initAsync();
    }

    async initAsync() {
        await fetchAppData();
        this.storage = new StorageManager();
        this.flashcardApp = new FlashcardApp(this.storage);
        this.quizApp = new QuizApp(this.storage);
        this.router = new Router(this);

        this.bindGlobalEvents();
        this.renderHome(); // Initial render

        // Expose global methods required by inline HTML onclicks
        window.App = this;
        window.nextCard = (score) => this.flashcardApp.processSrsRating(score);
        window.resetReview = () => this.quizApp.initSession();
        window.renderReviewQuestion = () => this.quizApp.nextAction();
    }

    bindGlobalEvents() {
        // Import Vocabulary Handling
        const importBtn = $('btnImportJson');
        if (importBtn) {
            importBtn.addEventListener('click', async () => {
                const urlInput = $('importUrl').value.trim();
                const fileInput = $('importFile').files[0];

                if (!urlInput && !fileInput) return toast('Vui lòng cung cấp URL hoặc File JSON.');

                try {
                    let jsonData;
                    importBtn.classList.add('loading');

                    if (fileInput) {
                        const text = await fileInput.text();
                        jsonData = JSON.parse(text);
                    } else if (urlInput) {
                        const res = await fetch(urlInput);
                        jsonData = await res.json();
                    }

                    const added = this.storage.importVocabulary(jsonData);
                    toast(`Đã import thành công ${added} từ vựng mới!`);
                    this.renderMyWords();
                    $('importUrl').value = '';
                    $('importFile').value = '';
                } catch (e) {
                    toast('Lỗi: File hoặc URL không đúng định dạng JSON.');
                } finally {
                    importBtn.classList.remove('loading');
                }
            });
        }

        // Translation Button
        const btnTranslate = document.getElementById('btnTranslate');
        if (btnTranslate) {
            btnTranslate.addEventListener('click', async () => {
                const word = $('newWord').value.trim();
                const feedback = $('translateFeedback');
                feedback.className = 'grammar-alert hide';

                if (!word) {
                    feedback.textContent = 'Vui lòng nhập từ tiếng Anh trước khi dịch.';
                    feedback.className = 'grammar-alert warning';
                    return;
                }

                btnTranslate.classList.add('loading');
                try {
                    const trans = await ApiManager.translate(word);
                    if (trans) {
                        $('newMeaning').value = trans;
                        feedback.textContent = 'Đã dịch thành công! Bạn có thể chỉnh sửa lại nghĩa nếu muốn.';
                        feedback.className = 'grammar-alert success';
                    } else {
                        throw new Error('No translation returned');
                    }
                } catch (e) {
                    feedback.textContent = 'Dịch vụ AI đang bận hoặc vượt quá giới hạn. Vui lòng thử lại sau hoặc tự nhập nghĩa.';
                    feedback.className = 'grammar-alert error';
                } finally {
                    btnTranslate.classList.remove('loading');
                }
            });
        }

        // Grammar Check Button
        const btnGrammar = document.getElementById('btnGrammar');
        if (btnGrammar) {
            btnGrammar.addEventListener('click', async () => {
                const sentence = $('newExample').value.trim();
                const feedback = $('grammarFeedback');
                feedback.className = 'grammar-alert hide';
                $('errorPreview').classList.add('hide');

                if (!sentence) {
                    feedback.textContent = 'Vui lòng viết câu ví dụ trước khi kiểm tra.';
                    feedback.className = 'grammar-alert warning';
                    return;
                }

                btnGrammar.classList.add('loading');
                try {
                    const result = await ApiManager.checkGrammar(sentence);
                    feedback.classList.add('hide'); // Ẩn feedback cũ
                    this.renderGrammarErrors(result);
                } catch (e) {
                    console.error("Lỗi:", e);
                    feedback.textContent = `Lỗi API: ${e.message}`;
                    feedback.className = 'grammar-alert warning';
                    feedback.classList.remove('hide');
                } finally {
                    btnGrammar.classList.remove('loading');
                }
            });
        }

        // Add Word Form Submit
        const wordForm = $('wordForm');
        if (wordForm) {
            wordForm.addEventListener('submit', async (e) => {
                e.preventDefault();
                const word = $('newWord').value.trim();
                let meaning = $('newMeaning').value.trim();

                if (!meaning) {
                    toast('Đang tự động dịch nghĩa...');
                    meaning = await ApiManager.translate(word);
                    if (!meaning) return toast('Lỗi dịch tự động, vui lòng tự nhập nghĩa.');
                }

                this.storage.personalWords.unshift({
                    word,
                    meaning,
                    example: $('newExample').value.trim(),
                    phonetic: '',
                    topic: $('newTag').value,
                    nextReview: 0
                });
                this.storage.saveData();
                wordForm.reset();
                $('translateFeedback').classList.add('hide');
                $('grammarFeedback').classList.add('hide');
                $('errorPreview').classList.add('hide');
                toast('Đã lưu từ vựng vào bộ nhớ!');
                this.renderMyWords();
            });
        }
    }

    renderGrammarErrors(result) {
        if (!result || !result.suggested_sentence) return;

        const html = `
            <div style="margin-top: 16px;">
                <div style="font-weight: 600; color: var(--success); margin-bottom: 8px;">Gợi ý câu chuẩn:</div>
                <div style="padding: 16px; background: var(--success-light); border-radius: var(--radius-sm); border-left: 4px solid var(--success); color: #065F46; font-size: 16px; font-weight: 500; margin-bottom: 12px; line-height: 1.5;">
                    ${escapeHtml(result.suggested_sentence)}
                </div>
                <div style="color: #4B5563; font-size: 14px; line-height: 1.6; padding: 0 4px;">
                    💡 <strong>Giải thích:</strong> ${escapeHtml(result.explanation)}
                </div>
            </div>
        `;

        $('errorPreview').innerHTML = html;
        $('errorPreview').classList.remove('hide');
    }

    renderHome() {
        if ($('streak')) $('streak').textContent = this.storage.streak;
        if ($('dueCount')) $('dueCount').textContent = this.storage.getDueWords().length;
        if ($('knownStat')) $('knownStat').textContent = this.storage.stats.learned;
        if ($('personalStat')) $('personalStat').textContent = this.storage.personalWords.length;
        if ($('reviewStat')) $('reviewStat').textContent = this.storage.stats.reviews;

        const topicsList = $('topicList');
        if (topicsList) {
            // Map GLOBAL_TOPICS to cards
            const dynamicTopics = GLOBAL_TOPICS.map(t =>
                `<div class="topic-card" onclick="App.router.navigate('learn', '${t.id}')">
                    <div class="topic-emoji">${t.icon}</div>
                    <div class="topic-name">${escapeHtml(t.name)}</div>
                    <div style="font-size:12px; color:var(--text-muted); margin-top:4px">${t.words ? t.words.length : 0} từ ready</div>
                </div>`
            ).join('');

            // Add Personal Words Card
            const personalCard = `
                <div class="topic-card" onclick="App.router.navigate('learn', 'personal')">
                    <div class="topic-emoji">💬</div>
                    <div class="topic-name">Personal Words</div>
                    <div style="font-size:12px; color:var(--text-muted); margin-top:4px">${this.storage.personalWords.length} từ ready</div>
                </div>`;

            topicsList.innerHTML = dynamicTopics + personalCard;
        }
    }

    renderMyWords() {
        const words = this.storage.personalWords; // Changed to only show personal/imported
        if ($('wordTotal')) $('wordTotal').textContent = `${words.length} words`;

        const table = $('wordTable');
        if (!table) return;

        if (words.length === 0) {
            table.innerHTML = '<div style="text-align:center; color:var(--text-muted)">Chưa có từ vựng nào.</div>';
            return;
        }

        table.innerHTML = `<table style="width: 100%; border-collapse: collapse; text-align: left;">
            <thead>
                <tr style="border-bottom: 1px solid var(--border-color)">
                    <th style="padding: 12px; font-size: 13px; color: var(--text-muted);">Word</th>
                    <th style="padding: 12px; font-size: 13px; color: var(--text-muted);">Meaning</th>
                    <th style="padding: 12px; font-size: 13px; color: var(--text-muted);">Topic</th>
                </tr>
            </thead>
            <tbody>
                ${words.map(w => `
                <tr style="border-bottom: 1px solid var(--border-color)">
                    <td style="padding: 12px;"><b>${escapeHtml(w.word)}</b></td>
                    <td style="padding: 12px; color: var(--text-muted);">${escapeHtml(w.meaning)}</td>
                    <td style="padding: 12px;"><span style="background: var(--primary-light); color: var(--primary); padding: 4px 8px; border-radius: 99px; font-size: 12px; font-weight: 600;">${escapeHtml(w.topic || 'Personal')}</span></td>
                </tr>
                `).join('')}
            </tbody>
        </table>`;
    }

    renderProgress() {
        if ($('pLearned')) $('pLearned').textContent = this.storage.stats.learned;
        if ($('pReviews')) $('pReviews').textContent = this.storage.stats.reviews;
        if ($('pDue')) $('pDue').textContent = this.storage.getDueWords().length;
    }
}

// Bootstrap Application
document.addEventListener('DOMContentLoaded', () => {
    window.VocabFlowApp = new VocabFlowApplication();
});
