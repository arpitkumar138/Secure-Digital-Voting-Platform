# 🛡️ Secure Digital Voting Platform

A modern, highly secure multi-stage electronic voting application built with **Python**, **Streamlit**, and **SQLite3**. This platform ensures strict identity verification and prevents duplicate voting through automated database locking.

---

## ✨ Features

* **3-Step Authentication Flow:**
  * **Step 1:** Electoral Voter ID validation against the database.
  * **Step 2:** 12-digit Government ID verification paired with Live Webcam Face Biometric capture.
  * **Step 3:** Locked ballot selection for political party candidates.
* **Database-Level One-Time Voting Lock:** Prevents any voter from casting multiple votes by locking their status once submitted.
* **Selection Lock Feature:** Freezes candidate choices prior to final confirmation to eliminate accidental vote changes.
* **Admin Control Panel:** Sidebar-integrated database reset tool designed for rapid testing and session management.
* **Responsive & Modern UI:** Styled with a dark theme layout using custom CSS for a clean user experience.

---

## 🛠️ Tech Stack

* **Language:** Python
* **Frontend/Framework:** Streamlit
* **Database:** SQLite3
* **Version Control:** Git & GitHub

---

## 🚀 How to Run Locally

### 1. Prerequisites
Ensure you have Python installed on your system.

### 2. Clone the Repository
```bash
git clone [https://github.com/arpitkumar138/Secure-Digital-Voting-Platform.git](https://github.com/arpitkumar138/Secure-Digital-Voting-Platform.git)
cd Secure-Digital-Voting-Platform
