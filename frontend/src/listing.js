import { Component } from 'react';


class Listing extends Component {

    constructor(props) {
        super(props)
        this.state = {
            records: []
        }

    }

    componentDidMount() {
        fetch('http://0.0.0.0:8000/v1/athena/sample-json')
            .then(response => response.json())
            .then(records => {
                this.setState({
                    records: records
                })
            })
            .catch(error => console.log(error))
    }

    renderListing() {
        let recordList = []
        this.state.records.map(record => {
            return recordList.push(`<li key={record.id}>{record.name}</li>`)
        })

        return recordList;
    }

    renderRecord() {
        return this.state.records;
    }

    render() {
        return (
            `<ul>
                {this.renderListing()}
            </ul>
            <p>
                {this.renderRecord()}
            </p>`

        );
    }
}

export default Listing;
