# exam-generator

A web application that generates new exams in the form and style of an old exam using a RAG model.

## How to start the application

### Prerequisites

1. **Docker Desktop** must be running (green icon / "Engine running") before proceeding.

2. **Set the LLM API Key** in your terminal.

   Get the API key from the WhatsApp group. NEVER commit the key to code – anyone on GitHub could steal it!

   These environment variables are **only valid while the terminal is open**. You need to set them again for each new terminal session.

   **Mac / Linux:**
```bash
   export LLM_API_KEY="sk-or-your-api-key-here"
```
   **Windows (Command Prompt):**
```cmd
   set LLM_API_KEY=sk-or-your-api-key-here
```
   **Windows (PowerShell):**
```powershell
   $env:LLM_API_KEY="sk-or-your-api-key-here"
```

3. **(Optional) Choose a different LLM model**

   The default model is `openai/gpt-4o-mini` (cost-effective). You can use **any model available on OpenRouter**.
   
   Browse available models at: https://openrouter.ai/models
   
   To use a different model, also set `LLM_MODEL`:
```bash
   export LLM_MODEL="anthropic/claude-3.5-sonnet"
```
   
   **Popular model examples:**
   - `openai/gpt-4o-mini` (default, cheap)
   - `openai/gpt-4o` (more capable)
   - `anthropic/claude-3.5-sonnet` (great for reasoning)
   - `google/gemini-pro-1.5` (large context)
   - `meta-llama/llama-3.1-70b-instruct` (open source)

### Start the application

Run `docker compose up --build` (or `docker-compose up --build`). This installs all requirements and builds the application from the ground up. This might take some time.

If you just want to restart your application, run the command without the `--build` flag.

### Access the application

- **Frontend (Website):** http://localhost:4200
- **Backend (API Docs):** http://localhost:8000/docs

### Stop the application
```bash
docker compose down
```

## Code Explanation in Use Cases

### A User uploads course material/an old exam

The backend receives a POST request to `/courses/{course_id}/upload/{material_type}` with the `course_id`, `material_type` and `file` (the course material file). Then we call the `chunk_and_enrich()` function in the `FileProcessor`. This function chunks the course material and extracts metadata from it. The metadata is saved in a `dict`. That way, we can dynamically add new metadata to it, without needing to change other data objects. The chunks of the course material and the metadata are then passed to the `index_{old_exam_questions | course_material}()` function of our `VectorDB`. The function computes embeddings for the text in the chunks and saves these embeddings, along with the original text and the metadata, in the Chroma Collection. If everything worked out fine, we return a HTTP 200 status code to the user. The frontend can then display some tech-savy, impressive quote like, "Your data is now enriching a multi-billion dollar application" or some shit, idk.

### A User generates a new exam

The backend receives a POST request to `/courses/{course_id}/generate` with the `course_id`, and two optional query parameters which specify how many questions the new exam should contain (`n_new_questions`) and what topics the exam should cover (`topics`). First we retrieve N relevant course material and old exam questions from our Vector DB. We do this by computing an embedding for the optional `topics`, or some other way, if we don't have a topic given, and comparing the cosine similarity between the `topics`-embedding and the embeddings of the text chunks in our VectorDB. Then we pass these relevant course material chunks/old exam questions to the `generate_questions()` function in our `QuestionGenerator`. This function then calls an LLM to generate new exam questions. The prompt used contains the relevant course material chunks and old exam question examples. The output is a list of newly generated questions. Lastly, we pass this list to the `generate_pdf()` function in `PDFGenerator`. The function then transforms the list into a new exam pdf, which we return to the user. When the pdf is ready on the frontend, the user should be able to download it via a button.
