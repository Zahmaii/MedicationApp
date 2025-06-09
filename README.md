# IZI Restaurant Inventory Management System
📖 Overview
- This is an intelligent inventory management system designed specifically for IZI Restaurant that uses machine learning to predict future inventory needs.
- The system provides comprehensive data analytics, forecasting capabilities, and automated ordering recommendations to optimize restaurant inventory management.
-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
🔖 Features
- **Secure Login System** with admin authentication
- **Interactive Data Entry** for daily inventory consumption tracking
- **Advanced Analytics Dashboard** with visual charts and key statistics
- **Machine Learning Predictions** using ANN, Linear Regression, and SVR models
- **Smart Inventory Calculations** with safety stock and current inventory considerations
- **Automated Order Management** with cost calculations and order history
- **Multi-day Forecasting** with customizable prediction periods (1-365 days)
- **Data Export Functionality** for forecast data in CSV format
- **Real-time Visual Feedback** with gradient color charts and metrics
🧰 Technologies Used
- **Python Programming** for core functionality
- **Streamlit** for web interface and interactive dashboard
- **TensorFlow/Keras** for Artificial Neural Network implementation
- **Scikit-learn** for Linear Regression and Support Vector Regression
- **Pandas & NumPy** for data manipulation and analysis
- **Matplotlib** for data visualization and charting
- **Streamlit Option Menu** for navigation interface
📂 APP Explanation
- **izi.py**: Main application file containing all functionality including:
  - User authentication and login system
  - Data entry interface for daily inventory tracking
  - Analytics dashboard with multiple ML prediction models
  - Inventory calculation engine with safety stock management
  - Order placement system with cost analysis and history tracking
-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
🍽️ Restaurant Management Features
- **Data Page**: Enter daily inventory consumption data for any food item
- **Analytics Page**: View consumption patterns, statistics, and ML-powered forecasts
- **Calculation Page**: Calculate optimal inventory levels with safety stock considerations
- **Orders Page**: Place orders with cost calculations and maintain order history
- **Secure Access**: Admin-only access with username/password protection
-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
🤖 Machine Learning Models
- **Artificial Neural Network (ANN)**: Deep learning model with dropout layers for robust predictions
- **Linear Regression**: Simple linear trend analysis for steady consumption patterns
- **Support Vector Regression (SVR)**: Non-linear regression for complex consumption patterns
- **Data Preprocessing**: StandardScaler normalization and train/test splitting
- **Early Stopping**: Prevents overfitting in neural network training
-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
📱 How to Implement it
1. **Clone the Repository**
   ```bash
   git clone [repository-link]
   cd izi-inventory-management
   ```

2. **Install Required Dependencies**
   ```bash
   pip install streamlit pandas numpy matplotlib tensorflow scikit-learn streamlit-option-menu
   ```

3. **Prepare Image Assets**
   - Add `Logo.png` for the sidebar logo
   - Add `westernimage1.png` for the welcome banner
   - Ensure images are in the same directory as izi.py

4. **Configure Login Credentials**
   - Default credentials: Username: `admin`, Password: `password`
   - Modify the `user_credentials` dictionary in the code for custom authentication

5. **Run the Application**
   ```bash
   streamlit run izi.py
   ```

6. **Access the System**
   - Open your web browser and navigate to the provided local URL
   - Login with admin credentials
   - Start entering daily inventory data for your restaurant items

7. **Using the System**
   - **Step 1**: Enter item name, pricing, and daily consumption data
   - **Step 2**: Analyze consumption patterns and generate forecasts
   - **Step 3**: Calculate optimal inventory levels with safety considerations
   - **Step 4**: Place orders based on recommendations and track order history
-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
🔐 Default Login Credentials
- **Username**: admin
- **Password**: password
- *Note: Change these credentials in the code for production use*
-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
📊 Analytics Capabilities
- **Key Statistics**: Average, maximum, and minimum consumption tracking
- **Visual Charts**: Gradient color bar charts for consumption visualization
- **Forecast Models**: Choose from 3 different ML models for predictions
- **Customizable Periods**: Forecast anywhere from 1 to 365 days ahead
- **Data Export**: Download forecast data as CSV files
- **Horizontal Data Display**: User-friendly data presentation format
-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
💰 Cost Management Features
- **Price Tracking**: Set and track price per kilogram for each item
- **Order Calculations**: Automatic total cost calculations for orders
- **Inventory Optimization**: Smart recommendations based on consumption patterns
- **Safety Stock Management**: Configurable safety stock levels
- **Order History**: Track and manage previous orders with delete functionality
-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
📜 License
This project is open-source and available under the MIT License.
💯 Acknowledgements
- **TensorFlow** for deep learning capabilities
- **Scikit-learn** for machine learning algorithms
- **Streamlit** for creating the interactive web application
- **Restaurant Industry** professionals who provided insights for inventory management best practices
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
🌟 If you found this project helpful for your restaurant management needs, please consider giving it a star on GitHub! 🌟
