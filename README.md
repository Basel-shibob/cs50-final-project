# 💰 Cash Track: A Comprehensive Personal Finance Manager
#### Video Demo: https://youtu.be/dI2XiJElIvc
#### Description:

## Overview
**Cash Track** is a robust, user-centric web application designed to help individuals take control of their financial lives. In an era dominated by digital micro-transactions, keeping a manual ledger is no longer practical. Cash Track bridges this gap by providing a clean, efficient, and responsive platform to record every income and expense, calculate real-time balances, and maintain a historical record of all financial activities.

This project was developed as the final requirement for **Harvard University's CS50x: Introduction to Computer Science**.

## Why Cash Track? (Design Choices)
During the development process, several architectural and design decisions were made to balance simplicity with functionality:

1. **Relational Database vs. Flat Files**: I chose **SQLite** over simple text or CSV files because financial data is inherently relational. Using SQL allowed me to ensure data integrity, perform complex queries (like calculating total balances per user), and scale the application easily if more features like "Categories" or "Monthly Reports" are added later.
2. **Framework Choice**: **Flask** was selected as the backend framework due to its "micro" nature. It allowed me to build the routing logic and session management from scratch, providing a deeper understanding of how HTTP requests (GET and POST) interact with a database.
3. **Security First**: Security is paramount in finance. I implemented **Werkzeug**'s security helpers to hash passwords before storing them. This ensures that even if the database is compromised, user credentials remain protected.
4. **User Experience (UX)**: I opted for **Bootstrap 5** for the styling. My goal was a "Mobile-First" design. Whether a user is at a grocery store adding a small expense via their phone or at home reviewing their monthly salary on a desktop, the interface adjusts perfectly to the screen size.

## Deep Dive into the Project Files

### 1. `app.py`
This is the main controller of the entire application. It contains all the "routes" that define the user's journey.
- **Login/Register**: These routes handle user authentication, session creation, and input validation to prevent duplicate usernames.
- **Index (Home)**: This is the dashboard. It queries the `transactions` table to display a user's history and calculates the net balance.
- **Add/Delete**: These routes handle the "CRUD" operations (Create and Delete). I spent a lot of time ensuring that deleting a transaction correctly triggers a recalculation of the displayed balance.

### 2. `helpers.py`
To keep the code clean and follow the **DRY (Don't Repeat Yourself)** principle, I moved utility functions here. This includes the `login_required` decorator, which protects sensitive routes from unauthorized access, and a currency formatter to ensure all numbers look professional.

### 3. `layout.html` & Templates
Using **Jinja2 template inheritance**, I created a master `layout.html`. This file contains the navigation bar and the "Flash Messages" logic. All other pages (login, index, add) "inherit" from this layout, ensuring a consistent look and feel across the app without repeating HTML code.

### 4. `static/styles.css`
While Bootstrap handles the layout, I wrote custom CSS to fine-tune the aesthetics. I focused on color psychology—using success-green for positive flashes and primary-blue for informational messages to guide the user's emotions.

### 5. `requirements.txt`
This file is crucial for **reproducibility**. It lists every library (Flask, CS50 SQL, etc.) and its specific version, allowing any developer to recreate my environment with a single command: `pip install -r requirements.txt`.

## Challenges & Troubleshooting
One of the most significant learning moments during this project was debugging a **TypeError** in the Flash Message system. I discovered a naming conflict between Flask's `flash` function and a system library called `curses` on my Ubuntu machine. Resolving this required a deep dive into Python's import system and taught me the importance of namespace management.

Another challenge was managing the **Connection** logic. I had to ensure that the database connection remained stable during multiple POST requests, which helped me understand the lifecycle of a web application.

## Conclusion
Cash Track is the culmination of everything I learned in CS50x—from C's logic and SQL's structure to Python's versatility and Web Development's creativity. It represents my transition from a background in accounting to the world of software engineering.

## 💻 How to Run
1. Clone the repository.
2. Install dependencies: `pip install -r requirements.txt`.
3. Run the app: `flask run`.

**This was CS50!**

---
*Created by Mohamed Shibob (Basel) - March 2026*