import React from 'react';
import { Link } from 'react-router-dom';
import CurrentInvestment from './CurrentInvestment'
import axios from 'axios'

export default class AppWrapper extends React.Component {
  constructor(props) {
    super(props)
    this.state = {
      investmentArray: [],
      portfolioValue: 0
    }
  }

  getData() {
    // console.log('Fetching Data')
    Promise.all([
      axios.get('/api/stocks'),
      axios.get('/api/portfolio')
    ]).then(([stocks, portfolio]) => {
      // console.log('Finished')
      this.setState({ investmentArray: stocks.data, portfolioValue: portfolio.data[0]['portfolioValue'] })
    })
  }

  componentDidMount() {
    // console.log('Mounted')
    this.getData()
  }

  render() {
    // console.log('Rendered')
    console.log(this.state)
    return (
      <div className='app-container'>
        <div id='currentStocks'>
          {this.state.investmentArray.map((currStock, index) =>
            <CurrentInvestment ticker={currStock.ticker}
              movement={currStock.movement} />
          )}
        </div>
        {/* <Link to={'/'}>Home</Link> */}
        {/* <Link to={'/about'}>About</Link> */}
        {/* <Link to={'/about/subroute'}>Subcomponent</Link> */}
        {/* {this.props.children} */}
      </div>
    )
  }
}