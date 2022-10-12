import React from "react";
// import { render } from 'react-dom';
import { createRoot } from 'react-dom/client';
import { ChakraProvider } from "@chakra-ui/react";

import Header from "./components/Header";
import Todos from "./components/Todos";  // new

function App() {
  return (
    <ChakraProvider>
      <Header />
      <Todos />  {/* new */}
    </ChakraProvider>
  )
}

// const rootElement = document.getElementById("root")
// render(<App />, rootElement)


const container = document.getElementById('root');
const root = createRoot(container); // createRoot(container!) if you use TypeScript
root.render(<App tab="home" />);
