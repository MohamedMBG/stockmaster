# StockMaster - Folder Structure and File Functionality Documentation

## Overview

This document provides a comprehensive explanation of the StockMaster application's folder structure and file functionalities after the restructuring to support separate client and admin/supervisor interfaces.

## Root Directory Structure

```
stockmaster/
├── manage.py                 # Django management script for running commands
├── db.sqlite3                # SQLite database file
├── stockmaster/              # Project settings package
├── core/                     # Shared functionality
├── client/                   # Client application
├── admin_portal/             # Admin/Supervisor application
├── static/                   # Static assets
├── templates/                # Base templates
├── staticfiles/              # Collected static files for production
├── mvc_architecture_design.md # Architecture documentation
└── folder_structure_documentation.md # This file
```

## Detailed Folder Structure

### 1. Project Settings (`stockmaster/`)

This package contains the Django project settings and configuration files.

- `__init__.py`: Package initialization file
- `settings.py`: Django settings including database, installed apps, middleware, etc.
- `urls.py`: Main URL routing configuration
- `asgi.py`: ASGI configuration for asynchronous web servers
- `wsgi.py`: WSGI configuration for traditional web servers

### 2. Core Module (`core/`)

Contains shared functionality used by both client and admin applications.

- `models/`: Base data models
  - `__init__.py`: Package initialization
  - `user.py`: User model with role-based access control
  - `product.py`: Product and inventory models
  - `order.py`: Order and transaction models
  - `system.py`: System-related models (alerts, messages)

- `utils/`: Utility functions and helpers
  - `__init__.py`: Package initialization
  - `permissions.py`: Custom permission classes
  - `validators.py`: Data validation utilities
  - `helpers.py`: General helper functions

- `middleware/`: Custom middleware
  - `__init__.py`: Package initialization
  - `role_middleware.py`: Role-based access middleware

### 3. Client Application (`client/`)

Contains all client-specific functionality, focused on product catalog browsing and order placement.

- `__init__.py`: Package initialization
- `apps.py`: Django app configuration
- `urls.py`: Client URL routing

- `views/`: Client view functions
  - `__init__.py`: Package initialization
  - `auth.py`: Authentication views for clients
  - `catalog.py`: Product catalog views
  - `orders.py`: Order management views
  - `profile.py`: Client profile views

- `forms/`: Client-specific forms
  - `__init__.py`: Package initialization
  - `auth.py`: Authentication forms
  - `order.py`: Order forms
  - `profile.py`: Profile forms

- `templates/client/`: Client UI templates
  - `base.html`: Base template with client sidebar
  - `dashboard.html`: Client dashboard
  - `catalog/`: Product catalog templates
  - `orders/`: Order management templates
  - `profile/`: Profile management templates

### 4. Admin Portal (`admin_portal/`)

Contains all admin and supervisor functionality for system management.

- `__init__.py`: Package initialization
- `apps.py`: Django app configuration
- `urls.py`: Admin URL routing

- `views/`: Admin view functions
  - `__init__.py`: Package initialization
  - `auth.py`: Authentication views for admins
  - `dashboard.py`: Admin dashboard views
  - `inventory.py`: Inventory management views
  - `users.py`: User management views
  - `orders.py`: Order processing views
  - `reports.py`: Reporting and analytics views

- `forms/`: Admin-specific forms
  - `__init__.py`: Package initialization
  - `inventory.py`: Inventory forms
  - `user.py`: User management forms
  - `order.py`: Order processing forms

- `templates/admin/`: Admin UI templates
  - `base.html`: Base template with admin sidebar
  - `dashboard.html`: Admin dashboard
  - `inventory/`: Inventory management templates
  - `users/`: User management templates
  - `orders/`: Order processing templates
  - `reports/`: Reporting templates

### 5. Static Assets (`static/`)

Contains all static files organized by application.

- `shared/`: Shared assets
  - `css/`: Shared stylesheets
    - `style.css`: Main stylesheet for both interfaces
  - `js/`: Shared JavaScript
    - `main.js`: Common JavaScript functionality
  - `images/`: Shared images
    - `logo.svg`: Application logo
    - `favicon.png`: Favicon

- `client/`: Client-specific assets
  - `css/`: Client stylesheets
    - `client-style.css`: Client-specific styles
  - `js/`: Client JavaScript
    - `catalog.js`: Catalog functionality
    - `orders.js`: Order management functionality

- `admin/`: Admin-specific assets
  - `css/`: Admin stylesheets
    - `admin-style.css`: Admin-specific styles
  - `js/`: Admin JavaScript
    - `dashboard.js`: Dashboard charts and analytics
    - `inventory.js`: Inventory management functionality

