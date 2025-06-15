# LINE Bot Game Role Assigner

This application is a LINE chatbot designed to manage and assign roles for social deduction games like Spyfall and Insider. An admin can control the game state, start games, and clear the lobby through a web-based admin panel, while players interact with the bot through your LINE Official Account.

The application is built with Python using the Flask framework and the `line-bot-sdk`. It uses `ngrok` to create a secure, public URL, allowing the LINE servers to communicate with the application running on your local machine.

---

## Prerequisites

Before you begin, ensure you have the following:

1.  **Python 3.7+**: Make sure Python is installed on your system.
2.  **LINE Developers Account**: You need an account to create a bot. You can sign up at the [LINE Developers Console](https://developers.line.biz/).
3.  **ngrok Account**: Required to create a public URL. A free account is sufficient.
    * Sign up at [ngrok.com](https://ngrok.com).
    * Install your authtoken by running the command provided on your [ngrok dashboard](https://dashboard.ngrok.com/get-started/your-authtoken).

---

## ⚙️ Setup Instructions

Follow these steps to get your application running.

### 1. Set Up Project Files

Ensure all project files are in a single folder with the following structure:

```
/project-folder
|
|-- templates/
|   |-- admin.html
|
|-- build/
|   |-- config.py
|   |-- game_logic.py
|   |--bot_handlers.py
|   |--admin_routes.py
|   |--app.py
|-- requirements.txt
|-- .env (Local environment variables)
```

### 2. Install Dependencies

Open your terminal, navigate to your project folder, and run the following command to install all the necessary Python packages:

```bash
pip install -r requirements.txt
```

### 3. Configure Credentials

1.  Open the `config.py` file.
2.  Replace `"YOUR_CHANNEL_SECRET"` and `"YOUR_CHANNEL_ACCESS_TOKEN"` with the actual credentials from your LINE Developers Console. You can find these under the "Messaging API" tab for your channel.

---

## ▶️ Running the Application

1.  **Start the Server**
    In your terminal, from the project folder, run the main script:
    ```bash
    python3 app.py
    ```

2.  **Update the LINE Webhook URL**
    * When the script starts, it will print an `ngrok` URL in the terminal. It will look like this:
        ```
        !!! IMPORTANT: Webhook URL: [https://only-optimal-pheasant.ngrok-free.app/callback](https://only-optimal-pheasant.ngrok-free.app/callback)
        ```
    * Copy the full Webhook URL (`https://.../callback`).
    * Go to your [LINE Developers Console](https://developers.line.biz/).
    * Navigate to your channel's "Messaging API" settings.
    * In the "Webhook URL" field, paste the URL you copied and click **Update**, then **Verify**.

3.  **Access the Admin Panel**
    * The terminal will also print the URL for the Admin Panel:
        ```
        Admin Panel: [https://only-optimal-pheasant.ngrok-free.app/admin](https://only-optimal-pheasant.ngrok-free.app/admin)
        ```
    * Open this URL in your web browser to control the game.

The application is now ready to use. Players can add your LINE bot as a friend and type their names to join the lobby.# line_chat_bot
