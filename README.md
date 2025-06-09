# Medication Management App

A comprehensive Streamlit-based web application for medication scanning, management, and delivery services with premium subscription tiers.

## 🚀 Features

### Core Features (Free Tier)
- **Medication Scanning**: Use your webcam to scan and identify medications
- **Medication Search**: Search through comprehensive medication databases
- **Basic Management**: Track medication inventory and set reminders
- **Premium Upgrade**: Access to subscription plans

### Prime Tier ($15/month or $150/year)
- All free features
- **History Tracking**: View past medication searches and reminders
- **Delivery Service**: Order medications with prescription upload

### Elite Tier ($20/month or $200/year)
- All Prime features
- **Family Plan**: Manage medications for up to 5 family members
- **Advanced Features**: Enhanced scheduling and delivery options

## 📋 Prerequisites

Before running the application, ensure you have the following installed:

- Python 3.7 or higher
- Required Python packages (see Installation section)
- Webcam access for scanning functionality

## 🛠️ Installation

1. Clone the repository or download the source files:
   ```bash
   git clone <repository-url>
   cd medication-management-app
   ```

2. Install required dependencies:
   ```bash
   pip install streamlit
   pip install pandas
   pip install numpy
   pip install fpdf2
   pip install streamlit-option-menu
   pip install streamlit-webrtc
   ```

3. Prepare the medication datasets:
   - Ensure `medications_1.csv` and `medications_2.csv` are in the same directory as `main.py`
   - Both CSV files should contain columns: `Drug Name`, `Therapeutic Class`, `sideEffect0`, `sideEffect1`, `sideEffect2`, `use0`

## 📊 Required Data Files

The application expects two CSV files with medication data:

### medications_1.csv & medications_2.csv
Required columns:
- `Drug Name`: Name of the medication
- `Therapeutic Class`: Medical classification
- `sideEffect0`, `sideEffect1`, `sideEffect2`: Side effects
- `use0`: Description/usage information

Example structure:
```csv
Drug Name,Therapeutic Class,sideEffect0,sideEffect1,sideEffect2,use0
Aspirin,Pain Reliever,Stomach upset,Bleeding risk,Allergic reaction,Used for pain relief and fever reduction
```

## 🚀 Running the Application

1. Navigate to the project directory
2. Run the Streamlit application:
   ```bash
   streamlit run main.py
   ```
3. Open your web browser and go to the provided local URL (typically `http://localhost:8501`)

## 🔐 Login Credentials

### Prime Account
- **Username**: `prime`
- **Password**: `primepass`

### Elite Account
- **Username**: `elite`
- **Password**: `elitepass`

## 📱 Application Structure

### Navigation Menu
The app uses a sidebar navigation menu that changes based on subscription tier:

#### Free Tier
- Scanning (Scan/Search medications)
- Management (Basic inventory and reminders)
- Premium (Upgrade options)

#### Prime Tier
- Scanning
- Management
- History
- Delivery
- Log Out

#### Elite Tier
- Scanning
- Management
- History
- Delivery
- Family Plan
- Log Out

## 🎯 Key Functionalities

### 1. Medication Scanning
- Real-time webcam feed for medication identification
- Automatic medication detection and information display
- Integration with medication databases

### 2. Medication Search
- Text-based search through medication databases
- Detailed medication information display
- Support for partial name matching

### 3. Medication Management
- Inventory tracking with quantity management
- Reminder system with customizable intervals (minimum 4 hours)
- Visual progress tracking

### 4. History Tracking (Prime+)
- Search history
- Reminder history
- Order history with detailed records

### 5. Delivery Service (Prime+)
- Prescription upload (PDF, JPG, PNG)
- Order processing with progress tracking
- Cost calculation and receipt generation
- PDF receipt download

### 6. Family Plan (Elite)
- Add up to 5 family members
- Individual medication tracking per family member
- Remove family members functionality

## 💰 Subscription Tiers

| Feature | Free | Prime | Elite |
|---------|------|-------|-------|
| Medication Scanning | ✅ | ✅ | ✅ |
| Basic Management | ✅ | ✅ | ✅ |
| History Tracking | ❌ | ✅ | ✅ |
| Delivery Service | ❌ | ✅ | ✅ |
| Family Plan | ❌ | ❌ | ✅ |
| **Monthly Price** | Free | $15 | $20 |
| **Yearly Price** | Free | $150 | $200 |

## 🔧 Technical Details

### Dependencies
- **Streamlit**: Web application framework
- **Pandas**: Data manipulation and analysis
- **NumPy**: Numerical computing
- **FPDF**: PDF generation for receipts
- **streamlit-option-menu**: Enhanced navigation menu
- **streamlit-webrtc**: Webcam streaming functionality

### Session State Management
The application uses Streamlit's session state to maintain:
- Authentication status
- Medication inventory
- Reminder settings
- Order history
- Family member information

### File Upload Support
- Prescription uploads support PDF, JPG, and PNG formats
- Temporary file handling for secure processing

## 🚨 Important Notes

1. **Webcam Access**: Ensure your browser allows webcam access for scanning functionality
2. **Data Files**: Both medication CSV files must be present in the application directory
3. **Minimum Reminder Interval**: Medication reminders must be set for at least 4-hour intervals
4. **Family Plan Limit**: Maximum of 5 family members per Elite account

## 🐛 Troubleshooting

### Common Issues

1. **CSV Loading Error**: Ensure medication CSV files are in the correct directory with proper column names
2. **Webcam Not Working**: Check browser permissions and webcam connectivity
3. **Login Issues**: Verify username and password are entered correctly (case-sensitive)
4. **File Upload Problems**: Ensure uploaded files are in supported formats (PDF, JPG, PNG)

### Error Messages
- "Error loading the datasets": Check CSV file paths and format
- "Please enter a dose interval of at least 4 hours": Reminder intervals must be ≥4 hours
- "You have reached the limit of 5 family members": Elite plan family member limit reached

## 📝 License

This project is provided as-is for educational and demonstration purposes.

## 🤝 Contributing

To contribute to this project:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📞 Support

For technical support or feature requests, please refer to the application's built-in help documentation or contact the development team.

---

**Note**: This application is designed for demonstration purposes. For production use, implement proper security measures, database integration, and user authentication systems.
