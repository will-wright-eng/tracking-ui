import { useEffect, useState } from "react";
import "./App.css";
import '../node_modules/bootstrap/dist/css/bootstrap.min.css';

function App() {
  const [data, setData] = useState([]);

  const fetchApiData = () => {
    const url = 'http://0.0.0.0:8000/v1/athena/sample-json';
    // https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API/Using_Fetch
    fetch(url, {method: 'GET'})
      .then(response => {
         if (!response.ok) {
             throw new Error("HTTP error " + response.status);
         }
         console.log(response)
         return response.json();
      })
      .then((actualData) => {
        console.log(actualData);
        setData(actualData.events);
      })
      .catch((err) => {
        console.log(err.message);
      });
  };

  useEffect(() => {
    fetchApiData();
  }, []);

  return (
    <div className="App">
      <tbody>
        <tr>
          <th>Tab Title</th>
          <th>Event</th>
          <th>Timestamp</th>
          <th>Tag</th>
        </tr>
        {data.map((item, index) => (
          <tr key={index}>
            <td>{item.tab_title}</td>
            <td>{item.tab_event}</td>
            <td>{item.created_timestamp}</td>
            <td>{item.manual_tag}</td>
          </tr>
        ))}
      </tbody>
    </div>
  );
}

export default App;
