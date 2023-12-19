# Introduction to the application:

The application is built using FastAPI and exposes five endpoints. It is containerized in Docker, allowing it to run on any environment. Logging is enabled, ensuring effective monitoring in case of errors. Additionally, the application includes logic to determine whether an API is responding within a specified time. Currently, this threshold is set to 50 milliseconds, but users can adjust it by modifying the `API_THRESHOLD` variable in the `.env` file located in the config folder.

The logging level of the application is configurable. Users can modify the logging level according to their needs by editing the `logging_config.ini` file.

To enhance endpoint security, JWT functionality is implemented. Users must first call the `/register` endpoint and provide a username and password to create an account within the application. User data is stored in a SQLite database, which is persisted inside the container. Even if the container is deleted, data will not be lost. To obtain a JWT token, users need to call the `/login` endpoint with the correct username and password. The token expires in 5 minutes, a setting that can also be configured.

The `/bot-score` endpoint accepts two features as input and responds with the probability of the transaction being initiated by a bot. Additionally, it provides a boolean value (0 or 1) indicating whether the transaction was bot-initiated or not.

Details about the endpoints and their documentation will be available at the following address once the application is deployed: [http://127.0.0.1:8887/docs](http://127.0.0.1:8887/docs).

Docker Compose has been utilized for ease of deployment.

# How to deploy the application:

The application deployment is simple, all you have to do is follow the below steps

1. Install docker on your computer
2. Extract the zip file
3. Open a terminal inside the extracted project
4. cd into the directory where the **docker-compose** file is present
5. Run the below command in the terminal:

   **docker-compose up -d**

6. Afeter the container is up and running you can view the endpoint docs on the link
   [http://127.0.0.1:8887/docs](http://127.0.0.1:8887/docs).

# How to monitor the application:

I have implemented the following features to monitor the application:

1.  **Logging Enabled:** Logging is enabled within the application. An `application.log` file is generated inside the container, which can be viewed in case the application reports any errors.
2.  **/Health Endpoint:** A `/health` endpoint has been created. It is a GET request that returns an "OK" message, indicating the health status of the application.
3.  **API response Monitoring:** Logic has been implemented to log messages as "critical" if an API takes too long to respond, ensuring timely detection of slow-performing endpoints.

# Other considerations:

I would like to highlight a few important considerations for this application:

1.  **Logging System:** For the current scope of this application, I have created a basic logging system. In a production environment, we would use tools like Grafana for logging. Additionally, custom alerts can be set up to notify us in case of abnormal system behavior.
2.  **Endpoint Caching:** Implementing caching for the endpoints can significantly improve response times. By caching results, we can return data much faster instead of processing requests frequently.
3.  **API Request Analysis:** Storing API requests in a database provides valuable insights. We can analyze the data to differentiate between bot and human traffic, track request timings, and identify peak request hours. These insights and trends can be utilized to enhance the system's performance and user experience.
4.  **Authentication Handling:** While I have implemented authentication features, in a production environment, it's common practice to handle authentication using a separate service. This approach ensures a separation of concerns and enhances the overall security of the system.
