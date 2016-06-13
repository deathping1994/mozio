# Mozio- Provider service

Master Branch contains List of polygons implementation for service area (Slightly slower)
multipolygon Branch contains Multipolygon implementation for service area (can be made faster with geowithin query and 2dsphereindexes)

Note: While using caching I've ignored thundering herd problem but that can be resolved using caceh.get_or_set()

#### Cache expiry time is 15 minutes for search results so if the search results are not as expected then wait for 15 minutes
#### All the known issues with delete and update service area have been fixed
#### Update[11/06/2016 11:19pm IST] Api is live at http://mozio.gauravshukla.xyz:8080/
#### <s>Update[11/06/2016 9:58pm IST]: I'll not be deploying this to aws because I don't have enough memory left on ews to install mongodb </s>
Provider service stores details of providers and performs search query on their service area.
It also allows user to update service area
# Current Status
It's almost time for submission so I am dropping an update.
- <s>The api part is done and there are some known issues.</s>
- Code is available at https://github.com/deathping1994/mozio

## Some choices and assumptions:
- I've used mongodb along with mongoengine
- Turns out mongoengine was a bad choice but I had to use it to stick to django ORM, - - alternative could have been using pymongo and enforcing the model validation manually
- I chose mongodb due to it's geo-spatial querying capabilities
- For Caching I've used redis
- I've assumed there would be some authentication method in place so I've not implemented and authentication
- If I were to implement something then it would have been token based authentication with token cached into redis
## Challenges:
- It was my first time trying to integrate mongodb and django so the basic setup took more time than expected
- I've never worked with geoJson before so figuring out the types of geometry took some time but it was quick 
- It was my second time trying to write unit tests with mongodb and Django and it is something I haven't figured out yet :(
## Known issues:
- <s>Deleting and updating the service area has not been tested well</s> FIXED
- I could not get test to run successfully because of the mongoengine not playing nice with django test runner, tests are written but partial 

## Models: Provider 
 Stores details of Provider
 
    class Provider(Document):
        name = StringField(max_length=30)
        email = EmailField(unique=True)
        phone = StringField(max_length=12)
        lang = StringField()
        currency = StringField(max_length=10)
        service_area = ListField(PolygonField())

## Error Handler

    def error_handler(e):
        response = dict()
        if isinstance(e,KeyError):
            response['error'] = str(e) + "is missing"
            response['stat'] = 400
        elif isinstance(e, DoesNotExist):
            response['error'] = "Service provider does not exist"
            response['stat'] = 400
        elif isinstance(e,ValidationError):
            response['error'] = e.message
            response['stat'] = 400
        elif isinstance(e, NotUniqueError):
            response['error'] = "Email Id already Registered"
            response['stat'] = 400
        elif isinstance(e,MethodError):
            response['error'] = e.msg
            response['stat'] = 400
        elif isinstance(e, ValueError):
            response['error'] = str(e)
            response['stat'] = 400
        elif isinstance(e, OperationError):
            response['error'] = str(e)
            response['stat'] = 400
        else:
            response['error'] = "Something went wrong"
            response['stat'] = 500
            print str(e)
            print type(e)
        return json_response(json.dumps(response), response['stat'])

## Api End Points
### endpoint: /provider/search/?lat={{latitude}}&&long={{longitude}}
    *** method: GET *** 
            response: Array of Service Provider objects that provide service at that lat,long
            eg : mozio.gauravshukla.xyz:8080/provider/search/?lat=5&&long=5.001
            response:
             [
          {
            "name": "Jytoi SHukla",
            "currency": "INR",
            "service_area": {
              "type": "Polygon",
              "coordinates": [
                [
                  [
                    0,
                    0
                  ],
                  [
                    10,
                    10
                  ],
                  [
                    10,
                    0
                  ],
                  [
                    0,
                    0
                  ]
                ]
              ]
            },
            "phone": "+91842343",
            "_cls": "Provider",
            "_id": {
              "$oid": "575c4d35a4fabe6cee145a53"
            },
            "email": "gaura.dhuk@m.com"
          }
        ]
