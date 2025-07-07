# 🌍 Travel Website (Django)

A simple and elegant **Travel Website** built with **Django**, allowing:

- **Admin** users to add, edit, and manage travel packages  
- **Users** to browse travel details, view more info, and download travel details as PDF files

---

## 🚀 Features

- Admin panel to **manage travel packages** (title, destination, dates, price, description)
- User-friendly frontend to **list all trips** and see detailed views
- PDF generation support for travel package details (using `xhtml2pdf` or `WeasyPrint`)
- Responsive UI built with Bootstrap (can be customized)

---

## 🛠️ Technology Stack

- Backend: Python 3, Django
- Database: SQLite (default, easy to switch)
- Frontend: HTML, CSS, Bootstrap
- PDF Generation: `xhtml2pdf` or `WeasyPrint`

---

## ⚙️ Getting Started

### Prerequisites

- Python 3.x installed
- Git installed

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/prashanthchaduvala/-Travel-Website-Django-.git
   cd Travel-Website-Django
2.Create and activate a virtual environment:
  python -m venv tours-env
  source tours-env/bin/activate   # Linux/macOS
  .\tours-env\Scripts\activate    # Windows

3.Install dependencies:
  pip install -r requirements.txt

4.Apply migrations:
  python manage.py migrate

5.Create a superuser to access the admin panel:
  python manage.py createsuperuser
6.Run the development server: 
  python manage.py runserver

