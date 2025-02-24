import json
import html
import datetime
import pytz
import os

# Timezone setup
chicago_tz = pytz.timezone("America/Chicago")

# Function to convert timestamps to readable format
def format_timestamp(timestamp):
    try:
        dt = datetime.datetime.fromtimestamp(float(timestamp), tz=chicago_tz)
        return dt.strftime("%Y-%m-%d %H:%M:%S %Z")
    except (ValueError, TypeError):
        return "Unknown"

# Function to extract Year, Week Number
def get_year_week(timestamp):
    try:
        dt = datetime.datetime.fromtimestamp(float(timestamp), tz=chicago_tz)
        year = dt.strftime("%Y")
        week = dt.strftime("%V")  # ISO Week number (01-53)
        return year, week
    except (ValueError, TypeError):
        return "Unknown", "00"

# Load JSON data
with open("conversations.json", "r", encoding="utf-8") as json_file:
    json_data = json.load(json_file)

# Group conversations into nested dictionary (Year ? Week ? List of conversations)
weekly_conversations = {}
for section in json_data:
    year, week = get_year_week(section.get("create_time"))
    
    if year not in weekly_conversations:
        weekly_conversations[year] = {}  # Ensure year is a dictionary
    
    if week not in weekly_conversations[year]:
        weekly_conversations[year][week] = []  # Ensure week is a list
    
    weekly_conversations[year][week].append(section)

# Ensure conversations folder exists
os.makedirs("conversations", exist_ok=True)

# Generate `conversations.html` (Main Page with Sidebar)
with open("conversations.html", "w", encoding="utf-8") as html_file:
    html_file.write("""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ChatGPT Conversations</title>
    <link rel="stylesheet" href="style.css">
    <script defer src="script.js"></script>
</head>
<body>
    <div id="sidebar">
        <h2>Conversations</h2>
        <input type="text" id="search-bar" placeholder="Search conversations..." oninput="searchConversations()">
        <div id="search-results"></div>
        <button class="expand-collapse-btn" onclick="expandAll()">Expand All</button>
        <button class="expand-collapse-btn" onclick="collapseAll()">Collapse All</button>
""")

    # Sidebar links grouped by Year and Week (Weeks sorted in descending order)
    for year in sorted(weekly_conversations.keys(), reverse=True):
        html_file.write(f'<div class="year" onclick="toggleSection(\'year_{year}\', \'arrow_{year}\')">'
                        f'<span id="arrow_{year}" class="arrow">&#9654;</span> {year}</div>\n')
        html_file.write(f'<div id="year_{year}" class="month-list">\n')

        for week in sorted(weekly_conversations[year].keys(), reverse=True):  # Reversed weeks
            html_file.write(f'<div class="month" onclick="toggleSection(\'week_{year}_{week}\', \'arrow_{year}_{week}\')">'
                            f'<span id="arrow_{year}_{week}" class="arrow">&#9654;</span> Week {week}</div>\n')
            html_file.write(f'<div id="week_{year}_{week}" class="conversation-list">\n')

            for section in weekly_conversations[year][week]:
                title = html.escape(section.get("title", "Untitled Conversation"))
                html_file.write(
                    f'<a class="conversation-link" data-file="conversations_{year}_W{week}.html" '
                    f'data-id="conv_{section.get("create_time")}" href="#">{title}</a>\n'
                )

            html_file.write('</div>\n')  # Close week div

        html_file.write('</div>\n')  # Close year div

    html_file.write("""</div>
    <div id="content">
        <p>Select a conversation from the left to load it here.</p>
    </div>
</body>
</html>""")

print("? Generated conversations.html!")

# Generate Weekly Conversation Files
for year, weeks in weekly_conversations.items():
    for week in sorted(weeks.keys(), reverse=True):  # Reversed weeks
        key = f"{year}_W{week}"  # Ensure correct file naming
        filename = f"conversations/conversations_{key}.html"
        
        with open(filename, "w", encoding="utf-8") as w_file:
            w_file.write("<div class='week-conversations'>\n")
            
            for section in weeks[week]:
                if not isinstance(section, dict):  # Ensure section is a dictionary
                    print(f"? Skipping invalid section: {section}")  # Debugging
                    continue
                
                title = html.escape(section.get("title", "Untitled Conversation"))
                create_time = format_timestamp(section.get("create_time"))

                w_file.write(f'<div class="conversation" id="conv_{section.get("create_time")}">\n')
                w_file.write(f'<h2>{title}</h2>\n')
                w_file.write(f'<div class="timestamp"><strong>Created:</strong> {create_time}</div>\n')
        
                # Extract conversation messages
                messages = section.get("mapping", {}).values()
                grouped_messages = []
                last_role = None
                grouped_text = []
            
                for message in messages:
                    if not message or "message" not in message or message["message"] is None:
                        continue
                    role = message["message"].get("author", {}).get("role", "Unknown").capitalize()
                    parts = message["message"].get("content", {}).get("parts", [])
                    formatted_parts = [html.escape(str(part)) for part in parts if part and isinstance(part, (str, dict))]
                
                    if not formatted_parts:
                        continue
                
                    content = "<br>\n".join(formatted_parts)
                
                    if role == last_role:
                        grouped_text.append(content)
                    else:
                        if grouped_text:
                            grouped_messages.append((last_role, "<br>\n".join(grouped_text)))
                        last_role = role
                        grouped_text = [content]
            
                if grouped_text:
                    grouped_messages.append((last_role, "<br>\n".join(grouped_text)))
            
                # Write messages to the file
                for role, content in grouped_messages:
                    css_class = "user" if role == "User" else "assistant"
                    w_file.write(f'<div class="message {css_class}">\n')
                    w_file.write(f'<strong>{role}:</strong><br>\n')
                    w_file.write(f'<pre>{content}</pre>\n')
                    w_file.write('</div>\n')
            
                w_file.write('</div>\n')  # Close conversation div

            w_file.write('</div>\n')  # Close week conversations div

print("? Generated all weekly conversation files!")
