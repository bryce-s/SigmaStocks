import React from 'react'
import FlipCard from 'react-flipcard'
import classNames from 'classnames'

let style = {
    // paddingTop: '30%',
    // paddingBottom: '30%'
}

export default class CurrentInvestment extends React.Component {
    // constructor(props) {
    //     super(props)
    //     this.state = {
    //         classes: ''
    //     }
    // }

    getClassName() {
        // console.log('Finding class')
        if (this.props.movement[0] == '+') {
            // style.backgroundColor = '#a5d6a7'
            // console.log(style)
            // return classNames('stockGrowth')
            return 'stockGrowth'
        }
        else if (this.props.movement[0] == '-') {
            // style.backgroundColor = '#ef9a9a'
            // console.log(style)
            // return classNames('stockDecline')
            return 'stockDecline'
        }
        return ''
        // return classNames('')
    }

    render() {
        return (
            <FlipCard style={{ vecticalAlign: 'middle' }} className={this.getClassName()}>
                <div className='front' style={style}>
                    <h3>
                        {this.props.ticker}
                    </h3>
                    <h4>
                        {this.props.movement}
                    </h4>
                </div>
                <div className='back'>Back</div>
            </FlipCard>
        )
    }
}