@echo off
echo ====================================
echo Installing FREE dependencies
echo ====================================

echo.
echo Step 1: Uninstalling old packages...
pip uninstall -y pydantic pydantic-core fastapi uvicorn google-cloud-translate

echo.
echo Step 2: Installing pre-compiled binaries...
pip install --only-binary=:all: pydantic==2.6.4

echo.
echo Step 3: Installing remaining packages...
pip install fastapi==0.109.0
pip install uvicorn[standard]==0.27.0
pip install deep-translator==1.11.4
pip install google-generativeai==0.3.2
pip install python-dotenv==1.0.0

echo.
echo ====================================
echo Installation complete!
echo ====================================
echo.
echo Next step:
echo Get FREE Gemini API key: https://makersuite.google.com/app/apikey
echo Add to .env: GEMINI_API_KEY=your_key_here
echo.
echo Run: python main.py
pause
