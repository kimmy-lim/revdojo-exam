# Setup Instructions

## Requirements
- Python 3.10+
- Django 3.5+

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/kimmy-lim/revdojo-exam.git

# List of API Endpoints

## Create Vehicle  
This endpoint will create a vehicle data.  
Endpoint: /vehicle  
Method: POST  
Content-Type: application/json  
Expected data in request body:  
- VIN or vin
  - type: Int
  - max-lenght: 17
  - unique: Yes
- stock_number
  - type: Int
  - max-lenght: 10
- status
  - type: Char
  - options: 'ONS' or 'SLD'
- vehicle_type
  - type: Char
  - options: 'NEW' or 'USED'
- description
  - type: Text
  - nullable: True
- price
  - type: Float
- photos_count
  - type: Int

Sample request body:
```
{
    'VIN': 10000000000000002,
    'stock_number': 1000000002,
    'status': 'SLD',
    'vehicle_type': 'USED',
    'description': 'Used Toyota Innova',
    'price': 15500000.50,
    'photos_count': 8,
}
```

Sample success response:
```
{'message': 'Vehicle created'}
status code: 200
```

## Update Vehicle Details
This endpoint will update a Vehicle data's details (except for status and end_date) using it's VIN.  
Endpoint: /vehicle/<int:vin>  
Method: PUT  
Content-Type: application/json  
> Note: It's not necessary to include all the data below. 

Data that can be added in the request body:  
- stock_number
  - type: Int
  - max-lenght: 10
- vehicle_type
  - type: Char
  - options: 'NEW' or 'USED'
- description
  - type: Text
  - nullable: True
- price
  - type: Float
- photos_count
  - type: Int

Sample request body:
```
{
    'stock_number': 1000000002,
    'vehicle_type': 'NEW',
}
```

Sample success response:
```
{'message': 'Vehicle updated'}
status code: 200
```

## Update Vehicle Status
This endpoint will update a vehicle's status to SLD.  
Endpoint: /vehicle/<int:vin>/sold  
Method: PATCH  
Content-Type: application/json  
> Note: A body is not required as the purpose of this endpoint is to change a vehicle's status to SLD and add in their end_date data. 

Sample success response:
```
{'message': 'Vehicle status updated'}
status code: 200
```

## Create Vehicle Statistics
This endpoint will create a statistic data for a specific vehicle.  
Endpoint: /vehicle/statistics
Method: POST  
Content-Type: application/json  
Expected data in request body:  
- VIN or vin
  - type: Int
  - max-lenght: 17
  - unique: Yes
- source
  - type: Char
  - options: 'ABC', 'XYZ' or 'QWE'
- vdp
  - type: Int
- srp
  - type: Int

Sample request body:
```
{
    'vin': 10000000000000001,
    'source': 'XYZ',
    'vdp': 30,
    'srp': 205,
}
```

Sample success response:
```
{'message': 'Vehicle statistics created'}
status code: 200
```

## Get Vehicle Details
This endpoint will give the details of a vehicle and their statistics grouped by their source. It allows combination of filters listed below.  
Endpoint: /vehicle/statistics
Method: GET  
Content-Type: application/json  
> Note: The response data is grouped by vehicle and source

Possible filters:  
- VIN or vin
  - type: Int
  - max-lenght: 17
  - unique: Yes
- stock_number
  - type: Int
  - max-lenght: 10
- vehicle_type
  - type: Char
  - options: 'NEW' or 'USED'
- source
  - type: Char
  - options: 'ABC', 'XYZ' or 'QWE'
- start_date
  - type: date string
  - format: YYYY-MM-DD
  - filters date in Statistics model
- end_date
  - type: date string
  - format: YYYY-MM-DD
  - filters date in Statistics model

Sample success response:
```
{
  'data': [{
      'VIN': '10000000000000001',
      'Stock Number': '1000000001',
      'Start Date': '2024-12-24',
      'Vehicle Type': 'NEW',
      'Description': 'Brand new Toyota Vios',
      'Price': 12000000.5,
      'Photos Count': 5,
      'Total VDP Count': 120,
      'Total SRP Count': 240,
      'Source': 'ABC'},
    {
      'VIN': '10000000000000001',
      'Stock Number': '1000000001',
      'Start Date': '2024-12-24',
      'Vehicle Type': 'NEW',
      'Description': 'Brand new Toyota Vios',
      'Price': 12000000.5,
      'Photos Count': 5,
      'Total VDP Count': 300,
      'Total SRP Count': 150,
      'Source': 'XYZ'}]
}
status code: 200
```

# Database Structure

**Vehicle**
```
vin = models.CharField(max_length=17, unique=True)
stock_number = models.CharField(max_length=10)
start_date = models.DateField(auto_now_add=True)
end_date = models.DateField(null=True, blank=True)
status = models.CharField(max_length=3)
vehicle_type = models.CharField(max_length=4)
description = models.TextField(null=True, blank=True)
price = models.FloatField()
photos_count = models.IntegerField()
```

