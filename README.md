# FeastiveEats Meal Planner 🎄🍽️

**FeastiveEats Meal Planner** is your ultimate companion for planning and organizing delightful Christmas meals. From browsing festive recipes to creating personalized meal plans, this application simplifies your holiday cooking experience.

## ✨ Features

- **Browse Recipes:** Explore a variety of Christmas-themed recipes.
- **Add Your Recipes:** Share your favorite festive recipes with the community.
- **Rate & Comment:** Provide feedback on recipes and help others make informed choices.
- **Plan Your Meals:** Organize meals effortlessly for the holiday season.

---

## ⚠️ Known Issues

Due to file size limitations, deployment on **PythonAnywhere** was not possible. Please follow the local setup instructions below to run the project.

---

## 🛠️ Setup Instructions

Follow these steps to set up and run the project locally:

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/jignasa-dcosta/FestiveEats-meal-planner.git
   cd feastiveeats-meal-planner
   ```

2. **Create a Virtual Environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies:**
   ```bash
   pip install Pillow
   ```

4. **Apply Database Migrations:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Run the Server:**
   ```bash
   python manage.py runserver
   ```

6. Open your browser and navigate to `http://127.0.0.1:8000/`

## 💻 Technologies Used

- **Backend:** Django
- **Frontend:** HTML5, CSS3, Bootstrap
- **Database:** SQLite

## Demo and Presentation
**Google Drive Link:** https://drive.google.com/file/d/1YszPPyFhOO4MyZ_EFMdUqAz0GXabgTvf/view?usp=drive_link

## 🚀 Usage

1. Browse recipes categorized for Christmas.
2. Add your own recipes to the collection.
3. Create and manage your meal plans.
4. Rate and comment on recipes.
5. Enjoy a stress-free festive cooking experience!

Happy cooking with **FeastiveEats Meal Planner**! 🎅✨

