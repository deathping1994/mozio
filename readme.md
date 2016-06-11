# Mozio- Provider service
Provider service stores details of providers and performs search query on their service area.
It also allows user to update service area

## Models: Provider 
 Stores details of Provider
 
    class Provider(Document):
        name = StringField(max_length=30)
        email = EmailField(unique=True)
        phone = StringField(max_length=12)
        lang = StringField()
        currency = StringField(max_length=10)
        service_area = PolygonField()

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
### endpoint: /provider/<id>/
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
            "lang": "INR",
            "name": "Jytoi SHukla",
            "phone": "+91842343",
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
            "currency": "YEN",
            "_cls": "Provider",
            "_id": {
              "$oid": "575be1380341ac5a66a4a647"
            },
            "email": "gae.dhuk@m.com"
          },
          {
            "lang": "INR",
            "name": "Jytoi SHukla",
            "phone": "+91842343",
            "_cls": "Provider",
            "_id": {
              "$oid": "575be2970341ac5bcf7aa4be"
            },
            "email": "gaura.dhuk@m.com"
          },
          {
            "name": "Jytoi SHukla",
            "currency": "INR",
            "phone": "+91842343",
            "_cls": "Provider",
            "_id": {
              "$oid": "575c263e0341ac14c13b28b3"
            },
            "email": "gaua.dhuk@m.com"
          }
        ]

### endpoint: /provider/<id>/area/
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
        body: Json (service_area: <array of valid polygon line strings>)
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
        body: Json (service_area: <line strings to add in existing polygon>)
        response: 200, Updated Service Provider Object
        eg:
            Body: {
                 "service_area":
                      [
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
                      ]
                      
                }
            Response: {
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
                  ],
                  [
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
                  ]
                ]
              }
            }
        or
            {
     "service_area":
          [
            [
              1.2,
              0.1
            ],
            [
              1.3,
              0.3
            ],
            [
              1.4,
              0.4
            ],
            [
              1.2,
              0.1
            ]
          ]
          
    }
    
    {
      "stat": 400,
      "error": "Could not save document (Can't extract geo keys: { _id: ObjectId('575be2970341ac5bcf7aa4be'), _cls: \"Provider\", name: \"Jytoi SHukla\", email: \"gaura.dhuk@m.com\", phone: \"+91842343\", lang: \"INR\", service_area: { type: \"Polygon\", coordinates: [ [ [ 1, 0 ], [ 10, 11 ], [ 12, 13 ], [ 1, 0 ] ], [ [ 1.2, 0.1 ], [ 1.3, 0.3 ], [ 1.4, 0.4 ], [ 1.2, 0.1 ] ] ] } }  Secondary loops not contained by first exterior loop - secondary loops must be holes: [ [ 1.2, 0.1 ], [ 1.3, 0.3 ], [ 1.4, 0.4 ], [ 1.2, 0.1 ] ] first loop: [ [ 1, 0 ], [ 10, 11 ], [ 12, 13 ], [ 1, 0 ] ])"
    }
        *** method: Delete ***
        body: Json(service_area: <line strings to delete from polygon>)
        response: 200, Updated Service provider object with one line string removed
        eg: 
            Body:    {
         "service_area":
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
        or ## If you try to delete the only string present in the field
                {
      "stat": 400,
      "error": "ValidationError (Provider:575be1380341ac5a66a4a647) (Invalid Polygon     must contain at least one valid linestring: ['service_area'])"
    }
    
    