# Remote-GUI User Guide

## How to Use the Remote-GUI Interface

This guide shows you how to use each page of the Remote-GUI interface step by step.

## Table of Contents

1. [Getting Started](#getting-started)
2. [Node Picker (Top Bar)](#node-picker-top-bar)
3. [Client Dashboard](#client-dashboard)
4. [Monitor Page](#monitor-page)
5. [SQL Query Generator](#sql-query-generator)
6. [Bookmarks Page](#bookmarks-page)
7. [Presets Page](#presets-page)
8. [Blockchain Manager](#blockchain-manager)
9. [View Files](#view-files)
10. [Policies](#policies)
11. [Add Data](#add-data)
12. [User Profile](#user-profile)

## Getting Started

1. **Open the application** in your web browser
2. **Select a node** using the Node Picker at the top
3. **Navigate** using the sidebar menu on the left
4. **Start with the Client Dashboard** to execute commands

---

## Node Picker (Top Bar)

The Node Picker is at the top of the interface and is used to connect to AnyLog nodes.

### How to Use:

1. **Add a New Node:**
   - Type an IP address and port in the format: `192.168.1.100:32349`
   - Click "Use" to connect to that node
   - The node will be added to your dropdown list

2. **Switch Between Nodes:**
   - Click the dropdown arrow next to the node field
   - Select any previously connected node from the list
   - The interface will switch to that node

3. **View Connected Node:**
   - The current node is displayed in the top bar
   - Shows as "Connected Node: [IP:Port]"

### Tips:
- Save frequently used nodes as bookmarks for quick access
- Make sure the AnyLog node is running and accessible
- Use the format `IP:Port` (e.g., `192.168.1.100:32349`)

---

## Client Dashboard

The main page for executing AnyLog commands.

### How to Use:

1. **Select a Node:**
   - Make sure you have a node selected in the top bar
   - If no node is selected, you'll see a message to select one first

2. **Enter a Command:**
   - Type your AnyLog command in the "Command" text area
   - Examples: `get status`, `blockchain get operator`, `run client () sql demo format = table "SELECT * FROM table_name"`

3. **Choose HTTP Method:**
   - Select "GET" for most commands
   - Select "POST" for commands that modify data

4. **Add Authentication (Optional):**
   - Click "Show Authentication Options" if needed
   - Enter username and password if the node requires authentication

5. **Use Presets (If Available):**
   - If you have saved presets, they'll appear organized into groups as dropdown menus.
   - Click a group dropdown to expand it and view the presets within that group.
   - Click any preset button inside a group to automatically fill the command and method.

6. **Execute the Command:**
   - Click "Send" to execute the command
   - Wait for the response to appear below

7. **View Results:**
   - **Table Data**: Shows in a formatted table
   - **JSON Data**: Shows formatted JSON
   - **Blob Data**: Shows file selection interface
   - **Text Data**: Shows plain text response

8. **Handle Blob Data:**
   - If the result contains blob data, you can select files
   - Click "View Blobs" to open the file viewer

### Tips:
- Use the "📋 Paste" button to paste commands from clipboard
- Save frequently used commands as presets
- Check the response type to understand the data format

---

## Monitor Page

Real-time monitoring of your AnyLog network.

### How to Use:

1. **Set Refresh Rate:**
   - Enter a number in seconds (must be 0 or a multiple of 20)
   - `0` = run once only
   - `20` = refresh every 20 seconds
   - `40` = refresh every 40 seconds, etc.

2. **Start Monitoring:**
   - Click "Start Monitoring" to begin
   - The button will show "Monitoring..." while running

3. **Stop Monitoring:**
   - Click "Stop Monitoring" to halt
   - Monitoring will stop immediately

4. **View Data:**
   - Results appear in a table below the controls
   - Data updates automatically based on your refresh rate
   - Each row shows monitoring information for a node

5. **Add Threshold:**
   - Use the threshold section to monitor specific columns for critical values.
   - To add a threshold:
     - Select a column from the dropdown.
     - Choose an operator (e.g., greater, less, equal).
     - Enter a value to compare against.
     - Click "Add Threshold" to apply it.
   - When a threshold is active, any cell in the table that meets the threshold condition will be highlighted (for example, with a red background and bold text).
   - You can remove a threshold by clicking the "Remove" (🗑️) button next to it.
   - You can add multiple thresholds for different columns or conditions.
   - Thresholds help you quickly spot values that exceed (or fall below) your set limits by changing the color and style of the affected cells.

### Tips:
- Use 0 for one-time checks
- Use 20+ for continuous monitoring
- Stop monitoring when done to save resources

---

## SQL Query Generator

Build and execute SQL queries for AnyLog databases.

### How to Use:

1. **Select Database:**
   - Choose a database from the dropdown
   - The system will fetch available databases from your node

2. **Select Table:**
   - Choose a table from the dropdown
   - Tables are loaded after selecting a database

3. **Choose Columns:**
   - **Select Columns Mode**: Click columns to include in your query
   - **Use Aggregations Mode**: Set up functions like COUNT, SUM, AVG
   - **Mixed Mode**: Combine regular columns with aggregations

4. **Configure Query Options:**
   - **Format**: Choose JSON or Table output
   - **Timezone**: Select timezone for date/time data

5. **Add Time-Series Analysis (Optional):**
   - **Increments**: For time-based analysis with automatic time buckets
   - **Periods**: For time-based filtering conditions

6. **Use Advanced Options (Optional):**
   - Click "Show Advanced Options"
   - Add WHERE conditions for filtering
   - Set GROUP BY columns
   - Add ORDER BY for sorting
   - Set LIMIT for result count

7. **Execute Query:**
   - Review the generated query in the text area
   - Click "Execute Query" to run it
   - View results in the table below

8. **Copy Query:**
   - Click "Copy Query" to copy the generated SQL
   - Use it in other tools or save for later

### Tips:
- Start simple with just column selection
- Use aggregations for summary data
- Add WHERE conditions to filter results
- Use increments for time-series analysis

---

## Bookmarks Page

Save and manage frequently used nodes.

### How to Use:

1. **Add a Bookmark:**
   - Enter a node name (e.g., `192.168.1.100:32349`)
   - Add a description (optional)
   - Click "Add Bookmark"

2. **Edit Descriptions:**
   - Click the "✏️ Edit" button next to any bookmark
   - Update the description
   - Click "💾 Save" to save changes
   - Click "❌ Cancel" to discard changes

3. **Delete Bookmarks:**
   - Click the "🗑️" button next to any bookmark
   - Confirm deletion in the popup

4. **Import Bookmarks:**
   - Click "Choose File" and select a JSON file
   - Preview the bookmarks to be imported
   - Click "Import All" to add them
   - Click "Cancel" to abort

5. **Export Bookmarks:**
   - Click "📤 Export All Bookmarks"
   - A JSON file will be downloaded with all your bookmarks

### Tips:
- Use descriptive names for easy identification
- Export bookmarks before major changes
- Import/export to share bookmark collections

---

## Presets Page

Create and manage command presets for quick execution.

### How to Use:

1. **Create a Group:**
   - Enter a group name (e.g., "Database Commands")
   - Click "Create"
   - Groups organize related presets

2. **Add Presets to a Group:**
   - Select a group from the dropdown
   - Enter a button label (what appears on the button)
   - Choose GET or POST method
   - Enter the command
   - Click "Add Preset"

3. **Use Presets:**
   - Go to the Client Dashboard
   - Click any preset button to execute that command
   - The command and method will be filled automatically

4. **Delete Presets:**
   - Click the "🗑️" button next to any preset
   - Confirm deletion

5. **Delete Groups:**
   - Click the "🗑️" button next to any group
   - This deletes the group and all its presets

6. **Import/Export Presets:**
   - **Import**: Choose a JSON file and click "Import All"
   - **Export**: Click "📤 Export All Presets" to download

### Tips:
- Create groups for different types of commands
- Use descriptive button labels
- Export presets to share with others

---

## Blockchain Manager

Query and manage blockchain policies and operators.

### How to Use:

1. **Select Query Type:**
   - Choose from: All, Operator, Query, Master, Cluster, or Table
   - Each type shows different blockchain data

2. **Add Name Filter (Optional):**
   - Enter a specific name to filter results
   - Leave empty to see all items of that type

3. **Execute Query:**
   - Click "Execute Query" to run the search
   - Results appear in cards below

4. **View Results:**
   - Each result shows in a detailed card
   - Information is organized by category
   - Look for network info, configuration, metadata, etc.

5. **Search Results:**
   - Use the search box to filter displayed results
   - Search works across all fields in the results

6. **Delete Items:**
   - Click "Delete" on any result card
   - Confirm deletion in the popup
   - Item will be removed from the blockchain

7. **Clear Results:**
   - Click "Clear Results" to remove all displayed data

### Tips:
- Start with "All" to see everything
- Use name filters to find specific items
- Be careful when deleting - this removes blockchain data

---

## View Files
> **IMPORTANT:**  
> The "View Files" page cannot be accessed directly.  
> It will open automatically when you run a query that returns blob data (files) in the Client Dashboard or other relevant pages.  
>  
> To view files:
> - Run a query that returns blob data (such as images or documents).
> - The "View Files" interface will appear automatically, showing the available files.
> - You do **not** need to navigate to this page manually.
>  
> If you do not see any files, make sure your last query returned blob data.


View files and blobs from your AnyLog queries.

### How to Use:

1. **Access Files:**
   - Files appear here when you run queries that return blob data
   - Files are automatically loaded from blob queries

2. **View Files:**
   - Click on any file to open it in full-screen mode
   - The system automatically detects file types (images, documents, etc.)

3. **Close Full-Screen:**
   - Click the "×" button to close full-screen view
   - Or click outside the file to return to grid view

4. **Navigate Files:**
   - Scroll through the grid to see all available files
   - Each file shows a preview thumbnail

### Tips:
- Files are loaded from blob queries in the Client Dashboard
- Supported file types include images, videos, audio, and more
- Use the Client Dashboard to run queries that return blob data

---

## Policies

Used for adding simple policies to the blockchain for convenience.

### How to Use:

1. **Add New Policy:**
   - Use the form to create a new simple policy.
   - Add key-value pairs by clicking the "Add" button for each pair you want to include.
   - When you submit the policy, the new policy's ID will be shown at the bottom of the form.

> **Note:** You cannot view or delete existing policies here. To view or delete policies, use the Blockchain Manager page.

### Tips:
- Policies control how your blockchain network operates
- Test policy changes in a safe environment first

---

## Add Data

Insert new data into AnyLog databases.

### How to Use:

1. **Select Database:**
   - Choose the target database from the dropdown

2. **Select Table:**
   - Choose the target table from the dropdown

3. **Enter Data:**
   - Add your data in the appropriate format
   - Follow the data structure for your table

4. **Submit Data:**
   - Click the submit button to insert the data
   - Check for confirmation messages

### Tips:
- Make sure you have the correct database and table selected
- Follow the data format expected by your table structure

---

## User Profile

Manage your user account and preferences.

### How to Use:

1. **View Profile:**
   - See your current user information

2. **Update Information:**
   - Modify your profile details

3. **Account Settings:**
   - Modify display options

### Tips:
- Keep your profile information up to date
- Check your account settings regularly
- Contact support if you need help with account issues

---

## Quick Reference

### Common Commands:
- `get status` - Check node status
- `blockchain get operator` - List network operators
- `run client () sql [database] format = table "SELECT * FROM [table]"` - Query database

### Navigation:
- **Sidebar**: Click any menu item to navigate
- **Top Bar**: Use node picker to switch nodes

### Getting Help:
- Check the browser console (F12) for error messages
- Verify your node is running and accessible
- Make sure you have the correct IP:Port format

---

*This guide covers all the main features of the Remote-GUI interface. Each page is designed to be intuitive, but don't hesitate to experiment with the different options available.*
