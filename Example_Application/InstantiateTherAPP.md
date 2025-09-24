# Example rApp Tutorial

## Overview

The **Example rApp in Python** serves as a reference point for how an rApp can be developed to work with the platform capabilities. Based on a set of discovered cells, the rApp reads the operational state and validates that PM counters are being collected. The rApp uses secure communication through **TLS** for integration with platform capabilities and produces logs through **mTLS**.

The Example rApp uses the following capabilities to implement its business logic:

  * **Topology & Inventory**
      * Discover a set of 10 `NRCellDU`s from the network.
  * **Network Configuration**
      * Read the `operationalState` attribute for each `NRCellDU`.
  * **Data Management**
      * Request PM counters for all `NRCellDU`s in the network.
  * **Message Bus**
      * Consume PM counters.

```
+------------------+
                                                     |   Example rApp   |
                                                     |       .  _       |
                                                     +------------------+
                                                              |
+-------------------------------------------------------------+--------------------------------------------------------------+
|                                                             |                                                              |
T                             T                               T                               T                T               T
|                             |                               |                               |                |               |
Produce logs to               Secure App                      Discover Network                Discover Network   Discover and    Consume messages
the platform                  Communication                   Entities                        Configuration      access data     asynchronously
|                             |                               |                               |                |               |
v                             v                               v                               v                v               v
+------------------+          +-----------------------+       +---------------------+         +----------------+ +---------------+ +----------------+
|    App Logging   |          | App Certificate Prov. |       | Topology & Inventory|         | Network Config | | Data Mgmt.    | |  Message Bus   |
|      ( O O )     |          |         ( O O )       |       |       ( O O )       |         |    ( O O )     | |    ( O O )    | |    ( O O )    |
+------------------+          +-----------------------+       +---------------------+         +----------------+ +---------------+ +----------------+
=====================================================================================================================================================
                                                  Automation Platform capabilities
-----------------------------------------------------------------------------------------------------------------------------------------------------
                                        Example rApp Interaction with Platform Capabilities
```

-----

## You will learn

This tutorial walks through the process of creating a Cloud Service Archive (CSAR) rApp package, onboarding, and instantiating the Example rApp in Python.

Through this tutorial you will:

  * Deploy the rApp and observe it running on the platform.
  * Validate through logs that the rApp is working as expected.

-----

## Prerequisites

> **Note**: In a Windows® environment, make sure to execute all commands and install the following prerequisites in **WSL**.

Before starting this tutorial, you need the following:

  * **EIC environment** to perform onboarding and instantiation of the rApp.
      * The rApp requires EIC version `1.2513` (2025 Q1) or higher.
  * Platform administrator has configured the platform to make the necessary data available.
  * **Curl**
  * **Docker™**
  * **Python**
  * **Helm®**

This tutorial is tested on **Ubuntu® 20.04.4 LTS** using **Python 3.13**.

Some command examples show placeholder variable values inside angular brackets `<>`. You must replace these with your own correct values.

### Download

See the **Download Example rApp in Python** page.

-----

## Part 1: Build the Docker Image

This section describes how to build the Docker image for the rApp. A `Dockerfile-template` is available in the rApp package.

### Step 1: Extract the downloaded Example rApp package

Extract the package `network-data-template-app.zip`. Using a command line, navigate into the extracted directory.

```sh
# The directory name includes the version, e.g., eric-oss-network-data-template-app-1.0.0-0
cd <PATH_TO_PROJECT>/eric-oss-network-data-template-app-<VERSION>

# Set the version as an environment variable
export VERSION="<VERSION>"
```

### Step 2: Set a unique name for the rApp package

To prevent naming conflicts, assign a unique name to the rApp. The package uses `RAPP_NAME` as a placeholder.

> **Note**: All subsequent commands must be run from the rApp project root directory.

```sh
# Make the script executable
chmod +x set_rapp_name.sh

# Set your unique rApp name as an environment variable
export RAPP_NAME="<RAPP_NAME>"

# Example:
export RAPP_NAME="my-new-rapp"

# Run the script to apply the name
./set_rapp_name.sh
```

