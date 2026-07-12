# 🗄️ HELP: Optimal Firebase Database Model

Detailed setup for your growth history database.

### 📜 Realtime Database Strategy
1.  **Project Name**: `Cucumber-Smart-System`
2.  **Database URL**: Copy your database URL (looks like `https://xxx.firebaseio.com/`).
3.  **Security Rules**: For development, set them to:
    ```json
    {
      "rules": {
        ".read": "true",
        ".write": "true"
      }
    }
    ```

### 🚀 Creating the Service Key (.json)
1.  **Console**: Project Settings (⚙️) > Service Accounts.
2.  **Generate**: Click "Generate New Private Key".
3.  **Save**: Download the file.
4.  **RENAME**: You **MUST** rename this file to exactly `firebase_key.json`.
5.  **FOLDER**: Put it in your main project folder.

### 📂 Data Structure
The app will automatically create this structure for you:
- `/detections/{timestamp}`: Full history of every run.
- `/latest`: Shows only the most recent measurement for the dashboard.

### 📡 Connection Settings
Update `configs/settings.yaml`:
```yaml
cloud:
  firebase_enabled: true
  firebase_db_url: "PASTE_YOUR_DATABASE_URL_HERE"
```
