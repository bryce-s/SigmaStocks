import React, {Component} from 'react'
import './App.css'
import axios from 'axios'
import CurrentInvestment from './CurrentInvestment/CurrentInvestment'
import {Switch, Typography} from 'antd'
import {Row} from 'react-flexbox-grid'

const {Title} = Typography;

// Container
class App extends Component {
    constructor(props) {
        super(props);
        this.state = {
            investmentArray: [],
            portfolioValue: 0,
            theme: 'light'
        }
    }

    getData() {
        // console.log('Fetching Data')
        Promise.all([
            axios.get(
                process.env.REACT_APP_HOST +
                ':' +
                process.env.REACT_APP_SERVERPORT +
                '/api/stocks'
            ),
            axios.get(
                process.env.REACT_APP_HOST +
                ':' +
                process.env.REACT_APP_SERVERPORT +
                '/api/portfolio'
            )
        ]).then(([stocks, portfolio]) => {
            // console.log('Finished')
            this.setState({
                investmentArray: stocks.data,
                portfolioValue: portfolio.data[0]['portfolioValue']
            })
        })
    }

    componentDidMount() {
        // console.log('Mounted')
        this.getData()
    }

    changeTheme = value => {
        const newTheme = value ? 'dark' : 'light';
        document.body.style.backgroundColor = this.getBackgroundColour(newTheme);
        this.setState({
            theme: newTheme
        })
    };

    getBackgroundColour = newTheme => {
        if (newTheme === 'dark') {
            return '#1D2229'
        }
        return '#FFF'
    };

    getTitleColour() {
        if (this.state.theme === 'dark') {
            return '#FFF'
        }
        return '#000'
    }

    render() {
        // Render portfolio value and number of cards based on JSON response

        // console.log('Rendered')
        console.log(this.state);
        return (
            <div
                className="app-container"
                style={{
                    textAlign: 'center',
                    marginTop: '20%'
                }}
            >
                <Title level={1} style={{color: this.getTitleColour()}}>
                    ${this.state.portfolioValue}
                </Title>

                <Switch
                    checked={this.state.theme === 'dark'}
                    onChange={this.changeTheme}
                    checkedChildren="Dark"
                    unCheckedChildren="Light"
                    style={{marginBottom: '1%'}}
                />

                <Row
                    id="currentStocks"
                    style={{
                        marginLeft: '1%',
                        marginRight: '1%'
                    }}
                >
                    {this.state.investmentArray.map((currStock, index) => (
                        <CurrentInvestment
                            key="stock_{index}"
                            ticker={currStock.ticker}
                            movement={currStock.movement}
                            theme={this.state.theme}
                        />
                    ))}
                </Row>
            </div>
        )
    }
}

export default App
