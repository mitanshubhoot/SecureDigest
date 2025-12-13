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

## 🌐 Deploy to Render

### Option 1: One-Click Deploy (Recommended)

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy)

### Option 2: Manual Deployment

1. **Create a Render account** at [render.com](https://render.com)

2. **Create a new Web Service**
   - Click "New +" → "Web Service"
   - Connect your GitHub repository: `mitanshubhoot/SecureDigest`

3. **Configure the service**
   - **Name**: `securedigests` (or your preferred name)
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

4. **Set environment variables** (optional)
   - `PYTHON_VERSION`: `3.11.0`

5. **Deploy**
   - Click "Create Web Service"
   - Render will automatically deploy your application
   - Your app will be live at: `https://securedigests.onrender.com`

### Using render.yaml (Blueprint)

This repository includes a `render.yaml` file for automated deployment:

1. In Render dashboard, click "New +" → "Blueprint"
2. Connect your GitHub repository
3. Render will automatically detect `render.yaml` and configure everything
4. Click "Apply" to deploy

---

## 🔄 Automated Daily Digests

SecureDaily includes a GitHub Actions workflow that automatically generates daily security digests.

### Setup GitHub Actions

The workflow is already configured in `.github/workflows/daily-digest.yml`. It runs daily at 9 AM UTC.

**To enable:**
1. Ensure the workflow file exists in your repository
2. GitHub Actions will automatically run on schedule
3. New digests are committed to the `digests/` folder daily

**Manual trigger:**
```bash
# Run the digest generation script locally
python scripts/generate_digest.py
```

---

## 🎨 Design System

SecureDaily uses a professional enterprise color palette inspired by leading security products:

### Color Palette

| Color | Hex | Usage |
|-------|-----|-------|
| Deep Ocean Blue | `#0F4C81` | Primary brand, trust |
| Sky Blue | `#0EA5E9` | Accents, highlights |
| Vibrant Orange | `#FF6B35` | Action, warnings |
| Cyan | `#06B6D4` | Information (Tips) |

### Typography
- **Font**: Inter (Google Fonts)
- **Weights**: 400 (body), 600-700 (headings), 800 (brand)

### Components
- **Glassmorphism**: Frosted glass cards with backdrop blur
- **Gradients**: Blue-based gradients for depth
- **Animations**: Smooth micro-animations for polish

---

## 🔧 Configuration

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

## 🙏 Acknowledgments

- Design inspired by enterprise security products (UpGuard, ProjectDiscovery)
- Built with FastAPI and modern web technologies
- Glassmorphism design trend for modern UI

---

**SecureDaily** - Enterprise Security Intelligence, Delivered Daily 🛡️
