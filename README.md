# GitHub Crawler

# Overview

This project collects data on GitHub repositories and their star counts using the GitHub GraphQL API.
The data is stored in a PostgreSQL database and exported as a CSV file through a GitHub Actions pipeline.

The goal is to crawl 100,000 GitHub repositories efficiently while respecting API rate limits and ensuring that the data can be updated continuously.

# What the Project Does

Uses GitHub’s GraphQL API to fetch repository data such as repository ID, name, star count, and last updated time.

Stores the data in a PostgreSQL database using a flexible schema.

Dumps the contents of the database into a CSV file and uploads it as an artifact in GitHub Actions.

Runs automatically on a daily schedule to continuously update and expand the dataset.

Works entirely with GitHub’s default token and does not require any private secrets.

# Pipeline Structure

The GitHub Actions pipeline includes the following steps:

PostgreSQL service container:
A PostgreSQL 15 service is started in the workflow environment using a container.

Setup and dependency installation:
The workflow installs Python 3.11 and dependencies listed in requirements.txt.

Setup-postgres step:
When the crawler runs, the database schema and table are automatically created if they do not exist.

Crawl-stars step:
The crawler uses the GitHub GraphQL API to collect data on repositories and their star counts.
It fetches data asynchronously to minimize duration and handle API rate limits.

Dump and upload artifact:
The PostgreSQL data is exported to a CSV file (repos.csv) and uploaded as an artifact at the end of the run.

Default GitHub token only:
The workflow uses the default ${{ github.token }} for authentication and does not require any custom tokens or secrets.





# Handling 100,000 Repositories

Each run fetches approximately 1,000 repositories due to GitHub’s default rate limits.
To reach 100,000 repositories, the crawler saves its last pagination cursor (last_cursor.json) and resumes from where it left off during the next run.
The workflow runs daily through GitHub Actions, allowing the dataset to grow incrementally until the target of 100,000 repositories is achieved.

# Scaling to 500 Million Repositories

If this crawler were scaled to 500 million repositories, the following changes would be made:

Rate Limits: Distribute crawling across multiple GitHub tokens or a GitHub App for higher rate limits.

Database Scaling: Use sharded or distributed databases such as AWS RDS or Google Cloud SQL.

Parallel Crawling: Deploy multiple crawler instances to process data concurrently.

Incremental Updates: Crawl only repositories that changed since the last run using timestamps.

Data Storage: Move older data to a data warehouse (e.g., BigQuery, Snowflake) for analytical use.

# Schema Evolution for More Metadata

If we need to collect additional data in the future (issues, pull requests, comments, CI checks, etc.),
the schema can evolve by adding new tables linked through foreign keys (repo_id, pr_id, etc.).
For example:

A pull_requests table referencing repositories(repo_id)

A pr_comments table referencing pull_requests(pr_id)

This structure ensures efficient updates, as new data affects only specific tables and minimal rows.

Clean Architecture and Software Engineering Practices

Immutability: Repository objects are defined as immutable data classes.

Separation of Concerns: GitHub API logic, database logic, and orchestration are separated across modules.

Anti-Corruption Layer: The GitHub client shields the system from API changes.

Efficient Updates: UPSERT ensures only changed data is updated in the database.

Automated Execution: The pipeline runs automatically without manual intervention.

# Output

At the end of each run, the workflow uploads a file named repos.csv containing the data from the repositories table.
This file can be downloaded from the workflow’s artifacts section.




