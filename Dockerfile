#Use official python image
FROM python:3.10-slim

#Set working directory
WORKDIR /app

#Copy dependency list
COPY requirements.txt .

#Install dependencies
RUN pip install --upgrade pip
RUN pip install --default-timeout=100 --no-cache-dir -r requirements.txt

#copy all project files
COPY . .

#Expose \streamlit default port
EXPOSE 8501

#Command to run SmartBurn
CMD ["streamlit", "run", "app.py", "--server.address=0.0.0.0"] 
