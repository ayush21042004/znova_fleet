# FleetFlow - Intelligent Fleet Management System

A comprehensive fleet management system built on the Znova framework, designed to replace manual logbooks with intelligent automation. FleetFlow optimizes vehicle lifecycle management, monitors driver safety, tracks financial performance, and provides data-driven insights for fleet operations.

**Built with:** FastAPI (Python) + Vue.js (TypeScript) + Znova Framework

---

## 📑 Quick Navigation

- [🚀 Quick Start](#-quick-start) - Get up and running in minutes
- [🚛 FleetFlow Features](#-fleetflow-features) - Core capabilities
- [👥 Demo Users](#default-access) - Login credentials for each role
- [🏭 Production Deployment](#-production-deployment) - Deploy to production
- [📁 Project Structure](#-project-structure) - Codebase organization
- [🔧 Business Logic](#-fleetflow-business-logic) - Model examples and validations
- [📖 Getting Started](#-getting-started-with-fleetflow) - User and developer guides
- [📚 Documentation](#-documentation) - Additional resources

---

## 🚀 Quick Start

### Prerequisites

- **Python 3.8+** - Backend runtime
- **Node.js 16+** - Frontend build tools
- **PostgreSQL 12+** - Database server

### Local Development Setup

#### 1. Clone and Configure

```bash
# Clone the repository
git clone <repository-url>
cd znova_fleet

# Copy environment file
cp .env.example .env
# Edit .env with your database credentials
```

**Environment Variables:**
```env
# Database
DATABASE_URL=postgresql://postgres:password@localhost:5432/fleet_db

# Security
SECRET_KEY=your-secret-key-here-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Application
ENVIRONMENT=development
DEBUG=True
CORS_ORIGINS=["http://localhost:5173"]

# Server
BACKEND_PORT=8000
FRONTEND_PORT=5173
```

#### 2. Database Setup

```bash
# Create PostgreSQL database
createdb fleet_db

# Or using psql
psql -U postgres
CREATE DATABASE fleet_db;
\q
```

#### 3. Backend Setup

```bash
# Create virtual environment
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r ../requirements.txt
```

#### 4. Frontend Setup

```bash
# Install frontend dependencies
cd frontend
npm install
cd ..
```

### Starting the Application

#### Option 1: Quick Start (Recommended for Development)

```bash
# From project root - starts backend with auto-migration
python run.py
```

This will:
- Check and create migrations if needed
- Apply database migrations
- Seed initial data (admin user, roles)
- Start the backend server on http://localhost:8000

In a separate terminal:
```bash
# Start frontend
cd frontend
npm run dev
```

Frontend will be available at http://localhost:5173

#### Option 2: Fresh Database Setup

```bash
# Drops existing database, recreates it, and starts server
python setup_fresh.py

# With demo data
python setup_fresh.py --demo
```

This will:
- Drop and recreate the database
- Clean old migration files
- Create fresh initial migration
- Apply migrations
- Seed initial data
- Start the backend server

#### Option 3: Manual Start

```bash
# Terminal 1 - Backend
cd backend
source venv/bin/activate
uvicorn main:app --reload --port 8000

# Terminal 2 - Frontend
cd frontend
npm run dev
```

### Default Access

**Demo Users:**
- **Fleet Manager**: manager@fleetflow.com / manager123 (Full access)
- **Dispatcher**: dispatcher@fleetflow.com / dispatch123 (Trip management)
- **Safety Officer**: safety@fleetflow.com / safety123 (Driver compliance)
- **Financial Analyst**: finance@fleetflow.com / finance123 (Analytics)
- **Admin**: admin@example.com / admin123 (System administration)

**Access Points:**
- **API Docs**: http://localhost:8000/docs
- **Frontend**: http://localhost:5173

## 🏭 Production Deployment

### Environment Configuration

```bash
# Update .env for production
ENVIRONMENT=production
DEBUG=False
DATABASE_URL=postgresql://user:password@host:5432/dbname
SECRET_KEY=<generate-strong-secret-key>
```

### Option 1: Docker Deployment

```bash
# Build and start services
docker-compose -f deploy/docker-compose.production.yml up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Option 2: Manual Production Deployment

#### Backend

```bash
# Install production dependencies
pip install -r requirements.txt gunicorn

# Run migrations
cd backend
alembic upgrade head

# Start with Gunicorn
gunicorn backend.main:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000 \
  --access-logfile - \
  --error-logfile -
```

#### Frontend

```bash
# Build for production
cd frontend
npm run build

# Serve with nginx (example config in deploy/nginx.prod.conf)
# Copy dist/ to nginx web root
sudo cp -r dist/* /var/www/html/
```

### Production Checklist

- [ ] Set strong SECRET_KEY in .env
- [ ] Configure proper DATABASE_URL
- [ ] Set ENVIRONMENT=production
- [ ] Disable DEBUG mode
- [ ] Configure CORS for your domain
- [ ] Set up SSL/TLS certificates
- [ ] Configure firewall rules
- [ ] Set up database backups
- [ ] Configure logging and monitoring
- [ ] Review security settings

## 🚛 FleetFlow Features

### Core Fleet Management
- **Vehicle Management**: Track vehicles, capacity, odometer, status, and lifecycle
- **Driver Management**: Monitor licenses, safety scores, compliance, and performance
- **Trip Management**: Create, dispatch, track, and complete delivery trips
- **Maintenance Logs**: Schedule and track vehicle maintenance and repairs
- **Expense Tracking**: Log fuel, tolls, and operational expenses

### Intelligent Automation
- **Automatic Status Updates**: Vehicle and driver status changes based on trip lifecycle
- **Odometer Tracking**: Automatic updates when trips are completed
- **Capacity Validation**: Prevents cargo overloading before dispatch
- **License Expiry Checks**: Blocks assignment of drivers with expired licenses
- **Maintenance Workflows**: Automatically removes vehicles from service during repairs

### Role-Based Access Control (RBAC)
- **Fleet Manager**: Full oversight of all operations
- **Dispatcher**: Trip creation and assignment (read-only on vehicles/drivers)
- **Safety Officer**: Driver compliance and safety inspections
- **Financial Analyst**: Read-only access to analytics and cost data

### Real-Time Analytics
- **Vehicle ROI**: Calculate return on investment per vehicle
- **Fuel Efficiency**: Track km/L and identify underperforming vehicles
- **Cost per km**: Monitor operational efficiency
- **Revenue Projections**: Estimate earnings based on distance
- **Performance Dashboards**: Real-time KPIs and visualizations

### Business Intelligence
- **Dashboard KPIs**: Active fleet, maintenance alerts, trip counts, pending cargo
- **Financial Reports**: Fuel vs maintenance cost breakdown
- **Efficiency Trends**: Fuel efficiency charts and comparisons
- **Driver Performance**: Completion rates and safety scores
- **Operational Insights**: Data-driven decision making

### Real-Time Notifications
- Trip dispatch and completion alerts
- Vehicle maintenance notifications
- Driver status change alerts
- Vehicle availability updates

## 📁 Project Structure

```
znova_fleet/
├── backend/                    # FastAPI Backend
│   ├── api/                   # API endpoints
│   │   └── v1/endpoints/      # Versioned API routes
│   ├── core/                  # Znova Framework core
│   │   ├── znova_model.py     # Base model with auto-CRUD
│   │   ├── fields.py          # Field types (Char, Selection, Many2one, etc.)
│   │   ├── acl.py             # Access control logic
│   │   ├── notification_helper.py  # Real-time notifications
│   │   └── middleware/        # Permission enforcement
│   ├── models/                # FleetFlow business models
│   │   ├── fleet/             # Fleet management models
│   │   │   ├── vehicle.py     # Vehicle management
│   │   │   ├── driver.py      # Driver management
│   │   │   ├── trip.py        # Trip lifecycle
│   │   │   ├── maintenance_log.py  # Maintenance tracking
│   │   │   └── expense.py     # Expense tracking
│   │   ├── user.py            # User authentication
│   │   ├── role.py            # Role definitions
│   │   └── notification.py    # Notification system
│   ├── data/                  # Initial data and menus
│   │   ├── init_data.py       # User roles and demo users
│   │   └── menus.py           # Role-based menu configuration
│   ├── migrations/            # Database migrations (Alembic)
│   └── main.py                # FastAPI application entry
├── frontend/                  # Vue.js Frontend
│   ├── src/
│   │   ├── components/        # Reusable UI components
│   │   ├── views/             # Page views
│   │   │   ├── DashboardView.vue    # Fleet dashboard
│   │   │   ├── AnalyticsView.vue    # Financial analytics
│   │   │   └── ModelView.vue        # Generic model CRUD
│   │   ├── stores/            # Pinia state management
│   │   └── router/            # Vue Router configuration
│   └── package.json
├── deploy/                    # Deployment configurations
├── run.py                     # Development startup script
├── setup_fresh.py             # Fresh database setup script
├── requirements.txt           # Python dependencies
└── README.md                  # This file
```

## 🔧 FleetFlow Business Logic

### Model Example: Vehicle

```python
from backend.core.znova_model import ZnovaModel
from backend.core import fields, api

class Vehicle(ZnovaModel):
    __tablename__ = "fleet_vehicle"
    _model_name_ = "fleet.vehicle"
    _name_field_ = "name"

    name = fields.Char(label="Vehicle Name", required=True, tracking=True)
    license_plate = fields.Char(label="License Plate", required=True)
    vehicle_type = fields.Selection([
        ('truck', 'Truck'),
        ('van', 'Van'),
        ('bike', 'Bike')
    ], label="Vehicle Type", required=True)
    max_capacity = fields.Float(label="Max Capacity (kg)", required=True)
    odometer = fields.Float(label="Odometer (km)", default=0.0)
    status = fields.Selection([
        ('available', 'Available'),
        ('in_use', 'In Use'),
        ('in_shop', 'In Shop'),
        ('retired', 'Retired')
    ], label="Status", default='available', readonly=True)
    
    # Computed fields
    fuel_efficiency = fields.Float(label="Fuel Efficiency (km/L)", 
                                   compute="_compute_analytics", store=False)
    vehicle_roi = fields.Float(label="ROI (%)", 
                               compute="_compute_analytics", store=False)
    
    # Relationships
    trip_ids = fields.One2many("fleet.trip", "vehicle_id", label="Trips")
    maintenance_log_ids = fields.One2many("fleet.maintenance.log", 
                                         "vehicle_id", label="Maintenance Logs")
    
    # Role-based permissions
    _role_permissions = {
        "fleet_manager": {"create": True, "read": True, "write": True, "delete": True},
        "dispatcher": {"create": False, "read": True, "write": False, "delete": False},
        "financial_analyst": {"create": False, "read": True, "write": False, "delete": False}
    }
    
    @api.depends('total_distance', 'total_fuel_liters', 'acquisition_cost')
    def _compute_analytics(self):
        # Fuel Efficiency: km / L
        if self.total_fuel_liters > 0:
            self.fuel_efficiency = self.total_distance / self.total_fuel_liters
        # ROI: (Revenue - Costs) / Acquisition Cost × 100
        if self.acquisition_cost > 0:
            self.vehicle_roi = ((self.total_revenue - self.total_operational_cost) 
                               / self.acquisition_cost) * 100
```

### Automatic API Generation

The Znova framework automatically generates REST endpoints:

- `GET /api/v1/models/fleet.vehicle` - List vehicles with filters
- `POST /api/v1/models/fleet.vehicle` - Create vehicle
- `GET /api/v1/models/fleet.vehicle/{id}` - Get vehicle details
- `PUT /api/v1/models/fleet.vehicle/{id}` - Update vehicle
- `DELETE /api/v1/models/fleet.vehicle/{id}` - Delete vehicle
- `POST /api/v1/models/fleet.vehicle/{id}/action_mark_available` - Custom action

### Business Validations

```python
# Trip model validation example
def _validate_cargo_capacity(self):
    """Validate that cargo weight doesn't exceed vehicle capacity"""
    if self.vehicle_id and self.cargo_weight > self.vehicle_id.max_capacity:
        raise ValidationError(
            f"Cargo weight ({self.cargo_weight} kg) exceeds "
            f"vehicle capacity ({self.vehicle_id.max_capacity} kg)"
        )

def _validate_driver_license(self):
    """Validate that driver has valid license"""
    if self.driver_id.license_expired:
        raise ValidationError(
            f"Driver '{self.driver_id.name}' has an expired license"
        )
```

### Automatic Status Updates

```python
def action_dispatch(self):
    """Dispatch the trip - automatically updates related records"""
    self._validate_cargo_capacity()
    self._validate_driver_license()
    
    # Update trip status
    self.write({'status': 'dispatched'})
    
    # Automatically update vehicle and driver status
    self.vehicle_id.write({'status': 'in_use'})
    self.driver_id.write({'status': 'on_duty'})
    
    # Send real-time notifications
    notify_fleet_managers(db, "Trip dispatched", ...)
    notify_safety_officers(db, "New trip started", ...)
```

## 🛠️ Tech Stack

**Backend:**
- **FastAPI** - Modern, high-performance Python web framework
- **SQLAlchemy** - Powerful ORM with relationship management
- **PostgreSQL** - Robust relational database
- **Alembic** - Database migration management
- **JWT** - Secure authentication tokens
- **WebSockets** - Real-time notifications

**Frontend:**
- **Vue.js 3** - Progressive JavaScript framework with Composition API
- **TypeScript** - Type-safe development
- **Pinia** - Intuitive state management
- **PrimeVue** - Rich UI component library
- **Vite** - Lightning-fast build tool
- **Chart.js** - Beautiful data visualizations

**Znova Framework:**
- **Auto-CRUD** - Automatic REST API generation from models
- **Field System** - Odoo-inspired field types (Char, Selection, Many2one, One2many, etc.)
- **Computed Fields** - Automatic calculation with dependency tracking
- **Domain Filtering** - Dynamic record filtering based on conditions
- **RBAC** - Role-based access control at model and field level
- **Audit Trail** - Automatic change tracking with `tracking=True`
- **Sequence System** - Auto-numbering for business records
- **Notification System** - Real-time WebSocket notifications

## 🆚 FleetFlow vs Manual Logbooks

| Feature | Manual Logbooks | FleetFlow |
|---------|----------------|-----------|
| **Trip Tracking** | Paper forms, prone to errors | Digital, validated, automated |
| **Vehicle Status** | Manual updates, often outdated | Real-time automatic updates |
| **Odometer Tracking** | Manual entry, inconsistent | Automatic calculation from trips |
| **Cargo Validation** | Manual calculation, risk of overload | Automatic validation before dispatch |
| **License Compliance** | Manual checks, easy to miss | Automatic expiry blocking |
| **Cost Tracking** | Spreadsheets, time-consuming | Automatic aggregation and analytics |
| **ROI Calculation** | Manual, infrequent | Real-time, per-vehicle |
| **Fuel Efficiency** | Estimated, unreliable | Precise tracking with trends |
| **Reporting** | Hours of manual work | Instant dashboards and charts |
| **Access Control** | Physical security only | Role-based digital permissions |
| **Audit Trail** | Limited or none | Complete change history |
| **Notifications** | Phone calls, emails | Real-time in-app alerts |

## 🎯 Why FleetFlow?

✅ **Eliminate Manual Errors** - Automated validations prevent common mistakes
✅ **Save Time** - Reduce administrative work by 70%
✅ **Improve Compliance** - Automatic license and safety checks
✅ **Optimize Costs** - Data-driven insights for better decisions
✅ **Increase Efficiency** - Real-time visibility into fleet operations
✅ **Scale Easily** - Handle growing fleet without adding overhead
✅ **Ensure Accountability** - Complete audit trail of all actions
✅ **Mobile Ready** - Access from any device, anywhere

## 📚 Documentation

- **[Development Guide](DEVELOPMENT.md)** - Complete framework documentation

## 🔑 Key Features

### Security
- JWT-based authentication
- Role-based access control
- Server-side validation
- CORS protection
- SQL injection prevention

### Performance
- Database connection pooling
- Automatic query optimization
- Lazy loading relationships
- Efficient WebSocket handling
- Static file optimization

### Developer Experience
- Automatic API generation
- Hot reload development
- Type safety with TypeScript
- Comprehensive error handling
- Built-in testing framework

## 📖 Getting Started with FleetFlow

### For Users

1. **Start the application** using Quick Start guide above
2. **Login** with one of the demo user accounts
3. **Explore the dashboard** to see fleet KPIs
4. **Create a trip** as Dispatcher to see automated workflows
5. **Review analytics** as Financial Analyst to see ROI calculations

### For Developers

1. **Explore the models** in `backend/models/fleet/`
2. **Understand the Znova framework** in `backend/core/`
3. **Review business logic** in model methods (action_dispatch, action_complete, etc.)
4. **Check validations** in `_validate_*` methods
5. **Study computed fields** using `@api.depends` decorator
6. **Review role permissions** in `_role_permissions` dictionaries
7. **Read the [Development Guide](DEVELOPMENT.md)** for framework details

### Key Workflows to Understand

1. **Trip Lifecycle**: Draft → Dispatched → In Progress → Completed
2. **Vehicle Status**: Available → In Use → Available (automated)
3. **Maintenance Flow**: Create log → Vehicle to "In Shop" → Mark Available
4. **Driver Validation**: License expiry check → Block assignment if expired
5. **Cargo Validation**: Check weight vs capacity → Prevent overloading

## 🎯 Business Use Cases

### Fleet Manager
- Add new vehicles to the fleet
- Review overall fleet performance
- Log maintenance and expenses
- Analyze vehicle ROI and efficiency
- Make strategic decisions based on analytics

### Dispatcher
- Create and dispatch delivery trips
- Assign available vehicles and drivers
- Monitor active trips
- Complete trips and update status
- Validate cargo capacity before dispatch

### Safety Officer
- Monitor driver compliance
- Update safety scores
- Check license expirations
- Suspend/activate drivers
- Create safety inspection logs

### Financial Analyst
- Review operational costs
- Analyze vehicle ROI
- Monitor fuel efficiency trends
- Identify cost optimization opportunities
- Generate financial reports

## 📊 Key Metrics & Analytics

- **Vehicle ROI**: (Revenue - Operational Cost) / Acquisition Cost × 100
- **Fuel Efficiency**: Total Distance / Total Fuel Liters (km/L)
- **Cost per km**: Total Operational Cost / Total Distance
- **Completion Rate**: Completed Trips / Total Trips × 100
- **Utilization Rate**: Active Vehicles / Total Available Vehicles

## 🔐 Security Features

- **JWT Authentication**: Secure token-based authentication
- **Role-Based Access Control**: 4 distinct roles with specific permissions
- **Field-Level Security**: Read-only enforcement at model level
- **Domain Filtering**: Automatic filtering based on user role
- **Audit Trail**: Track all changes with user and timestamp
- **Validation Rules**: Server-side validation for business logic

## 📚 Documentation

- **[Development Guide](DEVELOPMENT.md)** - Complete framework documentation
- **[Demo Script](DEMO_SCRIPT.md)** - Step-by-step demo walkthrough
- **[Role Permissions](ROLE_PERMISSIONS.md)** - Detailed RBAC documentation
- **[5-Min Video Script](FLEETFLOW_5MIN_VIDEO_SCRIPT.md)** - Video demo guide
- **[Complete Workflow](FLEETFLOW_COMPLETE_WORKFLOW.md)** - Business logic flows

---

## 📸 Screenshots

### Dashboard - Fleet Overview
![Dashboard](docs/screenshots/dashboard.png)
*Real-time KPIs: Active fleet, maintenance alerts, trips today, and fleet distribution*

### Trip Management - Dispatcher View
![Trip Management](docs/screenshots/trip-management.png)
*Create and dispatch trips with automatic validation and status updates*

### Analytics - Financial Performance
![Analytics](docs/screenshots/analytics.png)
*Vehicle ROI, fuel efficiency trends, and cost distribution analysis*

### Vehicle Details - Computed Metrics
![Vehicle Details](docs/screenshots/vehicle-details.png)
*Automatic calculation of fuel efficiency, ROI, and operational costs*

---

## 🔍 Troubleshooting

### Database Connection Issues

```bash
# Check PostgreSQL is running
sudo systemctl status postgresql

# Test connection
psql -U postgres -d fleet_db

# Reset database if needed
python setup_fresh.py
```

### Migration Errors

```bash
# Check current migration status
cd backend
alembic current

# Reset migrations (WARNING: drops all data)
python setup_fresh.py

# Manual migration
alembic upgrade head
```

### Frontend Build Issues

```bash
# Clear node_modules and reinstall
cd frontend
rm -rf node_modules package-lock.json
npm install

# Clear Vite cache
rm -rf .vite
npm run dev
```

### Port Already in Use

```bash
# Find process using port 8000
lsof -i :8000
kill -9 <PID>

# Or use different port
uvicorn main:app --port 8001
```

### Permission Errors

If you see "Permission denied" errors:
```bash
# Check role assignments in database
psql -U postgres -d fleet_db
SELECT email, role_id FROM users;

# Verify role permissions in backend/models/fleet/*.py
# Check _role_permissions dictionary
```

---

## 🧪 Testing

### Run Backend Tests

```bash
cd backend
pytest tests/ -v

# With coverage
pytest tests/ --cov=backend --cov-report=html
```

### Run Frontend Tests

```bash
cd frontend
npm run test

# With coverage
npm run test:coverage
```

### Manual Testing Checklist

- [ ] Login with each role (Fleet Manager, Dispatcher, Safety Officer, Financial Analyst)
- [ ] Create a trip and verify status updates
- [ ] Test cargo overweight validation
- [ ] Test expired license blocking
- [ ] Complete a trip and verify odometer update
- [ ] Create maintenance log and verify vehicle status change
- [ ] Check analytics calculations (ROI, fuel efficiency)
- [ ] Verify role-based menu visibility
- [ ] Test real-time notifications

---

## 🤝 Contributing

FleetFlow is built on the Znova framework. To contribute:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Follow the existing model patterns in `backend/models/fleet/`
4. Add tests for new features
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

### Development Guidelines

- Follow PEP 8 for Python code
- Use TypeScript for all frontend code
- Add docstrings to all model methods
- Include validation rules for business logic
- Update role permissions when adding new models
- Add computed fields for derived data
- Use `tracking=True` for audit trail
- Write tests for critical business logic

---

## 🏗️ About Znova Framework

FleetFlow is built on the **Znova Framework**, an enterprise-grade web application framework inspired by Odoo's architecture. Znova provides:

### Core Features

- **Declarative Models**: Define models with field types, relationships, and business logic
- **Auto-CRUD**: Automatic REST API generation from model definitions
- **Computed Fields**: Automatic calculation with `@api.depends` decorator
- **Domain Filtering**: Dynamic record filtering with Odoo-style domains
- **RBAC**: Role-based access control at model and field level
- **Audit Trail**: Automatic change tracking with user and timestamp
- **Sequence System**: Auto-numbering for business records (TRIP-001, MAINT-002, etc.)
- **Notification System**: Real-time WebSocket notifications
- **UI Auto-Generation**: Frontend forms and lists generated from model metadata

### Why Znova?

✅ **Rapid Development**: Build CRUD applications 10x faster
✅ **Enterprise Patterns**: Proven architecture from Odoo/ERP systems
✅ **Type Safety**: Full TypeScript support on frontend
✅ **Scalable**: Handle thousands of records with optimized queries
✅ **Maintainable**: Clear separation of concerns and consistent patterns
✅ **Extensible**: Easy to add new models and business logic

### Learn More

- Explore model examples in `backend/models/fleet/`
- Read field types in `backend/core/fields.py`
- Study the base model in `backend/core/znova_model.py`
- Check the API generator in `backend/core/api.py`

---

## 📝 License

[Your License Here]

---

## 🙏 Acknowledgments

- **Odoo** - Inspiration for the model system and field architecture
- **FastAPI** - Modern Python web framework
- **Vue.js** - Progressive JavaScript framework
- **PrimeVue** - Beautiful UI components

---

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/fleetflow/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/fleetflow/discussions)
- **Email**: support@fleetflow.com

---

**FleetFlow** - Intelligent Fleet Management, Powered by Znova Framework

*Replace manual logbooks with intelligent automation. Optimize costs. Drive efficiency.*

---

### Quick Links

- [🚀 Quick Start](#-quick-start)
- [📖 Getting Started](#-getting-started-with-fleetflow)
- [📚 Documentation](#-documentation)
- [🔍 Troubleshooting](#-troubleshooting)
- [🤝 Contributing](#-contributing)
