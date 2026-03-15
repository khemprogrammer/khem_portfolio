# Khem Bahadur Lodh - Portfolio Website

A modern, professional, and fully responsive portfolio website built with Django for Python Developer Khem Bahadur Lodh.

![Django](https://img.shields.io/badge/Django-5.0-green)
![Python](https://img.shields.io/badge/Python-3.10+-blue)
![License](https://img.shields.io/badge/License-MIT-yellow)

## Features

- **Modern Design**: Dark theme with gradient accents and smooth animations
- **Fully Responsive**: Mobile-first design that works on all devices
- **GitHub Integration**: Automatic fetching of repositories and stats
- **Admin Dashboard**: Easy content management via Django Admin
- **Contact Form**: With spam protection and email notifications
- **SEO Optimized**: Meta tags, structured data, and semantic HTML
- **Fast Loading**: Optimized static files and caching ready

## Pages

1. **Home** - Hero section with animated code window, stats, featured projects
2. **About** - Professional bio, highlights, education timeline
3. **Skills** - Technical skills with proficiency levels
4. **Projects** - Portfolio with filtering, search, and GitHub sync
5. **Experience** - Work history and focus areas
6. **Contact** - Contact form with validation

## Technology Stack

### Backend
- Python 3.10+
- Django 5.0
- PostgreSQL
- Django ORM
- Requests (GitHub API)

### Frontend
- HTML5
- CSS3
- Bootstrap 5
- JavaScript (Vanilla)
- Font Awesome
- Google Fonts (Inter)

## Installation

### Prerequisites
- Python 3.10 or higher
- pip
- Virtual environment (recommended)

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/khemprogrammer/portfolio.git
   cd portfolio
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Create environment file**
   ```bash
   cp .env.example .env
   ```
   Edit `.env` and update the settings:
   ```
   SECRET_KEY=your-secret-key-here
   DEBUG=True
   ALLOWED_HOSTS=localhost,127.0.0.1
   GITHUB_USERNAME=khemprogrammer
   ```

5. **Run migrations**
   ```bash
   python manage.py migrate
   ```

6. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

7. **Load initial data (optional)**
   ```bash
   python manage.py shell < initial_data.py
   ```

8. **Run development server**
   ```bash
   python manage.py runserver
   ```

9. **Access the website**
   - Portfolio: http://127.0.0.1:8000/
   - Admin: http://127.0.0.1:8000/admin/

## Project Structure

```
portfolio_project/
├── portfolio_project/      # Main Django project
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── portfolio/             # Portfolio app
│   ├── models.py          # Profile, Skills, Experience
│   ├── views.py
│   ├── admin.py
│   └── urls.py
├── projects/              # Projects app
│   ├── models.py          # Projects, Technologies
│   ├── github_api.py      # GitHub API integration
│   ├── views.py
│   └── admin.py
├── contact/               # Contact app
│   ├── models.py          # Contact messages
│   ├── forms.py
│   └── views.py
├── templates/             # HTML templates
│   ├── base.html
│   ├── portfolio/
│   ├── projects/
│   └── contact/
├── static/                # Static files
│   ├── css/
│   ├── js/
│   └── images/
├── media/                 # User uploaded files
├── requirements.txt
└── manage.py
```

## GitHub API Integration

The portfolio automatically fetches GitHub statistics:
- Public repositories count
- Total stars and forks
- Top programming languages
- Recent repositories

To enable:
1. Set `GITHUB_USERNAME` in your `.env` file
2. (Optional) Add `GITHUB_TOKEN` for higher rate limits

## Admin Dashboard

Access `/admin/` to manage:
- **Portfolio**: Profile, Skills, Experience, Education
- **Projects**: Add/edit projects with categories and technologies
- **Contact**: View and manage contact messages

## Deployment

### Deploy to Render (Recommended)

1. Create a `render.yaml`:
   ```yaml
   services:
     - type: web
       name: khem-portfolio
       runtime: python
       buildCommand: pip install -r requirements.txt
       startCommand: gunicorn portfolio_project.wsgi:application
       envVars:
         - key: SECRET_KEY
           generateValue: true
         - key: DEBUG
           value: "False"
   ```

2. Connect your GitHub repository to Render

3. Deploy automatically on push

### Deploy to Railway

1. Install Railway CLI
2. Run `railway login`
3. Run `railway init`
4. Run `railway up`

### VPS Deployment

1. Install requirements on server
2. Set up Gunicorn and Nginx
3. Configure environment variables
4. Run collectstatic

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `SECRET_KEY` | Django secret key | Required |
| `DEBUG` | Debug mode | True |
| `ALLOWED_HOSTS` | Allowed hosts | localhost |
| `DB_NAME` | PostgreSQL database name | portfolio_db |
| `DB_USER` | PostgreSQL user | postgres |
| `DB_PASSWORD` | PostgreSQL password | Required |
| `DB_HOST` | Database host | localhost |
| `DB_PORT` | Database port | 5432 |
| `GITHUB_USERNAME` | GitHub username | khemprogrammer |
| `GITHUB_TOKEN` | GitHub API token | None |
| `EMAIL_HOST` | SMTP host | localhost |
| `EMAIL_PORT` | SMTP port | 587 |

## Customization

### Changing Colors
Edit `static/css/style.css` and modify CSS variables:
```css
:root {
    --primary: #6366f1;
    --secondary: #ec4899;
    /* ... */
}
```

### Adding Projects
1. Log in to admin panel
2. Go to Projects → Add Project
3. Fill in details and upload images
4. Link to GitHub repository for auto-sync

### Updating Skills
1. Go to Portfolio → Skill Categories
2. Add categories and skills
3. Mark featured skills to show on homepage

## License

This project is licensed under the MIT License.

## Author

**Khem Bahadur Lodh**
- GitHub: [@khemprogrammer](https://github.com/khemprogrammer)
- Location: Nepal
- Email: contact@khemlodh.com.np

## Acknowledgments

- Bootstrap 5 for responsive components
- Font Awesome for icons
- Google Fonts for typography
- Django community for the amazing framework