# Example rApp in Python

## Overview

The **Example rApp in Python** reports the status of PM counter collection and the operational state of a set of 5G cells in the network.

-----

## Using the Example rApp

The Example rApp determines whether PM counters have been collected for a set of `NRCellDU`s, then produces a report every 15 minutes to Log Viewer.

### rApp Startup

The Example rApp begins its workflow immediately after instantiation:

  * Discover the first 10 `NRCellDU`s from the network.
  * Log the expected time of the first report.
  * Enter the Report Cycle.

### Report Cycle

This cycle repeats every 15 minutes:

  * For each of the 10 `NRCellDU`s:
      * Retrieve the operational state.
      * Determine if PM counters were collected.
  * Log a report.

### Report Format

The report is logged in the following format:

```
Collected PM counters for {nrcelldus_with_counters} out of 10 NRCellDUs between {start_time} and {end_time} (UTC): 
fdn={fdn}; operationalState={operational_state}; countersCollected={counters_collected}...

Next report at {next_report} (UTC)
```

  * **`nrcelldus_with_counters`**: Number of `NRCellDU`s that counters were collected for out of the 10 discovered.
  * **`start_time`**: Start time of this report.
  * **`end_time`**: End time of this report.
  * **`fdn`**: Fully distinguished name of the `NRCellDU`.
  * **`operational_state`**: The operational state of the `NRCellDU`.
  * **`counters_collected`**: `True` or `false`, whether counters were collected for the `NRCellDU` or not.
  * **`next_report`**: Time at which the next report will be logged.

A full report is shown in the following example:

```log
Collected PM counters for 10 out of 10 NRCellDUs between 09:02 and 09:17 (UTC): fdn=urn:3gpp:dn:SubNetwork=Europe,SubNetwork=Ireland,MeContext=NR01gNodeBRadio00001,ManagedElement=NR01gNodeBRadio00001,GNBDUFunction=1,NRCellDU=NR01gNodeBRadio00001-1;operationalState=ENABLED;countersCollected=True
fdn=urn:3gpp:dn:SubNetwork=Europe,SubNetwork=Ireland,MeContext=NR01gNodeBRadio00002,ManagedElement=NR01gNodeBRadio00002,GNBDUFunction=1,NRCellDU=NR01gNodeBRadio00002-1;operationalState=ENABLED;countersCollected=True
fdn=urn:3gpp:dn:SubNetwork=Europe,SubNetwork=Ireland,MeContext=NR01gNodeBRadio00003,ManagedElement=NR01gNodeBRadio00003,GNBDUFunction=1,NRCellDU=NR01gNodeBRadio00003-1;operationalState=ENABLED;countersCollected=True
fdn=urn:3gpp:dn:SubNetwork=Europe,SubNetwork=Ireland,MeContext=NR01gNodeBRadio00004,ManagedElement=NR01gNodeBRadio00004,GNBDUFunction=1,NRCellDU=NR01gNodeBRadio00004-1;operationalState=ENABLED;countersCollected=True
fdn=urn:3gpp:dn:SubNetwork=Europe,SubNetwork=Ireland,MeContext=NR01gNodeBRadio00005,ManagedElement=NR01gNodeBRadio00005,GNBDUFunction=1,NRCellDU=NR01gNodeBRadio00005-1;operationalState=ENABLED;countersCollected=True
fdn=urn:3gpp:dn:SubNetwork=Europe,SubNetwork=Ireland,MeContext=NR01gNodeBRadio00006,ManagedElement=NR01gNodeBRadio00006,GNBDUFunction=1,NRCellDU=NR01gNodeBRadio00006-1;operationalState=ENABLED;countersCollected=True
fdn=urn:3gpp:dn:SubNetwork=Europe,SubNetwork=Ireland,MeContext=NR01gNodeBRadio00007,ManagedElement=NR01gNodeBRadio00007,GNBDUFunction=1,NRCellDU=NR01gNodeBRadio00007-1;operationalState=ENABLED;countersCollected=True
fdn=urn:3gpp:dn:SubNetwork=Europe,SubNetwork=Ireland,MeContext=NR01gNodeBRadio00008,ManagedElement=NR01gNodeBRadio00008,GNBDUFunction=1,NRCellDU=NR01gNodeBRadio00008-1;operationalState=ENABLED;countersCollected=True
fdn=urn:3gpp:dn:SubNetwork=Europe,SubNetwork=Ireland,MeContext=NR01gNodeBRadio00009,ManagedElement=NR01gNodeBRadio00009,GNBDUFunction=1,NRCellDU=NR01gNodeBRadio00009-1;operationalState=ENABLED;countersCollected=True
fdn=urn:3gpp:dn:SubNetwork=Europe,SubNetwork=Ireland,MeContext=NR01gNodeBRadio00010,ManagedElement=NR01gNodeBRadio00010,GNBDUFunction=1,NRCellDU=NR01gNodeBRadio00010-1;operationalState=ENABLED;countersCollected=True

Next report at 09:32 (UTC)
```

