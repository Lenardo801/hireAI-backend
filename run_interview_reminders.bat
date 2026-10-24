@echo off
cd /d "D:\project\Login 360\HireAI\backend"
"D:\project\Login 360\HireAI\backend\env\Scripts\python.exe" "D:\project\Login 360\HireAI\backend\manage.py" send_interview_reminders >> "D:\project\Login 360\HireAI\backend\interview_reminder.log" 2>&1