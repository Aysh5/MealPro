# MealPro
meal planning mobile app

1. clone the repo 
git clone https://github.com/Aysh5/MealPro.git
cd MealPro/backend
2. create and activate virtual env
python3 -m venv .venv
source .venv/bin/activate
3. install dependencies
pip install -r requirements.txt
4. run the server
uvicorn app.main:app --reload
5. open browser at http:***/docs
6. on GET /recipes click Try, then click Execute 
