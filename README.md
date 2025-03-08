# Apache Airflow with Docker

This guide provides step-by-step instructions to set up Apache Airflow using Docker Compose, run services, configure connections, execute a DAG, and monitor it.

---

## 1. DAG Overview

The DAG in this project automates the extraction, transformation, and loading (ETL) of weather data. It fetches weather data from the **Open-Meteo API**, converts it into a **Pandas DataFrame** for ease of handling, and then inserts the structured data into a **PostgreSQL database**. The DAG is scheduled to run **daily** and leverages **PostgresHook** for efficient database connection management.

### **DAG Workflow:**
1. **Extract**: Fetch weather data from the Open-Meteo API in JSON format.
2. **Transform**: Convert the JSON data into a structured Pandas DataFrame.
3. **Load**: Insert the transformed data into a PostgreSQL table (`new_dag_data`).
4. **Monitor**: Log the number of inserted rows for tracking and debugging.

### **Why Pandas?**
- Pandas simplifies data handling, filtering, and transformations.
- It provides built-in support for writing data directly into SQL databases.
- It allows easy manipulation and visualization of tabular data.

---

## 2. Prerequisites

### **Install Docker on Windows**
1. Download and install **Docker Desktop** from [here](https://www.docker.com/products/docker-desktop/).
2. Ensure **WSL 2 Backend** is enabled (required for Windows).
3. Restart your computer if needed.

### **Get the Docker Compose File**
- If you don't have Docker Compose, download it from [here](https://docs.docker.com/compose/install/).
- If using **Docker Desktop**, Docker Compose is already included.

Ensure Docker is running before proceeding.

---

## 3. Install & Start Airflow

### **Step 1: Clone the Repository**
```powershell
git clone <repository-url>
cd <repository-folder>
```

### **Step 2: Initialize Airflow**
Before starting the services, initialize Airflow metadata:
```powershell
docker-compose up airflow-init
```

### **Step 3: Start Airflow Services**
Now, bring up all Airflow services:
```powershell
docker-compose up -d
```
This starts the following services:
- Airflow Scheduler
- Airflow Webserver
- PostgreSQL Database

### **Step 4: Access the Airflow Web UI**
Once the services are up, open your browser and go to:
```
http://localhost:8080
```
**Default Credentials:**
- Username: `airflow`
- Password: `airflow`

---

## 4. Configure Airflow Connection

To allow Airflow to interact with external databases or APIs, configure a connection.

### **Step 1: Open Airflow UI**
Navigate to **Admin → Connections**.

### **Step 2: Add a New Connection**
Click **"+ (Create)"** and fill in:

| Field        | Value |
|-------------|------|
| Connection ID | `postgres_default` |
| Connection Type | `Postgres` |
| Host | `host.docker.internal` *(if Airflow is in Docker)*, `postgres` *(if running natively)* |
| Schema | `airflow` |
| Login | `airflow` |
| Password | `airflow` |
| Port | `5432` |

Click **Save**.

---

## 5. Running and Monitoring a DAG

### **Step 1: Place the DAG File**
Ensure your DAG file (`etlweather.py`) is inside the `dags/` folder.

### **Step 2: Refresh DAGs**
In the Airflow UI, navigate to **DAGs → Refresh (⟳)** to detect new DAGs.

### **Step 3: Trigger the DAG**
Click the **Trigger DAG ▶** button next to your DAG.

### **Step 4: Monitor DAG Execution**
- **Graph View**: Visualizes the DAG structure and execution flow.
- **Tree View**: Displays the status of tasks across multiple runs.
- **Task Logs**: Click a task to view logs for debugging.

---

## 6. Stopping Airflow Services
To stop all running services:
```powershell
docker-compose down
```
To remove all containers and volumes (CAUTION: Deletes all Airflow metadata):
```powershell
docker-compose down --volumes --remove-orphans
```

---

## 7. Troubleshooting
- If the Airflow Webserver is not responding, restart services:
  ```powershell
  docker-compose restart
  ```
- If you experience network issues inside Docker, restart the Docker engine:
  ```powershell
  Restart-Service docker
  ```

---

Now, you're ready to run Apache Airflow with Docker! 🚀

