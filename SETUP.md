# GitHub Setup Instructions

Follow these steps to deploy your Mensa Calendar to GitHub with automated daily updates.

## Prerequisites

- A GitHub account
- Git installed on your computer
- Python 3.11+ installed locally (for testing)

## Step 1: Test Locally

Before deploying to GitHub, test that everything works locally:

```bash
cd /path/to/your/project
python test_setup.py
```

This will verify that:
- Dependencies install correctly
- The main script runs without errors
- The `mensa.ics` file is generated properly

## Step 2: Create GitHub Repository

1. Go to [GitHub.com](https://github.com) and sign in
2. Click the "+" icon in the top right and select "New repository"
3. Choose a repository name (e.g., `mensa-calendar`)
4. Make sure it's set to **Public** (required for raw file access)
5. Don't initialize with README, .gitignore, or license (we already have them)
6. Click "Create repository"

## Step 3: Push Code to GitHub

In your project directory, run these commands (replace with your actual GitHub username and repository name):

```bash
# Initialize git repository
git init

# Add all files
git add .

# Make initial commit
git commit -m "Initial commit: Mensa calendar generator"

# Add GitHub remote (replace YOUR_USERNAME and YOUR_REPO_NAME)
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git

# Push to GitHub
git branch -M main
git push -u origin main
```

## Step 4: Verify GitHub Action

1. Go to your repository on GitHub
2. Click on the "Actions" tab
3. You should see the "Update Mensa Calendar" workflow
4. The workflow will run automatically every day at 5 AM UTC
5. You can also trigger it manually by clicking "Run workflow"

## Step 5: Get Your Calendar URL

Once deployed, your calendar will be available at:
```
https://raw.githubusercontent.com/YOUR_USERNAME/YOUR_REPO_NAME/main/mensa.ics
```

Replace `YOUR_USERNAME` and `YOUR_REPO_NAME` with your actual values.

## Step 6: Subscribe to Calendar

### Google Calendar
1. Go to [Google Calendar](https://calendar.google.com)
2. Click the "+" next to "Other calendars"
3. Select "From URL"
4. Paste your calendar URL
5. Click "Add calendar"

### Outlook
1. Go to [Outlook.com](https://outlook.com)
2. Click "Add calendar" → "Subscribe from web"
3. Paste your calendar URL
4. Give it a name like "Mensa Stuttgart Vaihingen"
5. Click "Import"

### Apple Calendar (macOS/iOS)
1. Open Calendar app
2. File → New Calendar Subscription (macOS) or Settings → Accounts → Add Account → Other (iOS)
3. Paste your calendar URL
4. Configure refresh frequency (recommend daily)

### Thunderbird
1. Right-click in the calendar list
2. Select "New Calendar" → "On the Network"
3. Choose "CalDAV" and paste your URL
4. Follow the setup wizard

## Troubleshooting

### GitHub Action Permission Denied (403 Error)
If you see an error like `Permission to username/repo.git denied to github-actions[bot]`:

1. Go to your repository on GitHub
2. Click on "Settings" tab
3. Scroll down to "Actions" in the left sidebar
4. Click on "General"
5. Under "Workflow permissions", select "Read and write permissions"
6. Check "Allow GitHub Actions to create and approve pull requests"
7. Click "Save"

Alternatively, you can check if the workflow has the correct permissions in the YAML file (which should already be set).

### GitHub Action Not Running
- Check that your repository is public
- Verify the workflow file is in `.github/workflows/update-calendar.yml`
- Check the Actions tab for error messages

### Calendar Not Updating
- The action runs at 5 AM UTC daily
- You can manually trigger it from the Actions tab
- Check if the mensa API is accessible

### Calendar App Not Refreshing
- Most calendar apps refresh subscribed calendars every few hours to daily
- You can usually force a refresh in the calendar settings
- Some apps may cache the calendar data

## Manual Updates

To manually update the calendar:

```bash
# Pull latest changes
git pull

# Run the script
python main.py

# Commit and push changes
git add mensa.ics
git commit -m "Manual calendar update"
git push
```

## Customization

### Change Update Time
Edit `.github/workflows/update-calendar.yml` and modify the cron expression:
```yaml
- cron: '0 5 * * *'  # 5 AM UTC daily
```

### Different Mensa
Modify the URL in `main.py` to point to a different mensa API endpoint.

### Calendar Properties
Modify the calendar properties in `main.py`:
- `prodid`: Product identifier
- Event summaries and descriptions
- All-day vs timed events
