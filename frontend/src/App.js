import { useEffect, useState } from "react";
import "./App.css";
import '../node_modules/bootstrap/dist/css/bootstrap.min.css';

function App() {
  const [data, setData] = useState([]);

  const fetchData = () => {
    fetch(`http://0.0.0.0:8000/v1/athena/sample-json`)
      .then((response) => response.json())
      .then((actualData) => {
        console.log(actualData);
        setData(actualData.events);
        console.log(data);
      })
      .catch((err) => {
        console.log(err.message);
      });
  };

  useEffect(() => {
    fetchData();
  }, []);

  return (
    <div className="App">
      <tbody>
        <tr>
          <th>Name</th>
          <th>Brand</th>
        </tr>
        {data.map((item, index) => (
          <tr key={index}>
            <td>{item.tab_url}</td>
            <td>{item.tab_title}</td>
          </tr>
        ))}
      </tbody>
    </div>
  );
}

export default App;
