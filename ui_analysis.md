# UI Analysis of Reference GitHub Stock Management System

## Overview
The reference GitHub repository (https://github.com/DonGuillotine/stock-management-system) features a modern, responsive UI with a clean design. The system includes role-based authentication, dashboard views, and various management interfaces for inventory, orders, and reporting.

## Base Template Structure
The base template (`base.html`) serves as the foundation for all pages and includes:

1. **Header Section**:
   - Includes a separate headers.html file
   - Uses crispy forms for form styling
   - Uses static files for CSS and JavaScript

2. **CSS Styling**:
   - Primary color: `#854fff` (purple)
   - Font family: "DM Sans", sans-serif
   - Clean, modern styling with rounded corners
   - Consistent padding and margins
   - Responsive design elements

3. **Layout Structure**:
   - Uses a nested div structure with classes:
     - `nk-app-root` (main container)
     - `nk-main` (main content area)
     - `nk-wrap` (content wrapper)
     - `nk-content` (page content)

4. **Navigation**:
   - Sidebar navigation with collapsible sections
   - Top header with user profile dropdown
   - Role-based menu visibility

## Authentication UI
1. **Login Page**:
   - Clean, centered form with logo
   - Input fields with validation
   - Remember me checkbox
   - Forgot password link
   - Register link for new clients only

2. **Registration Page**:
   - Only available for client registration
   - Form with validation
   - Fields: username, email, password, confirm password

## Dashboard UI
1. **Admin Dashboard**:
   - Statistics cards at the top (total products, low stock, orders)
   - Recent transactions list
   - Charts for inventory levels and sales
   - Quick action buttons
   - Dark/light mode toggle

2. **Client Dashboard**:
   - Order history
   - Product catalog view
   - Shopping cart functionality
   - Profile management

3. **Supervisor Dashboard**:
   - Order approval interface
   - Stock monitoring
   - Staff performance metrics

## Stock Management UI
1. **Stock List View**:
   - Data table with search, sort, and pagination
   - Action buttons (edit, delete, view)
   - Status indicators for low stock
   - Category filtering

2. **Add/Edit Stock Forms**:
   - Form with validation
   - Dynamic category selection
   - Image upload
   - Price and quantity fields

## Color Scheme
- Primary: `#854fff` (purple)
- Secondary: `#364a63` (dark blue)
- Success: `#1ee0ac` (green)
- Info: `#09c2de` (light blue)
- Warning: `#f4bd0e` (yellow)
- Danger: `#e85347` (red)
- Dark: `#1c2b46` (dark blue)
- Light: `#ebeef2` (light gray)

## Typography
- Headings: "DM Sans", sans-serif
- Body text: "Roboto", sans-serif
- Font sizes: 
  - Base: 14px
  - Headings: 18px-32px
  - Small text: 12px

## Components
1. **Buttons**:
   - Primary buttons: Purple with white text
   - Secondary buttons: Outlined style
   - Icon buttons for actions
   - Hover effects with transitions

2. **Cards**:
   - White background with subtle shadow
   - Rounded corners (4px)
   - Consistent padding (20px)
   - Optional header with border-bottom

3. **Tables**:
   - Striped rows
   - Hover effect
   - Responsive design
   - Action buttons in the last column

4. **Forms**:
   - Labels above inputs
   - Validation messages
   - Consistent spacing
   - Submit buttons aligned right

5. **Alerts/Notifications**:
   - Color-coded by type
   - Dismissible
   - Icons for different alert types

## Special Features
1. **Dark/Light Mode Toggle**:
   - Switch in the header
   - Persistent preference storage

2. **Responsive Design**:
   - Mobile-friendly layouts
   - Collapsible sidebar on small screens
   - Responsive tables with horizontal scroll

3. **Charts and Visualizations**:
   - Bar charts for inventory levels
   - Line charts for sales trends
   - Pie charts for category distribution

## Authentication Logic
- Admin creates supervisor accounts
- Only clients can self-register
- Role-based access control for all pages
- Password reset functionality

## Key UI Pages to Implement
1. Login/Registration
2. Role-specific dashboards
3. Stock management (list, add, edit, delete)
4. Order management
5. User profile management
6. Reports and analytics
