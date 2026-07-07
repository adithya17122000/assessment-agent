├── app/
│   ├── __init__.py
│   ├── main.py                          # FastAPI app instantiation, router registration
│   │
│   ├── config/
│   │   ├── __init__.py
│   │   ├── settings.py                  # env vars, DB URL, LLM provider config
│   │   └── database.py                  # SQLAlchemy engine/session setup
│   │
│   ├── constants/
│   │   ├── __init__.py
│   │   ├── assessment_constants.py      # status enums (In Progress/Completed), default question count
│   │   └── error_codes.py
│   │
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── datetime_utils.py
│   │   └── id_generator.py              # req-xx, asmt-xx style ID generation
│   │
│   ├── eligibility/                     # Capability: Assessment Eligibility
│   │   ├── __init__.py
│   │   ├── models.py                    # AssessmentEligibility ORM model
│   │   ├── schemas.py                   # Team 3 inbound payload schema, dropdown response schema
│   │   ├── helper.py                # insert row, fetch by employee, fetch by employee+course
│   │   └── service.py                   # topic aggregation/union query logic lives here
│   │
│   ├── assessment_management/           # Capability: Assessment Management
│   │   ├── __init__.py
│   │   ├── models.py                    # AssessmentRequest, Assessment ORM models
│   │   ├── schemas.py                   # request/response schemas for "Take Assessment" flow
│   │   ├── helper.py
│   │   └── service.py                   # orchestrates request creation, status transitions
│   │
│   ├── question_generation/             # Capability: AI Question Generation
│   │   ├── __init__.py
│   │   ├── models.py                    # Question ORM model
│   │   ├── schemas.py
│   │   ├── helper.py
│   │   ├── llm_client.py                # LLM provider integration (provider-agnostic interface)
│   │   └── service.py                   # prompt construction, question generation orchestration
│   │
│   ├── evaluation/                      # Capability: Assessment Evaluation
│   │   ├── __init__.py
│   │   ├── models.py                    # Response, Evaluation ORM models
│   │   ├── schemas.py                   # answer submission schema, scoring output schema
│   │   ├── helper.py
│   │   └── service.py                   # scoring logic, pass/fail determination
│   │
│   ├── result_management/               # Capability: Result Management
│   │   ├── __init__.py
│   │   ├── schemas.py                   # dashboard-facing read response schema
│   │   ├── helper.py                # read-only queries joining Assessment + Evaluation
│   │   └── service.py                   # assembles exposed result payload
│   │
│   ├── employee_integration/             # Team 1 API consumption
│   │   ├── __init__.py
│   │   ├── client.py                    # Team 1 API client
│   │   └── schemas.py                   # employee data shape expected from Team 1
│   │
│   └── api/
│       ├── __init__.py
│       ├── eligibility_routes.py        # Team 3 POST/PATCH endpoint, dropdown GET endpoint
│       ├── assessment_routes.py         # Take Assessment, get questions
│       ├── evaluation_routes.py         # submit responses
│       └── result_routes.py             # dashboard-facing GET endpoint
│
├── requirements.txt
├── .env
└── README.md