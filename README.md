# StockMaster - Django Stock Management System

## Project Structure

```
stock_management_system/
├── stockmaster/              # Main project directory
│   ├── __init__.py
│   ├── settings.py           # Project settings
│   ├── urls.py               # Main URL routing
│   ├── asgi.py               # ASGI configuration
│   └── wsgi.py               # WSGI configuration
├── stock/                    # Main app directory
│   ├── migrations/           # Database migrations
│   ├── __init__.py
│   ├── admin.py              # Admin site configuration
│   ├── apps.py               # App configuration
│   ├── forms.py              # Form definitions
│   ├── models.py             # Database models
│   ├── tests.py              # Test cases
│   ├── urls.py               # App URL routing
│   └── views.py              # View functions and logic
├── templates/                # HTML templates
│   ├── base.html             # Base template with common layout
│   └── stock/                # App-specific templates
│       ├── login.html        # Login page
│       ├── register.html     # Registration page
│       ├── dashboard.html    # Main dashboard
│       ├── profile.html      # User profile
│       ├── add_supervisor.html # Admin-only supervisor creation
│       ├── stock_list.html   # Inventory listing
│       ├── stock_detail.html # Product details
│       └── add_stock.html    # Add new product
├── static/                   # Static files
│   └── css/
│       └── style.css         # Custom CSS styles
├── media/                    # User-uploaded files (created at runtime)
│   ├── products/             # Product images
│   └── profile_images/       # User profile images
├── manage.py                 # Django management script
└── db.sqlite3                # SQLite database (created at runtime)
```

## Models

### User Model
- Custom user model with role-based permissions
- Roles: Admin, Supervisor, Client, Supplier, Virtual Assistant
- Extended with profile fields (phone_number, user_address, profile_image)

### Product Models
- Category: Product categories
- Product: Inventory items with stock tracking
- Supplier: Product suppliers

### Order Models
- Order: Customer orders with status tracking
- OrderItem: Individual items within an order

### Stock Models
- StockTransaction: Tracks stock movements (in/out)
- Alert: System alerts for low stock, etc.

### Communication Models
- Message: Internal messaging system

## API Endpoints

### Authentication
- `/login/` - User login
- `/register/` - Client registration
- `/logout/` - User logout

### Dashboard
- `/` - Main dashboard (role-specific)

### Profile Management
- `/profile/` - View user profile
- `/profile/update/` - Update profile information
- `/profile/image/update/` - Update profile image

### Admin Functions
- `/supervisors/add/` - Add supervisor account (admin only)

### Stock Management
- `/stock/` - List all stock items
- `/stock/<id>/` - View stock details
- `/stock/add/` - Add new stock
- `/stock/<id>/edit/` - Edit stock item
- `/stock/<id>/delete/` - Delete stock item

### Category Management
- `/categories/add/` - Add new category

### Export Functions
- `/export/stock/csv/` - Export stock data to CSV

## Setup Instructions

### Prerequisites
- Python 3.8 or higher
- Django 4.2 or higher
- Pillow (for image processing)

### Installation

1. Clone the repository:
```
git clone <repository-url>
cd stock_management_system
```

2. Create a virtual environment and activate it:
```
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```
pip install django pillow
```

4. Apply migrations:
```
python manage.py migrate
```

5. Create a superuser (admin):
```
python manage.py createsuperuser
```

6. Run the development server:
```
python manage.py runserver
```

7. Access the application at http://127.0.0.1:8000/

### User Roles and Permissions

- **Admin**: Full access to all features, can create supervisor accounts
- **Supervisor**: Can manage inventory, validate orders, and generate reports
- **Client**: Can browse products, place orders, and manage their profile
- **Supplier**: Can view and update product availability
- **Virtual Assistant**: Can analyze stock levels and respond to client messages

### Business Rules

1. Only administrators can create supervisor accounts
2. Only clients can self-register if their account doesn't exist
3. Stock levels are automatically tracked with every transaction
4. Low stock alerts are generated when quantity falls below reorder level

## Customization

### Adding New Features

1. Define models in `stock/models.py`
2. Create forms in `stock/forms.py`
3. Implement views in `stock/views.py`
4. Add URL patterns in `stock/urls.py`
5. Create templates in `templates/stock/`

### Styling

The UI is based on Bootstrap 5 with custom styling in `static/css/style.css`.
