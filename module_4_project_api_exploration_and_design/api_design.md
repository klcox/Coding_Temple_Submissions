# Module 4 Project — Part 2: Study Tracker API Design



**Version: v1**



---



## The App: Study Tracker

This API design pertains to a Study Tracker app. Students utilize the app to enroll in courses, set weekly study goals per course, log study sessions, and track progress. The purposes of the app include facilitating organized, efficient studying, fostering encouragement and confidence in students as they visualize their progress, and, ultimately, aiding overall student success in their respective courses.



---



## Section 1 — Resources



|**Resource**|**Description**|**Key Attributes**|
|-|-|-|
|Students|People who use the platform|student_id, name, email_address, phone, date_created|
|Courses|Classes for which students set goals and log study sessions|course_id, course_num, subject, title, instructor, course_start, course_end|
|Study Sessions|Study sessions which students log per course|session_id, student (object), course_id, session_start, session_end, total_hours, notes (optional)|
|Goals|Study goals (target hours) which students set weekly per course|goal_id, student (object), course_id, goal_start, goal_end, target_hours, description (optional)|







## Section 2 — Relationships



|**Relationship**|**Type**|**Description**|
|-|-|-|
|Students, Courses|Many-to-many|A student can be enrolled in multiple courses, and a course can have multiple students enrolled|
|Students, Study Sessions|One-to-many|A student can have multiple study sessions, but each study session belongs to one student|
|Students, Goals|One-to-many|A student can have multiple goals, but each goal belongs to one student|
|Courses, Study Sessions|One-to-many|A course can have multiple study sessions, but each study session belongs to one course|
|Courses, Goals|One-to-many|A course can have multiple goals, but each goal belongs to one course|







## Section 3 — Endpoints



|**HTTP Method**|**URI**|**Description**|
|-|-|-|
|POST|/auth/login|User (student) log-in|
|-|-|-|
|GET|/students/{student_id}|Get a specific student profile|
|POST|/students|Create a new student account|
|PATCH|/students/{student_id}|Update a specific student account/profile|
|DELETE|/students/{student_id}|Delete a specific student account|
|-|-|-|
|GET|/courses|List all courses|
|GET|/courses?course_num=101&subject=BIO|Filter courses (e.g. by course_num and subject)|
|GET|/students/{student_id}/courses|List all courses in which a specific student is enrolled|
|GET|/courses/{course_id}|Get details for a specific course|
|POST|/courses|Create a new course|
|PATCH|/courses/{course_id}|Update a specific course|
|DELETE|/courses/{course_id}|Delete a specific course|
|-|-|-|
|GET|/students/{student_id}/sessions|List all study sessions for a specific student|
|GET|/students/{student_id}/sessions?course_id=2|Filter study sessions for a specific student (e.g. by course_id)|
|POST|/students/{student_id}/sessions|Log a new study session|
|PATCH|/students/{student_id}/sessions/{session_id}|Update a specific study session for a specific student|
|DELETE|/students/{student_id}/sessions/{session_id}|Delete a specific study session for a specific student|
|-|-|-|
|GET|/students/{student_id}/goals|List all goals for a specific student|
|GET|/students/{student_id}/goals?course_id=2|Filter goals for a specific student (e.g. by course_id)|
|POST|/students/{student_id}/goals|Create a new weekly goal for a specific student|
|PATCH|/students/{student_id}/goals/{goal_id}|Update a specific goal for a specific student|
|DELETE|/students/{student_id}/goals/{goal_id}|Delete a specific goal for a specific student|
|-|-|-|
|GET|/students/{student_id}/progress|Get progress toward all study goals for a specific student|
|GET|/students/{student_id}/courses/{course_id}/progress|Get progress toward all study goals for a specific course, for a specific student|
|GET|/students/{student_id}/goals/{goal_id}/progress|Get progress toward a specific study goal for a specific student|



Note: As each goal covers a particular week of study, progress would be calculated from existing resource attributes, e.g. date ranges for goals and study sessions, target_hours for goals, and total_hours per session.







## Section 4 — Request/Response Schemas



### POST /students/{student_id}/sessions — Log a new study session



**Request body:**
```json
{
	"course_id": 2,                                     ← integer, required

	"session_start": "2026-09-15T13:30:00",             ← datetime, required

	"session_end": "2026-09-15T15:30:00"	            ← datetime, required
}
```

**Success response (201 Created):**
```json
{
	"session_id": 1,                                    ← integer

	"student": {                                        ← object

		"student_id": 1,		                          ← integer

		"name": "Kelly Cox",                              ← string

		"email_address": "test@gmail.com",                ← string

		"phone": "555-555-5555",                          ← string

		"date_created": "2026-09-13T16:00:00"             ← datetime
	},

	"course_id": 2,                                     ← integer

	"session_start": "2026-09-15T13:30:00",             ← datetime

	"session_end": "2026-09-15T15:30:00",               ← datetime

	"total_hours": 2.00,                                ← float 

	"notes": null	                                    ← string or null (optional for request)
}
```



### POST /students/{student_id}/goals — Create a new weekly goal



**Request body:**
```json
{ 
	"course_id": 2,                                     ← integer, required

	"goal_start": "2026-09-14T00:00:00",                ← datetime, required

	"goal_end": "2026-09-20T23:59:00",                  ← datetime, required

	"target_hours": 15.00                               ← float, required
}
```

**Success response (201 Created):**
```json
{
	"goal_id": 1,                                       ← integer

	"student": {                                        ← object

		"student_id": 1,                                 ← integer

		"name": "Kelly Cox",                             ← string

		"email_address": "test@gmail.com",               ← string

		"phone": "555-555-5555",                         ← string

		"date_created": "2026-09-13T16:00:00"            ← datetime

	},

	"course_id": 2,                                     ← integer

	"goal_start": "2026-09-14T00:00:00",                ← datetime

	"goal_end": "2026-09-20T23:59:00",                  ← datetime

	"target_hours": 15.00,                              ← float

	"description": null                                 ← string or null (optional for request)
}
```

