# AI_NOTES.md

## AI Tools Used

* ChatGPT (OpenAI)

## How AI Was Used

AI was used as a development assistant throughout the project. My workflow was as follows:

1. I designed the overall architecture, project structure, and implementation approach for the API before writing the application.
2. I consulted AI for FastAPI and Python best practices, including project organization, REST API design, and testing strategies.
3. I asked AI to generate initial skeletons for individual files (such as models, routes, storage, and tests) based on the requirements. These served as starting points rather than final implementations.
4. I implemented the application by completing and integrating the code, ensuring it met the assignment requirements.
5. After implementation, I used AI to review the code for readability, maintainability, and adherence to best practices.
6. When issues arose during development, I debugged them with AI's assistance by analyzing error messages, identifying root causes, and applying the appropriate fixes.
7. AI also assisted in drafting the project README documentation.

## What I Validated, Tested, or Changed

I reviewed and validated all AI-assisted output before including it in the project. In particular, I:

* Replaced deprecated FastAPI startup events with the recommended lifespan implementation.
* Refined the storage layer to support configurable file paths, making it easier to isolate test data.
* Ensured expense IDs remain unique and are not reused after deletion.
* Implemented proper RESTful HTTP responses, including `201 Created`, `204 No Content`, and `404 Not Found`.
* Improved the total summary response to return `"Overall"` when no category filter is applied.
* Verified all endpoints manually using the FastAPI Swagger UI.
* Wrote and executed an automated test suite covering the required functionality and common validation scenarios, resulting in all tests passing successfully.

## AI Suggestions Not Used

Some AI suggestions were intentionally not adopted because they were unnecessary for the scope of this assignment. These included:

* Introducing a database instead of the required local JSON storage.
* Making the storage layer asynchronous despite using synchronous file I/O.
* Adding additional abstraction layers that would increase complexity without providing meaningful benefits for this project.

I chose to keep the implementation focused, lightweight, and aligned with the assignment requirements while following standard Python and FastAPI best practices.
