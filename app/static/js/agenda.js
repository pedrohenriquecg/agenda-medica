(() => {
    const tableElement = document.getElementById("appointments-table");
    const dataElement = document.getElementById("appointments-data");

    if (!tableElement || !dataElement) {
        return;
    }

    const searchInput = document.getElementById("appointment-search");
    const loadingMessage = document.getElementById("appointments-loading");
    const stateMessage = document.getElementById("appointments-message");
    const searchableFields = ["patient", "cpf", "doctor", "specialty", "insurance", "status"];
    const hasApiError = tableElement.dataset.hasError === "true";

    const messages = {
        empty: "Nenhum agendamento encontrado.",
        searchEmpty: "Nenhum agendamento corresponde à busca.",
        tableUnavailable: "Não foi possível carregar a tabela de agendamentos.",
    };

    const hideLoadingMessage = () => {
        if (loadingMessage) {
            loadingMessage.hidden = true;
        }
    };

    const disableSearch = () => {
        if (searchInput) {
            searchInput.disabled = true;
        }
    };

    const showStateMessage = (message) => {
        if (stateMessage) {
            stateMessage.textContent = message;
            stateMessage.hidden = false;
        }
    };

    const hideStateMessage = () => {
        if (stateMessage) {
            stateMessage.textContent = "";
            stateMessage.hidden = true;
        }
    };

    const normalizeValue = (value) => String(value ?? "").toLowerCase();

    const matchesSearch = (data, searchTerm) => {
        const normalizedSearchTerm = normalizeValue(searchTerm).trim();

        if (!normalizedSearchTerm) {
            return true;
        }

        return searchableFields.some((field) => (
            normalizeValue(data[field]).includes(normalizedSearchTerm)
        ));
    };

    const updateStateMessage = (activeCount, searchTerm, totalCount) => {
        if (hasApiError) {
            return;
        }

        const normalizedSearchTerm = searchTerm.trim();

        if (activeCount > 0) {
            hideStateMessage();
            return;
        }

        if (normalizedSearchTerm) {
            showStateMessage(messages.searchEmpty);
            return;
        }

        if (totalCount === 0) {
            showStateMessage(messages.empty);
            return;
        }

        hideStateMessage();
    };

    const getStatusText = (value) => {
        if (value === null || value === undefined || String(value).trim() === "") {
            return "Sem status";
        }

        return String(value);
    };

    const statusFormatter = (cell) => {
        const value = getStatusText(cell.getValue());
        const statusKey = value.trim().toLowerCase();
        const colors = {
            confirmado: { background: "#e8f5e9", text: "#1b5e20" },
            pendente: { background: "#fff8e1", text: "#7a4f01" },
            cancelado: { background: "#ffebee", text: "#8a1c1c" },
            reagendado: { background: "#e3f2fd", text: "#0d47a1" },
        };
        const selectedColors = colors[statusKey] || { background: "#f5f5f5", text: "#333333" };
        const element = document.createElement("span");

        element.textContent = value;
        element.style.backgroundColor = selectedColors.background;
        element.style.borderRadius = "4px";
        element.style.color = selectedColors.text;
        element.style.display = "inline-block";
        element.style.fontWeight = "600";
        element.style.padding = "2px 8px";

        return element;
    };

    const parseAppointments = () => {
        try {
            const data = JSON.parse(dataElement.textContent || "[]");

            if (Array.isArray(data)) {
                return data;
            }
        } catch (error) {
            return [];
        }

        return [];
    };

    const appointments = parseAppointments();

    if (hasApiError) {
        hideLoadingMessage();
        disableSearch();
        return;
    }

    if (typeof Tabulator === "undefined") {
        hideLoadingMessage();
        disableSearch();
        showStateMessage(messages.tableUnavailable);
        return;
    }

    const table = new Tabulator(tableElement, {
        data: appointments,
        layout: "fitColumns",
        pagination: "local",
        paginationSize: 5,
        placeholder: "",
        responsiveLayout: "collapse",
        columns: [
            { title: "Paciente", field: "patient", sorter: "string" },
            { title: "CPF", field: "cpf", sorter: "string" },
            { title: "Médico", field: "doctor", sorter: "string" },
            { title: "Especialidade", field: "specialty", sorter: "string" },
            { title: "Data", field: "date", sorter: "string" },
            { title: "Horário", field: "time", sorter: "string" },
            { title: "Convênio", field: "insurance", sorter: "string" },
            { title: "Status", field: "status", sorter: "string", formatter: statusFormatter },
        ],
    });

    table.on("tableBuilt", () => {
        hideLoadingMessage();
        updateStateMessage(table.getDataCount("active"), searchInput?.value || "", appointments.length);
    });

    table.on("dataFiltered", (filters, rows) => {
        updateStateMessage(rows.length, searchInput?.value || "", appointments.length);
    });

    if (searchInput) {
        searchInput.addEventListener("input", () => {
            const searchTerm = searchInput.value.trim();

            if (!searchTerm) {
                table.clearFilter();
                updateStateMessage(table.getDataCount("active"), "", appointments.length);
                return;
            }

            table.setFilter((data) => matchesSearch(data, searchTerm));
        });
    }
})();
