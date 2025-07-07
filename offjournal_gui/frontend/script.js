document.addEventListener('DOMContentLoaded', () => {
    // --- State Management ---
    let state = {
        currentView: 'diary',
        currentEntryId: null,
        isDirty: false,
        allEntries: [], // NOVO: Armazena a lista completa de entradas recebida do backend
    };

    // --- Debounce for saving ---
    let saveTimeout = null;
    let statusTimeout = null;

    // --- DOM Elements ---
    const elements = {
        views: {
            diary: document.getElementById('diary-view'),
            planner: document.getElementById('planner-view'),
        },
        navButtons: {
            diary: document.getElementById('nav-diary'),
            planner: document.getElementById('nav-planner'),
        },
        entryList: document.getElementById('entry-list'),
        eventList: document.getElementById('event-list'),
        spinners: {
            diary: document.getElementById('diary-spinner'),
            planner: document.getElementById('planner-spinner'),
        },
        searchInput: document.getElementById('search-input'), // NOVO: Referência ao campo de busca
        entryWelcome: document.getElementById('entry-welcome'),
        entryEditor: document.getElementById('entry-editor'),
        editorTextarea: document.getElementById('editor-textarea'),
        saveStatus: document.getElementById('save-status'),
        btnNewEntry: document.getElementById('btn-new-entry'),
        btnAddEvent: document.getElementById('btn-add-event'),
        plannerDate: document.getElementById('planner-date'),
        plannerTitle: document.getElementById('planner-title'),
    };

    // --- API Communication Layer ---
    const api = {
        send: (command, payload = {}) => {
            const spinner = command.startsWith('entries:') ? elements.spinners.diary : elements.spinners.planner;
            if (spinner) spinner.style.display = 'flex';

            try {
                window.webkit.messageHandlers.bridge.postMessage(JSON.stringify({ command, payload }));
            } catch (error) {
                console.error("Falha na comunicação com o backend Python.", error);
                if (spinner) spinner.style.display = 'none';
            }
        },
        entries: {
            list: () => api.send('entries:list'),
            getContent: (id) => api.send('entries:get_content', { id }),
            update: (id, content) => api.send('entries:update', { id, content }),
            create: (title) => api.send('entries:create', { title }),
            delete: (id) => api.send('entries:delete', { id }),
        },
        planner: {
            list: () => api.send('planner:list'),
            add: (date, title) => api.send('planner:add', {date, title}),
            delete: (id) => api.send('planner:delete', {id}),
        }
    };

    // --- UI Rendering & Logic ---
    const ui = {
        switchView(viewName) {
            if (state.isDirty && !confirm("Você tem alterações não salvas. Deseja descartá-las?")) return;
            ui.showWelcome();

            state.currentView = viewName;
            Object.values(elements.views).forEach(v => v.classList.remove('active-view'));
            Object.values(elements.navButtons).forEach(b => b.classList.remove('active'));
            elements.views[viewName].classList.add('active-view');
            elements.navButtons[viewName].classList.add('active');

            if (viewName === 'diary') api.entries.list();
            if (viewName === 'planner') api.planner.list();
        },
        renderEntryList(entriesToRender) {
            elements.entryList.innerHTML = '';
            if (!entriesToRender || entriesToRender.length === 0) {
                elements.entryList.innerHTML = '<li class="empty-list">Nenhuma entrada encontrada.</li>';
                return;
            }
            entriesToRender.forEach(entry => {
                const li = document.createElement('li');
                li.dataset.id = entry.id;
                li.className = (entry.id === state.currentEntryId) ? 'selected' : '';
                li.innerHTML = `
                    <span class="item-title">${entry.title}</span>
                    <span class="item-subtitle">${entry.id}</span>
                `;
                li.addEventListener('click', () => handlers.selectEntry(entry.id));
                elements.entryList.appendChild(li);
            });
        },
        renderEventList(events) {
            elements.eventList.innerHTML = '';
             if (!events || events.length === 0) {
                elements.eventList.innerHTML = '<li class="empty-list">Nenhum evento no planejador.</li>';
                return;
            }
            events.forEach(event => {
                const li = document.createElement('li');
                li.innerHTML = `
                    <div class="item-list-row">
                        <span class="event-date">${event.date}</span>
                        <span class="event-title">${event.title}</span>
                        <button class="btn-delete-event" data-id="${event.id}" title="Excluir evento">×</button>
                    </div>
                `;
                li.querySelector('.btn-delete-event').addEventListener('click', (e) => {
                    e.stopPropagation();
                    handlers.deleteEvent(event.id, event.title);
                });
                elements.eventList.appendChild(li);
            });
        },
        showEditor(content) {
            elements.entryWelcome.style.display = 'none';
            elements.entryEditor.style.display = 'flex';
            elements.editorTextarea.value = content;
            elements.editorTextarea.focus();
            state.isDirty = false;
        },
        showWelcome() {
            elements.entryWelcome.style.display = 'flex';
            elements.entryEditor.style.display = 'none';
            state.currentEntryId = null;
            state.isDirty = false;
            document.querySelectorAll('#entry-list li').forEach(item => item.classList.remove('selected'));
        },
        updateSaveStatus(message, isError = false, persistent = false) {
            elements.saveStatus.textContent = message;
            elements.saveStatus.style.color = isError ? 'var(--danger-color)' : 'var(--text-secondary)';
            clearTimeout(statusTimeout);
            if (!persistent) {
                statusTimeout = setTimeout(() => elements.saveStatus.textContent = '', 3000);
            }
        }
    };

    // --- Event Handlers ---
    const handlers = {
        selectEntry(id) {
            if (state.isDirty && !confirm("Você tem alterações não salvas. Deseja descartá-las?")) return;
            
            state.currentEntryId = id;
            api.entries.getContent(id);
            document.querySelectorAll('#entry-list li').forEach(item => item.classList.remove('selected'));
            document.querySelector(`#entry-list li[data-id='${id}']`)?.classList.add('selected');
        },
        saveCurrentEntry() {
            if (state.currentEntryId && state.isDirty) {
                api.entries.update(state.currentEntryId, elements.editorTextarea.value);
                state.isDirty = false;
            }
        },
        onEditorInput() {
            if (!state.isDirty) {
                state.isDirty = true;
                ui.updateSaveStatus('Alterações pendentes...', false, true);
            }
            clearTimeout(saveTimeout);
            saveTimeout = setTimeout(handlers.saveCurrentEntry, 1500);
        },
        createNewEntry() {
            const title = prompt("Digite o título para a nova entrada:", "Nova Entrada");
            if (title && title.trim()) {
                api.entries.create(title);
            }
        },
        deleteCurrentEntry() {
            if (state.currentEntryId && confirm("Tem certeza que deseja excluir esta entrada? A ação não pode ser desfeita.")) {
                api.entries.delete(state.currentEntryId);
            }
        },
        addNewEvent() {
            const date = elements.plannerDate.value;
            const title = elements.plannerTitle.value;
            if (date && title.trim()) {
                api.planner.add(date, title);
            } else {
                alert("Por favor, preencha a data e o título do evento.");
            }
        },
        deleteEvent(id, title) {
            if (confirm(`Tem certeza que deseja excluir o evento "${title}"?`)) {
                api.planner.delete(id);
            }
        },
        navigateEntryList(direction) {
            const items = Array.from(elements.entryList.querySelectorAll('li[data-id]'));
            if (items.length === 0) return;

            const currentIndex = items.findIndex(item => item.dataset.id === state.currentEntryId);
            let nextIndex;

            if (direction === 'down') {
                nextIndex = (currentIndex === -1) ? 0 : Math.min(currentIndex + 1, items.length - 1);
            } else { // 'up'
                nextIndex = (currentIndex <= 0) ? 0 : currentIndex - 1;
            }
            
            items[nextIndex].click();
        },
        handleKeyDown(e) {
            if (e.ctrlKey && e.key === 's') {
                e.preventDefault();
                clearTimeout(saveTimeout);
                handlers.saveCurrentEntry();
                return;
            }
            if (e.ctrlKey && e.key === 'n') {
                e.preventDefault();
                if (state.currentView === 'diary') {
                    handlers.createNewEntry();
                }
                return;
            }
            if (state.currentView === 'diary' && !e.target.matches('textarea, input')) {
                if (e.key === 'ArrowDown') {
                    e.preventDefault();
                    handlers.navigateEntryList('down');
                } else if (e.key === 'ArrowUp') {
                    e.preventDefault();
                    handlers.navigateEntryList('up');
                }
            }
        },
        // NOVO: Lógica para filtrar as entradas
        filterEntries() {
            const searchTerm = elements.searchInput.value.toLowerCase();
            if (!searchTerm) {
                ui.renderEntryList(state.allEntries); // Mostra tudo se a busca estiver vazia
                return;
            }
            const filteredEntries = state.allEntries.filter(entry => 
                entry.title.toLowerCase().includes(searchTerm)
            );
            ui.renderEntryList(filteredEntries);
        },
    };

    // --- Python Response Handler ---
    window.handlePythonResponse = ({ status, command, data, message }) => {
        const spinner = command.startsWith('entries:') ? elements.spinners.diary : elements.spinners.planner;
        if (spinner) spinner.style.display = 'none';

        if (status === 'error') {
            alert(`Erro no comando '${command}': ${message || data?.message || 'Erro desconhecido'}`);
            return;
        }

        switch (command) {
            case 'entries:list':
                state.allEntries = data; // Armazena a lista completa
                handlers.filterEntries(); // Renderiza com base no filtro atual
                break;
            case 'entries:get_content': ui.showEditor(data); break;
            case 'entries:update': ui.updateSaveStatus(data.message, data.status === 'error'); break;
            case 'entries:create':
                elements.searchInput.value = ''; // Limpa a busca para a nova entrada aparecer
                api.entries.list();
                handlers.selectEntry(data.data.id);
                break;
            case 'entries:delete':
                ui.showWelcome();
                api.entries.list();
                break;
            case 'planner:list': ui.renderEventList(data); break;
            case 'planner:add':
            case 'planner:delete':
                 api.planner.list();
                 if (command === 'planner:add' && data.status === 'success') {
                     elements.plannerTitle.value = '';
                     elements.plannerTitle.focus();
                 }
                break;
        }
    };

    // --- Initialize Application ---
    const init = () => {
        // Event listeners para cliques
        document.getElementById('nav-diary').addEventListener('click', () => ui.switchView('diary'));
        document.getElementById('nav-planner').addEventListener('click', () => ui.switchView('planner'));
        document.getElementById('btn-new-entry').addEventListener('click', handlers.createNewEntry);
        document.getElementById('btn-save-entry').addEventListener('click', handlers.saveCurrentEntry);
        document.getElementById('btn-delete-entry').addEventListener('click', handlers.deleteCurrentEntry);
        elements.btnAddEvent.addEventListener('click', handlers.addNewEvent);
        
        // Event listeners para teclado
        elements.editorTextarea.addEventListener('input', handlers.onEditorInput);
        document.addEventListener('keydown', handlers.handleKeyDown);
        
        elements.plannerTitle.addEventListener('keydown', (e) => {
            if (e.key === 'Enter') {
                e.preventDefault();
                handlers.addNewEvent();
            }
        });

        // NOVO: Event listener para o campo de busca
        elements.searchInput.addEventListener('input', handlers.filterEntries);

        elements.plannerDate.value = new Date().toISOString().split('T')[0];
        ui.switchView('diary');
    };

    init();
});