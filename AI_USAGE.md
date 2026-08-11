# AI Usage

I used Claude to help build this project, mainly as a coding assistant and sounding board for the engineering logic. Three examples of how it was used:

## 1. Understanding the pipe flow formulas

**Prompt:** "Walk me through the formulas for pipe flow — Reynolds number, friction factor, pressure drop — before we write any code."

I wanted to actually understand the physics before seeing implementation, rather than just accepting whatever code came out. When I hand-calculated a test case afterward to check the code, my own manual math was actually off — I'd made an arithmetic slip working out the friction factor. The code was correct; redoing the calculation by hand showed the two matched once I fixed my own error.

## 2. Designing the engineering classes

**Prompt:** "Design the Fluid/Pipe and Wall/CoolingObject classes so each has one method that returns all the results together, instead of separate methods for each value."

Claude originally suggested having each result (velocity, Reynolds number, etc.) computed by its own separate method. I asked for a single `analyze()` method instead, since it's simpler to call from the Streamlit UI and avoids recalculating shared values multiple times — a design change I made based on how the app would actually be used.

## 3. Building the Streamlit pages

**Prompt:** "Build the Streamlit page for [module], with sidebar inputs, metric displays, and a plot."

After getting each page's code, I ran it live and tested every input, slider, and button myself before moving on. One issue I ran into (not really an AI mistake) was trying to run a page file directly with Python instead of through `streamlit run app.py`, which threw a `ModuleNotFoundError` — fixed by running it the correct way.