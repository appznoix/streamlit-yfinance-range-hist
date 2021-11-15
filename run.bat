@echo off
cls
if "%~1"=="" goto blank

streamlit run %1
goto end

:blank
streamlit run app.py

:end