document.addEventListener("DOMContentLoaded", function() {
    // Load conversation dynamically when a link is clicked
    document.querySelectorAll(".conversation-link").forEach(link => {
        link.addEventListener("click", function(e) {
            e.preventDefault();
            let file = `conversations/${this.getAttribute("data-file")}`; // Ensure path has 'conversations/' prefix
            let id = this.getAttribute("data-id");

            fetch(file)
                .then(response => response.text())
                .then(html => {
                    document.getElementById("content").innerHTML = html;
                    let selectedConv = document.getElementById(id);
                    if (selectedConv) {
                        selectedConv.scrollIntoView({ behavior: "smooth" });
                    }
                })
                .catch(error => console.error("Error loading conversation:", error));
        });
    });

    // Expand/Collapse Year & Week Sections
    window.toggleSection = function(id, arrowId) {
        let section = document.getElementById(id);
        let arrow = document.getElementById(arrowId);
        if (section && arrow) {
            if (section.style.display === "none" || section.style.display === "") {
                section.style.display = "block";
                arrow.innerHTML = "&#9660;"; // Down arrow (expanded)
            } else {
                section.style.display = "none";
                arrow.innerHTML = "&#9654;"; // Right arrow (collapsed)
            }
        } else {
            console.error(`toggleSection: Missing elements for ID: ${id} or ${arrowId}`);
        }
    };

    // Expand All Sections
    window.expandAll = function() {
        document.querySelectorAll('.month-list, .conversation-list').forEach(el => el.style.display = "block");
        document.querySelectorAll('.arrow').forEach(el => el.innerHTML = "&#9660;"); // Set all arrows to "expanded"
    };

    // Collapse All Sections
    window.collapseAll = function() {
        document.querySelectorAll('.month-list, .conversation-list').forEach(el => el.style.display = "none");
        document.querySelectorAll('.arrow').forEach(el => el.innerHTML = "&#9654;"); // Set all arrows to "collapsed"
    };

    // Search Conversations
    window.searchConversations = function() {
        let query = document.getElementById("search-bar").value.toLowerCase();
        let resultsContainer = document.getElementById("search-results");
        resultsContainer.innerHTML = "";

        if (query.length < 3) return; // Require at least 3 characters

        let files = [];
        for (let year = 2020; year <= 2030; year++) {
            for (let week = 1; week <= 53; week++) {
                let formattedWeek = week.toString().padStart(2, '0');
                let filename = `conversations/conversations_${year}_W${formattedWeek}.html`; // Ensure path has 'conversations/' prefix
                files.push(filename);
            }
        }

        files.forEach(file => {
            fetch(file)
                .then(response => {
                    if (!response.ok) throw new Error(`File not found: ${file}`);
                    return response.text();
                })
                .then(html => {
                    let tempDiv = document.createElement("div");
                    tempDiv.innerHTML = html;

                    let conversations = tempDiv.querySelectorAll(".conversation");
                    conversations.forEach(convo => {
                        let convoText = convo.innerText.toLowerCase();
                        if (convoText.includes(query)) {
                            let title = convo.querySelector("h2").innerText;
                            let convoId = convo.getAttribute("id");
                            let resultItem = document.createElement("div");
                            resultItem.classList.add("search-result");
                            resultItem.innerHTML = `<a href="#" onclick="loadConversation('${file}', '${convoId}', '${query}')">${title}</a>`;
                            resultsContainer.appendChild(resultItem);
                        }
                    });
                })
                .catch(error => console.error(`Error searching in ${file}:`, error));
        });
    };

    // Modify loadConversation to highlight search terms
    window.loadConversation = function(file, convoId, searchTerm = "") {
        fetch(file)
            .then(response => response.text())
            .then(html => {
                document.getElementById("content").innerHTML = html;
                let selectedConv = document.getElementById(convoId);
                if (selectedConv) {
                    selectedConv.scrollIntoView({ behavior: "smooth" });

                    if (searchTerm) {
                        highlightText(searchTerm);
                    }
                }
            })
            .catch(error => console.error("Error loading conversation:", error));
    };

    // Function to highlight text inside content
    function highlightText(searchTerm) {
        let content = document.getElementById("content");
        let regex = new RegExp(`(${searchTerm})`, "gi");
        content.innerHTML = content.innerHTML.replace(regex, `<span class="highlight">$1</span>`);
    }

    collapseAll();
});
