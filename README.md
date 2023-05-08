# Web Services and Web Data Coursework 2

## Local Guide Service

### Domain: [http://sc20jmt.pythonanywhere.com/](http://sc20jmt.pythonanywhere.com/)

### Credential to access the admin account

|              |  |
|--------------|----------|
| **Username** | ammar       |
| **Password** | ammar       |

## Core Endpoints

### /api/attractions

- Listing all attractions (filtered by parameters if provided)
- If no parameter is provided, all attractions are listed
- All listed categories can be obtained by requesting */api/categories*
- E.g. http://sc20jmt.pythonanywhere.com/api/attractions?location=Rivia&category=Natural

| Parameter name | Required? | Value type |                Description                |
|:--------------:|:---------:|:----------:|:-----------------------------------------:|
|    location    |    No     |   String   | The country the attraction takes place in |
|    category    |    No     |   String   |      The category of the attraction       |
|   min_price    |    No     |    Int     |               Minimum price               |
|   max_price    |    No     |    Int     |               Maximum price               |

--------------------------------------------

### /api/tours

- Listing all tours (filtered by parameters if provided)
- If no parameter is provided, all tours are listed
- E.g. http://sc20jmt.pythonanywhere.com/api/tours?location=Czech%20Republic

|   Parameter name   | Required? | Value type |              Description              |
|:------------------:|:---------:|:----------:|:-------------------------------------:|
|      location      |    No     |   String   |  The country the tour takes place in  |
|    duration_max    |    No     |    Int     | Maximum number of days the tour lasts |
|     min_price      |    No     |    Int     |            Minimum price              |
|     max_price      |    No     |    Int     |            Maximum  price             |
| attractions_no_max |    No     |    Int     |     Maximum number of attractions     |

--------------------------------------------

### /api/book

- Booking an attraction/tour
- Eg. http://sc20jmt.pythonanywhere.com/api/book?tour_attraction_ID=A2&psp_id=2&psp_checkout_id=2137&start_date=2005-04-0221:37:00.666666
...

|     Parameter name      | Required? | Value type |                                                               Description                                                                |
|:-----------------------:|:---------:|:---------:|:----------------------------------------------------------------------------------------------------------------------------------------:|
| tour_attraction_ID      |    Yes    |   String  | The *tour_attraction_ID* starts with *A* for booking a single attraction and with *T*. <br> e.g. *A2* (booking the attraction with ID=2) |
|         psp_id          |    Yes    |    Int    |                                                               The PSP's ID                                                               |
|     psp_checkout_id     |    Yes    |    Int    |                                                             Transaction's ID                                                             |
|       start_date        |  Yes      | Datetime  |                                                       Tour/attraction's start date                                                       |
|        adults_no        |    No     |    Int    |                                                         Number of adults guests                                                          |
|         kids_no         |    No     |    Int    |                                                           Number of kid guests                                                           |
|       seniors_no        |    No     |    Int    |                                                         Number of senior guests                                                          |

--------------------------------------------

### /api/make_tour
- Creating a new tour from existing attractions providing IDs of attractions in a list
- E.g. http://sc20jmt.pythonanywhere.com/api/make_tour?attractions=[1,2,4]

--------------------------------------------
## Additional Endpoints
### /api/categories
- listing all categories

--------------------------------------------
### /api/discounts
- listing all discounts

--------------------------------------------
### /api/bookings
- listing all bookings

--------------------------------------------
### /api/add_attraction
- adding a new attraction to the database

--------------------------------------------
```
cd existing_repo
git remote add origin https://gitlab.com/Calanthe/web-services-cw2.git
git branch -M main
git push -uf origin main
```

