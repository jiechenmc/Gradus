# Gradus

#### Setting up
- Create .env as defined in example.env before running the following command
```bash
pip install -r requirements.txt
```
####

#### Running the script
```bash
python main.py
```
- A cache will be created as a file (.cache) with the current page url if any exceptions arise
- The cached url allows the script to pick up exactly where you left off of
- .cache should be removed if you do not intend to continue where you left off of
####

#### Migrating to MongoDB Atlas
```bash
python migrate.py
```
- Make sure .env is filled out before migrating
####
