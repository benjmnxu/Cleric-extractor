# Cleric-extractor

Built out with FastAPI backend and Next.js frontend.

Used an Agent-based solution with one Agent reading and extracting from each log and a second agent, Merger, reconciling and merging the differences in the two sets of facts. I've left in some vestigial code to give a better sense of my though process. My initial idea was to use one Agent and ask it to both analyze multiple logs and reconcile different facts (Seen through the followup prompts in prompts.py). I then tried seeing if a method of getting every fact from the log then reconciling them would improve results (You can still see the reconcile function in Merger). Ultimately, I landed on the current solution, trading a little bit of runtime with much better results and more deterministic behavior. I believe directly working with the API to have specific control for a simpler task such as this is much preferred to a importing large/intensive LLM frameworks/abstractions like LangChain.

The asynchronous parts (not busy waiting on gpt) are handled via FastAPI's background tasks. Vercel's lack of uvicorn/gunicorn are why I deployed on render.com instead.

Test logs are included in the test_logs folder. Relatively minimal, these tests, generated by a third model, were manually verified to follow the task specifications and validified.
