# CPSC-491-Capstone-Project
CPSC 491 Capstone Project (Credible Sorcerer)

# 🧙‍♂️ Credible Sorcerer

**AI-Powered Article & PDF Credibility Analyzer**

---

## 📌 Overview

Credible Sorcerer is a web application that analyzes the credibility of online articles and PDF documents using a combination of:

* Natural Language Processing (NLP)
* AI-powered summarization
* Metadata extraction
* AI detection scoring

The system evaluates sources and presents users with a **credibility score**, **summary**, and **detailed breakdown** of factors influencing trustworthiness.

---

## 🚀 Features

* 🔗 **URL Analysis** – Paste any article link for instant analysis
* 📄 **PDF Upload Support** – Upload research papers or documents
* 🧠 **AI Summarization** – Concise summaries and key points
* ⚖️ **Credibility Scoring System** – Based on metadata, authorship, citations, and AI detection
* 📊 **Visual Score Breakdown** – Interactive progress bars for each factor
* 🔎 **Related Articles** – Academic-style references using search queries

---

## 🖥️ How to Use

### 1. Open the Website

Navigate to the deployed site:

```
[https://your-frontend-url.netlify.app](https://cpsc491capstone.netlify.app)
```

---

### 2. Choose Input Type

You can analyze content in two ways:

#### Option A: Analyze a URL

* Paste a valid article URL into the input field
* Click **"Analyze Article"**

#### Option B: Upload a PDF

* Click the file input box
* Upload a `.pdf` document
* Click **"Analyze Article"**

> ⚠️ Only one input method should be used at a time

---

### 3. Wait for Processing

* A loading spinner will appear
* The system will:

  * Extract content
  * Analyze text using AI
  * Calculate credibility score

---

### 4. View Results (Report Page)

You will be redirected automatically to the **Report Page**, which includes:

* 📄 Document summary
* 👤 Author and publication info
* 📊 Overall credibility score
* 🧾 Quick analysis summary (metadata, citations, AI confidence)

---

### 5. Explore Further

#### 🔍 Detailed Report

* View document preview
* See key points and related articles

#### 📊 Score Page

* View full breakdown:

  * Title / Metadata
  * Authorship
  * Publication Date
  * Citations
  * AI Detection

---

## 🧠 How Scoring Works

The credibility score is calculated out of **100 points**, based on:

| Category          | Weight |
| ----------------- | ------ |
| Title / Metadata  | 10     |
| Authorship        | 30     |
| Publication Date  | 15     |
| Citations / Links | 5      |
| AI Detection      | 40     |

* Higher scores indicate stronger credibility
* AI-generated content reduces credibility proportionally

---

## 🏗️ Tech Stack

### Frontend

* HTML, CSS (Bootstrap)
* JavaScript (Fetch API)

### Backend

* FastAPI (Python)
* OpenAI API (text analysis)
* Sapling API (AI detection)
* PyMuPDF (PDF extraction)
* BeautifulSoup (web scraping)

### Deployment

* Frontend: Netlify
* Backend: Render

---

## ⚠️ Limitations

* AI detection is probabilistic, not definitive
* Some websites may block scraping
* PDF extraction depends on document structure
* Results should be used as guidance, not absolute truth

---

## 📌 Future Improvements

* Improved UI/UX and animations
* Better citation validation
* Multi-language support
* User accounts and saved reports

---

## 👨‍💻 Authors

* Nathan Hendratno
* Liyuhan Zhou
* Jake Mendez
* Seamus Flanagan

---

## 📄 License

This project is for academic and educational purposes.

---

## ✨ Final Note

Credible Sorcerer is designed to help users **think critically about information sources**, not replace human judgment. Always verify important information through multiple trusted sources.

---
