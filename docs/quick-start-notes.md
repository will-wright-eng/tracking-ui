# quick start notes

```bash
docker-compose run --rm backend alembic upgrade head
```

- modified flower container
- `npm update` wont update major versions
- python docker image to 3.11

- removed celery and flower entirely
- bash scripts/build.sh

```bash
rm pyproject.toml
cat requirements.txt | xargs poetry add
poetry export -f requirements.txt --output requirements.txt
docker build -t test .
```

Change the line:
"react": "^16.13.1"

to:
"react": "^17.0.2"

```bash
cd frontend/
npm install react react-dom
npm audit fix --force
```
```
 There might be a problem with the project dependency tree.
 It is likely not a bug in Create React App, but something you need to fix locally.

 The react-scripts package provided by Create React App requires a dependency:

   "babel-eslint": "9.0.0"

 Don't try to install it manually: your package manager does it automatically.
 However, a different version of babel-eslint was detected higher up in the tree:

   /app/node_modules/babel-eslint (version: 10.1.0)

 Manually installing incompatible versions is known to cause hard-to-debug issues.

 If you would prefer to ignore this check, add SKIP_PREFLIGHT_CHECK=true to an .env file in your project.
 That will permanently disable this message but you might encounter other issues.

 To fix the dependency tree, try following the steps below in the exact order:

1. Delete package-lock.json (not package.json!) and/or yarn.lock in your project folder.
2. Delete node_modules in your project folder.
3. Remove "babel-eslint" from dependencies and/or devDependencies in the package.json file in your project folder.
4. Run npm install or yarn, depending on the package manager you use.
```

## reconstruct package.json

To recreate the package.json file using npm commands, you would need to initialize a new npm project and then install each dependency one by one. Here are the commands you would need to run:

```bash
npm init -y
npm install --save ra-data-json-server@latest ra-data-simple-rest@latest react@latest react-admin@latest react-dom@latest react-router-dom@latest react-scripts@latest react-truncate@latest standard@latest jwt-decode@latest @material-ui/lab@latest
npm install --save-dev typescript@latest @testing-library/jest-dom@latest @testing-library/react@latest @typescript-eslint/eslint-plugin@latest @typescript-eslint/parser@latest @testing-library/user-event@latest @types/jest@latest @types/node@latest @types/react@latest @types/react-dom@latest @types/react-router-dom@latest @types/jwt-decode@latest eslint-config-airbnb@latest eslint-config-react-app@latest eslint-plugin-flowtype@latest eslint-plugin-import@latest eslint-plugin-jsx-a11y@latest eslint-plugin-react@latest eslint-plugin-react-hooks@latest prettier@latest react-test-renderer@latest
```

After running these commands, you would need to manually add the "scripts", "eslintConfig", and "browserslist" sections to your package.json file. Here's what those sections would look like:

```js
"scripts": {
  "start": "react-scripts start",
  "build": "react-scripts build",
  "test": "CI=true react-scripts test",
  "eject": "react-scripts eject"
},
"eslintConfig": {
  "extends": "airbnb"
},
"browserslist": {
  "production": [
    ">0.2%",
    "not dead",
    "not op_mini all"
  ],
  "development": [
    "last 1 chrome version",
    "last 1 firefox version",
    "last 1 safari version"
  ]
}
```

Please note that the versions installed by these commands will be the latest versions available at the time the commands are run, and may not match the versions specified in your original package.json file.