-----

## Viewing rApp Output

The Example rApp output can be viewed through its logs. To gain insights on its performance, use the metrics provided.

### Logging

Access Log Viewer using the user credentials provided by your platform administrator. Within Log Viewer, filter for logs specific to the Example rApp using the following query:

`service_id:"rapp-eric-oss-network-data-template-app"`

> **Note:** The `service_id` to provide depends on the configured name of the rApp when it is packaged. In the previous query, the name is `rapp-eric-oss-network-data-template-app`.

See logs from the Example rApp similar to the following:

> **Note:** By clicking on an individual message, you can see the full contents.

Read more about the **App Logging capability**.

### Metrics

To view metrics, contact your platform administrator.

> **Note:** When querying for metrics, prepend the metric name with the rApp name and use underscores `_` as a separator. For example, if the rApp name is `eric-oss-network-data-template-app`, then the metric name is `eric_oss_network_data_template_app_network_configuration_successful_requests_total`.

All metrics shown are **counters**.

| Counter | Description |
| :--- | :--- |
| `messages_consumed_total` | Messages consumed from Message Bus |
| `filtered_messages_by_motype_total` | Messages that have been filtered by MO Type |
| `filtered_messages_by_fdn_total` | Messages that are relevant to the cells collected at startup |
| `complete_batch_of_messages_consumed_total` | Complete batches consumed |
| `partial_batch_of_messages_consumed_total` | Batches which have reached timeout that are partially filled |
| `empty_batch_of_messages_consumed_total` | Batches which have reached timeout with zero messages |
| `network_configuration_successful_requests_total` | Successful Network Configuration requests |
| `network_configuration_failed_requests_total` | Failed Network Configuration requests |
| `topology_successful_requests_total` | Successful Topology & Inventory requests |
| `topology_failed_requests_total` | Failed Topology & Inventory requests |
| `schema_registry_successful_requests_total` | Successful requests made to Schema Registry |
| `schema_registry_failed_requests_total` | Failed requests made to Schema Registry |

Read more about the platform's **App Metrics capability**.

-----

## Example rApp Instantiation

### Prerequisites

The Example rApp should only be deployed on a network with:

  * 5G cells.
  * The number of `NRCellDU`s specified in Cloud Resources.

See the **Example rApp Cloud Resources requirements**.

The Example rApp is onboarded and instantiated using the **App Administration use cases**.

### Instantiation Parameters

The following parameters must be configured during instantiation and must be obtained from the platform administrator:

| Parameter | Description | Example |
| :--- | :--- | :--- |
| `appCertFileName` | The file name of the App certificate. | `tls.crt` |
| `appKeyFileName` | The file name of the generated App private key. | `tls.key` |
| `appSecretName` | The Kubernetes® secret name which contains the generated App certificate-key pair information. | `rapp-mtls-secret` |
| `iamBaseUrl` | The hostname to access the server on which EIC is installed. | `eic.<hostname>` |
| `kafkaCaCertSecretName` | The secret that contains the Kafka certificate used for TLS connection to EIC. | `kafka-tls-secret` |
| `logEndpoint` | The Log Aggregator endpoint to stream logs, which is a combination of host:port. | `my-log-endpoint.<hostname>` |
| `platformCaCertFileName` | The file name of your target platform host/capability Intermediate CA certificate. | `ca.crt` |
| `platformCaCertSecretName`| The Kubernetes secret name which contains the target platform host Intermediate CA certificates information. | `platform-certificates` |

### Verify Deployment Health

After deployment, you must check that the status of the App instance is **`DEPLOYED`**. Any error during the deployment of any App Component instance results in the App instance state **`DEPLOY_ERROR`**.

More details about **deploying an App instance**.

Once your app is in **`DEPLOYED`** status, view the Log Viewer output and look for the following logs:

```
Network Data Template App is now ready
Next report at HH:MM (UTC)
```

These logs indicate that the App is now ready and the first report will be produced shortly.

If the App is in **`DEPLOY_ERROR`** status, collect the following information for troubleshooting:

  * The App instance ID of your deployment (for example, `rapp-<RAPP_NAME>-12345678`)
  * The App's logs.

Contact your platform administrator if you encounter any issues and provide them with this information.
