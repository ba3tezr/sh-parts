Create a comprehensive web application for a car dismantling and parts resale business. The system will manage the entire workflow from car acquisition to parts inventory and sales.

Core Requirements
Database Structure
Car makes, models, and years
Parts categorization by system (engine, transmission, body, etc.)
Parts compatibility across different car models
Inventory tracking with location, condition, and pricing
Customer and supplier information
Functional Modules
1. Car Intake Module
Registration of incoming vehicles (VIN, make, model, year, condition)
Interactive checklist for received parts with visual car diagram
Checkbox system to mark all available parts
Automatic inventory creation based on checked parts
Photos upload capability
Parts condition assessment (new, used-good, used-fair)
2. Inventory Management
Warehouse location assignment
QR code/barcode generation for parts tracking
Stock level monitoring and alerts
Part condition classification
Parts image gallery
3. Sales Module
Customer search by car make/model/year
Compatible parts display with filtering options
Real-time inventory availability
Pricing information
Quantity selection
Invoice generation
4. Customer Management
Customer profiles with purchase history
Credit tracking system
Payment recording and outstanding balance
Notifications for payment due dates
5. Reporting System
Inventory valuation reports
Sales analytics by part type, car model, etc.
Revenue and profit margin analysis
Customer debt reports
Stock movement (in/out) with detailed filtering
Technical Requirements
Backend
Django framework with REST API
PostgreSQL database
Authentication system with JWT
Role-based access control (Admin, Manager, Sales, Warehouse)
Frontend
Bootstrap 5 with responsive design
Theme system with 3 options (default: dark blue with black accents)
Arabic and English language support with RTL capabilities
Advanced search with autocomplete suggestions
Modern modal dialogs and notifications
Interactive dashboards with charts
Data Integration
Initial data seeding with car makes/models/parts from public APIs
Parts database integration with images and specifications
Excel import/export functionality
PDF report generation
Detailed Feature Specifications
Authentication System
Secure login page with 2FA option
Password recovery
User roles: Administrator, Manager, Sales, Warehouse
Car Intake Process
Enter basic vehicle information
Generate parts checklist based on car model
Mark received parts (with condition indicators)
System automatically creates inventory entries
Print reception report
Parts Inventory
Hierarchical categorization (e.g., Engine > Cooling > Radiator)
Condition status (New, Used-Excellent, Used-Good, Used-Fair)
Multiple images per part
Current quantity, minimum threshold
Location tracking (warehouse, shelf, bin)
Price calculation based on part condition and market value
Sales Process
Customer selects vehicle make/model/year
System displays compatible parts
Advanced filtering by part category, condition, price range
Add parts to cart with quantity
Generate quotation or invoice
Process payment (full or partial)
Track unpaid balance
Reporting Module
Custom report builder with drag-drop fields
Multiple filter options (date range, part type, customer, etc.)
Export to Excel, PDF formats
Scheduled reports via email
Visual charts and graphs
UI/UX Requirements
Clean, modern interface
Responsive design for mobile access
3 theme options with central theme management
Fast-loading components with loading indicators
Arabic/English language toggle
RTL support for Arabic
Technical Architecture
Database Design
Normalized PostgreSQL schema
Indexing for performance optimization
Regular backups
Backend Structure
Django with Django REST framework
Modular code organization
Comprehensive test coverage
API documentation with Swagger
Frontend Architecture
Component-based structure
Responsive Bootstrap 5 framework
Theme system with CSS variables
Multilingual support with translation files
Integration Points
Payment gateway integration
Email notification system
SMS notifications for important events
External data sources for parts information
Development Guidelines
Follow PEP 8 for Python code
Implement comprehensive docstrings
Use Git for version control with feature branches
Continuous integration with automated testing
Regular code reviews
Deployment Considerations
Containerization with Docker
CI/CD pipeline setup
Regular database backups
Monitoring and logging system
Performance optimization
This prompt provides a comprehensive framework for building the sh_parts system that will serve a car dismantling and parts resale business, with full support for the Arabic market and multilingual capabilities.