### GET /students/{student_id}/goals?course_id=2 — Get (filter) all goals for a specific student for a specific course



**Response (200 OK):**
```json
{
	"data": [                                            ← list of dictionaries
		{
			"goal_id": 1,                                     ← integer

			"student": {                                      ← object

				"student_id": 1,                               ← integer

				"name": "Kelly Cox",                           ← string

				"email_address": "test@gmail.com",             ← string

				"phone": "555-555-5555",                       ← string

				"date_created": "2026-09-13T16:00:00"          ← datetime

			},

			"course_id": 2,                                   ← integer

			"goal_start": "2026-09-14T00:00:00",              ← datetime

			"goal_end": "2026-09-20T23:59:00",                ← datetime

			"target_hours": 15.00,                            ← float

			"description": null                               ← string or null
		},

		[...additional goals]

	],

	"meta": { 

		"total": 10,                                          ← integer

		"page": 1,                                            ← integer

		"per_page": 5,                                        ← integer

		"total_pages": 2                                      ← integer
	
	}
}
```


### GET /students/{student_id}/progress — Get progress for a specific student



**Response (200 OK):**
```json
{
	"data": [                                             ← list of dictionaries
		{
			"course_id": 2,                                   ← integer

			"goal_id": 1,                                     ← integer

			"target_hours": 15.00,                            ← float

			"hours_studied": 2.00,                            ← float

			"progress_percent": 13.33                         ← float

		},

		[...additional progress objects]

	],

	"meta": {

		"total": 15,                                          ← integer

		"page": 1,                                            ← integer

		"per_page": 5,                                        ← integer 

		"total_pages": 3                                      ← integer	
	}
}
```




## Section 5 — Authentication



|**Endpoint**|**Auth Required**|**Who can access?**|
|-|-|-|
|POST /auth/login|No|Students with an account (password required)|
|-|-|-|
|GET /students/{student_id}|Yes|Only the student themself|
|POST /students|No|Public|
|PATCH /students/{student_id}|Yes|Only the student themself|
|DELETE /students/{student_id}|Yes|Only the student themself|
|-|-|-|
|GET /courses|Yes|Any logged-in student|
|GET /courses?course_num=101&subject=BIO|Yes|Any logged-in student|
|GET /students/{student_id}/courses|Yes|Only the student themself|
|GET /courses/{course_id}|Yes|Any logged-in student|
|POST /courses|Yes|Admin only|
|PATCH /courses/{course_id}|Yes|Admin only|
|DELETE /courses/{course_id}|Yes|Admin only|
|-|-|-|
|GET /students/{student_id}/sessions|Yes|Only the student themself|
|GET /students/{student_id}/sessions?course_id=2|Yes|Only the student themself|
|POST /students/{student_id}/sessions|Yes|Only the student themself|
|PATCH /students/{student_id}/sessions/{session_id}|Yes|Only the student themself|
|DELETE /students/{student_id}/sessions/{session_id}|Yes|Only the student themself|
|-|-|-|
|GET /students/{student_id}/goals|Yes|Only the student themself|
|GET /students/{student_id}/goals?course_id=2|Yes|Only the student themself|
|POST /students/{student_id}/goals|Yes|Only the student themself|
|PATCH /students/{student_id}/goals/{goal_id}|Yes|Only the student themself|
|DELETE /students/{student_id}/goals/{goal_id}|Yes|Only the student themself|
|-|-|-|
|GET /students/{student_id}/progress|Yes|Only the student themself|
|GET /students/{student_id}/courses/{course_id}/progress|Yes|Only the student themself|
|GET /students/{student_id}/goals/{goal_id}/progress|Yes|Only the student themself|



**Auth method and rationale:**



The auth method should be JWT (JSON Web Token) as it is standard for user-level authentication in modern applications. User-level authentication is necessary for this app as it is intended for individual use such that each student should only be able to access their own courses, study sessions, and goals. Hence, an API key would not be sufficient as it only identifies the application/client (not the user), and, considering the app's current version, I do not see a need to involve a third-party for OAuth.



To obtain a JWT:

1. The user would send their username and password to the login endpoint noted above.
2. The server would verify the credentials, create the JWT if verified, and return the JWT to the client.
3. The client (user) would then include the token in the Authorization header of every subsequent request (e.g. `"Authorization": f"Bearer {JWT}"`)
4. With each request, the server verifies the token in order to identify the user and to determine authorization.



---



## Section 6 — Error Responses for POST /students/{student_id}/sessions



|**Status Code**|**Description**|**Occurs When**|
|-|-|-|
|201|Created|The study session was logged successfully|
|400|Bad Request|Required fields are missing|
|401|Unauthorized|The request requires auth, but the token was either missing or invalid|
|404|Not Found|The student or course does not exist|
|422|Unprocessable Entity|The request contains valid JSON, but one or more values are not the correct data type or format, or one or more values violate a validation rule (e.g., the study session falls outside the date range for the applicable course)|
|429|Too Many Requests|Too many API calls were made within the time limit|
|500|Internal Server Error|There is an unexpected server error|
|503|Service Unavailable|The server is overloaded or down for maintenance|







## Section 7 - Notes for Future Consideration



* Cascading deletions - when deleting an object (student, course, study session, goal), determine how related objects should be handled (e.g. deleted, archived, etc.)
* Validate study session and goal dates — prevent students from creating, updating, or deleting study sessions/goals outside of the applicable course date range





