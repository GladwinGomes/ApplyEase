# ApplyEase Chrome Extension

This Manifest V3 Chrome extension lets you autofill job application forms using your ApplyEase profile and log submitted applications directly to your tracker.

## Loading Unpacked in Chrome

1. Start the ApplyEase Django server locally at `http://localhost:8000`.
2. Open Google Chrome and navigate to `chrome://extensions/`.
3. Enable **Developer mode** using the toggle in the top-right corner.
4. Click **Load unpacked**.
5. Select the `extension/` directory inside your `ApplyEase` project folder.
6. Pin the **ApplyEase Autofill & Tracker** extension to your toolbar.

## Usage

1. Click the extension icon and sign in with your ApplyEase email and password.
2. Navigate to any job application form (e.g., `/mock-forms/form1/`).
3. Click **Fill Form** to autofill matching fields.
4. Click **Log Application** to save the current page to your ApplyEase tracker.
