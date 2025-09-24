# Production-Ready rApp Template

This repository contains a production-ready, generic template for creating a new rApp. It provides a complete, working application skeleton that already integrates with key platform capabilities, allowing you to focus on building your specific business logic.

This template includes functional, simplified modules for:
-   OAuth2-Authenticated API clients (Async and Sync)
-   mTLS Logging to the platform's log aggregator
-   Health check endpoints
-   A generic client for **Network Configuration**
-   A generic **Message Bus** (Kafka) consumer


## Disclaimer

> ⚠️ **Important Disclaimer:**
> The link below is accessible only to those who
> **already have full access** to the EIAP Ecosystem.
> If you do not have this access, **please do not proceed.**

Python Example rApp Documentation [Here](https://developer.intelligentautomationplatform.ericsson.net/#tutorials/example-rapp-in-python).

**Note:**
If you need help accessing the EIAP Ecosystem,
contact support at this **email address:** intelligent.automation.platform@ericsson.com


## How to Use This Template

### 1. Initialize Your rApp

First, choose a unique, lowercase, alphanumeric name for your rApp (dashes are allowed). Then, run the `set_rapp_name.sh` script to initialize the project.

```bash
# Make the script executable
chmod +x set_rapp_name.sh

# Run the script with your new rApp name
./set_rapp_name.sh my-new-rapp
```

This script will replace all placeholders (`RAPP_NAME`) with your chosen name throughout the project.

### 2. Configure Environment

Copy the `.env.example` file to `.env` and fill in the required values for your development environment. These variables are essential for the rApp to connect to the platform.

```bash
cp .env.example .env
# Now edit .env with your values
```

### 3. Start Development

Your application's source code lives in the `src/` directory. The structure is set up to get you started quickly.

-   **`src/main.py`**: The main entry point for your FastAPI application. It handles the application lifecycle, including the startup of background tasks like the message consumer.
-   **`src/routes.py`**: Define your rApp's API endpoints here. An example is provided that uses the generic network configuration client.
-   **`src/clients.py`**: Manages authenticated `httpx` clients. **You don't need to change this.** Import `oauth_manager` to make authenticated API calls.
-   **`src/mtls_logging.py`**: Production-ready mTLS logging. **You don't need to change this.** Import the `logger` object and use it.
-   **`src/network_configuration.py`**: Contains a generic function `get_attribute_for_source_id` to read data from a network element. You can use this as a starting point for any network configuration interactions.
-   **`src/message_bus_consumer.py`**: A simplified Kafka consumer. **You need to add your logic** inside the `consume_messages` loop to handle deserialization and processing of messages from your specific topic.

**Your Task:**

1.  Add new Python files in `src/` for your specific business logic (e.g., a module to interact with the Topology service).
2.  Modify the `TODO` section in `src/message_bus_consumer.py` to process your data.
3.  Add new API endpoints to `src/routes.py` to expose your rApp's functionality.

### 4. Configure rApp-Specifics

-   **Python Dependencies**: Add any new Python libraries to `requirements.txt`.
-   **Helm Chart**: Modify `charts/<your-rapp-name>/values.yaml` to adjust deployment settings.
-   **CSAR Package**: Review and edit the files in `csar/` to match your rApp's metadata and data requirements.

This template provides a solid and functional foundation, enabling you to build robust rApps more efficiently.

