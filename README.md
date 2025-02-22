# Resonance
Software Engineering's Project
Look at the [Nuxt documentation](https://nuxt.com/docs/getting-started/introduction) to learn more.
This is the [Folder Structure](https://vueschool.io/articles/vuejs-tutorials/understanding-the-directory-structure-in-nuxt-3/).
We will use "snake_case" variables
## Setup

Make sure to install dependencies:

```bash
# npm
npm install

# pnpm
pnpm install

# yarn
yarn install

# bun
bun install
```

## Front-End Development

Start the development server on `http://localhost:3000`:

```bash
# npm
npm run dev

# pnpm
pnpm dev

# yarn
yarn dev

# bun
bun run dev
```
## Back-End Developement
After Clone then, start env module in project folder:
Backend Development Setup

1. Clone the Repository
```bash
git clone https://github.com/KKhamwiset/Resonance
cd your-repo
```

2. Create a Virtual Environment

Inside the project folder, run:
```bash
python -m venv <your-env-folder-name>
```
💡 Example:
```bash
python -m venv env
```
3. Activate the Virtual Environment

🔹 On Windows (PowerShell)
```bash
./<your-env-folder-name>/Scripts/Activate
```
💡 Example:
```bash
./env/Scripts/Activate
```
🔹 On Mac/Linux
```bash
source <your-env-folder-name>/bin/activate
```
💡 Example:
```bash
source env/bin/activate
```
4. Install Dependencies

Once the environment is activated, install required dependencies:
```bash
pip install -r backend/requirements.txt
```
5. Apply Database Migrations

Ensure the database is up to date by running:
```bash
python manage.py makemigrations server
python manage.py migrate
```
6. Run the Django Server

Start the backend server with:
```bash
python manage.py runserver
```

## Production

Build the application for production:

```bash
# npm
npm run build

# pnpm
pnpm build

# yarn
yarn build

# bun
bun run build
```

Locally preview production build:

```bash
# npm
npm run preview

# pnpm
pnpm preview

# yarn
yarn preview

# bun
bun run preview
```