### endpoint: /provider/:id:/
        *** method: GET ***
        response: Service provider object stored in Database
        eg: http://localhost:8000/provider/575be1380341ac5a66a4a647/ 
        (Don't forget the trailing slash, without the trailing slash array of all objects is returned)
            response:{
                  "_id": {
                    "$oid": "575be1380341ac5a66a4a647"
                  },
                  "_cls": "Provider",
                  "name": "GAurav SHukla",
                  "email": "gaurva.dhk@m.com",
                  "phone": "+91842343",
                  "lang": "INR",
                  "service_area": {
                    "type": "Polygon",
                    "coordinates": [
                      [
                        [
                          0,
                          0
                        ],
                        [
                          10,
                          10
                        ],
                        [
                          10,
                          0
                        ],
                        [
                          0,
                          0
                        ]
                      ]
                    ]
                  }
                }
        *** method: Post ***
        body: Json (name,email,phone,currency)
        response: 201, Newly created Service provider object
        eg: localhost:8000/provider/
            Body: {
                    "lang": "eng",
                    "phone": "+91842343",
                    "name":"Jytoi SHukla",
                    "currency":"INR",
                    "email": "gaua.dhuk@m.com"
                }
            Response:{
                  "_id": {
                    "$oid": "575c263e0341ac14c13b28b3"
                  },
                  "_cls": "Provider",
                  "name": "Jytoi SHukla",
                  "email": "gaua.dhuk@m.com",
                  "phone": "+91842343",
                  "currency": "INR"
                }
        *** method: PUT ***
        body: Json (name,email,phone,currency)
        response: 200, Updated Service Provider Object
        eg:localhost:8000/provider/575be1380341ac5a66a4a647/
        Body: {
            "lang": "eng",
            "phone": "+91842343",
            "name":"Jytoi SHukla",
            "currency":"YEN",
            "email": "gaa.dhuk@m.com"
            
        }
        Response: {
          "_id": {
            "$oid": "575be1380341ac5a66a4a647"
          },
          "_cls": "Provider",
          "name": "Jytoi SHukla",
          "email": "gaa.dhuk@m.com",
          "phone": "+91842343",
          "lang": "INR",
          "currency": "YEN",
          "service_area": {
            "type": "Polygon",
            "coordinates": [
              [
                [
                  0,
                  0
                ],
                [
                  10,
                  10
                ],
                [
                  10,
                  0
                ],
                [
                  0,
                  0
                ]
              ]
            ]
          }
        }
       *** method: Delete ***
        response: 204, No content
### endpoint: /provider/all
        *** method: GET ***
        response: Array of all service provider objects
        eg:
        Response:
        [
  {
    "name": "Gaurav SHukla",
    "currency": "INR",
    "service_area": [],
    "phone": "+918375847862",
    "_cls": "Provider",
    "_id": {
      "$oid": "575d1402a4fabe42b9b9b885"
    },
    "email": "gaua.dh@m.com"
  },
  {
    "name": "Jytoi SHukla",
    "currency": "INR",
    "service_area": [
      {
        "type": "Polygon",
        "coordinates": [
          [
            [
              43.9453125,
              58.07787626787517
            ],
            [
              43.9453125,
              43.58039085560786
            ],
            [
              52.03125,
              48.69096039092549
            ],
            [
              54.140625,
              56.75272287205736
            ],
            [
              43.9453125,
              58.07787626787517
            ]
          ]
        ]
      },
      {
        "type": "Polygon",
        "coordinates": [
          [
            [
              79.1015625,
              63.54855223203644
            ],
            [
              123.74999999999999,
              68.65655498475735
            ],
            [
              119.88281249999999,
              48.69096039092549
            ],
            [
              83.3203125,
              52.05249047600099
            ],
            [
              92.8125,
              45.089035564831036
            ],
            [
              71.015625,
              53.74871079689897
            ],
            [
              75.9375,
              58.63121664342478
            ],
            [
              92.10937499999999,
              56.36525013685606
            ],
            [
              102.3046875,
              61.10078883158897
            ],
            [
              85.078125,
              62.59334083012024
            ],
            [
              75.234375,
              60.58696734225869
            ],
            [
              79.1015625,
              63.54855223203644
            ]
          ]
        ]
      }
    ],
    "phone": "+918423438900",
    "_cls": "Provider",
    "_id": {
      "$oid": "575d138ca4fabe42b9b9b884"
    },
    "email": "gaua.dhuk@m.com"
  }
]

### endpoint: /provider/:id:/area/
        *** method: GET ***
        response: Service area of service provider with id passes in url
        eg: localhost:8000/provider/575be1380341ac5a66a4a647/area/
            Response: {
              "type": "Polygon",
              "coordinates": [
                [
                  [
                    0,
                    0
                  ],
                  [
                    10,
                    10
                  ],
                  [
                    10,
                    0
                  ],
                  [
                    0,
                    0
                  ]
                ]
              ]
            }
    
        *** method: Post ***
        body: Json (service_area: <array of valid polygon coordinate>)
        response: 200, Updated Service provider object
### Notice that service area must be valid GeoJson Polygon Line String
        eg: localhost:8000/provider/575be1380341ac5a66a4a647/area/
        Body:{
             "service_area": 
                  [[
                    [
                      0,
                      0
                    ],
                    [
                      10,
                      11
                    ],
                    [
                      12,
                      13
                    ],
                    [
                      0,
                      0
                    ]
                  ]]
                  
            }
        Response:
            {
              "_id": {
                "$oid": "575be1380341ac5a66a4a647"
              },
              "_cls": "Provider",
              "name": "Jytoi SHukla",
              "email": "gae.dhuk@m.com",
              "phone": "+91842343",
              "lang": "INR",
              "currency": "YEN",
              "service_area": {
                "type": "Polygon",
                "coordinates": [
                  [
                    [
                      0,
                      0
                    ],
                    [
                      10,
                      11
                    ],
                    [
                      12,
                      13
                    ],
                    [
                      0,
                      0
                    ]
                  ]
                ]
              }
            }
        *** method: PUT ***
        body: Json (service_area: <Polygon strings to add in existing polygon list>)
        response: 200, Updated Service Provider Object
        eg:
            Body: {
                 "service_area":
                      [[
                        [
                          3,
                          0
                        ],
                        [
                          10,
                          11
                        ],
                        [
                          17,
                          13
                        ],
                        [
                          3,
                          0
                        ]
                      ]]
                      
                }
        *** method: Delete ***
        body: Json(service_area: <Polygon strings to delete from polygon list >)
        response: 200, Updated Service provider object with one line string removed
        eg: 
            Body:    {
         "service_area":[
              [
                [
                  0,
                  0
                ],
                [
                  10,
                  11
                ],
                [
                  12,
                  13
                ],
                [
                  0,
                  0
                ]
              ]
              ]
        }
 .      Response:
            {
            
              "_id": {
                "$oid": "575be1380341ac5a66a4a647"
              },
              "_cls": "Provider",
              "name": "Jytoi SHukla",
              "email": "gae.dhuk@m.com",
              "phone": "+91842343",
              "lang": "INR",
              "currency": "YEN",
              "service_area": {
                "type": "Polygon",
                "coordinates": [
                  [
                    [
                      0,
                      0
                    ],
                    [
                      10,
                      11
                    ],
                    [
                      12,
                      13
                    ],
                    [
                      0,
                      0
                    ]
                  ]
                ]
              }
            }