This script replaces all instances of the placeholder throughout the project.

### Step 3: Prepare the Dockerfile

Edit the `Dockerfile-template` and replace `<PYTHON_IMAGE_NAME>` with a slim Python base image.

```dockerfile
FROM python:3.13-slim
```

Now, rename the file to `Dockerfile`.

```sh
mv Dockerfile-template Dockerfile
```

### Step 4: Build the Docker image

Run the following command to build the image.

> **Note**: Ensure the final dot `.` is included in the command.

```sh
docker build . -t proj-eric-oss-drop/$RAPP_NAME:$VERSION --build-arg APP_VERSION=$VERSION
```

### Step 5: Check if the Docker image is built

Run the following command:

```sh
docker images proj-eric-oss-drop/$RAPP_NAME
```

**Example Output:**

```
REPOSITORY                                              TAG       IMAGE ID       CREATED          SIZE
proj-eric-oss-drop/eric-oss-network-data-template-app   2.0.0-3   551449bda9ab   18 seconds ago   185MB
```

-----

## Part 2: Create a CSAR Package

This section describes how to create a CSAR rApp package using the **App Package Tool**.

### Prerequisites

Download the App Package Tool Docker image as described in **Download the App Package Tool**.

### Create a CSAR package

The following diagram describes the package structure.

All commands should be run from within your project directory `eric-oss-network-data-template-app-<VERSION>`.

#### Step 1 & 2: Prepare the CSAR directory

The `csar` directory, which contains the required structure, is already included in the zip file.

#### Step 3: Create a .tgz archive from the Helm® charts

Generate an archive of the chart:

```sh
helm package charts/$RAPP_NAME/ -d csar/OtherDefinitions/ASD/
```

#### Step 4: Save the Docker image for the CSAR package

Generate an archive of the Docker image and store it in the `csar/Artifacts/Images` directory:

```sh
mkdir -p csar/Artifacts/Images
docker save proj-eric-oss-drop/$RAPP_NAME:$VERSION -o csar/Artifacts/Images/docker.tar
```

#### Step 5: Create the CSAR rApp package

Run the following command to create the CSAR package. Use the `<APP_PACKAGE_TOOL_IMAGE>` and `<TAG>` from the tool you downloaded.

```sh
mkdir -p csar-output
docker run --rm -v $(pwd):/work <APP_PACKAGE_TOOL_IMAGE>:<TAG> \
  --package-path /work/csar \
  --output-path /work/csar-output \
  --package-name examplerAppPackage
```

The generated `examplerAppPackage.csar` will be in the `./csar-output` directory.

#### Step 6: Verify the CSAR rApp package

Run `ls csar-output/` to verify the package was created successfully.

-----

## Part 3: Onboard the rApp

### Prerequisites

Contact your platform administrator to request the following:

  * A **CA certificate** for secure API communication.
  * **Client Access** credentials (Client ID and Client Secret) with the following roles:
      * `AppMgr_Application_Administrator`
      * `AppMgr_Application_Operator`

Generate a valid access token:

```sh
curl --cacert <PATH_TO_CA_CERTIFICATE> --request POST \
  https://<eic-host>/auth/realms/master/protocol/openid-connect/token \
  --header 'content-type: application/x-www-form-urlencoded' \
  --data "grant_type=client_credentials&client_id=<IAM_CLIENT_ID>&client_secret=<IAM_CLIENT_SECRET>"
```

The response will contain the `access_token`.

### Step 1: Onboard the rApp CSAR package

Start the onboarding process:

```sh
curl --cacert <PATH_TO_CA_CERTIFICATE> --location --request POST \
  'https://<eic-host>/app-onboarding/v2/app-packages' \
  --header 'Authorization: Bearer <access-token>' \
  --header 'accept: application/json' \
  --form 'file=@"<PATH_TO_CSAR>/examplerAppPackage.csar"'
```

From the response, get the onboarding **`JOB_ID`**. Use it to check the status until it becomes `ONBOARDED`.

```sh
curl --cacert <PATH_TO_CA_CERTIFICATE> --location --request GET \
  'https://<eic-host>/app-onboarding/v2/onboarding-jobs/<JOB_ID>' \
  --header 'Authorization: Bearer <access-token>' \
  --header 'accept: application/json'
```

