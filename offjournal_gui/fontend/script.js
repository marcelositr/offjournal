document.addEventListener('DOMContentLoaded', () => {
    // --- State Management ---
    let state = {
        currentView: 'diary',
        currentEntryId: null,
        isDirty: false, // Flag to check if the editor has unsaved changes
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
        entryWelcome: document.getElementById('entry-welcome'),
        entryEditor: document.getElementById('entry-editor'),
        editorTextarea: document.getElementById('editor-textarea'),
        saveStatus: document.getElementById('save-status'),
        btnSaveEntry: document.getElementById('btn-save-entry'),
        btnDeleteEntry: document.getElementById('btn-delete-entry'),
        btnNewEntry: document.getElementById('btn-new-entry'),
        btnAddEvent: document.getElementById('btn-add-event'),
        plannerDate: document.getElementById('planner-date'),
        plannerTitle: document.getElementById('planner-title'),
    };

    // --- API Communication Layer ---
    const api = {
        send: (command, payload = {}) => {
            try {
                window.webkit.messageHandlers.bridge.postMessage(JSON.stringify({ command, payload }));
            } catch (error) {
                console.error("Falha na comunicação com o backend Python. A aplicação está sendo executada no modo GUI?", error);
                alert("Erro de comunicação: Não foi possível contatar o backend.");
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

    // --- UI Rendering ---
    const ui = {
        switchView(viewName) {
            state.currentView = viewName;
            Object.values(elements.views).forEach(v => v.classList.remove('active-view'));
            Object.values(elements.navButtons).forEach(b => b.classList.remove('active'));
            elements.views[viewName].classList.add('active-view');
            elements.navButtons[viewName].classList.add('active');

            if (viewName === 'diary') api.entries.list();
            if (viewName === 'planner') api.planner.list();
        },
        renderEntryList(entries) {
            elements.entryList.innerHTML = '';
            if (!entries || entries.length === 0) {
                elements.entryList.innerHTML = '<li class="empty-list">Nenhuma entrada encontrada.</li>';
                return;
            }
            entries.forEach(entry => {
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
        updateSaveStatus(message, isError = false) {
            elements.saveStatus.textContent = message;
            elements.saveStatus.style.color = isError ? 'var(--danger-color)' : 'var(--text-secondary)';
            clearTimeout(statusTimeout);
            statusTimeout = setTimeout(() => elements.saveStatus.textContent = '', 3000);
        }
    };

    // --- Event Handlers & Logic ---
    const handlers = {
        selectEntry(id) {
            if (state.isDirty && !confirm("Você tem alterações não salvas. Deseja descartá-las?")) {
                return;
            }
            state.currentEntryId = id;
            api.entries.getContent(id);
            document.querySelectorAll('#entry-list li').forEach(item => item.classList.remove('selected'));
            document.querySelector(`#entry-list li[data-id='${id}']`)?.classList.add('selected');
        },
        saveCurrentEntry() {
            if (state.currentEntryId) {
                api.entries.update(state.currentEntryId, elements.editorTextarea.value);
                state.isDirty = false;
            }
        },
        onEditorInput() {
            state.isDirty = true;
            ui.updateSaveStatus('Alterações não salvas...');
            clearTimeout(saveTimeout);
            saveTimeout = setTimeout(handlers.saveCurrentEntry, 2000); // Auto-save after 2 seconds of inactivity
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
        handleKeyDown(e) {
            // Salvar com Ctrl+S
            if (e.ctrlKey && e.key === 's') {
                e.preventDefault();
                clearTimeout(saveTimeout); // Prevent auto-save from firing
                handlers.saveCurrentEntry();
            }
        }
    };

    // --- Python Response Handler ---
    window.handlePythonResponse = (response) => {
        console.log('Received from Python:', response);
        const { status, command, data, message } = response;

        if (status === 'error') {
            alert(`Erro no comando '${command}': ${message}`);
            ui.updateSaveStatus(`Erro: ${message}`, true);
            return;
        }

        switch (command) {
            case 'entries:list':
                ui.renderEntryList(data);
                break;
            case 'entries:get_content':
                ui.showEditor(data);
                break;
            case 'entries:update':
                if (data.status === 'success') {
                    ui.updateSaveStatus(data.message);
                } else {
                    ui.updateSaveStatus(data.message, true);
                }
                break;
            case 'entries:create':
                state.currentEntryId = data.data.id;
                api.entries.list(); // Refresh list
                handlers.selectEntry(state.currentEntryId);
                break;
            case 'entries:delete':
                ui.showWelcome();
                api.entries.list(); // Refresh list
                break;
            case 'planner:list':
                ui.renderEventList(data);
                break;
            case 'planner:add':
            case 'planner:delete':
                 api.planner.list(); // Refresh list on add/delete
                 if (command === 'planner:add' && data.status === 'success') {
                     elements.plannerTitle.value = '';
                     elements.plannerTitle.focus();
                 }
                break;
        }
    };

    // --- Initialize ---
    const init = () => {
        // Setup event listeners
        elements.navButtons.diary.addEventListener('click', () => ui.switchView('diary'));
        elements.navButtons.planner.addEventListener('click', () => ui.switchView('planner'));
        elements.btnNewEntry.addEventListener('click', handlers.createNewEntry);
        elements.btnSaveEntry.addEventListener('click', handlers.saveCurrentEntry);
        elements.btnDeleteEntry.addEventListener('click', handlers.deleteCurrentEntry);
        elements.btnAddEvent.addEventListener('click', handlers.addNewEvent);
        elements.editorTextarea.addEventListener('input', handlers.onEditorInput);
        document.addEventListener('keydown', handlers.handleKeyDown);

        // Set planner date to today and load initial view
        elements.plannerDate.value = new Date().toISOString().split('T')[0];
        ui.switchView('diary');
    };

    init();
});
