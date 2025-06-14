OrionAI 🌌

OrionAI is a cutting-edge AI-powered application that enables users to generate images and text using intelligent prompt enhancement. It supports multiple AI models and provides a gamified learning experience through a task-based prompt system.

🚀 Features

🧠 Prompt Enhancement SystemAutomatically improves user-entered prompts based on task descriptions and objectives.
🖼️ AI Image GenerationGenerate stunning images using services like DALL·E, DeepArt, NightCafe, etc.
🗣️ AI Text GenerationCreate contextual AI-generated stories, dialogues, or content based on tasks.
🎮 Gamified ExperienceInteractive game-like system with 3 levels, 5 tasks, and 1 challenge per level.
🔒 Authentication & User ProfilesSecure user login system and personalized task tracking.

🛠️ Tech Stack
Frontend: React, Tailwind CSS
Backend: Django, Django REST Framework
Database: MongoDB

APIs Used:
OpenAI (for DALL·E / GPT-3.5)
RapidAPI, Clipdrop, Limmewire (for image/text generation services)

📂 Project Structure

orionai/
├── backend/
│   ├── orionai/              
│   ├── api/                   
│   └── media/                 
├── frontend/
│   ├── src/
│   ├── components/
│   └── pages/
└── README.md

🧪 How to Run Locally

Backend (Django)

cd backend
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver

Frontend (React)

cd frontend
npm install
npm start

Ensure to configure environment variables for API keys and endpoints in .env files for both frontend and backend.

![Picture2](https://github.com/user-attachments/assets/95d7bb3b-4161-4007-8bbf-6138d4224bd2)
![Picture11](https://github.com/user-attachments/assets/22721d91-981c-4055-8f02-f589a81c60e3)
![Picture10](https://github.com/user-attachments/assets/cf7d072f-8c04-4bf4-962a-e368abfc02e0)
![Picture9](https://github.com/user-attachments/assets/261ef95d-6756-493c-85fa-cdd66d3429fe)
![Picture8](https://github.com/user-attachments/assets/2ab190e7-6c4f-425b-b40d-2ba79639b4ce)
![Picture7](https://github.com/user-attachments/assets/3ff99d7e-a7b7-462d-838e-176d964364e5)
![Picture6](https://github.com/user-attachments/assets/be53f806-dd39-41f9-a837-e4ece34362cb)
![Picture5](https://github.com/user-attachments/assets/0f2502d3-20e7-44d0-8c75-05814250eeb8)
![Picture4](https://github.com/user-attachments/assets/d98ff46e-781e-4ef5-9681-d020289c6766)
![Picture3](https://github.com/user-attachments/assets/b3e8fa51-da08-4b58-a487-27797e96f97a)


🧩 Future Plans

Add user progress analytics
Add leaderboard and challenge mode
Support multilingual prompts
Integrate speech-to-text input

🤝 Contribution

Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.
https://github.com/VDDayarathne/Orion_backend.git
