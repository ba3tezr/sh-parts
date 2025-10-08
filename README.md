# نظام SH Parts - إدارة قطع غيار السيارات
# SH Parts - Car Dismantling & Parts Resale Management System

نظام متكامل لإدارة أعمال تفكيك السيارات وبيع قطع الغيار، مع دعم كامل للغة العربية والإنجليزية.

A comprehensive web application for managing car dismantling and parts resale business operations, with full support for Arabic and English languages.

## Features

### Core Modules

1. **Car Intake Module**
   - Vehicle registration with VIN tracking
   - Interactive parts checklist
   - Photo upload capability
   - Parts condition assessment
   - Automatic inventory creation

2. **Inventory Management**
   - Warehouse location tracking
   - QR code generation for parts
   - Stock level monitoring and alerts
   - Multiple part images
   - Part condition classification

3. **Sales Module**
   - Customer search by car make/model/year
   - Compatible parts display
   - Shopping cart functionality
   - Invoice generation
   - Payment tracking (full/partial)

4. **Customer Management**
   - Customer profiles with purchase history
   - Credit limit tracking
   - Payment recording
   - Outstanding balance monitoring
   - Customer notes system

5. **Reporting System**
   - Inventory valuation reports
   - Sales analytics
   - Revenue and profit margin analysis
   - Customer debt reports
   - Stock movement tracking

### Technical Features

- JWT-based authentication with role-based access control
- RESTful API with Django REST Framework
- Multilingual support (Arabic/English)
- RTL support for Arabic
- PostgreSQL/SQLite database support
- QR code generation for inventory tracking
- Responsive admin interface

## Installation

### Prerequisites

- Python 3.13+
- PostgreSQL (optional, SQLite works for development)
- Redis (for Celery tasks)

### Setup Instructions

1. **Clone the repository**
   ```bash
   cd /path/to/project
   ```

2. **Create virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your settings
   ```

5. **Run migrations**
   ```bash
   python manage.py migrate
   ```

6. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run development server**
   ```bash
   python manage.py runserver
   ```

8. **Access the application**
   - Admin Interface: http://localhost:8000/admin/
   - API Root: http://localhost:8000/api/

## API Endpoints

### Authentication
- `POST /api/token/` - Obtain JWT token
- `POST /api/token/refresh/` - Refresh JWT token

### Cars
- `/api/cars/makes/` - Car makes management
- `/api/cars/models/` - Car models management
- `/api/cars/parts/` - Parts catalog
- `/api/cars/vehicles/` - Vehicle intake

### Inventory
- `/api/inventory/items/` - Inventory items
- `/api/inventory/locations/` - Warehouse locations
- `/api/inventory/movements/` - Stock movements

### Customers
- `/api/customers/` - Customer management
- `/api/customers/{id}/credits/` - Customer credits
- `/api/customers/{id}/notes/` - Customer notes

### Sales
- `/api/sales/` - Sales transactions
- `/api/sales/cart/` - Shopping cart
- `/api/sales/payments/` - Payment processing

### Reports
- `/api/reports/saved/` - Saved reports
- `/api/reports/generate/` - Generate reports

## User Roles

- **Administrator**: Full system access
- **Manager**: Business operations and reports
- **Sales**: Customer and sales management
- **Warehouse**: Inventory and stock management

## Database Schema

### Main Models

- **User**: Custom user model with role-based permissions
- **CarMake/CarModel**: Vehicle information hierarchy
- **Part**: Parts catalog with compatibility mapping
- **Vehicle**: Incoming vehicles for dismantling
- **InventoryItem**: Stock items with QR codes
- **Customer**: Customer profiles and credit tracking
- **Sale**: Sales transactions with line items
- **Payment**: Payment records and tracking

## Configuration

### Database Setup (PostgreSQL)

```bash
# Create database
createdb sh_parts_db

# Create user
createuser sh_parts_user

# Grant privileges
psql -c "GRANT ALL PRIVILEGES ON DATABASE sh_parts_db TO sh_parts_user;"

# Update .env file
DB_ENGINE=django.db.backends.postgresql
DB_NAME=sh_parts_db
DB_USER=sh_parts_user
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
```

### Environment Variables

See `.env.example` for all available configuration options.

## Development

### Running Tests
```bash
pytest
```

### Creating Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Collecting Static Files
```bash
python manage.py collectstatic
```

### Translation
```bash
python manage.py makemessages -l ar
python manage.py compilemessages
```

## Deployment

### Using Docker

```bash
docker-compose up -d
```

### Production Settings

1. Set `DEBUG=False` in `.env`
2. Configure proper `SECRET_KEY`
3. Set up PostgreSQL database
4. Configure Redis for Celery
5. Set up Nginx as reverse proxy
6. Use Gunicorn as WSGI server

## Project Structure

```
sh_parts/
├── authentication/      # User authentication and authorization
├── cars/               # Vehicle and parts management
├── inventory/          # Stock and warehouse management
├── sales/              # Sales and payment processing
├── customers/          # Customer relationship management
├── reports/            # Reporting and analytics
├── core/               # Shared utilities
├── sh_parts/           # Project settings
├── templates/          # HTML templates
├── static/             # Static files (CSS, JS)
├── media/              # User uploads
├── locale/             # Translation files
├── manage.py
├── requirements.txt
└── README.md
```

## Contributing

1. Create a feature branch
2. Make your changes
3. Run tests
4. Submit a pull request

## License

Proprietary - All rights reserved

## Support

For support and questions, contact: support@shparts.com

## Version

Current Version: 1.0.0

## Changelog

### Version 1.0.0 (2025-01-08)
- Initial release
- Complete car intake module
- Inventory management with QR codes
- Sales and payment processing
- Customer management
- Reporting system
- Arabic/English localization
