# Seared Quail
#### A web application for digital restaurant menus

## Deprecated

This project is no longer being maintained by the owner.

---

![CI](https://github.com/RevolutionTech/seared-quail/actions/workflows/ci.yml/badge.svg)
[![codecov](https://codecov.io/gh/RevolutionTech/seared-quail/branch/main/graph/badge.svg)](https://codecov.io/gh/RevolutionTech/seared-quail)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/bf08621ec3d54837b3d64f8e880f6d9e)](https://www.codacy.com/app/RevolutionTech/seared-quail)

![Seared Quail](https://revolutiontech.s3.amazonaws.com/media/img/searedquail1.png)

## About

Seared Quail is an open-source digital restaurant menu web application. Below are instructions for setup and deployment for which you can create your own Seared Quail instance in a restaurant setting. Once your instance is deployed you can customize the menu in the Django admin interface for your restaurant. You are also welcome to fork the project and make changes specific to your use case as per the license provided in this project.

## Setup

### Prerequisites

Seared Quail requires [PostgreSQL](https://www.postgresql.org/) to be installed.

### Installation

Use [poetry](https://github.com/sdispater/poetry) to install Python dependencies:

    poetry install

### Configuration

Seared Quail reads in environment variables from your local `.env` file. See `.env-sample` for configuration options. Be sure to [generate your own secret key](http://stackoverflow.com/a/16630719).

With everything installed and all files in place, you may now create the database tables. You can do this with:

    poetry run ./manage.py migrate
