# Ecommerce CDC Pipeline

Change Data Capture (CDC) pipeline that streams changes from a PostgreSQL ecommerce database into Snowflake using Debezium, Kafka, and the Snowflake Kafka Connector.

**Architecture:** PostgreSQL → Debezium (Kafka Connect source) → Kafka → Snowflake Kafka Connector (sink) → Snowflake

## Prerequisites

Before building the Docker image, download the following JAR files and place them in this directory. They are excluded from the repo via `.gitignore` due to size.

### Required JARs

| File | Version | Purpose | Download |
|------|---------|---------|----------|
| `snowflake-kafka-connector-4.0.0.jar` | 4.0.0 | Snowflake Kafka Connector — sinks Kafka topics into Snowflake tables | [Maven Central](https://repo1.maven.org/maven2/com/snowflake/snowflake-kafka-connector/4.0.0/snowflake-kafka-connector-4.0.0.jar) |
| `bcprov-jdk18on-1.84.jar` | 1.84 | Bouncy Castle cryptography provider — required by the Snowflake connector for key-pair authentication | [Maven Central](https://repo1.maven.org/maven2/org/bouncycastle/bcprov-jdk18on/1.84/bcprov-jdk18on-1.84.jar) |
| `bcpkix-jdk18on-1.84.jar` | 1.84 | Bouncy Castle PKIX — handles parsing of PEM-encoded private keys used by the Snowflake connector | [Maven Central](https://repo1.maven.org/maven2/org/bouncycastle/bcpkix-jdk18on/1.84/bcpkix-jdk18on-1.84.jar) |
| `bcutil-jdk18on-1.84.jar` | 1.84 | Bouncy Castle utility library — dependency of the PKIX and provider JARs above | [Maven Central](https://repo1.maven.org/maven2/org/bouncycastle/bcutil-jdk18on/1.84/bcutil-jdk18on-1.84.jar) |
| `bc-fips-2.1.0.jar` | 2.1.0 | Bouncy Castle FIPS API — FIPS-compliant cryptographic operations required by the Snowflake connector | [Bouncy Castle](https://downloads.bouncycastle.org/fips-java/bc-fips-2.1.0.jar) |
| `bcpkix-fips-2.1.8.jar` | 2.1.8 | Bouncy Castle FIPS PKIX — FIPS-compliant PEM/PKIX support required by the Snowflake connector | [Bouncy Castle](https://downloads.bouncycastle.org/fips-java/bcpkix-fips-2.1.8.jar) |

> The four `bc*` Bouncy Castle JARs are all dependencies of the Snowflake Kafka Connector. The connector uses them for RSA key-pair authentication against Snowflake.
> use curl.exe -L -O <URL> for Windows and curl -L -O <URL> for Mac to download `bc-fips-2.1.0.jar` and `bcpkix-fips-2.1.8.jar`
> use 

## Setup

### 1. Build the Kafka Connect image

```bash
docker build -f Dockerfile.connect -t debezium-connect-snowflake:2.6 .
```

### 2. Start the stack

```bash
docker compose up -d
```

This starts Zookeeper, Kafka, and the custom Kafka Connect worker.

### 3. Register the Debezium source connector

Streams CDC events from the `data_engineering` PostgreSQL database:

```bash
curl -X POST http://localhost:8083/connectors \
  -H "Content-Type: application/json" \
  -d @connector.json
```

### 4. Register the Snowflake sink connector

Sinks Kafka topics into Snowflake (`ECOMMERCE_DW.RAW_CDC`). Fill in `snowflake.private.key` in the connector config before posting:

```bash
curl -X POST http://localhost:8083/connectors \
  -H "Content-Type: application/json" \
  -d @snowflake-sink-v2.json
```

## Tables tracked

`public.customers`, `public.addresses`, `public.products`, `public.inventory`, `public.orders`, `public.order_items`, `public.payments`, `public.customer_events`
