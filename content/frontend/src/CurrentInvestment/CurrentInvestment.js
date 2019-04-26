import React, {Component} from 'react'
import {Card, Icon, Statistic} from 'antd'
import {Col} from 'react-flexbox-grid'
// import candlestickModal from './candlestickModal.js'


// CurrentInvestment object
export default class CurrentInvestment extends Component {
    constructor(props) {
        super(props);
        this.state = {
            movementDirection: this.props.movement[0]
        }
    }

    getArrowType() {
        if (this.state.movementDirection === '-') {
            return 'arrow-down'
        } else if (this.state.movementDirection === '+') {
            return 'arrow-up'
        } else {
            return 'minus'
        }
    }

    getStockValueColour() {
        if (this.props.theme === 'dark') {
            if (this.state.movementDirection === '-') {
                return '#EB999A'
            } else if (this.state.movementDirection === '+') {
                return '#93CF9C'
            } else {
                return '#67A9ED'
            }
        }
        if (this.state.movementDirection === '-') {
            return '#cf1322'
        } else if (this.state.movementDirection === '+') {
            return '#3f8600'
        } else {
            return '#ECECEC'
        }
    }

    getCardBackgroundColour() {
        if (this.props.theme === 'dark') {
            return '#4C5160'
        }
        return '#FFF'
    }

    getTitleColour() {
        if (this.props.theme === 'dark') {
            return '#FFF'
        }
        return '#000'
    }

    getValue(movement) {
        return movement.substring(1)
    }

    showCandlestick() {
        alert("I tried");
    }

    render() {
        // Rendering a card with style decided
        return (
            <Col xs style={{marginBottom: '3%', marginTop: '3%'}}>
                <Card
                    style={{backgroundColor: this.getCardBackgroundColour()}}
                    onClick={this.showCandlestick}
                >
                    <Statistic
                        title={this.props.ticker}
                        value={this.getValue(this.props.movement)}
                        precision={2}
                        valueStyle={{color: this.getStockValueColour()}}
                        prefix={<Icon type={this.getArrowType()}/>}
                        suffix="%"
                        style={{
                            marginLeft: '-1%',
                            color: this.getTitleColour()
                        }}
                    />
                </Card>
            </Col>
        )
    }
}
