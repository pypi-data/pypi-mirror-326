# FastAPI Kickstart

A simple FastAPI kickstart library for creating APIs quickly and easily.

## Installation

To install the library, use `pip`:

```sh
pip install fastapi-kickstart

## Usage

Here's an example of how to use the library:

```python
from fastapi import FastAPI
from fastapi_kickstart.main import app

# Run the FastAPI app
# uvicorn fastapi_kickstart.main:app --reload

## Endpoints

- `GET /`: Returns a welcome message.
- `GET /get-item/{item_id}`: Retrieves an item by its ID.
- `POST /create-item/{item_id}`: Creates a new item.
- `PUT /update-item/{item_id}`: Updates an existing item.
- `DELETE /delete-item/{item_id}`: Deletes an item.

## NOTE: 
Detailed instructions can be found here https://madalynbartman.github.io/sunday-summary/2024/12/15/FastAPI.html