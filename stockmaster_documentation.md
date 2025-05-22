# StockMaster - Comprehensive Documentation

## Table of Contents

1. [Introduction](#introduction)
2. [System Architecture](#system-architecture)
3. [User Roles and Access Control](#user-roles-and-access-control)
4. [Client Application](#client-application)
5. [Admin/Supervisor Application](#adminsupervisor-application)
6. [Installation and Setup](#installation-and-setup)
7. [Development Guidelines](#development-guidelines)
8. [API Reference](#api-reference)
9. [Troubleshooting](#troubleshooting)

## Introduction

StockMaster is a comprehensive inventory and order management system designed to handle stock tracking, order processing, and user management through a role-based access control system. The application is built using Django and follows the Model-View-Controller (MVC) architecture pattern.

### Key Features

- **Role-Based Access Control**: Separate interfaces for clients, supervisors, and administrators
- **Inventory Management**: Track stock levels, categories, and suppliers
- **Order Processing**: Handle customer orders from placement to delivery
- **User Management**: Manage users with different roles and permissions
- **Reporting and Analytics**: Generate reports and visualize data
- **Responsive Design**: Mobile-friendly interface with collapsible sidebar

### Technology Stack

- **Backend**: Django (Python)
- **Frontend**: HTML, CSS, JavaScript, Bootstrap 5
- **Database**: SQLite (development), PostgreSQL (production)
- **UI Libraries**: Font Awesome, Chart.js
- **Authentication**: Django Authentication System

## System Architecture

StockMaster follows a modular MVC architecture with clear separation of concerns between client and admin/supervisor interfaces.

### Application Structure

The application is divided into three main modules:

1. **Core Module**: Contains shared models, utilities, and middleware
2. **Client Application**: Handles product catalog browsing and order placement
3. **Admin Portal**: Manages inventory, users, orders, and reporting

### MVC Implementation

- **Models (M)**: Define data structure and business logic
- **Views (V)**: Render the user interface
- **Controllers (C)**: Process user input and manage application flow

### Authentication Flow

1. Users access the shared login page
2. After authentication, users are redirected to their role-specific dashboard
3. Role-based middleware ensures users can only access authorized sections

## User Roles and Access Control

StockMaster implements a comprehensive role-based access control system with three primary roles:

### Client Role

- **Access Level**: Limited to client application
- **Permissions**:
  - Browse product catalog
  - Place and track orders
  - Manage personal profile
  - View order history

### Supervisor Role

- **Access Level**: Admin portal with restricted permissions
- **Permissions**:
  - Manage inventory (add, edit, delete products)
  - Process orders
  - Generate reports
  - Cannot manage users or create other supervisors

### Administrator Role

- **Access Level**: Full access to admin portal
- **Permissions**:
  - All supervisor permissions
  - User management (create, edit, delete)
  - Create supervisor accounts
  - System configuration
  - Access to all reports and analytics

## Client Application

The client application provides a streamlined interface for customers to browse products and place orders.

### Dashboard

The client dashboard displays:
- Recent orders
- Order status updates
- Featured products
- Account summary

### Product Catalog

The catalog section allows clients to:
- Browse products by category
- Search for specific items
- View detailed product information
- Add products to cart

### Order Management

Clients can manage their orders through:
- Shopping cart functionality
- Order placement
- Order history
- Order tracking

### Profile Management

Clients can manage their profile information:
- Personal details
- Contact information
- Password changes
- Profile image

## Admin/Supervisor Application

The admin portal provides comprehensive management tools for supervisors and administrators.

### Dashboard

The admin dashboard displays:
- Inventory overview
- Recent orders
- Low stock alerts
- Sales analytics
- System notifications

### Inventory Management

Administrators and supervisors can manage inventory through:
- Product listing with filtering and search
- Add/edit/delete products
- Category management
- Supplier management
- Stock level tracking
- Low stock alerts

### Order Processing

Order management features include:
- Order listing with status filtering
- Order details view
- Status updates (approve, ship, deliver, cancel)
- Order history
- Customer communication

### User Management (Admin Only)

Administrators can manage users through:
- User listing with role filtering
- Add/edit/delete users
- Create supervisor accounts
- Role assignment
- Account activation/deactivation

### Reporting and Analytics

The reporting section provides:
- Sales reports
- Inventory reports
- User activity reports
- Export functionality (CSV, PDF)
- Visual charts and graphs

## Installation and Setup

### Prerequisites

- Python 3.8+
- pip (Python package manager)
- Git

### Development Setup

1. Clone the repository:
   ```
   git clone https://github.com/MohamedMBG/stockmaster.git
   cd stockmaster
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Apply migrations:
   ```
   python manage.py migrate
   ```

5. Create a superuser:
   ```
   python manage.py createsuperuser
   ```

6. Run the development server:
   ```
   python manage.py runserver
   ```

7. Access the application at http://127.0.0.1:8000/

### Production Deployment

For production deployment, additional steps are required:

1. Update settings in `stockmaster/settings.py`:
   - Set `DEBUG = False`
   - Configure `ALLOWED_HOSTS`
   - Set up a production database (PostgreSQL recommended)
   - Configure static files storage

2. Collect static files:
   ```
   python manage.py collectstatic
   ```

3. Set up a production web server (Nginx, Apache) with WSGI (Gunicorn, uWSGI)

4. Configure SSL for secure connections

5. Set up database backups

## Development Guidelines

### Coding Standards

- Follow PEP 8 for Python code
- Use Django's coding style for templates and models
- Implement proper docstrings and comments
- Follow the MVC pattern consistently

### Git Workflow

- Use feature branches for new development
- Create pull requests for code review
- Write descriptive commit messages
- Keep commits focused and atomic

### Testing

- Write unit tests for models and views
- Implement integration tests for workflows
- Test across different devices and browsers
- Verify role-based access control

## API Reference

StockMaster provides a set of internal APIs for frontend-backend communication.

### Authentication Endpoints

- `POST /api/auth/login/`: User login
- `POST /api/auth/logout/`: User logout
- `POST /api/auth/register/`: Client registration

### Client API Endpoints

- `GET /api/client/products/`: List available products
- `GET /api/client/products/{id}/`: Get product details
- `GET /api/client/orders/`: List client orders
- `POST /api/client/orders/`: Create new order
- `GET /api/client/profile/`: Get client profile
- `PUT /api/client/profile/`: Update client profile

### Admin API Endpoints

- `GET /api/admin/inventory/`: List inventory
- `POST /api/admin/inventory/`: Add new product
- `PUT /api/admin/inventory/{id}/`: Update product
- `DELETE /api/admin/inventory/{id}/`: Delete product
- `GET /api/admin/orders/`: List all orders
- `PUT /api/admin/orders/{id}/`: Update order status
- `GET /api/admin/users/`: List users (admin only)
- `POST /api/admin/users/`: Create user (admin only)

## Troubleshooting

### Common Issues

1. **Login Issues**
   - Verify email and password
   - Check if account is active
   - Clear browser cookies and cache

2. **Permission Errors**
   - Verify user role assignment
   - Check if middleware is properly configured
   - Ensure views have appropriate decorators

3. **UI Display Problems**
   - Test in different browsers
   - Clear browser cache
   - Check for JavaScript console errors
   - Verify CSS loading

4. **Database Errors**
   - Check database connection settings
   - Verify migrations are applied
   - Look for integrity constraint violations

### Support Channels

- GitHub Issues: https://github.com/MohamedMBG/stockmaster/issues
- Email Support: support@stockmaster.example.com
- Documentation: https://stockmaster.example.com/docs/

## UI Improvements

The application has been enhanced with several UI improvements:

### Collapsible Sidebar

- Toggle button to expand/collapse the sidebar
- Collapsed state shows only icons
- Expanded state shows icons and text
- State is remembered between sessions
- Mobile-responsive behavior

### Responsive Design

- Adapts to different screen sizes
- Mobile-friendly navigation
- Optimized tables and forms
- Touch-friendly interface elements

### Visual Enhancements

- Modern, clean design
- Consistent color scheme
- Improved typography
- Card-based layout
- Subtle animations and transitions
- Dark mode support

### Accessibility Features

- Proper contrast ratios
- Keyboard navigation support
- Screen reader compatibility
- Focus indicators
- Semantic HTML structure
