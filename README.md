# ALX Portfolio Project

This project fulfills a requirement for the online Software Engineering program at ALX, where learners are tasked with creating their own projects to demonstrate their understanding of backend and frontend concepts. For my project, I developed the Salinity App for Electrochem GH LTD, a salt production company in Ghana.

The Salinity App is a specialized web application designed to streamline and automate the tracking, monitoring, and analysis of salinity levels in the salt production process. It enables Brine Attendants to manually log salinity and brine levels across various crystallizing pans and reservoirs. Additionally, the app provides Production Managers with real-time access to this data through an intuitive dashboard, facilitating informed decision-making and enhancing operational efficiency.


## Features
- Data Entry: Brine Attendants can log into the system, select specific pans, and enter salinity readings along with the brine levels.
- Monitoring & Visualization: The app presents Production Managers with an up-to-date overview of salinity levels across all pans, allowing for informed decision-making and optimization of the salt production process.
- Reporting: Managers can generate reports based on specific time periods, and export the data in formats like CSV

## Installation
1. Clone the repository:
    ```bash
    git clone https://github.com/Mawuawoe/ALX-Portfolio-Project.git
    ```
2. Navigate into the project directory:
    ```bash
    cd Salinity/webflask/app.py
    ```

3. Install the necessary dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage
To start the project,
after installing the requirement, setup your database
run:
```bash
mysql -uroot -p < setup_mysql.sql
```
run:
```bash
MYSQL_USER=your_db_user MYSQL_PWD=your_password MYSQL_HOST=localhost MYSQL_DB=your_db TYPE_OF_STORAGE=db ./app.py
```

The Salinity App is designed for efficient usage by both Brine Attendants and Production Managers in the salt production process. Here’s an overview of how each user group interacts with the app:

Usage for Brine Attendants
1. User Authentication: Brine Attendants log in to the app using secure credentials to ensure that only authorized personnel can access the data.

2. Data Entry:
--> After log in, they are directed to the home page, where the can navigate to the data entry.
--> They manually input salinity levels and brine levels through a straightforward form interface.
--> The system automatically records the timestamp of each entry to maintain a historical record.

3. Data Confirmation: Once data is submitted, the app provides confirmation of successful entry, ensuring that Brine Attendants are aware that their inputs have been recorded accurately.

Usage for Production Managers
1. Dashboard Access: Production Managers log in to the app to access a centralized dashboard displaying the latest salinity data from all pans.

2. Data Visualization:
The dashboard presents real-time data displayed in a clear and digestible format for quick analysis.
Managers can view salinity levels, brine levels, timestamps, and the names of Brine Attendants who logged the data.

3. Data Filtering:
The app allows Production Managers to filter the data by specific criteria, such as date , pan or reservoir, to facilitate detailed analysis and reporting.

4. Reporting Features:
Reports can be exported CSV formats for offline analysis or record-keeping.

Overall Benefits
Efficiency: By automating data collection and providing real-time access to information, the Salinity App enhances operational efficiency in monitoring salinity levels.
Improved Decision-Making: The app’s reporting and visualization features enable Production Managers to make data-driven decisions that optimize the salt production process.
User-Friendly Interface: The intuitive design of the app ensures that both Brine Attendants and Production Managers can navigate it easily, reducing training time and improving user adoption.