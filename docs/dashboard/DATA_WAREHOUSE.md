# Future data warehouse

## ETL/ELT strategy

Use change-data capture or watermark-based incremental extraction from PostgreSQL into immutable landing storage. Pseudonymize user IDs before the analytics zone, validate consent at event time, and separate restricted research demographics. Transform into conformed dimensions and atomic facts, then publish semantic marts. Record run ID, source watermark, row counts, schema hash and data-quality results.

Dimensions use surrogate warehouse keys and Type 2 history where attributes change meaningfully: user academic affiliation, book classification, device location/status, and AI pricing/status. Date/time are Type 0. Facts are append-only at their natural event grain; corrections arrive as compensating records or controlled restatements.

Recommended dimensions: date, time, pseudonymous user, book, device, location, AI model, genre, academic organization, experiment group. Recommended facts: session, borrow/return, search/result, recommendation impression/action, AI request, game, authentication, survey, and location traffic.

## ML lifecycle

`ml_datasets` governs purpose, privacy class and retention. Dataset versions record immutable storage/schema/watermark/anonymization provenance. Feature sets version feature definitions and code. Training runs bind dataset, features, parameters, code, seed, model artifact and experiment. Evaluation metrics retain split-specific offline results. Large datasets and artifacts stay in governed object storage, not PostgreSQL.

## BI connectivity

Expose a stable `analytics` schema of facts, dimensions and materialized views. Grant BI service accounts `SELECT` only, enforce statement timeouts and row-level/column security, and publish relationships and measures through each BI tool’s semantic model. Grafana should favor time-series views; Power BI/Metabase/Superset should favor star facts and dimensions.
