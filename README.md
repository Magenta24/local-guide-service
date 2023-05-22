# Web Services and Web Data Coursework 2

## Local Guide Service

### Domain: [http://sc20jmt.pythonanywhere.com/](http://sc20jmt.pythonanywhere.com/)

## Core Endpoints

### /api/attractions

- Listing all attractions (filtered by parameters if provided)
- If no parameter is provided, all attractions are listed
- All listed categories can be obtained by requesting */api/categories*
- E.g. http://sc20jmt.pythonanywhere.com/api/attractions?location=Rivia&category=Natural

| Parameter name | Required? | Value type |          Description           |
|:--------------:|:---------:|:----------:|:------------------------------:|
|    location    |    No     |   String   |          Country name          |
|    category    |    No     |   String   | The category of the attraction |
|   min_price    |    No     |   Number   |         Minimum price          |
|   max_price    |    No     |   Number   |         Maximum price          |
|   adults_no    |    No     |   Number   |     Number of adult guests     |
|    kids_no     |    No     |   Number   |      Number of kid guests      |
|   seniors_no   |    No     |   Number   |    Number of senior guests     |

--------------------------------------------

### /api/tours

- Listing all tours (filtered by parameters if provided)
- If no parameter is provided, all tours are listed
- E.g. http://sc20jmt.pythonanywhere.com/api/tours?location=Czech%20Republic

|   Parameter name   | Required? | Value type |              Description              |
|:------------------:|:---------:|:----------:|:-------------------------------------:|
|      location      |    No     |   String   |  The country the tour takes place in  |
|    duration_max    |    No     |   Number   | Maximum number of days the tour lasts |
|     min_price      |    No     |   Number   |             Minimum price             |
|     max_price      |    No     |   Number   |            Maximum  price             |
| attractions_no_max |    No     |   Number   |     Maximum number of attractions     |
|     adults_no      |    No     |   Number   |        Number of adult guests         |
|      kids_no       |    No     |   Number   |         Number of kid guests          |
|     seniors_no     |    No     |   Number   |        Number of senior guests        |

--------------------------------------------

### /api/book
- Request: method: POST
- Purpose: Booking an attraction/tour
- Response: JSON with the booking details
- Incoming request body: JSON format

|     Parameter name      | Required? | Value type |                                                               Description                                                                |
|:-----------------------:|:---------:|:----------:|:----------------------------------------------------------------------------------------------------------------------------------------:|
| tour_attraction_ID      |    Yes    |   String   | The *tour_attraction_ID* starts with *A* for booking a single attraction and with *T*. <br> e.g. *A2* (booking the attraction with ID=2) |
|         psp_id          |    Yes    |   Number   |                                                               The PSP's ID                                                               |
|     psp_checkout_id     |    Yes    |   Number   |                                                             Transaction's ID                                                             |
|       start_date        |    Yes    |  Datetime  |                                      Tour/attraction's start date in ISO format (e.g. 2024-05-11T13:35:48.123456)                                       |
|        adults_no        |    No     |   Number   |                                                         Number of adults guests                                                          |
|         kids_no         |    No     |   Number   |                                                           Number of kid guests                                                           |
|       seniors_no        |    No     |   Number   |                                                         Number of senior guests                                                          |

--------------------------------------------

### /api/make_tour
- Request: method: POST
- Purpose: Creating a custom tour from already existing attractions
- Response: JSON with the new tour’s details
- Incoming request body: JSON format

| Parameter name | Required? | Value type |                Description                |
|:--------------:|:---------:|:----------:|:-----------------------------------------:|
|   tour_name    |    Yes    |   String   |              New tour's name              |
|  attractions   |    Yes    |   Array    | List of attraction to include in new tour |

--------------------------------------------
## Additional Endpoints
### /api/categories
- listing all categories
- Response: JSON

--------------------------------------------
### /api/discounts
- listing all discounts
- - Response: JSON

--------------------------------------------
### /api/bookings
- listing all bookings
- Response: JSON

--------------------------------------------
### /api/countries
- listing all countries
- Response: JSON

--------------------------------------------

## Running
### Create Python environment
```
python -m venv /path/to/new/env/venv_name
```
### Activate
```
./path/to/new/env/venv_name/bin/activate # activate the environment
```
### Install requirements (Django and Requests)
```
pip install -r requirements.txt
```
### Run the Django server
```
python .\web_services_cw2\manage.py runserver 
```
