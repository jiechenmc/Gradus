# Gradus [API](https://github.com/jiechenmc/Gradus-API)
#### Setting up
- Create .env as defined in example.env before running the following command
- When scraping, index 1 is the latest term.
```bash
pip install -r requirements.txt
playwright install # if this is your first time using playwright
playwright install-deps # if this is your first time using playwright
```

####

#### Running the script
```bash
python main.py
```
- A cache will be created as a file `.cache` with the current page url if any exceptions arise
- The cached url allows the script to pick up exactly where you left off of
- `.cache` should be removed if you do not intend to continue where you left off of
####

#### Migrating data to MongoDB Atlas
```bash
python migrate.py
```
- After verifying the migration, you can safely delete `data.json` and `.cache`
####