**Statistics**
```
date = models.DateField(auto_now_add=True)
source = models.CharField(max_length=3)
vdp = models.IntegerField()
srp = models.IntegerField()
vin = models.ForeignKey(Vehicle, to_field='vin', on_delete=models.CASCADE, related_name='stats')
```

**Clean function sample for source field**
```
def clean(self):
    # Validate the field explicitly
    if self.source not in SOURCE_CHOICES:
        raise ValidationError({'error': 'Invalid source value. Allowed values are "ABC", "XYZ" or "QWE".'})
```
## Database Thought Process
Since the fields and their specifications were already listed in the instructions given, I went with going as straightforward as possible while trying to see imagine which fields could allow null or blank values in case a user decides it's too bothersome to key in.  
The addition that I've done for my models was add in a clean function that would validate status, vehicle_type, and source as these three fields should only be accepting specific things.

# Coding Thought Process
My original intention when I first read the exam was to make multiple functions but I wanted to minimize the amount of url endpoints and thought that it could be cleaner if the API were grouped together.  
The first API is inside the VehicleView class. I didn't intend to put it all in one class but as I was working on it, it just made sense that they're together.  

I started with the create vehicle endpoint as it was the prerequisite of everything else and opt for using POST method since it would be better if the data wasn't openly exposed in the url.  
I wanted to avoid as much user error as possible so I added checking for content-type, checking if the json body they sent was valid, and lastly, go through the keys in the data and lower it down just in case someone key in 'VIN' rather than 'vin'.  
The next step was to validate the data to the model (i.e. checking if the characters are within the character limit, etc). This was easily done by calling the full_clean() method of Django models.  
Once that's all done, we save the data and return a status code 200 and a short message that says 'Vehicle created'.  

For the next endpoint, I chose the update vehicle details as I thought it had more to update compared to the status update. I had it under PUT as I thought it was beffiting that method commonly used for updates.  
I added a list called ignore_field which contains vin and status as these two were not intended to be updated. VIN, in my point of view, was my primary key and giving the user the ability to update it casually could turn chaotic.  

I was unable to change vin into primary_key in the models mainly due to time constraint on my part. I attempted it but it caused issues in my migration files so I opt out of it, but admittedly, this should have been done in my initial migration file.  
The same steps to avoid user error was placed here as well and I opt to loop into the data sent for processing and using setattr() as I thought it would be the easier and cleaner was of doing things in comparison to a block of if conditions.  
Once the data is saved, it would also return a status code 200 and a short message that says 'Vehicle updated'.  

For the last enpoint in the first API, I used PATCH since it's said to be used for partial updates. 
I originally wanted to have this similar to the update vehicle details but I thought it would be redundant.  
Then I had this thought that this endpoint's goal was to update the status of a vehicle so rather than adding the additional checks I had in the previous two endpoints, I just went straight to checking if the vehicle exists and then updating it immediately.  
The room for user error is a lot smaller here since the most important data was the vin and the get_object_or_404() method was enough to handle issues of non-existent vin.  

As for the second API, I had to add in one more endpoint which would create a statistic data for a vehicle.  
Originally, I planned to put that endpoint with the first API but the more I worked on it, the more I realized that it would be better to group this endpoint with the get details endpoint since both would be accessing both Vehicle and Statistic models unlike the first API that only uses the Vehicle model.  

The create statistic endpoint follows the format of the create vehicle endpoint. It was here that I realized my mistake with forgetting to make vin as my primary key.  
Overall, very similar to the create vehicle endpoint except for the minor changes so the data fits the Statistics model.  

The get vehicle details is probably the longest I worked with as I had an internal debate on how the filters would work and interact (i.e. if vin or stock_number was a mandatory filter), and I unfortunately do not have the time to ask more question as I did not expect myself to be busy with holiday preparations as well.  
I decided to go with the assumption that the filters listed in the instructions can be used at the same time. I had initialized all the variables that would get the filters and if they weren't used then they are defaulted to None.  
I also had the vehicle model filtered for 'ONS' status first as it was in the instructions that only On sale items are to be returned. After getting all ONS vehicled, I have a block of conditional statements to check and add more filters as asked by the user in their request.  

Next, I looped through each vehicle and filtered it all accordingly as well. Once that was done, my next dilema came from how I wanted to present the data.  
Given the list of columns in the instructions and the fact that I have written in that vin or stock_number as optional filters, it was possible to have either more than one vehicle or more than one source. The instruction seemed to imply that it's expecting only one data to return, but with the assumption I'm working with, multiple data was likely to occur.  
For consistency sake, I decided to continue with what I already have and allow my data response to return more than one data.  
While looping through each vehicle, I took the list of distinct sources and loop through and filter each source in the Statistics model before building the structured response to be appended to the final list of response data. 
Once that's done, I return the reponse data with status code 200.
