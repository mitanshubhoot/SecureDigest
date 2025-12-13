# SecureDaily - Enterprise Security Intelligence

![SecureDaily Logo](https://img.shields.io/badge/SecureDaily-Enterprise%20Security%20Intelligence-0F4C81?style=for-the-badge&logo=shield&logoColor=white)

**Enterprise Security Intelligence, Delivered Daily**

SecureDaily is a professional security intelligence platform that delivers curated security insights, best practices, and risk management guidance to enterprise security teams. Built with modern web technologies and designed for scalability.

---

## 🎯 Features

- **Daily Security Briefings**: Curated security intelligence delivered daily
- **Professional UI**: Enterprise-grade design with glassmorphism and modern aesthetics
- **Color-Coded Insights**: Visual categorization (Tips, Checks, Patterns)
- **Responsive Design**: Mobile-first, works on all devices
- **Fast & Lightweight**: Built with FastAPI for optimal performance
- **Easy Deployment**: One-click deployment to Render

---

## 🚀 Quick Start

### Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/mitanshubhoot/SecureDigest.git
   cd SecureDigest
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

5. **Open in browser**
   ```
   http://localhost:8000
   ```

---

## 📦 Project Structure

```
SecureDigest/
├── app/
│   ├── main.py              # FastAPI application
│   ├── static/
│   │   └── styles.css       # Enterprise styling
│   └── templates/
│       ├── index.html       # Homepage
│       └── digest.html      # Digest detail page
├── digests/                 # JSON digest storage
│   └── 2025-12-13.json     # Example digest
├── scripts/
│   └── generate_digest.py   # Digest generation script
├── .github/
│   └── workflows/
│       └── daily-digest.yml # GitHub Actions workflow
├── requirements.txt         # Python dependencies
├── render.yaml             # Render deployment config
└── README.md               # This file
```
---

## Configuration

### Adding New Digests

Digests are stored as JSON files in the `digests/` folder:

```json
{
  "date": "2025-12-13",
  "headline": "Your Security Briefing Headline",
  "digest_items": [
    {
      "type": "tip",
      "title": "Security Tip Title",
      "why": "Why this matters...",
      "fix": "Recommended action..."
    }
  ]
}
```

**Item Types:**
- `tip`: Information and best practices (Cyan)
- `check`: Warnings and actions needed (Orange)
- `pattern`: Security patterns (Sky Blue)

---

## 📊 API Endpoints

SecureDaily provides a simple REST API:

### Get All Digests
```
GET /api/digests
```
Returns a list of all available digests.

### Get Specific Digest
```
GET /digest/{date}
```
Returns the digest for a specific date (format: `YYYY-MM-DD`).

---

## 🛠️ Technology Stack

- **Backend**: FastAPI (Python)
- **Frontend**: HTML5, CSS3, Jinja2 Templates
- **Deployment**: Render
- **Automation**: GitHub Actions
- **Fonts**: Google Fonts (Inter)
- **Icons**: SVG (custom shield logo)

---

## 🔒 Security

SecureDaily is designed with security best practices:

- ✅ No external dependencies for frontend (self-hosted fonts optional)
- ✅ Static file serving with proper MIME types
- ✅ CORS configured for API access
- ✅ No sensitive data stored in repository
- ✅ Environment variables for configuration

---

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📧 Contact

**Mitanshu Bhoot**
- GitHub: [@mitanshubhoot](https://github.com/mitanshubhoot)
- Repository: [SecureDigest](https://github.com/mitanshubhoot/SecureDigest)

---

**SecureDaily** - Enterprise Security Intelligence, Delivered Daily 🛡️