Once onboarded, the response will contain the **`APP_ID`**.

### Step 2: Initialize the rApp

Use the **`APP_ID`** from the previous step to initialize the rApp:

```sh
curl --cacert <PATH_TO_CA_CERTIFICATE> --location --request POST \
  'https://<eic-host>/app-lifecycle-management/v3/apps/<APP_ID>/initialization-actions' \
  --header 'Content-Type: application/json' \
  --header 'Authorization: Bearer <access-token>' \
  -d '{"action": "INITIALIZE"}'
```

Check the status until it becomes `INITIALIZED`:

```sh
curl --cacert <PATH_TO_CA_CERTIFICATE> --location --request GET \
  'https://<eic-host>/app-lifecycle-management/v3/apps/<APP_ID>' \
  --header 'Content-Type: application/json' \
  --header 'Authorization: Bearer <access-token>'
```

### Step 3: Enable the rApp mode

Switch the App from `DISABLED` to `ENABLED`:

```sh
curl --cacert <PATH_TO_CA_CERTIFICATE> --location --request PUT \
  'https://<eic-host>/app-lifecycle-management/v3/apps/<APP_ID>/mode' \
  --header 'Content-Type: application/json' \
  --header 'Authorization: Bearer <access-token>' \
  -d '{"mode": "ENABLED"}'
```

-----

## Part 4: Instantiate the rApp

### Prerequisites

  * You need the access token from the previous section.
  * Contact your platform administrator for various certificates, keys, secrets, and endpoints required for the `userDefinedHelmParameters`.

### Step 1: Create rApp instance

Use the **`APP_ID`** to create an instance:

```sh
curl --cacert <PATH_TO_CA_CERTIFICATE> --location --request POST \
  'https://<eic-host>/app-lifecycle-management/v3/app-instances' \
  --header 'accept: application/json' \
  --header 'Content-Type: application/json' \
  --header 'Authorization: Bearer <access-token>' \
  -d '{
    "appId": "<APP_ID>"
  }'
```

The response will contain the **`APP_INSTANCE_ID`**.

### Step 2: Deploy rApp instance

Use the **`APP_INSTANCE_ID`** and provide the required Helm parameters to deploy:

```sh
curl --cacert <PATH_TO_CA_CERTIFICATE> --location --request POST 'https://<eic-host>/app-lifecycle-management/v3/app-instances/<APP_INSTANCE_ID>/deployment-actions' \
--header 'accept: application/json' \
--header 'Content-Type: application/json' \
--header "Authorization: Bearer <access-token>" \
-d @- <<EOF
{
  "type": "DEPLOY",
  "additionalData": {
    "componentInstances": [
      {
        "name": "$RAPP_NAME",
        "properties": {
          "timeout": 5,
          "userDefinedHelmParameters": {
            "platformCaCertSecretName": "<PLATFORM_CA_CERT_SECRET>",
            "platformCaCertFileName": "<PLATFORM_CA_CERT_FILENAME>",
            "iamBaseUrl": "https://<eic-host>",
            "appSecretName": "<APP_MTLS_SECRET>",
            "logEndpoint": "<LOG_ENDPOINT>",
            "appKeyFileName": "<APP_PRIVATE_KEY>",
            "appCertFileName": "<APP_CERTIFICATE>",
            "kafkaCaCertSecretName": "<KAFKA_CA_CERT_SECRET>"
          }
        }
      }
    ]
  }
}
EOF
```

Check the deployment status until it changes to `DEPLOYED`:

```sh
curl --cacert <PATH_TO_CA_CERTIFICATE> --location --request GET \
  'https://<eic-host>/app-lifecycle-management/v3/app-instances/<APP_INSTANCE_ID>' \
  --header 'accept: application/json' \
  --header 'Content-Type: application/json' \
  --header 'Authorization: Bearer <access-token>'
```

### Step 3: View rApp logs

When the status is `DEPLOYED`, the rApp is running. To view its logs, see the section **Viewing rApp Output** in the Example App User Guide.
