@echo off
echo Activating virtual environment...
call .\.venv\Scripts\activate

echo Running Streamlit app...
call streamlit run src\test.py

echo Streamlit app has stopped.
pause