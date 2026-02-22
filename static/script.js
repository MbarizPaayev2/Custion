const API_URL = window.location.origin;

async function sendMessage() {
    const messageInput = document.getElementById('messageInput');
    const text = messageInput.value.trim();
    
    if (!text) {
        return;
    }

    // Add user message to chat
    addUserMessage(text);
    
    // Clear input
    messageInput.value = '';
    
    // Disable send button
    const sendBtn = document.getElementById('sendBtn');
    const sendIcon = document.getElementById('sendIcon');
    const sendLoader = document.getElementById('sendLoader');
    
    sendBtn.disabled = true;
    sendIcon.style.display = 'none';
    sendLoader.style.display = 'block';

    try {
        const response = await fetch(`${API_URL}/analyze`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ text })
        });

        if (!response.ok) {
            throw new Error('API sorğusu uğursuz oldu');
        }

        const data = await response.json();
        addBotResponse(data);

    } catch (error) {
        addErrorMessage('Xəta baş verdi: ' + error.message);
    } finally {
        // Reset button
        sendBtn.disabled = false;
        sendIcon.style.display = 'block';
        sendLoader.style.display = 'none';
    }
}

function addUserMessage(text) {
    const chatMessages = document.getElementById('chatMessages');
    
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message user-message';
    messageDiv.innerHTML = `
        <div class="message-wrapper">
            <div class="message-header">
                <div class="message-avatar">👤</div>
                <div class="message-content">
                    <p>${escapeHtml(text)}</p>
                </div>
            </div>
        </div>
    `;
    
    chatMessages.appendChild(messageDiv);
    scrollToBottom();
}

function addBotResponse(data) {
    const chatMessages = document.getElementById('chatMessages');
    
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message bot-message';
    
    let vocabularyHtml = '';
    if (data.vocabulary_list && data.vocabulary_list.length > 0) {
        vocabularyHtml = '<div class="vocab-list">';
        data.vocabulary_list.forEach(item => {
            vocabularyHtml += `
                <div class="vocab-item">
                    <div class="vocab-word">${escapeHtml(item.word)}</div>
                    <div class="vocab-definition">${escapeHtml(item.a2_definition)}</div>
                </div>
            `;
        });
        vocabularyHtml += '</div>';
    }
    
    messageDiv.innerHTML = `
        <div class="message-wrapper">
            <div class="message-header">
                <div class="message-avatar">🤖</div>
                <div class="message-content">
                    <div class="result-section">
                        <h3>🇦🇿 Azərbaycan Tərcüməsi</h3>
                        <p class="result-text">${escapeHtml(data.az_translation)}</p>
                    </div>
                    
                    ${data.vocabulary_list.length > 0 ? `
                    <div class="result-section">
                        <h3>📚 Lüğət (A2 Səviyyə)</h3>
                        ${vocabularyHtml}
                        <p class="word-count">Naməlum söz sayı: <span>${data.unknown_words_count}</span></p>
                    </div>
                    ` : ''}
                    
                    <div class="result-section">
                        <h3>💡 Mini Qeyd</h3>
                        <div class="mini-note">
                            <p class="result-text">${escapeHtml(data.security_plus_mini_note)}</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `;
    
    chatMessages.appendChild(messageDiv);
    scrollToBottom();
}

function addErrorMessage(message) {
    const chatMessages = document.getElementById('chatMessages');
    
    const errorDiv = document.createElement('div');
    errorDiv.className = 'error-message';
    errorDiv.textContent = message;
    
    chatMessages.appendChild(errorDiv);
    scrollToBottom();
    
    setTimeout(() => {
        errorDiv.remove();
    }, 5000);
}

function scrollToBottom() {
    const chatMessages = document.getElementById('chatMessages');
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Enter key support
document.getElementById('messageInput').addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
    }
});
