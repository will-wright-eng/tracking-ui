# fastapi-react-slim

## modifed fastapi-react

- removed celery and flower entirely

```
tracking-ui-frontend-1  | Starting the development server...
tracking-ui-frontend-1  |
tracking-ui-frontend-1  | Failed to compile.
tracking-ui-frontend-1  |
tracking-ui-frontend-1  | /app/src/index.tsx
tracking-ui-frontend-1  | TypeScript error in /app/src/index.tsx(8,4):
tracking-ui-frontend-1  | 'Router' cannot be used as a JSX component.
tracking-ui-frontend-1  |   Its instance type 'BrowserRouter' is not a valid JSX element.
tracking-ui-frontend-1  |     The types returned by 'render()' are incompatible between these types.
tracking-ui-frontend-1  |       Type 'React.ReactNode' is not assignable to type 'import("/node_modules/@types/react-transition-group/node_modules/@types/react/ts5.0/index").ReactNode'.  TS2786
tracking-ui-frontend-1  |
tracking-ui-frontend-1  |      6 |
tracking-ui-frontend-1  |      7 | ReactDOM.render(
tracking-ui-frontend-1  |   >  8 |   <Router>
tracking-ui-frontend-1  |        |    ^
tracking-ui-frontend-1  |      9 |     <App />
tracking-ui-frontend-1  |     10 |   </Router>,
tracking-ui-frontend-1  |     11 |   document.getElementById('root')
```

## usage

```bash
git clone https://github.com/will-wright-eng/fastapi-react-slim.git
cookiecutter fastapi-react-slim
```