### 6. Templates (`templates/`)

Contains base templates and shared template components.

- `shared/`: Shared template components
  - `auth/`: Authentication templates
    - `login.html`: Login page
    - `register.html`: Registration page
  - `components/`: Reusable UI components
    - `alerts.html`: Alert messages
    - `pagination.html`: Pagination controls
  - `errors/`: Error pages
    - `404.html`: Not found page
    - `500.html`: Server error page

## Key Files and Their Functions

### 1. Base Templates

- `/client/templates/client/base.html`: 
  - Serves as the foundation for all client pages
  - Implements the collapsible sidebar menu
  - Provides responsive layout for mobile devices
  - Includes dark mode toggle functionality
  - Manages user session and profile dropdown

- `/admin_portal/templates/admin/base.html`:
  - Serves as the foundation for all admin/supervisor pages
  - Implements the collapsible sidebar with nested submenus
  - Provides responsive layout for mobile devices
  - Includes dark mode toggle functionality
  - Manages user session and profile dropdown

### 2. Stylesheets

- `/static/shared/css/style.css`:
  - Defines the common styling for both interfaces
  - Implements responsive design principles
  - Provides dark mode support
  - Defines layout structure and component styling
  - Ensures consistent UI across the application

- `/static/client/css/client-style.css`:
  - Contains client-specific styling
  - Customizes the appearance of catalog and order pages
  - Provides client-specific color schemes and branding

- `/static/admin/css/admin-style.css`:
  - Contains admin-specific styling
  - Customizes the appearance of dashboard and management pages
  - Provides admin-specific color schemes and branding

### 3. JavaScript Files

- `/static/shared/js/main.js`:
  - Provides common functionality for both interfaces
  - Manages sidebar toggling and responsive behavior
  - Handles dark mode preferences
  - Implements common UI interactions

- `/static/client/js/catalog.js`:
  - Manages product catalog browsing
  - Implements filtering and search functionality
  - Handles shopping cart operations

- `/static/admin/js/dashboard.js`:
  - Creates and updates dashboard charts and visualizations
  - Provides real-time data updates
  - Manages dashboard widgets and layout

### 4. URL Configuration

- `/stockmaster/urls.py`:
  - Main URL configuration
  - Routes to client or admin applications based on URL path
  - Handles authentication URLs
  - Manages static and media file serving

- `/client/urls.py`:
  - Client-specific URL routing
  - Maps URLs to client view functions
  - Organizes routes for catalog, orders, and profile

- `/admin_portal/urls.py`:
  - Admin-specific URL routing
  - Maps URLs to admin view functions
  - Organizes routes for inventory, users, orders, and reports

### 5. View Functions

- `/client/views/catalog.py`:
  - Handles product catalog display
  - Implements product filtering and search
  - Manages product detail views

- `/client/views/orders.py`:
  - Handles order creation and management
  - Processes shopping cart operations
  - Manages order history and tracking

- `/admin_portal/views/inventory.py`:
  - Handles inventory management
  - Processes stock additions, updates, and removals
  - Manages categories and suppliers

- `/admin_portal/views/users.py`:
  - Handles user management
  - Processes user creation, updates, and deactivation
  - Manages role assignments

## MVC Architecture Implementation

The application follows the Model-View-Controller (MVC) architecture pattern:

1. **Models (M)**: 
   - Located in `/core/models/`
   - Define data structure and business logic
   - Implement validation and relationships
   - Provide data access methods

2. **Views (V)**:
   - Located in `/client/templates/` and `/admin_portal/templates/`
   - Render the user interface
   - Display data to users
   - Capture user input

3. **Controllers (C)**:
   - Located in `/client/views/` and `/admin_portal/views/`
   - Process user input
   - Interact with models to retrieve and update data
   - Select appropriate views to render

## Role-Based Access Control

The application implements role-based access control through:

1. **User Model**:
   - Defines roles (ADMIN, SUPERVISOR, CLIENT)
   - Provides role-checking methods

2. **Middleware**:
   - Validates user roles for each request
   - Redirects unauthorized access attempts

3. **URL Routing**:
   - Separates client and admin URLs
   - Enforces role-based access at the routing level

4. **View Decorators**:
   - Apply fine-grained permission checks
   - Ensure appropriate access to specific functionality

## Authentication Flow

1. **Login Process**:
   - Shared login page at `/login/`
   - Role detection after authentication
   - Redirection to appropriate dashboard based on role

2. **Registration**:
   - Client self-registration at `/register/`
   - Admin-only creation of supervisor accounts

3. **Session Management**:
   - Secure cookie-based sessions
   - Role information stored in session
   - Session timeout and security measures
